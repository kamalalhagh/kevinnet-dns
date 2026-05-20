"""Tests for the pure-function input validators in kevinnet.py.

These run with no GUI and no network — they're meant to be fast and to
catch regressions in user-input handling, which has historically caused
the most confusing field bug reports ("parse TOML failed" etc.).
"""
import pytest


@pytest.fixture(scope="module")
def kn():
    import kevinnet
    return kevinnet


class TestValidateDomain:
    def test_normal_tunnel_domain(self, kn):
        ok, _ = kn.validate_domain("v.example.com")
        assert ok

    def test_apex_two_label_domain(self, kn):
        ok, _ = kn.validate_domain("example.com")
        assert ok

    def test_deep_subdomain(self, kn):
        ok, _ = kn.validate_domain("a.b.c.d.example.com")
        assert ok

    def test_trailing_dot_accepted(self, kn):
        ok, _ = kn.validate_domain("v.example.com.")
        assert ok

    def test_empty_rejected(self, kn):
        ok, err = kn.validate_domain("")
        assert not ok and "empty" in err.lower()

    def test_whitespace_only_rejected(self, kn):
        ok, _ = kn.validate_domain("   ")
        assert not ok

    def test_no_tld_rejected(self, kn):
        ok, _ = kn.validate_domain("example")
        assert not ok

    def test_spaces_rejected(self, kn):
        ok, _ = kn.validate_domain("foo bar.com")
        assert not ok

    def test_double_quote_rejected(self, kn):
        # Double-quote would break TOML — catch it at the gate
        ok, _ = kn.validate_domain('v"x.example.com')
        assert not ok

    def test_underscore_in_label_rejected(self, kn):
        # Underscores aren't valid in hostnames per RFC 1035
        ok, _ = kn.validate_domain("v_x.example.com")
        assert not ok

    def test_overlong_rejected(self, kn):
        ok, _ = kn.validate_domain("a" * 250 + ".com")
        assert not ok


class TestValidateMasterDNSKey:
    def test_exact_32_chars(self, kn):
        ok, _ = kn.validate_masterdns_key("a" * 32)
        assert ok

    def test_exact_32_mixed(self, kn):
        ok, _ = kn.validate_masterdns_key("AbCd1234" * 4)
        assert ok

    def test_too_short(self, kn):
        ok, err = kn.validate_masterdns_key("a" * 31)
        assert not ok and "32" in err

    def test_too_long(self, kn):
        ok, err = kn.validate_masterdns_key("a" * 33)
        assert not ok and "32" in err

    def test_empty(self, kn):
        ok, _ = kn.validate_masterdns_key("")
        assert not ok

    def test_with_trailing_whitespace_stripped(self, kn):
        ok, _ = kn.validate_masterdns_key("  " + "a" * 32 + "  ")
        assert ok

    def test_double_quote_rejected(self, kn):
        bad = '"' + "a" * 31
        ok, _ = kn.validate_masterdns_key(bad)
        assert not ok

    def test_backslash_rejected(self, kn):
        bad = "\\" + "a" * 31
        ok, _ = kn.validate_masterdns_key(bad)
        assert not ok

    def test_newline_rejected(self, kn):
        bad = "\n" + "a" * 31
        ok, _ = kn.validate_masterdns_key(bad)
        assert not ok


class TestValidateVayDNSPubkey:
    def test_exact_64_lowercase_hex(self, kn):
        ok, _ = kn.validate_vaydns_pubkey("0a1b2c3d" * 8)
        assert ok

    def test_uppercase_hex_accepted(self, kn):
        # We normalise to lowercase on save, but the validator accepts both.
        ok, _ = kn.validate_vaydns_pubkey("ABCDEF12" * 8)
        assert ok

    def test_too_short(self, kn):
        ok, _ = kn.validate_vaydns_pubkey("ab" * 31)
        assert not ok

    def test_too_long(self, kn):
        ok, _ = kn.validate_vaydns_pubkey("ab" * 33)
        assert not ok

    def test_non_hex_chars_rejected(self, kn):
        ok, err = kn.validate_vaydns_pubkey("xyz" + "0" * 61)
        assert not ok and "hex" in err.lower()

    def test_empty(self, kn):
        ok, _ = kn.validate_vaydns_pubkey("")
        assert not ok


class TestValidateFolderName:
    def test_simple_name(self, kn):
        ok, _ = kn.validate_folder_name("Iran")
        assert ok

    def test_with_spaces(self, kn):
        ok, _ = kn.validate_folder_name("Iran VPN")
        assert ok

    def test_path_separator_rejected(self, kn):
        ok, _ = kn.validate_folder_name("foo/bar")
        assert not ok

    def test_backslash_rejected(self, kn):
        ok, _ = kn.validate_folder_name("foo\\bar")
        assert not ok

    def test_dot_rejected(self, kn):
        ok, _ = kn.validate_folder_name(".")
        assert not ok

    def test_double_dot_rejected(self, kn):
        ok, _ = kn.validate_folder_name("..")
        assert not ok

    def test_empty(self, kn):
        ok, _ = kn.validate_folder_name("")
        assert not ok

    def test_pipe_rejected(self, kn):
        # Windows reserved character
        ok, _ = kn.validate_folder_name("foo|bar")
        assert not ok
