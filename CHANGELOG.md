# Changelog

All notable changes to **KevinNet DNS** are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and version numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This changelog covers releases that ship on GitHub. The intermediate
3.3.x development versions were internal iterations and are not published
separately; all of their changes are rolled into 4.0.0 below.

---

## [4.0.0] - 2026-05-22

A major release covering everything between v3.2.2 and v4.0.0. This is a
substantial visual refresh, a meaningful security and robustness pass,
and a real expansion of what KevinNet can scan and save.

### Highlights at a glance

- **Complete visual redesign** with new design system: card-based layout
  with accent bars, segmented control for VPN mode, restyled tab bar
  with underline indicator, branded top bar with logo mark, modern
  status bar with pulse indicator and progress bar
- New **light theme** with toggle, plus automatic detection of the OS
  appearance setting
- New **Scan DoH/DoT** button that probes encrypted DNS endpoints
  (much harder for Iranian DPI to fingerprint than plain UDP/53)
- DoH/DoT scan results save directly into VayDNS profiles
- New **HTML help file** opens in your browser, themed to match the app
- **92 unit tests** now run in CI before any release build
- Profile rows no longer truncate long names or wrap metadata badly
- All MasterDNS encryption keys and config files are now created with
  restrictive permissions on Linux/macOS
- Cleaned up two thousand lines of hardcoded data into editable text
  files under `data/` (still bundled into the binary as fallback)
- Em-dashes and decorative emoji removed throughout

### Added

#### Visual design

- **Iranian Sky palette** with proper dark and light themes. Dark
  uses deep `#0E1419` backgrounds with `#1A2128` elevated cards;
  light uses warm `#FAFAF5` background with pure white cards. Teal
  `#14B8A6` accent throughout, with blue for MasterDNS, purple for
  VayDNS, plus rose, lime, orange for status states.
- **Branded top bar** with square teal logo mark + wordmark +
  vertical divider + tagline. Replaces the previous flat colored
  text-only top bar.
- **Icon-based action buttons** in the top right - Help (`?`),
  theme toggle (sun/moon), and language pill - styled like a
  cohesive set with hover states.
- **Underlined tab bar** with accent text for the active tab and
  a 2px accent underline. Hover state subtly brightens inactive
  tabs. Cleaner than the previous flat colored-pill approach.
- **Card-based scanner panel** with four cards (VPN Engine,
  Connection, Scan Options, Actions). Each card has a colored
  accent bar in its header. The Connection card's accent bar
  recolors to match the active mode (blue for MasterDNS, purple
  for VayDNS).
- **Segmented control** for MasterDNS / VayDNS mode selection.
  The active half lifts visually to the card background with its
  mode color; inactive half stays sunk in the input shade. Cleaner
  than the previous pair of independent pills.
- **Form fields with uppercase labels, monospace inputs where
  appropriate, and focus rings.** Hints wrap properly instead of
  being clipped at the right edge.
- **Status bar above results** with a pulse dot, status text,
  inline progress bar, and a tinted count badge. Replaces the
  three separate widgets the old layout had.
- **Restyled Treeview** with proper column header styling that
  matches the card aesthetic, hover row highlights, and accent-tinted
  selection.
- **Wider profile list pane** (300px instead of 230) so names with
  3+ hyphenated parts fit on one line. Names that DO overflow wrap
  cleanly to a second line instead of being clipped.

#### Functionality

- **Scan DoH/DoT button** (visible only in VayDNS mode) tests 25 DoH
  endpoints and 18 DoT endpoints. Working endpoints stream into the
  results with a 🔒 marker and a latency number.
- **Save DoH/DoT results as VayDNS profiles** - the existing Save to
  VayDNS Profiles button is now transport-aware. If your scan finds
  both DoH and DoT endpoints, you get two profiles (e.g. `Iran-DoH`
  and `Iran-DoT`), each with all the working endpoints baked in.
- **Multi-endpoint launch script** for DoH and DoT - previously only
  UDP profiles could fall through multiple resolvers; now any transport
  can. If the first endpoint stalls or fails, the script kills it and
  tries the next one automatically.
- **Light theme** with a one-click toggle in the top bar (sun/moon
  glyph). Persisted across launches. New users get whatever their OS
  is set to (Windows AppsUseLightTheme registry key, macOS
  AppleInterfaceStyle, Linux gsettings color-scheme).
- **HTML help file** generated next to the binary on first click of
  the Help button. Themed to match the active palette, mobile-friendly,
  works offline, easy to copy/paste server-setup commands from.
- **Right-click context menu** on the resolver tree: Copy IP, Copy all
  IPs, Open output folder. Works on Linux/Windows (right-click), macOS
  multi-button mice and trackpads (two-finger), and macOS single-button
  Magic Mouse (Ctrl-click).
- **Last-launched indicator** on each profile (`launched 5m ago`,
  `launched 3h ago`). Makes the active profile obvious in a long list.
- **Persisted UI state** across restarts: last domain, country folder,
  and VPN mode (stored in `kevinnet_settings.json` next to the binary).
- **"Don't show again" checkbox** on the startup help dialog. Hidden
  when help is opened explicitly from the header button.
- **Input validators** for tunnel domain, encryption key, public key,
  and folder name. Bad input is rejected at scan-start with a clear
  translated error message instead of producing confusing `parse TOML
  failed` errors later.
- **87 unit tests** covering validators, scanner helpers, profile
  config building, and the settings module. Runs in CI before every
  release build via a new `test` job that gates the platform builds.
- **SHA-256 manifest** (`SHA256SUMS.txt`) attached to every release
  alongside the binaries. Users can verify downloads haven't been
  tampered with on mirror sites.
- **Mode-context hint** under the VPN mode pills explaining what
  the current mode will scan, so the workflow is obvious instead
  of inferred.

### Changed

- **Scanner panel reshapes based on VPN mode.** The Scan DoH/DoT
  button only appears under VayDNS mode (MasterDNS doesn't support
  encrypted transports). MasterDNS-only and VayDNS-only fields hide
  themselves when the other mode is selected.
- **Profile row sizing** - long profile names now wrap to a second
  line instead of being clipped on the right edge. Metadata
  (`date . N resolvers . transport . launched X ago`) wraps cleanly
  when long. Row padding increased for better readability.
- **Profile filenames** include a 4-character random suffix in
  addition to the timestamp, preventing collisions when two profiles
  are saved within the same second.
- **TOML string escaping** when building `client_config.toml`. A stray
  `"` or `\` in the domain or key field no longer breaks the generated
  config.
- **shlex.quote() defence in depth** on pubkey and domain values
  when building the VayDNS launch command (Unix).
- **Iran CIDR sampling** now correctly avoids network and broadcast
  addresses on every range, and gracefully returns an empty list if
  no ranges are loaded.
- **SlipNet output parser** uses a strict per-octet IPv4 regex plus
  `ipaddress.IPv4Address` validation - invalid IPs in tool output
  are silently dropped instead of being treated as resolvers.
- **Data files extracted from source.** Around 2,400 lines of hardcoded
  data (Iranian CIDRs, public resolvers, WhiteDNS list, DoH/DoT
  endpoint lists) moved into `data/*.txt` files. The full lists are
  also embedded in the source as fallbacks, so the app works on its
  own with no `data/` folder; external files take priority when
  present so advanced users can override the bundled lists.
- **Em-dashes removed throughout.** Replaced with colons or hyphens
  depending on context, in code comments, log messages, and docs.
- **Decorative emoji removed.** Functional emoji that communicate
  status or action stay. Decorative ones are gone.

### Fixed

- **Profile JSONs and client_config.toml are created with 0600
  permissions** on Linux/macOS so other users on the same machine
  can't read your MasterDNS shared encryption key.
- A bare `except:` block in the VPN-mode switcher now catches only
  `Exception` so `KeyboardInterrupt` and `SystemExit` still propagate.
- `_safe_profile_stem` no longer produces filenames starting with `_`
  when the user enters only special characters or emoji. Falls back
  to a default stem.
- DoH/DoT button now hides correctly under MasterDNS mode at startup
  (previously stayed visible on first launch even though the mode
  didn't support it).
- The Save to VayDNS Profiles button now correctly enables after a
  successful DoH/DoT scan.

### Security

- MasterDNS encryption keys are still stored in plaintext in profile
  JSONs (now protected by file permissions on Unix). Moving to
  OS-native keystores (Windows DPAPI, macOS Keychain, Linux Secret
  Service) is planned for a future release.

### Known limitations

- **Theme switching requires a restart.** Tkinter doesn't have a real
  theme system - widget colors are baked in at creation time, ttk
  widgets ignore bg/fg overrides, and hover/selected states have
  their own colors. Attempts at live re-coloring left the UI in a
  half-themed state that looked worse than picking a side. The
  theme toggle now shows a toast confirming the preference was
  saved and a restart will apply it.
- **Profile detail panels (right side of MasterDNS / VayDNS Profiles
  tabs) still use the v3.2.2 visual design**, not the new card
  system. The profile rows in the left list ARE redesigned. A full
  profile-detail port is deferred to a future release to keep this
  push reviewable.
- **Profile tabs don't rebuild on language switch.** Labels in
  the detail panels stay in whatever language was active when the
  tab was first built. Pre-existing behavior, not introduced here.

### Notes for distributors

- The `data/` folder must be bundled with PyInstaller. All bundled
  build scripts and CI workflows already handle this.
- The test job runs on every push and tag and must pass before
  binaries are built. `pip install pytest dnspython` then
  `pytest tests/` to run the suite locally.

---

## [3.2.2] - 2026-04-XX

Last release before the 4.0.0 cleanup pass. See the GitHub release
notes for details.

---

<!--
Add new releases at the top. Sections in this order, omit any that
don't apply:  Added . Changed . Deprecated . Removed . Fixed . Security
-->
