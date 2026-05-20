"""Tests for the small settings module (kevinnet_settings.json)."""
import json
import pytest


@pytest.fixture(scope="module")
def kn():
    import kevinnet
    return kevinnet


@pytest.fixture
def isolated_settings(tmp_path, monkeypatch, kn):
    """Redirect _settings_path to a fresh temp file per test."""
    monkeypatch.setattr(kn, "_settings_path", lambda: tmp_path / "settings.json")
    return tmp_path / "settings.json"


def test_load_missing_returns_empty_dict(isolated_settings, kn):
    assert isolated_settings.exists() is False
    assert kn.load_settings() == {}


def test_save_and_load_round_trip(isolated_settings, kn):
    kn.save_settings({"last_mode": "vaydns", "help_dismissed": True})
    assert isolated_settings.exists()
    loaded = kn.load_settings()
    assert loaded["last_mode"] == "vaydns"
    assert loaded["help_dismissed"] is True


def test_save_preserves_unicode(isolated_settings, kn):
    kn.save_settings({"last_country": "ایران"})
    loaded = kn.load_settings()
    assert loaded["last_country"] == "ایران"
    # On disk it must NOT be \u-escaped — ensure_ascii=False is important
    on_disk = isolated_settings.read_text(encoding="utf-8")
    assert "ایران" in on_disk


def test_corrupted_file_returns_empty(isolated_settings, kn):
    isolated_settings.write_text("{ this is not json")
    assert kn.load_settings() == {}


def test_format_last_launched_just_now(kn):
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out = kn._format_last_launched(now)
    assert "just now" in out.lower() or "همین" in out


def test_format_last_launched_empty(kn):
    assert kn._format_last_launched("") == ""
    assert kn._format_last_launched(None) == ""


def test_format_last_launched_unparseable(kn):
    assert kn._format_last_launched("not a date") == ""


def test_format_last_launched_minutes_ago(kn):
    from datetime import datetime, timedelta
    past = (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    out = kn._format_last_launched(past)
    assert "5m" in out


def test_format_last_launched_hours_ago(kn):
    from datetime import datetime, timedelta
    past = (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    out = kn._format_last_launched(past)
    assert "3h" in out


def test_format_last_launched_fa(kn):
    from datetime import datetime, timedelta
    past = (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    out = kn._format_last_launched(past, fa=True)
    # Persian output should contain Persian characters, not English
    assert "m ago" not in out
    assert "دقیقه" in out or "5" in out
