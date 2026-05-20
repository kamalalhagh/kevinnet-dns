# Changelog

All notable changes to **KevinNet DNS** will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and version numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This changelog starts at **v3.3.0**. Earlier releases are not retroactively
documented — see git history and GitHub releases for changes prior to this
version.

---

## [3.3.1] — 2026-05-22

### Fixed

- **Scans found very few resolvers when running from source without a
  `data/` folder next to `kevinnet.py`** — and the DoH/DoT button
  reported "no endpoints configured" for the same reason. The 3.3.0
  release introduced external `data/*.txt` files but only kept a
  five-IP fallback for the embedded constants, which meant the app
  degraded to a near-empty scan list when those files weren't found.
- **DoH and DoT endpoint lists** had no embedded fallback at all, so
  `get_doh_endpoints()` and `get_dot_endpoints()` returned an empty
  list whenever the `data/` folder wasn't present.

### Changed

- **Embedded data lists are now the full lists, not stubs.** The app
  ships with the complete resolver, CIDR, WhiteDNS, and DoH/DoT lists
  baked into the Python source and works correctly out of the box
  with no `data/` folder at all. External `data/*.txt` files still
  take priority when present, so advanced users can still override
  the bundled lists without rebuilding.

---

## [3.3.0] — 2026-05-21

### Added

- **DoH / DoT scanning** — new `🔒  Scan DoH/DoT` button on the scanner
  tab probes a curated list of well-known DNS-over-HTTPS (port 443) and
  DNS-over-TLS (port 853) endpoints. Because the traffic is TLS, it's
  much harder for Iranian DPI to fingerprint as tunnel traffic than
  plain UDP/53. Found endpoints feed straight into VayDNS profiles.
  Curated lists ship in `data/doh_endpoints.txt` and
  `data/dot_endpoints.txt`; both files can be edited or replaced
  without rebuilding the app.
- **Right-click context menu** on the resolver tree: Copy IP, Copy all
  IPs, Open output folder. Works on Linux/Windows (right-click), macOS
  multi-button mice and trackpads (two-finger), and macOS single-button
  Magic Mouse (Ctrl-click).
- **"Last launched" indicator** on each profile in the MasterDNS and
  VayDNS profile lists (`launched 5m ago`, `launched 3h ago`, etc.). Makes
  it obvious which profile is currently active when you have many.
- **"Don't show again" checkbox** on the help dialog when it auto-opens
  at startup. The checkbox is hidden when help is opened explicitly
  from the header button.
- **Persisted UI state** — the app remembers your last domain, country
  folder, and VPN mode across restarts (stored in
  `kevinnet_settings.json` next to the executable).
- **Input validators** for tunnel domains, encryption keys, public keys,
  and folder names. Bad input is now rejected at the start of the scan
  with a clear, translated error message instead of producing confusing
  `parse TOML failed` errors later.
- **Unit test suite** (`tests/`) with 87 tests covering validators,
  scanner helpers, profile config building, and the settings module.
  Runs in CI before any release build — no broken refactor ships.
- **SHA-256 manifest** (`SHA256SUMS.txt`) attached to every GitHub
  release alongside the binaries. Users can verify downloads haven't
  been tampered with on mirror sites.

### Changed

- **Project structure** — the three large hardcoded data blocks (Iranian
  CIDR ranges, public resolvers, WhiteDNS Iran list, ~2,400 lines total)
  moved from `kevinnet.py` into separate text files under `data/`. The
  main file shrunk from ~6,800 to ~4,900 lines and the data lists are
  now editable without rebuilding. Minimal fallback constants stay
  embedded so the app still starts if `data/` is missing.
- **Profile file permissions** — profile JSONs and `client_config.toml`
  files are now created with `0600` permissions on Linux/macOS so other
  users on the same machine can't read your MasterDNS encryption key.
- **Profile filenames** now include a 4-character random suffix in
  addition to the timestamp, preventing collisions when two profiles
  are saved within the same second.
- **TOML values are properly escaped** when building `client_config.toml`.
  An accidentally-pasted `"` or `\` in the domain or key field no longer
  breaks the generated config.
- **Shell command building** for VayDNS launch scripts now uses
  `shlex.quote()` on the pubkey and domain values (Unix). Defence in
  depth — the validators reject bad input upstream, but quoting
  guarantees the shell can never misinterpret the command.
- **Iran CIDR sampling** (`get_iran_sample`) now correctly avoids
  network and broadcast addresses on every range, and gracefully
  returns an empty list if no CIDR ranges are loaded.
- **SlipNet output parser** uses a strict per-octet IPv4 regex plus
  `ipaddress.IPv4Address` validation — invalid IPs in tool output are
  silently dropped instead of being treated as resolvers.

### Fixed

- A bare `except:` block in the VPN-mode switcher now catches only
  `Exception` so `KeyboardInterrupt` and `SystemExit` still propagate.
- `_safe_profile_stem` no longer produces filenames starting with `_`
  when the user enters only special characters or emoji — falls back to
  the default stem name.

### Security

- MasterDNS encryption keys are still stored in plaintext in profile
  JSONs — the `0600` permissions reduce the local-machine exposure,
  but moving to OS-native keystores (Windows DPAPI, macOS Keychain,
  Linux Secret Service) is planned for a future release.

### Notes for Distributors

- The `data/` folder must be bundled with PyInstaller. All bundled
  build scripts (`build_linux.sh`, `build_mac_universal.sh`,
  `build_windows.bat`) and CI workflows already handle this.
- The test job runs on every push/tag and must pass before binaries
  are built. `pip install pytest dnspython` + `pytest tests/` to run
  the suite locally.

---

<!--
Add new releases at the top. Sections (in this order, omit any that
don't apply):  Added · Changed · Deprecated · Removed · Fixed · Security
-->
