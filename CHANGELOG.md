# Changelog

All notable changes to **KevinNet DNS** are documented in this file.

This project ships only two public releases:

- **v3.2.2** — the original stable release. Still available, still works.
- **v4.1.4** — the current release. Recommended for all users.

There are no intermediate versions on GitHub. Older internal iterations
(3.3.x, 3.4.x, 4.0.x, 4.1.0, 4.1.1, 4.1.2, 4.1.3) were superseded and
are no longer published.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and version numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [4.1.4] — 2026-05-25

A bug fix release on top of 4.1.3.

### Fixed

- **The Results table no longer clears when you switch language after
  a scan.**

  Previous behavior: after running a scan and getting verified
  resolvers, clicking the language toggle (English ↔ فارسی) wiped
  the Results table visually, even though the resolvers were still
  in memory (Save and Export still worked, but the list was no
  longer visible).

  Root cause: the language refresh rebuilds the scanner panel from
  scratch to make sure all card titles, button labels, and hint text
  pick up the new language. The rebuild created a fresh Treeview
  widget and didn't repopulate it from the existing scan results.

  Fix: the language refresh now snapshots the current Treeview rows
  (with their values and tag colors) and the activity log contents
  before destroying the old widgets, then restores them into the new
  ones after rebuild. The badge text and Save/Export button state are
  also re-synced based on `_found_ips`, so the post-scan summary
  stays visible across language toggles.

### Affected users

Anyone who ran a scan and then changed the interface language while
results were still on screen. The data was never actually lost — Save
to MasterDNS/VayDNS Profiles and Export DNS List continued to work —
but the missing visual feedback was confusing.

---

## [4.1.3] — 2026-05-25

A bug fix release on top of 4.1.2 that resolves the Windows-only
Persian text rendering problem.

### Fixed

- **Persian/Arabic text now renders correctly on Windows.**

  Previous behavior on Windows: Persian labels throughout the UI
  (tab names like "اسکنر", card titles like "موتور VPN" and "اتصال",
  button text like "شروع اسکن", status text "آماده", etc.) appeared
  as disconnected isolated letterforms in reversed order. Letters
  weren't joined and the visual order was wrong.

  Root cause: the new card-based UI introduced in 4.1.0 wrote Persian
  text directly to Tk widgets, bypassing the existing
  `arabic_reshaper + python-bidi` pipeline. On macOS, the native
  CoreText renderer shapes Arabic-script text correctly without help.
  On Windows (GDI) and Linux (FreeType), Tk needs the text pre-shaped
  into visual order. The old 3.2.2 code path used this pipeline
  everywhere; the new UI helpers (`make_card`, `field`, `make_seg`,
  `primary_btn`, `secondary_btn`, `save_btn`, tab labels, status bar,
  RESULTS/ACTIVITY headers, mode hints, toasts, dialogs) all missed it.

  Fixed by wrapping every Persian text site with `_bidi()`, which is
  a no-op on macOS (CoreText handles shaping) and applies
  `arabic_reshaper + python-bidi` on Windows and Linux. The fix
  affects approximately 30 widget sites.

- Also removed the stray `.upper()` calls on Persian labels (e.g.
  "موتور VPN", "اتصال") — Persian has no uppercase form, and the
  `.upper()` call could strip directional control marks. English
  labels still get `.upper()` for the design's small-caps appearance.

### Affected users

Anyone running KevinNet on Windows with the app's default Persian
interface. macOS users were unaffected.

If you're on Windows with 4.1.0, 4.1.1, or 4.1.2 and the Persian text
looks broken, upgrade to 4.1.3. As a workaround in older builds,
switching the interface to English via the language toggle worked
around the bug (English text isn't affected).

---

## [4.1.2] — 2026-05-25

A bug fix release on top of 4.1.1.

### Fixed

- **Saving after a scan no longer fails with "No resolvers found" when
  the user toggled the VPN mode between MasterDNS and VayDNS.**

  Previous behavior: switching VPN engine via the segmented control
  silently wiped the in-memory scan results, so clicking Save afterwards
  showed "No resolvers found" even though the log still displayed the
  successful verification line ("Phase 3 complete: 69 resolvers E2E
  verified, ready to save").

  Fixed by removing the unconditional reset on mode change. Scan results
  now persist across mode toggles, and the appropriate save button is
  enabled for whichever engine is active. This also lets users save the
  same scan under both MasterDNS and VayDNS profiles, which several
  users had asked for.

  Workaround in older versions: if you hit this in 4.1.1 or 4.1.0,
  re-run the scan before switching modes, or upgrade to 4.1.2.

- The trash/Clear button still resets everything (results, tree, log,
  buttons) as before — this is the explicit way to start fresh.

---

## [4.1.1] — 2026-05-22

A maintenance release on top of 4.1.0. The list below covers everything
that changed between v3.2.2 and v4.1.1, written from the perspective
of a user upgrading from 3.2.2.

If you were already on 4.1.0, the only new items in 4.1.1 are:

- Buttons in the top bar (Help, Theme, Language) and the VPN mode
  switcher are now disabled while a scan is running, so you can't
  accidentally break the running scan
- When a DoH/DoT scan finishes with results, a one-time guidance
  dialog explains that the existing "Save to VayDNS Profiles" button
  works for DoH/DoT too — the app creates separate `-DoH` and `-DoT`
  profiles automatically. Dismissible with "Don't show again"

The rest of the entry below is what you get if you're coming from 3.2.2.

A major release. This is the recommended version for everyone.

If you've been using v3.2.2, here's what you actually get by upgrading,
explained the way you'd care about it as a user.

### What's new for you

**A redesigned interface**
The whole app got a new look — cleaner panels with proper card layout,
a brand mark in the top left, a colored bar along the side of each
section, an underlined active tab so you can see where you are. The
new design feels closer to a modern desktop app and less like a script
with a window glued on top.

**Light theme, with automatic detection**
There's now a sun/moon icon in the top bar. Click it and the theme
preference flips between dark and light. New users get whatever their
operating system is set to (macOS dark mode, Windows Apps light/dark,
Linux GNOME color scheme). Restart the app once after switching for
the change to take effect everywhere.

**A new scan mode: DoH/DoT (encrypted endpoints)**
Plain UDP/53 DNS traffic gets fingerprinted by Iranian DPI. KevinNet
can now scan public DNS-over-HTTPS (port 443) and DNS-over-TLS (port
853) endpoints. The traffic looks like normal HTTPS and is much
harder to identify as a tunnel. The new "Scan DoH/DoT" button is
visible only in VayDNS mode (MasterDNS doesn't support those
transports). 25 DoH and 18 DoT endpoints ship pre-configured.

**Save DoH/DoT results straight into VayDNS profiles**
After a successful DoH/DoT scan, click the same "Save to VayDNS
Profiles" button you'd use for a normal UDP scan. If your scan found
both DoH and DoT endpoints, the app creates two profiles
automatically — one suffixed `-DoH` and one suffixed `-DoT`. A
one-time guidance dialog appears the first time explaining how this
works.

**Two VPN engines, cleanly separated**
The mode selector (MasterDNS / VayDNS) is now a segmented control
where the active half lifts up with the mode's color (blue for
MasterDNS, purple for VayDNS). The fields and buttons reshape
automatically so you only see what's relevant. The DoH/DoT scan
button disappears when MasterDNS is selected.

**Right-click on the resolver list**
Right-click any IP in the results (or two-finger click / Ctrl-click
on macOS) to get a menu: Copy IP, Copy all IPs, Open output folder
in your file manager.

**Last-launched indicator on profiles**
Each saved profile shows "launched 5m ago", "launched 3h ago", etc.,
in the list — makes it obvious which profile is currently active.

**Profile rows that fit your names**
Long profile names used to get clipped on the right. They now wrap
to a second line. The list is also wider so most names fit on one
line in the first place.

**A real help page**
Click the `?` button. Your browser opens with a clean help page
(themed to match the app) covering the workflow, options, and
troubleshooting — much easier to copy-paste server-setup commands
from than the old in-app dialog. Works offline; mobile-friendly if
you screenshot and read on your phone.

**The app remembers what you last typed**
Your tunnel domain, output folder, and last-used VPN mode are
restored when you reopen the app, so you don't have to retype them
on every launch.

**Clearer error messages**
If you paste a malformed domain, encryption key, or public key, the
app catches it before scanning starts and tells you exactly what's
wrong — instead of failing later with a confusing "parse TOML
failed" or similar.

**Buttons lock during scans**
While a scan is running, the top bar (Help, Theme, Language) and the
VPN mode switcher are disabled. You can no longer accidentally
break the running scan by clicking around. The Stop button stays
enabled — that's your way out.

### What's safer

**Better protection for your encryption keys**
On Linux and macOS, the JSON files that store your MasterDNS
encryption keys (and the generated `client_config.toml`) are now
created with `0600` permissions. Other users on the same machine
can no longer read them.

**Generated configs no longer break on tricky input**
Stray quotes, backslashes, or special characters in your domain or
key field used to produce a broken `client_config.toml`. Inputs are
now properly escaped, and the launch script uses safe shell quoting
on Unix.

**More accurate scans**
The output parser used by the SlipNet verification step is stricter
now — invalid IPs in tool output are silently dropped instead of
being treated as resolvers.

### What's safer to update

**Verifiable downloads**
Every release on GitHub now ships with a `SHA256SUMS.txt` alongside
the binaries. If you download from anywhere other than the official
Releases page, you can verify the binary hasn't been tampered with:

```bash
shasum -a 256 -c SHA256SUMS.txt    # macOS / Linux
Get-FileHash -Algorithm SHA256 KevinNet_Windows_x64.exe   # Windows
```

**Tested before every release**
The build pipeline now runs a 92-test pytest suite before producing
any platform binary. If a test fails, no release is built — so the
code that ships actually works.

### What's the same

- All the original options you know from 3.2.2 are still there
- MasterDNS Profiles and VayDNS Profiles tabs work the same way
- Profile JSON format is backwards compatible — old profiles you
  saved in 3.2.2 will load and launch correctly in 4.1.1
- The bundled VPN binaries (MasterDnsVPN, vaydns-client) are the
  same upstream versions

### Known limitations

- **Theme switching needs a restart.** Tkinter doesn't have a
  proper theme system — colors are baked into widgets at creation
  time. Live re-coloring on toggle produced a half-themed result
  that looked worse than picking a side. The toggle now saves your
  preference and shows a toast confirming the change; restart the
  app once and everything switches cleanly.
- **Profile detail panel still uses the older design.** Only the
  list rows on the left got the new visual treatment. The detail
  panel on the right is functional but looks less polished than
  the rest of the app. This is a deliberate scope decision to keep
  the release manageable — a full port is planned for a future
  release.
- **Profile detail labels don't refresh when you change language.**
  Labels there stay in whatever language was active when the tab
  was first opened. Switch back to the Scanner tab and reopen the
  Profiles tab to refresh them. This is a pre-existing limitation
  from v3.2.2, not introduced in 4.1.1.

### How to upgrade

1. Download `KevinNet_<your-platform>` from the [Releases page](../../releases/latest)
2. (Recommended) verify the SHA-256 against `SHA256SUMS.txt`
3. Run the new binary
4. Your old profiles from 3.2.2 are loaded automatically — nothing
   to migrate

If you hit any problem with 4.1.1, you can keep using v3.2.2 (still
available on the Releases page) while you report the issue.

---

## [3.2.2] — 2026-04-XX

The previous stable release. Still works, still available.

If you used 3.2.2 before, it does exactly the same things it always
did: scans Iranian DNS resolvers, saves MasterDNS or VayDNS profiles,
and launches the VPN client.

**You should pick 3.2.2 only if:**

- You have a working setup on 3.2.2 and don't want to change anything
- You're on an unusual environment where 4.1.1 has a regression you
  reported and we haven't fixed yet

**For everyone else, use 4.1.1.** It has the same features plus the
new ones above (DoH/DoT scanning, light theme, redesigned UI,
hardened input handling, better security on Unix).

Profile files saved in 3.2.2 work in 4.1.1 unchanged, so upgrading
later is risk-free — you can switch versions back and forth without
losing your data.

---
