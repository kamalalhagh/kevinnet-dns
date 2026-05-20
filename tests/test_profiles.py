"""Tests for profile-config building — TOML escaping, command building,
filename safety. These are the things that produced confusing field
bugs (e.g. "parse TOML failed") before the v3.3.0 hardening.
"""
import pytest


@pytest.fixture(scope="module")
def kn():
    import kevinnet
    return kevinnet


class TestTomlStrEscape:
    def test_plain_string(self, kn):
        assert kn._toml_str_escape("hello") == "hello"

    def test_double_quote_escaped(self, kn):
        out = kn._toml_str_escape('he"llo')
        assert '\\"' in out

    def test_backslash_escaped(self, kn):
        out = kn._toml_str_escape("he\\llo")
        assert "\\\\" in out

    def test_newline_escaped(self, kn):
        out = kn._toml_str_escape("a\nb")
        assert "\\n" in out

    def test_unicode_preserved(self, kn):
        # ensure_ascii=False keeps Persian characters readable in TOML
        out = kn._toml_str_escape("سلام")
        assert "سلام" in out


class TestBuildConfigFromProfile:
    def test_simple_profile_contains_domain_and_key(self, kn):
        profile = {
            "domain": "v.example.com",
            "key":    "a" * 32,
            "options": {},
        }
        cfg = kn.build_config_from_profile(profile)
        assert "v.example.com" in cfg
        assert "a" * 32 in cfg

    def test_domain_with_quotes_does_not_break_toml(self, kn):
        # Pathological input — the validator should reject this upstream,
        # but the escaper guarantees the TOML is still parseable as a
        # defence-in-depth measure.
        profile = {
            "domain": 'evil".com',
            "key":    "a" * 32,
            "options": {},
        }
        cfg = kn.build_config_from_profile(profile)
        # The DOMAINS line should still parse — verify by extracting and
        # checking quote balance on that line.
        for line in cfg.splitlines():
            if line.startswith("DOMAINS"):
                # Should have escaped quotes inside, not raw
                # i.e. DOMAINS = ["evil\".com"] not DOMAINS = ["evil".com"]
                assert '\\"' in line

    def test_options_substituted(self, kn):
        profile = {
            "domain": "v.example.com",
            "key":    "a" * 32,
            "options": {
                "listen_port":        12345,
                "encryption_method":  2,
                "balancing_strategy": 4,
            },
        }
        cfg = kn.build_config_from_profile(profile)
        assert "LISTEN_PORT = 12345" in cfg
        assert "DATA_ENCRYPTION_METHOD = 2" in cfg


class TestBuildVayDNSCommand:
    def test_basic_udp_command(self, kn):
        profile = {
            "domain": "t.example.com",
            "pubkey": "ab" * 32,
            "options": {"transport": "udp"},
        }
        cmd = kn.build_vaydns_command(profile, "1.2.3.4:53", "./vaydns")
        assert "./vaydns" in cmd
        assert "-udp 1.2.3.4:53" in cmd
        assert "-domain" in cmd
        assert "-pubkey" in cmd

    def test_doh_transport(self, kn):
        profile = {
            "domain": "t.example.com",
            "pubkey": "ab" * 32,
            "options": {"transport": "doh"},
        }
        cmd = kn.build_vaydns_command(
            profile, "https://1.1.1.1/dns-query", "./vd")
        assert "-doh https://1.1.1.1/dns-query" in cmd

    def test_dot_transport(self, kn):
        profile = {
            "domain": "t.example.com",
            "pubkey": "ab" * 32,
            "options": {"transport": "dot"},
        }
        cmd = kn.build_vaydns_command(profile, "1.1.1.1:853", "./vd")
        assert "-dot 1.1.1.1:853" in cmd

    def test_optional_flags_present_when_set(self, kn):
        profile = {
            "domain": "t.example.com",
            "pubkey": "ab" * 32,
            "options": {
                "transport":         "udp",
                "max_num_labels":    5,
                "max_streams":       10,
                "kcp_window_size":   2048,
                "rps":               50,
                "udp_shared_socket": True,
            },
        }
        cmd = kn.build_vaydns_command(profile, "8.8.8.8:53", "./vd")
        assert "-max-num-labels 5" in cmd
        assert "-max-streams 10" in cmd
        assert "-kcp-window-size 2048" in cmd
        assert "-rps 50" in cmd
        assert "-udp-shared-socket" in cmd

    def test_optional_flags_absent_when_zero(self, kn):
        profile = {
            "domain": "t.example.com",
            "pubkey": "ab" * 32,
            "options": {
                "transport":     "udp",
                "max_num_labels": 0,
                "max_streams":    0,
            },
        }
        cmd = kn.build_vaydns_command(profile, "8.8.8.8:53", "./vd")
        assert "-max-num-labels" not in cmd
        assert "-max-streams" not in cmd


class TestSafeProfileStem:
    def test_simple_name_preserved(self, kn):
        assert kn._safe_profile_stem("Iran") == "Iran"

    def test_spaces_become_underscores(self, kn):
        assert kn._safe_profile_stem("Iran VPN") == "Iran_VPN"

    def test_special_chars_become_underscores(self, kn):
        result = kn._safe_profile_stem("Iran/VPN!")
        assert "/" not in result
        assert "!" not in result

    def test_empty_falls_back_to_default(self, kn):
        # An empty input used to produce just "_<timestamp>.json" — fixed.
        assert kn._safe_profile_stem("") == "profile"

    def test_only_special_falls_back(self, kn):
        # User pastes emoji/symbols — must still produce a usable stem
        assert kn._safe_profile_stem("🚀💀!@#") == "profile"

    def test_custom_default(self, kn):
        assert kn._safe_profile_stem("", default="vaydns") == "vaydns"


class TestProfileFilename:
    def test_includes_random_suffix(self, kn):
        # Two filenames generated back-to-back must differ even when stem
        # and second are identical — that's the whole point of the salt.
        a = kn._profile_filename("Iran")
        b = kn._profile_filename("Iran")
        assert a != b

    def test_ends_with_json(self, kn):
        assert kn._profile_filename("Iran").endswith(".json")

    def test_prefix_applied(self, kn):
        assert kn._profile_filename("X", prefix="vd_").startswith("vd_X_")


class TestVayDNSLaunchScriptDoH:
    """Tests for v3.3.2: DoH/DoT profiles with multiple endpoints should
    generate a fallthrough launch script the same way UDP does, instead
    of silently using only the custom_resolver field.
    """

    def test_doh_profile_with_multiple_endpoints_uses_loop(self, kn, tmp_path, monkeypatch):
        # Redirect output folder to a temp dir so we don't pollute the repo
        monkeypatch.setattr(kn, "app_dir", lambda: tmp_path)

        profile = {
            "name":    "Iran-DoH",
            "domain":  "t.example.com",
            "pubkey":  "ab" * 32,
            "country": "Iran-DoH",
            "resolvers": [
                "https://1.1.1.1/dns-query",
                "https://8.8.8.8/dns-query",
                "https://dns.google/dns-query",
            ],
            "options": {"transport": "doh"},
        }
        script = kn.write_vaydns_launch_script(profile)
        body = script.read_text()
        # Multi-endpoint script must use the RESOLVERS=( ... ) loop pattern
        assert "RESOLVERS=(" in body
        # All three endpoints present
        assert "https://1.1.1.1/dns-query" in body
        assert "https://8.8.8.8/dns-query" in body
        assert "https://dns.google/dns-query" in body
        # The transport flag should be -doh, never -udp
        assert "-doh" in body
        assert "-udp http" not in body  # paranoia: no UDP flag with HTTP URLs

    def test_dot_profile_with_multiple_endpoints_uses_loop(self, kn, tmp_path, monkeypatch):
        monkeypatch.setattr(kn, "app_dir", lambda: tmp_path)

        profile = {
            "name":    "Iran-DoT",
            "domain":  "t.example.com",
            "pubkey":  "ab" * 32,
            "country": "Iran-DoT",
            "resolvers": ["1.1.1.1:853", "8.8.8.8:853", "9.9.9.9:853"],
            "options": {"transport": "dot"},
        }
        script = kn.write_vaydns_launch_script(profile)
        body = script.read_text()
        assert "RESOLVERS=(" in body
        assert "1.1.1.1:853" in body
        assert "9.9.9.9:853" in body
        assert "-dot" in body

    def test_doh_profile_with_single_endpoint_runs_directly(self, kn, tmp_path, monkeypatch):
        monkeypatch.setattr(kn, "app_dir", lambda: tmp_path)
        profile = {
            "name":    "Iran-DoH",
            "domain":  "t.example.com",
            "pubkey":  "ab" * 32,
            "country": "Iran-DoH-single",
            "resolvers": ["https://1.1.1.1/dns-query"],
            "options": {"transport": "doh"},
        }
        script = kn.write_vaydns_launch_script(profile)
        body = script.read_text()
        # Single endpoint should NOT use the fallthrough loop
        assert "RESOLVERS=(" not in body
        # Still uses DoH transport flag
        assert "-doh https://1.1.1.1/dns-query" in body

    def test_doh_profile_with_no_endpoints_prints_error(self, kn, tmp_path, monkeypatch):
        # Edge case: empty resolvers list and no custom_resolver — the
        # launch script must emit a clear error message, not silently
        # produce a half-broken vaydns-client invocation.
        monkeypatch.setattr(kn, "app_dir", lambda: tmp_path)
        profile = {
            "name":    "Empty",
            "domain":  "t.example.com",
            "pubkey":  "ab" * 32,
            "country": "Empty-DoH",
            "resolvers": [],
            "options": {"transport": "doh"},
        }
        script = kn.write_vaydns_launch_script(profile)
        body = script.read_text()
        assert "ERROR" in body
        assert "doh" in body.lower()

    def test_custom_resolver_still_works_for_doh(self, kn, tmp_path, monkeypatch):
        # Backwards compatibility: profiles saved before v3.3.2 only had
        # custom_resolver and no resolvers list. They must still work.
        monkeypatch.setattr(kn, "app_dir", lambda: tmp_path)
        profile = {
            "name":    "Old-DoH",
            "domain":  "t.example.com",
            "pubkey":  "ab" * 32,
            "country": "Old-DoH",
            "resolvers": [],
            "options": {
                "transport":       "doh",
                "custom_resolver": "https://9.9.9.9/dns-query",
            },
        }
        script = kn.write_vaydns_launch_script(profile)
        body = script.read_text()
        assert "https://9.9.9.9/dns-query" in body
        assert "-doh" in body
