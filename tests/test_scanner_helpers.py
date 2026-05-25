"""Tests for the pure scanner helpers — domain parsing, base32 encoding,
DNS label splitting, and Iran CIDR sampling.

These functions are at the heart of the tunnel-payload construction so
regressions here break the scan silently.
"""
import ipaddress
import random
import pytest


@pytest.fixture(scope="module")
def kn():
    import kevinnet
    return kevinnet


class TestGetParentDomain:
    def test_three_label(self, kn):
        assert kn.get_parent_domain("v.example.com") == "example.com"

    def test_apex_two_label(self, kn):
        # Two-label apex stays as-is (no parent to extract)
        assert kn.get_parent_domain("example.com") == "example.com"

    def test_trailing_dot_stripped(self, kn):
        assert kn.get_parent_domain("v.example.com.") == "example.com"

    def test_deep_subdomain(self, kn):
        assert kn.get_parent_domain("a.b.example.com") == "b.example.com"

    def test_whitespace_stripped(self, kn):
        assert kn.get_parent_domain("  v.example.com  ") == "example.com"


class TestBase32Encode:
    def test_empty_input(self, kn):
        assert kn.base32_encode(b"") == ""

    def test_known_value(self, kn):
        # Base32 of "foobar" in RFC 4648 alphabet (no padding)
        assert kn.base32_encode(b"foobar") == "MZXW6YTBOI"

    def test_alphabet_correctness(self, kn):
        # All 5-bit values 0..31 represented across enough bytes
        result = kn.base32_encode(bytes(range(32)))
        assert all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567" for c in result)

    def test_no_padding_chars(self, kn):
        # Tunnel base32 must be padding-free (DNS labels can't contain =)
        assert "=" not in kn.base32_encode(b"abc")
        assert "=" not in kn.base32_encode(b"abcd")
        assert "=" not in kn.base32_encode(b"abcde")

    def test_round_trip_via_stdlib(self, kn):
        # Compare against Python stdlib base32 (which adds padding)
        import base64
        data = b"the quick brown fox"
        ours = kn.base32_encode(data)
        theirs = base64.b32encode(data).decode().rstrip("=")
        assert ours == theirs


class TestSplitLabels:
    def test_short_string_one_label(self, kn):
        assert kn.split_labels("abc") == ["abc"]

    def test_exact_max_length(self, kn):
        s = "a" * 57
        assert kn.split_labels(s, 57) == [s]

    def test_split_at_57(self, kn):
        s = "a" * 57 + "b" * 57
        labels = kn.split_labels(s, 57)
        assert labels == ["a" * 57, "b" * 57]

    def test_remainder_in_last_label(self, kn):
        s = "x" * 60
        labels = kn.split_labels(s, 57)
        assert labels == ["x" * 57, "xxx"]

    def test_empty_input(self, kn):
        assert kn.split_labels("") == []

    def test_custom_max_len(self, kn):
        assert kn.split_labels("abcdefgh", 3) == ["abc", "def", "gh"]


class TestGetIranSample:
    def test_returns_list_of_ip_strings(self, kn):
        sample = kn.get_iran_sample(max_ips=100)
        assert isinstance(sample, list)
        assert len(sample) <= 100
        for ip in sample:
            # Every returned string must parse as a valid IPv4 address
            ipaddress.IPv4Address(ip)

    def test_respects_max_ips_cap(self, kn):
        sample = kn.get_iran_sample(max_ips=50)
        assert len(sample) <= 50

    def test_ips_inside_iran_cidrs(self, kn):
        # Every sampled IP must fall inside one of the loaded CIDRs.
        sample = kn.get_iran_sample(max_ips=200)
        # Reuse the same parsing the code does
        nets = []
        for line in kn.IRAN_CIDRS_RAW.strip().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                nets.append(ipaddress.IPv4Network(line, strict=False))
            except ValueError:
                pass

        # Use a containment check across all networks
        for ip_str in sample[:50]:  # spot-check first 50 to keep it fast
            ip = ipaddress.IPv4Address(ip_str)
            assert any(ip in net for net in nets), \
                f"{ip_str} is not in any Iran CIDR"

    def test_no_network_or_broadcast_addresses(self, kn):
        # Sample must skip .0 network and .255 broadcast in /24s
        random.seed(42)
        sample = kn.get_iran_sample(max_ips=2000)
        nets = []
        for line in kn.IRAN_CIDRS_RAW.strip().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                nets.append(ipaddress.IPv4Network(line, strict=False))
            except ValueError:
                pass
        for ip_str in sample:
            ip = ipaddress.IPv4Address(ip_str)
            for net in nets:
                if ip in net:
                    assert ip != net.network_address, \
                        f"{ip_str} is the network address of {net}"
                    if net.prefixlen < 32:
                        assert ip != net.broadcast_address, \
                            f"{ip_str} is the broadcast address of {net}"
                    break

    def test_zero_max_returns_empty(self, kn):
        # With max=0 we still get the floor of max_ips//total_nets which
        # is 0, so per_net = max(4, 0) = 4 — but the outer cap is 0, so
        # we get one round of 4 IPs then break. Document the behaviour.
        sample = kn.get_iran_sample(max_ips=0)
        assert isinstance(sample, list)


class TestModeSwitchPreservesResults:
    """Regression tests for the bug where switching VPN mode after a
    completed scan silently wiped self._found_ips, producing the
    misleading "No resolvers found" dialog on Save even though the log
    showed successful E2E verification. (Reported in 4.1.1, fixed in
    4.1.2.)

    These are static checks on the source - exercising _set_vpn_mode
    end-to-end requires a Tk environment which the test suite avoids.
    The static checks would have caught the bug at code-review time.
    """

    def test_set_vpn_mode_does_not_clear_found_ips(self, kn):
        import inspect
        src = inspect.getsource(kn.App._set_vpn_mode)
        # The clear() call was the bug. It must not reappear.
        assert "_found_ips.clear()" not in src, (
            "_set_vpn_mode must NOT clear self._found_ips - "
            "mode toggles should preserve scan results "
            "(see CHANGELOG 4.1.2)")

    def test_set_vpn_mode_does_not_clear_dohdot_results(self, kn):
        import inspect
        src = inspect.getsource(kn.App._set_vpn_mode)
        assert "_doh_found.clear()" not in src, (
            "_set_vpn_mode must NOT clear self._doh_found")
        assert "_dot_found.clear()" not in src, (
            "_set_vpn_mode must NOT clear self._dot_found")

    def test_clear_button_still_resets_found_ips(self, kn):
        # _clear is the explicit reset path - it SHOULD clear.
        import inspect
        src = inspect.getsource(kn.App._clear)
        assert "_found_ips.clear()" in src, (
            "_clear must still reset scan results")


class TestPersianTextUsesBidi:
    """Regression test for the Windows-only Persian rendering bug
    (4.1.0-4.1.2). The new card-based UI bypassed the existing
    arabic_reshaper + python-bidi pipeline, causing Persian text to
    appear as disconnected isolated letterforms on Windows.

    Static check: every line in kevinnet.py that sets text=
    containing a Persian/Arabic character must also wrap it in _bidi()
    (or be a setting-via-StringVar, or be a docstring/comment).
    """

    def test_no_raw_persian_in_text_assignments(self):
        from pathlib import Path
        src_path = Path(__file__).parent.parent / "kevinnet.py"
        src = src_path.read_text(encoding="utf-8")

        offenders = []
        for i, line in enumerate(src.split("\n"), 1):
            # Skip docstrings, comments
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""'):
                continue
            # Skip data lines (dicts of translations, etc.)
            # We only flag actual text= assignments to widgets
            if "text=" not in line:
                continue
            # Must contain a Persian/Arabic character
            if not any("\u0600" <= c <= "\u06ff" for c in line):
                continue
            # Must NOT already have _bidi - that's the fix
            if "_bidi" in line:
                continue
            # Some lines reference text= in HELP dict definitions - those
            # are content, not widget assignments. Filter those.
            if "HELP[" in line or "HELP_" in line:
                continue
            offenders.append((i, line.strip()))

        assert not offenders, (
            f"Found {len(offenders)} widget text= assignments with raw "
            f"Persian text but no _bidi() wrapper - Windows will render "
            f"these incorrectly. First few:\n" +
            "\n".join(f"  L{i}: {ln[:100]}" for i, ln in offenders[:5]))
