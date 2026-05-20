"""
KevinNet DNS
Created by Kevin Haji  |  kevinhaji.com  |  kevin.fullstack.dev@gmail.com
Cross-platform: Windows (x86/ARM), macOS, Linux (x86/ARM)
"""
from __future__ import annotations
import asyncio, os, queue, random, sys, threading, time
from datetime import datetime
from pathlib import Path

__version__ = "3.3.0"

# ── Embedded app icon (base64 PNG, 256x256) ────────────────────
ICON_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAJ7UlEQVR4nO3dPW4byRYG0PLDAAYmUWJoDY68EL3lMPIKHGk5w4U48hoIJ0oMOPJLHjUU1WT/VXfdqjonGUi2yAanv4+3qptWSgAAAEAPPpQ+gEsPnz7/KX0MsIeXnz9CZK/YQQg7vFWiFHZ9QqGHafYqg12eRPBhma2LYNMHXxL8j38/bHEoEMbvXy+zf2arItjkQecEX+Dp3ZxCyF0E2QtgSviFHoZNKYOcJZC1AMbCL/gwzVgR5CqBLA8i+LCNrYtgdQHcC7/gQx73imBNCfxn6Q+mJPywl3t5WnOZfXEBCD/sa4sSWDQ63HoywYd93FoSzF0OzJ4AhB/Ku5W3uZPAqj2AsYMBtpMjd7MKYKhdhB/KGcrfnClgcgH4QA/UY2peJxWAdT/EtWY/YPEegPBDHEvzOFoA1v1QhyX7AVmuAgB1ulsA3v2hLnOnABMAdOxmAXj3hzrNmQJMANCxyQXg3R/qMTWvgwXgrj9oz1CuLQGgY5MKwPgP9ZmSWxMAdEwBQMfeFYANQGjXdb5HJwDrf6jXWH4tAaBjCgA6pgCgY3+VPgBozel4+Hr9vcen528ljmXMu18icL1LaBOQ6E7HQ3p8ei59GIPBv1aiCK5/icjlLw+xBKBqp+PhzX8LHsdo+Of8vb1UOwHUNGaxjaHQl5gEloR6z3O1uQng1gserV3Zzq13/L0ngaXnXJRztboCGHvhorywbON0PIyGvPRyoCZVFUCt6yzyiBbstedZhPO0qgKgX3PDH60solIAhLc0zAFK4J/SBzDGjUCEtjbEa+8ROB0PX1YdQHAKgLByvYOvDfHj0/P3G49bfA2/VnX3AUS924q8Mo/vX1JK37e4R2BNCex1nt67D6C6CeDx6fnbvRd9rxd1y/VlhNtaS9nodf1+fuyeX9shVW4C3gq5d/667bFpl/s5lp5zUc7V6iaAsygvIHkE2LFfbGwqHfr7Wx7PHFVOALSlwO272R9zaqgjhT+liicA2lDqnX+L/YBzuGv6oJoCoJjSY/9Wm4JRwz7EEoDdTflAz16iHEcpCoBdRQtc75cFFQC7Ef54FAC7EP6YbAKyuUjhF/y3TABsSvhjUwBsRvjjswQgu0jBT0n47zEBkJXw10UBkI3w10cBkIXw18keAKtFCr/gz2MCYBXhr5sCYDHhr58lALNFCn5Kwr+GCYBZhL8tCoDJhL89lgBMEin8gp+PCYBRwt8uBcBdwt82BcBNwt8+ewC8Eyn4KQn/lkwAvCH8fVEAvBL+/lgCkFKKFX7B348JAOHvmALonPD3zRKgU5GCn5Lwl2IC6JDwc6YAOiP8XFIAHRF+rtkD6ESk8At+HCaADgg/tyiAxgk/91gCNCpS8FMS/qhMAA0SfqZSAI0RfuawBGhIpPALfh1MAI0QfpZQAA0QfpZSAJUTftawB1CpSMFPSfhrZQKokPCTiwKojPCTkyVARSKFX/DbYAKohPCzBQVQAeFnK5YAgUUKfkrC3yITQFDCzx4UQEDCz14UAHcJf9vsATBI8PtgAuAd4e+HAuAN4e+LAuCV8PdHAZBSEv5eKQCEv2MKoHPC3zeXATsl+KRkAuiS8HOmADoj/FxSAB0Rfq4pgE4IP0MUQAeEn1tcBWiY4DNGATRK+Ms5HQ9fr7/3+PT8rcSxjLEEaJDwlzMU/nvfL00BNEb4yxkLecQSUAABLQ2x8JczNdzRSkABBDU3zMLPEgoAOqYAgpr7LwNH+5eEqYMCCGhpmJUAcymAxiiBMqZe5492P4ACaJASKGMs3NHCn5ICaJYSKONWyCOGP6WUPlx/4+HT5z+XX3/8+2G/o6lITQFzibBvv3+9vPn65eeP19ybADpQU1mxLwXQCSXAEAXQESXANQXQGSXAJQXQISXAmQLo1Ol4UAQogN4pgb4pAJRAxxQAKSUl0CsFwCsl0B8FwBtKoC8KgHeUQD8UAINcJuyDAuAuJdA2BRBQtI/vKoF2KYCglAB7UACBPT49hyoCJdAeBVABJcBWFEAllABbUAAViVYCiqB+CqAykUogJdNA7RRAhZQAuSiASrlCQA4KoHJKgDUUQAOUAEspgEYoAZZQAA2JVgKKID4F0JhIJZCSaSA6BdAgJcBUCqBRLhMyhQJonBLgHgXQASXALQqgE9FKQBHEoAA6EqkEUjINRKAAOqMEuKQAOqQEOFMAnXKZkJQUQPeUQN8UAEqgYwqAlFK8ElAE+1AAvIpUAimZBvagAHhDCfRFAfCOKwT9UADcpATapwC4Swm0TQEwSgm0SwEwSbQSUAR5KAAmi1QCKZkGclAAzKIE2qIAmM1lwnYoABZTAvVTAKyiBOqmAFgtWgkogukUAFlEKoGUTANTKQCyUQL1UQBkpQTqogDIzmXCeigANqME4lMAbEoJxKYA2Fy0ElAE/1IA7CJSCaRkGjhTAOxGCcSjANiVEohFAbC7SJcJoxxHKQqAYkqHr/TzR/BX6QOgb49Pz0XG8C3Dfzoevg4837fNnnAFBUBxe5fAVuEfCv71n0UrAksAQqh9HL8X/iV/by/VTgA1jVlMs8cksEXRzA316Xj4GuVcrXICuPWCR2tX5tvyCkGE8K/9udyqmwDGXri92rX2kTW63NOA/1/DqpoAal1nsUzG0H7J9UCX1p5nEc7T6iYA+rJ2Ejj//Ol4WFwCj0/P3xcfQHAKgPCWlsB5glgT4NPx8GVNeaSU/rviZzenAKjC3BLItXy4Vx4TRvh/shzEhqraA6BvFW7khX73T6myApi6ux/lGiv5TblMuFdRrD3PIpynVRVASuMvWoQXle3dCnmFU0JR1RVASrdDLvx9uQ57ifAvPeeinKsfrr/x8Onzn8uvP/79sN/RwAKn46H4O/+ca/p7h//3r5c3X7/8/PGa+yonALhUOvz/P4Yq96dMAJBZtA+q3ZsAFAA0zhIAGKQAoGMKADo2WgDX6wegHmP5fVcAlxsEQFuu820JAB1TANCxSQVgHwDqMyW3JgDo2GAB2AiE9gzlevIEYBkA9ZiaV0sA6NjNAhgaF0wBEN9QTm8t600A0LG7BWAKgLrMefdPyQQAXRstAFMA1GHuu39KKyYAJQBxLM3jpAK41SJKAMq7lcMpN/RNngDcHQj1mJrXWUsA+wEQy5J1/6UsVwGUAOwvR+5mF4D9AChvzbr/0uJ1/fXvD7jkdwnANu690S7Zp1u8BLj3ZKYByC93+FNauQegBGAfW4Q/pRVLgEv3lgMpWRLAUmNvpGsvz2e9tq8III+tg3+W/eaesRJISRHALVOWzjlvytvk7r4pJXCmDOjdnP2y3Hfkbnp775wiOFMItG7JBvlWt+Lvcn//kiIAtv8Mzq4f8FEEMM1eH74r9gk/ZQBvlfjEbaiP+CoFeuHj9QAAQAH/AzFTLcS0T04yAAAAAElFTkSuQmCC"
)

# Windows asyncio fix — MUST be before any asyncio usage

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

try:
    import tkinter as tk
    from tkinter import messagebox, scrolledtext, ttk, simpledialog
    import tkinter.font as tkfont
except ImportError:
    import subprocess, platform
    msg = "tkinter not found.\n\n"
    if platform.system() == "Darwin":
        msg += "Fix:\n  brew install python-tk\n\nThen rebuild the app."
    elif platform.system() == "Linux":
        msg += "Fix:\n  sudo apt install python3-tk\n\nThen rebuild the app."
    else:
        msg += "Reinstall Python from https://python.org (include tcl/tk option)."
    try:
        # Try to show a native dialog even without tkinter
        if platform.system() == "Darwin":
            subprocess.run(["osascript", "-e",
                f'display dialog "{msg}" buttons {{"OK"}} default button "OK" with icon stop'],
                capture_output=True)
        elif platform.system() == "Linux":
            subprocess.run(["zenity", "--error", "--text", msg], capture_output=True)
    except Exception:
        pass
    print(msg)
    sys.exit(1)

try:
    import dns.asyncresolver, dns.exception, dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

# ── Save directory: next to the .exe / .py ──────────────────────
def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


# ── Input validators ─────────────────────────────────────────────
# Used both at scan-start (UI-driven) and by tests. Pure functions —
# all return (ok: bool, error_message_en: str).

import re as _re_mod
_DOMAIN_RE = _re_mod.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,63}\.?$"
)
_HEX_RE   = _re_mod.compile(r"^[0-9a-fA-F]+$")


def validate_domain(domain: str) -> tuple[bool, str]:
    """Validate a tunnel domain like v.example.com or t.example.com.

    Accepts any RFC-1035-style domain with at least two labels and a
    valid TLD. Trailing dot is allowed.
    """
    d = (domain or "").strip()
    if not d:
        return False, "Domain is empty"
    if len(d) > 253:
        return False, "Domain is too long (max 253 chars)"
    if not _DOMAIN_RE.match(d):
        return False, "Domain format looks invalid (e.g. v.example.com)"
    return True, ""


def validate_masterdns_key(key: str) -> tuple[bool, str]:
    """Validate the MasterDNS shared encryption key.

    Must be exactly 32 characters. We don't enforce hex because some
    server setups use printable ASCII keys generated by the upstream
    project's helper script.
    """
    k = (key or "").strip()
    if not k:
        return False, "Encryption key is empty"
    if len(k) != 32:
        return False, f"Encryption key must be 32 characters (got {len(k)})"
    # Reject control characters and shell metas — defence in depth
    if any(c < " " or c == '"' or c == "\\" for c in k):
        return False, "Encryption key contains invalid characters"
    return True, ""


def validate_vaydns_pubkey(pubkey: str) -> tuple[bool, str]:
    """Validate the VayDNS public key. Must be 64 lowercase hex chars.

    Mixed case is accepted (we normalise on save) — but only hex chars."""
    k = (pubkey or "").strip()
    if not k:
        return False, "Public key is empty"
    if len(k) != 64:
        return False, f"Public key must be 64 hex characters (got {len(k)})"
    if not _HEX_RE.match(k):
        return False, "Public key must contain only hex characters (0-9, a-f)"
    return True, ""


def validate_folder_name(name: str) -> tuple[bool, str]:
    """Validate a country/folder name. Must produce a non-empty safe stem."""
    n = (name or "").strip()
    if not n:
        return False, "Folder name is empty"
    # Reject filesystem path separators and reserved characters
    if any(c in n for c in "/\\:*?\"<>|"):
        return False, "Folder name contains invalid characters"
    if n in (".", ".."):
        return False, "Folder name cannot be '.' or '..'"
    return True, ""


# ── App settings (small JSON file next to the app) ───────────────
# Used for "don't show help again", remembering last domain/country/mode,
# and similar UI preferences. Intentionally separate from profiles so it
# can be deleted without losing user configs.

def _settings_path() -> Path:
    return app_dir() / "kevinnet_settings.json"


def load_settings() -> dict:
    import json as _json
    p = _settings_path()
    if not p.exists():
        return {}
    try:
        return _json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_settings(settings: dict) -> None:
    import json as _json
    try:
        _settings_path().write_text(
            _json.dumps(settings, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


def _format_last_launched(ts_str: str, fa: bool = False) -> str:
    """Format a 'YYYY-MM-DD HH:MM:SS' string as a short relative time.

    Returns empty string if input is empty or unparseable. Used by the
    profile list to show "launched 5m ago" etc.

    Why relative time: absolute timestamps are noisy in a list of many
    profiles; relative time makes the most-recent profile obvious at a glance.
    """
    if not ts_str:
        return ""
    try:
        then = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return ""
    delta = datetime.now() - then
    secs  = int(delta.total_seconds())
    if secs < 0:
        # Clock skew or future timestamp — treat as just-now
        return "launched just now" if not fa else "همین الان اجرا شد"
    if secs < 60:
        return ("launched just now" if not fa else "همین الان اجرا شد")
    if secs < 3600:
        m = secs // 60
        return (f"launched {m}m ago" if not fa else f"{m} دقیقه پیش اجرا شد")
    if secs < 86400:
        h = secs // 3600
        return (f"launched {h}h ago" if not fa else f"{h} ساعت پیش اجرا شد")
    d = secs // 86400
    if d < 30:
        return (f"launched {d}d ago" if not fa else f"{d} روز پیش اجرا شد")
    # Older than 30 days — show the absolute date, more informative
    return (f"launched {ts_str[:10]}" if not fa else f"اجرا شد {ts_str[:10]}")


def get_masterdns_exe() -> Path | None:
    """
    Find the MasterDnsVPN binary.
    Priority:
      1. Next to the .exe / app (already extracted or placed by user)
      2. Inside PyInstaller _MEIPASS → copy to app_dir() so it persists
      3. Next to the .py script (dev mode)
    """
    fname = "MasterDnsVPN.exe" if sys.platform == "win32" else "MasterDnsVPN"

    # 1. Already sitting next to the compiled app
    local = app_dir() / fname
    if local.exists():
        return local

    # 2. Bundled inside PyInstaller temp dir (_MEIPASS)
    # Return the _MEIPASS path directly — write_profile_files copies it to the
    # country folder. We never copy to app_dir() to avoid leaving the binary
    # sitting next to the app after every save.
    if getattr(sys, "frozen", False):
        meipass = Path(getattr(sys, "_MEIPASS", ""))
        bundled = meipass / fname
        if bundled.exists():
            return bundled

    # 3. Next to the .py script (running from source)
    src_local = Path(__file__).resolve().parent / fname
    if src_local.exists():
        return src_local

    return None


def bind_mousewheel(widget, canvas):
    """Bind touchpad/mousewheel scroll on widget to scroll canvas.
    Works on macOS (delta), Windows (delta/120), Linux (Button-4/5).
    Call this on every widget inside a scrollable canvas so the
    entire area responds to the touchpad — not just the scrollbar."""
    def _scroll(e):
        if sys.platform == "darwin":
            canvas.yview_scroll(-1 * int(e.delta), "units")
        elif sys.platform == "win32":
            canvas.yview_scroll(-1 * int(e.delta / 120), "units")
        else:
            canvas.yview_scroll(-1 if e.num == 4 else 1, "units")
    widget.bind("<MouseWheel>", _scroll, add="+")
    widget.bind("<Button-4>",   _scroll, add="+")
    widget.bind("<Button-5>",   _scroll, add="+")


def bind_mousewheel_recursive(widget, canvas):
    """Recursively bind mousewheel on widget and all its children."""
    bind_mousewheel(widget, canvas)
    for child in widget.winfo_children():
        bind_mousewheel_recursive(child, canvas)

# ═══════════════════════════════════════════════════════════════
# Data files (CIDR ranges, public resolvers, WhiteDNS Iran list) live in
# the `data/` folder next to the app — bundled into PyInstaller `_MEIPASS`
# at build time, but can be replaced/extended by dropping a newer file
# alongside the executable without rebuilding.
def _data_file(name: str) -> Path | None:
    """Locate a data file by name. Priority:
      1. `data/<name>` next to the .exe / .py (user-editable)
      2. `<name>` next to the .exe / .py (legacy / flat layout)
      3. PyInstaller `_MEIPASS/data/<name>` (bundled fallback)
      4. PyInstaller `_MEIPASS/<name>` (bundled fallback, flat layout)
    Returns None if no copy is found.
    """
    candidates = [
        app_dir() / "data" / name,
        app_dir() / name,
    ]
    if getattr(sys, "frozen", False):
        mp = Path(getattr(sys, "_MEIPASS", ""))
        candidates += [mp / "data" / name, mp / name]
    for p in candidates:
        if p.exists():
            return p
    return None


def _read_data_lines(name: str, fallback: str = "") -> str:
    """Read a bundled data file and return its raw contents.
    Falls back to the provided string literal if no copy is found —
    keeps the app functional even if data files are missing."""
    p = _data_file(name)
    if p is None:
        return fallback
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return fallback


# Minimal embedded fallback — just enough to start the app if data/ is missing.
# The full lists live in data/public_resolvers.txt and data/iran_cidrs.txt.
_MIN_PUBLIC_RESOLVERS = """
8.8.8.8
8.8.4.4
1.1.1.1
1.0.0.1
9.9.9.9
"""

_MIN_IRAN_CIDRS = """
2.176.0.0/12
5.22.0.0/17
5.52.0.0/16
5.106.0.0/16
"""

_MIN_WHITE_DNS = """
185.51.200.1
217.218.155.155
"""

BUILTIN_RESOLVERS = _read_data_lines("public_resolvers.txt", _MIN_PUBLIC_RESOLVERS)

# ═══════════════════════════════════════════════════════════════
#  IRAN IPv4 CIDR RANGES  (loaded from data/iran_cidrs.txt)
# ═══════════════════════════════════════════════════════════════
IRAN_CIDRS_RAW = _read_data_lines("iran_cidrs.txt", _MIN_IRAN_CIDRS)


CONFIG_TEMPLATE = '''\
# ==============================================================================
# MasterDnsVPN Go Client Configuration (Sample)
# This sample is written for the current Go client implementation.
# Every key below is read by code or intentionally kept as an active runtime knob.
# Profile below is biased toward lossy / high-latency links with many resolvers.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1) Tunnel Identity & Security
# What this section does:
# - Defines which tunnel domains this client will use.
# - Defines payload encryption and the shared key that must match the server.
# ------------------------------------------------------------------------------

# Tunnel domains used to build DNS queries.
# Must match server DOMAIN values exactly.
# At least one domain is required.
# All domains must be handled by the same server. Do not use different domains across multiple servers.
DOMAINS = ["{domain}"]

# Encryption method for tunnel payloads.
# Allowed values:
# 0 = None
# 1 = XOR
# 2 = ChaCha20
# 3 = AES-128-GCM
# 4 = AES-192-GCM
# 5 = AES-256-GCM
# Must match server DATA_ENCRYPTION_METHOD.
DATA_ENCRYPTION_METHOD = {encryption_method}

# Shared encryption key.
# Required on the client.
# Must match the server-side key file contents.
ENCRYPTION_KEY = "{key}"

# ------------------------------------------------------------------------------
# 2) Local Proxy Listener
# What this section does:
# - Controls where the local client proxy listens.
# - Controls whether local SOCKS authentication is required.
# ------------------------------------------------------------------------------

# Local mode.
# Allowed values:
# "SOCKS5" = normal proxy mode for browsers/apps
# "TCP"    = raw TCP tunnel mode
PROTOCOL_TYPE = "SOCKS5"

# Local bind address for the client proxy.
# For local-only use, "127.0.0.1" is fine.
# On systems where apps prefer IPv6 localhost (for example some macOS setups),
# "localhost" can be a better choice.
# If you want other devices on your network to use this proxy, use "0.0.0.0"
# and enable SOCKS5_AUTH.
LISTEN_IP = "127.0.0.1"
LISTEN_PORT = {listen_port}

# Local SOCKS5 authentication.
# This protects the local proxy itself, not the remote server.
SOCKS5_AUTH = false
SOCKS5_USER = "master_dns_vpn"
SOCKS5_PASS = "master_dns_vpn"

# ------------------------------------------------------------------------------
# 3) Local DNS Service
# What this section does:
# - Controls the optional built-in local DNS listener.
# - Controls local DNS cache size, TTL, pending timeout, and fragment assembly.
# ------------------------------------------------------------------------------

# When true, the client exposes a local DNS server on LOCAL_DNS_IP:LOCAL_DNS_PORT.
LOCAL_DNS_ENABLED = false
LOCAL_DNS_IP = "127.0.0.1"
LOCAL_DNS_PORT = 53

# Local DNS cache sizing.
# Must be >= 1.
LOCAL_DNS_CACHE_MAX_RECORDS = 10000

# TTL used by the local DNS cache in seconds.
# If <= 0, code falls back to a default.
LOCAL_DNS_CACHE_TTL_SECONDS = 14400.0

# Maximum time a local DNS request is allowed to remain pending before it is
# treated as expired locally.
LOCAL_DNS_PENDING_TIMEOUT_SECONDS = 300.0

# Timeout for reassembling fragmented DNS tunnel responses.
# Used when DNS_QUERY_RES packets arrive in multiple fragments.
# Clamped in code to [1s, 600s].
DNS_RESPONSE_FRAGMENT_TIMEOUT_SECONDS = 60.0

# Persist local DNS cache to disk.
LOCAL_DNS_CACHE_PERSIST_TO_FILE = true

# Flush interval for persisted local DNS cache.
LOCAL_DNS_CACHE_FLUSH_INTERVAL_SECONDS = 60.0

# ------------------------------------------------------------------------------
# 4) Resolver Selection, Duplication, and Health
# What this section does:
# - Chooses how resolvers are selected.
# - Controls packet duplication for lossy networks.
# - Controls stream-aware resolver failover.
# - Controls background recheck and auto-disable of bad resolvers.
# ------------------------------------------------------------------------------

# Resolver balancing strategy.
# Allowed values:
# 1 = Random
# 2 = Round Robin
# 3 = Least Loss
# 4 = Lowest Latency
# Modes 3 and 4 use runtime feedback from sends/successes.
RESOLVER_BALANCING_STRATEGY = {balancing_strategy}

# Duplicate each normal outgoing tunnel packet this many times.
# Clamped in code to [1, 8].
# Higher values improve resilience but increase bandwidth and CPU usage.
PACKET_DUPLICATION_COUNT = {packet_duplication}

# Duplicate stream setup packets (STREAM_SYN / SOCKS5_SYN) this many times.
# Clamped in code to [PACKET_DUPLICATION_COUNT, 8].
SETUP_PACKET_DUPLICATION_COUNT = {packet_duplication}

# Stream-aware resolver failover.
# If a stream keeps resending on the same preferred resolver, it can move.
# Threshold is clamped to [1, 128].
STREAM_RESOLVER_FAILOVER_RESEND_THRESHOLD = 3

# Minimum seconds between preferred-resolver switches for the same stream.
# Clamped to [0.1s, 120s].
STREAM_RESOLVER_FAILOVER_COOLDOWN = 8.0

# If true, resolvers rejected during initial MTU testing are rechecked in the
# background using the current synced upload/download MTUs.
RECHECK_INACTIVE_SERVERS_ENABLED = true

# Full background recheck cycle interval.
# Clamped to [60s, 86400s].
RECHECK_INACTIVE_INTERVAL_SECONDS = 60.0

# Delay between background rechecks of individual resolver entries.
# Clamped to [1s, 600s].
RECHECK_SERVER_INTERVAL_SECONDS = 5.0

# Number of inactive/runtime-disabled resolver entries rechecked per cycle.
# Clamped to [1, 1024].
RECHECK_BATCH_SIZE = 5

# If true, a resolver is runtime-disabled when it stays timeout-only across the
# configured window and enough observations have been collected.
AUTO_DISABLE_TIMEOUT_SERVERS = true

# Timeout-only observation window in seconds.
# Clamped to [1s, 86400s].
AUTO_DISABLE_TIMEOUT_WINDOW_SECONDS = 90.0

# Minimum observations required before auto-disable can trigger.
# Clamped to [1, 10000].
AUTO_DISABLE_MIN_OBSERVATIONS = 8

# Frequency of auto-disable evaluation.
# Clamped to [0.25s, 600s].
AUTO_DISABLE_CHECK_INTERVAL_SECONDS = 4.0

# If true, payload labels are base-encoded before tunneling.
# Usually keep false unless a specific resolver path behaves better with it.
BASE_ENCODE_DATA = false

# ------------------------------------------------------------------------------
# 5) Compression
# What this section does:
# - Controls payload compression negotiation for upload and download directions.
# ------------------------------------------------------------------------------

# Allowed values:
# 0 = OFF
# 1 = ZSTD
# 2 = LZ4
# 3 = ZLIB
UPLOAD_COMPRESSION_TYPE = 0
DOWNLOAD_COMPRESSION_TYPE = 0

# Minimum payload size before compression is attempted.
# Must be >= 1.
COMPRESSION_MIN_SIZE = 120

# ------------------------------------------------------------------------------
# 6) MTU Discovery
# What this section does:
# - Controls initial resolver validation and MTU discovery.
# - Controls optional export/logging of working resolver MTUs.
# ------------------------------------------------------------------------------

# Minimum accepted upload/download MTUs after testing.
# 0 can be used to effectively disable a bound, but keep realistic values.
MIN_UPLOAD_MTU = {min_upload_mtu}
MIN_DOWNLOAD_MTU = {min_download_mtu}

# Initial maximum MTU search bounds.
# Must be >= the matching MIN value if both are set.
MAX_UPLOAD_MTU = {max_upload_mtu}
MAX_DOWNLOAD_MTU = {max_download_mtu}

# MTU probe retries, timeout, and parallelism.
# Retries and parallelism must be >= 1.
MTU_TEST_RETRIES = 2
MTU_TEST_TIMEOUT = 2.0
MTU_TEST_PARALLELISM = 32

# Export successful MTU-tested resolvers to a file.
SAVE_MTU_SERVERS_TO_FILE = false

# Output file naming / formatting.
# Supported placeholders depend on the logger path:
# {time}, {IP}, {UP_MTU}, {DOWN_MTU}, {DOWN-MTU}, {CAUSE}, {TIME}
MTU_SERVERS_FILE_NAME = "masterdnsvpn_success_test_{time}.log"
MTU_SERVERS_FILE_FORMAT = "{IP} - UP: {UP_MTU} DOWN: {DOWN-MTU}"
MTU_USING_SECTION_SEPARATOR_TEXT = ""
MTU_REMOVED_SERVER_LOG_FORMAT = "Resolver {IP} removed at {TIME} due to {CAUSE}"
MTU_ADDED_SERVER_LOG_FORMAT = "Resolver {IP} added back at {TIME} (UP {UP_MTU}, DOWN {DOWN_MTU})"

# ------------------------------------------------------------------------------
# 7) Runtime Workers, Queues, and Timers
# What this section does:
# - Controls async reader/writer/processor worker counts.
# - Controls queue sizes and dispatcher polling.
# - Controls stream cleanup retention and local UDP associate timeout.
# ------------------------------------------------------------------------------

# Async tunnel runtime worker counts.
# Each must be >= 1.
TUNNEL_READER_WORKERS = 5
TUNNEL_WRITER_WORKERS = 5
TUNNEL_PROCESS_WORKERS = 5

# Per-packet tunnel timeout used in async runtime paths.
# Clamped to [0.5s, 120s].
TUNNEL_PACKET_TIMEOUT_SECONDS = 10.0

# Dispatcher idle polling interval.
# Lower values reduce wake latency but consume more CPU.
# Clamped to [0.001s, 1s].
DISPATCHER_IDLE_POLL_INTERVAL_SECONDS = 0.020

# Channel sizes for async TX/RX pipelines.
# Clamped in code to [64, 65536].
TX_CHANNEL_SIZE = 12288
RX_CHANNEL_SIZE = 16384

# UDP connection pool size per resolver key.
# Clamped to [1, 1024].
RESOLVER_UDP_CONNECTION_POOL_SIZE = 128

# Initial queue/store capacities.
# These reduce reallocations under many active streams.
STREAM_QUEUE_INITIAL_CAPACITY = 256
ORPHAN_QUEUE_INITIAL_CAPACITY = 64
DNS_RESPONSE_FRAGMENT_STORE_CAPACITY = 512

# Local UDP ASSOCIATE read timeout.
# Clamped to [1s, 3600s].
SOCKS_UDP_ASSOCIATE_READ_TIMEOUT_SECONDS = 30.0

# How long terminal streams are retained before cleanup.
# Clamped to [1s, 3600s].
CLIENT_TERMINAL_STREAM_RETENTION_SECONDS = 45.0

# How long cancelled setup streams are retained before cleanup.
# Clamped to [1s, 3600s].
CLIENT_CANCELLED_SETUP_RETENTION_SECONDS = 120.0

# Session init retry profile.
# These shape retry delays after failed init/reset attempts.
# Base/step/max are durations; linear_after is a count threshold.
SESSION_INIT_RETRY_BASE_SECONDS = 1.0
SESSION_INIT_RETRY_STEP_SECONDS = 1.0
SESSION_INIT_RETRY_LINEAR_AFTER = 5
SESSION_INIT_RETRY_MAX_SECONDS = 60.0

# Retry delay after SESSION_BUSY.
# Clamped to [1s, 3600s].
SESSION_INIT_BUSY_RETRY_INTERVAL_SECONDS = 60.0

# Ping/keepalive pacing.
# These control how aggressively the client sends ping traffic depending on
# recent activity.
PING_AGGRESSIVE_INTERVAL_SECONDS = 0.200
PING_LAZY_INTERVAL_SECONDS = 0.750
PING_COOLDOWN_INTERVAL_SECONDS = 2.0
PING_COLD_INTERVAL_SECONDS = 15.0
PING_WARM_THRESHOLD_SECONDS = 5.0
PING_COOL_THRESHOLD_SECONDS = 15.0
PING_COLD_THRESHOLD_SECONDS = 30.0

# ------------------------------------------------------------------------------
# 8) ARQ Reliability & Packing
# What this section does:
# - Controls data/control retransmission behavior.
# - Controls per-stream buffering limits and batch packing.
# ------------------------------------------------------------------------------

# Maximum control blocks packed together in one outgoing batch.
# Clamped to [1, 64].
MAX_PACKETS_PER_BATCH = 5

# ARQ data/control behavior.
# These values are clamped in code and should stay internally consistent.
ARQ_WINDOW_SIZE = 1000
ARQ_INITIAL_RTO_SECONDS = 0.6
ARQ_MAX_RTO_SECONDS = 3.0
ARQ_CONTROL_INITIAL_RTO_SECONDS = 0.5
ARQ_CONTROL_MAX_RTO_SECONDS = 2.0
ARQ_MAX_CONTROL_RETRIES = 120
ARQ_INACTIVITY_TIMEOUT_SECONDS = 1800.0
ARQ_DATA_PACKET_TTL_SECONDS = 2400.0
ARQ_CONTROL_PACKET_TTL_SECONDS = 1200.0
ARQ_MAX_DATA_RETRIES = 120

# Maximum out-of-order gap ahead of rcvNxt that can trigger STREAM_DATA_NACK.
# 0 disables NACK generation entirely.
# Keep this small so only near-miss gaps cause early resend requests.
ARQ_DATA_NACK_MAX_GAP = 64

# Minimum seconds between repeated NACKs for the same missing sequence number.
# Clamped to [0.1s, 30s].
ARQ_DATA_NACK_INITIAL_DELAY_SECONDS = 0.4
ARQ_DATA_NACK_REPEAT_SECONDS = 0.8

ARQ_TERMINAL_DRAIN_TIMEOUT_SECONDS = 120.0
ARQ_TERMINAL_ACK_WAIT_TIMEOUT_SECONDS = 90.0

# ------------------------------------------------------------------------------
# 9) Logging
# What this section does:
# - Controls console/file logger verbosity.
# ------------------------------------------------------------------------------

# Typical values: DEBUG, INFO, WARN, ERROR
LOG_LEVEL = "{log_level}"
'''

RESOLVER_HEADER = '''\
# ==============================================================================
# MasterDnsVPN – Client Resolvers
# Generated by KevinNet DNS · Kevin Haji
# Website: kevinhaji.com  |  Email: kevin.fullstack.dev@gmail.com
# Generated: {timestamp}
# Country: {country}
# ==============================================================================

# One resolver per line.
# Format: IP  or  IP:PORT

'''

# ═══════════════════════════════════════════════════════════════
#  DNS SCANNER
# ═══════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════
#  WHITE DNS IRAN LIST  (loaded from data/white_dns_iran.txt)
# ═══════════════════════════════════════════════════════════════
WHITE_DNS_UDP = _read_data_lines("white_dns_iran.txt", _MIN_WHITE_DNS)

def get_builtin_resolvers() -> list[str]:
    """
    Returns shuffled list of resolvers to test.
    Priority order:
      1. WhiteDNS Iran list (pre-verified from range-scout — best quality)
      2. Well-known public resolvers (Google, Cloudflare, etc.)
    """
    # WhiteDNS Iran pre-verified resolvers (from range-scout android app)
    white_dns = [l.strip() for l in WHITE_DNS_UDP.strip().splitlines()
                 if l.strip() and not l.strip().startswith("#")]

    # Well-known public resolvers
    public = [l.strip() for l in BUILTIN_RESOLVERS.strip().splitlines()
              if l.strip() and not l.strip().startswith("#")]

    # White DNS first (higher quality), then public, deduplicated
    seen = set()
    ips  = []
    for ip in white_dns + public:
        if ip not in seen:
            seen.add(ip)
            ips.append(ip)
    return ips


def get_iran_sample(max_ips: int = 200_000) -> list[str]:
    """Sample IPs evenly from Iran CIDR ranges.

    Returns an empty list if no valid CIDR ranges are loaded (e.g. data file
    missing and fallback is empty) — protects callers from div/0 and surprises.
    """
    import ipaddress as _ip
    nets = []
    for line in IRAN_CIDRS_RAW.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            nets.append(_ip.IPv4Network(line, strict=False))
        except ValueError:
            pass
    total_nets = len(nets)
    if total_nets == 0:
        return []
    random.shuffle(nets)
    per_net    = max(4, max_ips // total_nets)
    ips = []
    for net in nets:
        # Skip network + broadcast addresses (count is usable host count).
        count = net.num_addresses - 2
        if count <= 0:
            continue
        take = min(per_net, count)
        # randint inclusive on both ends — offset 0..count-take so the window
        # [start+1 .. start+take] always stays inside the usable host range.
        offset = random.randint(0, count - take)
        hosts = [str(net.network_address + 1 + offset + i) for i in range(take)]
        ips.extend(hosts)
        if len(ips) >= max_ips:
            break
    random.shuffle(ips)
    return ips[:max_ips]


def get_parent_domain(domain: str) -> str:
    """
    Strip the first label from a domain.
    e.g. v.example.com → example.com
         example.com   → example.com  (already apex)
    """
    trimmed = domain.strip().rstrip(".")
    parts   = trimmed.split(".", 1)
    if len(parts) == 2 and "." in parts[1]:
        return parts[1]
    return trimmed


def base32_encode(data: bytes) -> str:
    """Base32 without padding — matches DNSTT tunnel format."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    output   = []
    buf, bits = 0, 0
    for byte in data:
        buf   = (buf << 8) | byte
        bits += 8
        while bits >= 5:
            output.append(alphabet[(buf >> (bits - 5)) & 0x1F])
            bits -= 5
    if bits > 0:
        output.append(alphabet[(buf << (5 - bits)) & 0x1F])
    return "".join(output)


def split_labels(value: str, max_len: int = 57) -> list[str]:
    """Split a long string into DNS label-sized chunks."""
    return [value[i:i+max_len] for i in range(0, len(value), max_len)]


# ── Core DNS query helper ────────────────────────────────────────
async def _resolve(ip, qname, qtype, timeout, use_edns=False, edns_size=1232):
    """
    Query ip for qname/qtype using dns.asyncresolver.
    Returns (responded, nxdomain, answer_or_none, elapsed_ms)
    """
    try:
        r = dns.asyncresolver.Resolver(configure=False)
        r.nameservers = [ip]
        r.timeout  = timeout
        r.lifetime = timeout
        if use_edns:
            r.use_edns(edns=0, payload=edns_size)
        t0 = time.perf_counter()
        try:
            ans = await r.resolve(qname, qtype)
            return True, False, ans, (time.perf_counter() - t0) * 1000
        except dns.resolver.NXDOMAIN:
            return True, True,  None, (time.perf_counter() - t0) * 1000
        except dns.resolver.NoAnswer:
            return True, False, None, (time.perf_counter() - t0) * 1000
        except dns.resolver.NoNameservers as e:
            errs = getattr(e, "errors", []) or []
            ms   = (time.perf_counter() - t0) * 1000
            if any(len(x) > 4 and x[4] is not None for x in errs):
                return True, False, None, ms
            return False, False, None, 0.0
        except (dns.exception.Timeout, asyncio.TimeoutError):
            return False, False, None, 0.0
    except Exception:
        return False, False, None, 0.0


# ── Transparent proxy detector ────────────────────────────────────
# RFC 3330 documentation IPs — should NEVER have open DNS resolvers.
# If any respond, there is a transparent proxy between client and internet.
_TRANSPARENT_PROXY_IPS = ["192.0.2.1", "198.51.100.1", "203.0.113.1"]

async def detect_transparent_proxy(domain: str, timeout: float) -> bool:
    """Return True if a transparent DNS proxy is detected."""
    parent = get_parent_domain(domain)
    tasks  = [
        asyncio.create_task(
            _resolve(ip, f"{random.randbytes(4).hex()}.{parent}", "A", timeout)
        )
        for ip in _TRANSPARENT_PROXY_IPS
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return any(
        isinstance(r, tuple) and r[0]   # responded = True → proxy present
        for r in results
    )


# ── Phase 1: quick alive check ────────────────────────────────────
async def _quick_alive(ip, domain, timeout, sem):
    """Fast warmup query — only accept response (any rcode)."""
    async with sem:
        # Warmup: direct query to the tunnel domain (as range-scout does)
        responded, _, _, ms = await _resolve(ip, domain, "A", timeout)
        return ip, responded, ms


# ── Phase 2: full 6-check (range-scout algorithm) ────────────────
async def _full_check(ip, domain, timeout, sem):
    """
    6/6 checks — ported from range-scout DnsScanEngine:
      1 NS→A        : resolver forwards to real authoritative NS
      2 TXT         : handles TXT queries (tunnel carries data in TXT)
      3 RND         : forwards random double-subdomain (tested twice)
      4 TUNNEL-REAL : accepts real DNSTT Base32 payload format
      5 EDNS        : supports EDNS payloads 512/900/1232
      6 NXD         : returns real NXDOMAIN for *.invalid (not hijacked)
    """
    async with sem:
        score  = 0
        parts  = []
        ms_out = 0.0
        rnd_ok = dpi_ok = edns_ok = False
        parent = get_parent_domain(domain)

        # Warmup query (range-scout does this before the 6 checks)
        warmup_ok, _, _, ms_out = await _resolve(ip, domain, "A", timeout)
        if not warmup_ok:
            return ip, 0, 6, 0.0, "TIMEOUT", False

        # 1 · NS→A ─────────────────────────────────────────────
        # Query NS records for parent domain, then resolve one NS hostname → A
        try:
            ok, _, ans, _ = await _resolve(ip, parent, "NS", timeout)
            ns_ok = False
            if ok and ans:
                for rdata in ans:
                    ns_host = str(getattr(rdata, "target", "")).rstrip(".")
                    if ns_host:
                        resp2, _, _, _ = await _resolve(ip, ns_host, "A", timeout)
                        if resp2:
                            ns_ok = True
                            break
            score += ns_ok
            parts.append("NS→A" + ("✓" if ns_ok else "✗"))
        except Exception:
            parts.append("NS→A✗")

        # 2 · TXT ──────────────────────────────────────────────
        # Query TXT for random subdomain of parent (not tunnel domain itself)
        try:
            rnd_label = random.randbytes(4).hex()
            ok, _, _, _ = await _resolve(ip, f"{rnd_label}.{parent}", "TXT", timeout)
            score += ok
            parts.append("TXT" + ("✓" if ok else "✗"))
        except Exception:
            parts.append("TXT✗")

        # 3 · RND ──────────────────────────────────────────────
        # Two levels of random: rand.rand.domain, tried twice (range-scout repeat(2))
        try:
            rnd_ok = False
            for _ in range(2):
                l1 = random.randbytes(4).hex()
                l2 = random.randbytes(4).hex()
                ok, _, _, _ = await _resolve(
                    ip, f"{l1}.{l2}.{domain.rstrip('.')}", "A", timeout)
                if ok:
                    rnd_ok = True
                    break
            score += rnd_ok
            parts.append("RND" + ("✓" if rnd_ok else "✗"))
        except Exception:
            parts.append("RND✗")

        # 4 · TUNNEL-REAL (DPI check) ──────────────────────────
        # Build a real DNSTT-format query: Base32-encoded random bytes
        # split into 57-char labels — this is the actual tunnel payload format.
        # Iran's DPI drops these. If we get ANY response, DPI is not blocking.
        try:
            # Calculate payload size (from range-scout tunnelRealismPayload)
            suffix_len  = len(domain.rstrip(".")) + 2
            overhead    = 12 + 4 + suffix_len
            query_size  = 200   # typical DNSTT query size
            available   = max(10, query_size - overhead)
            payload_len = max(5, min(100, available * 5 // 9))

            payload_bytes = random.randbytes(payload_len)
            encoded       = base32_encode(payload_bytes)
            labels        = split_labels(encoded, 57)
            qname         = ".".join(labels) + "." + domain.rstrip(".")
            ok, _, _, _   = await _resolve(ip, qname, "TXT", timeout)
            dpi_ok = ok
            score += dpi_ok
            parts.append("DPI" + ("✓" if dpi_ok else "✗"))
        except Exception:
            parts.append("DPI✗")

        # 5 · EDNS ─────────────────────────────────────────────
        # Test 512, 900, 1232 byte payloads; stop on FORMERR or no OPT record
        try:
            edns_ok = False
            edns_sz = 0
            rnd_sub = random.randbytes(4).hex() + "." + parent
            for buf in (512, 900, 1232):
                responded, nxd, ans, _ = await _resolve(
                    ip, rnd_sub, "A", timeout, use_edns=True, edns_size=buf)
                if not responded:
                    break
                # Check for FORMERR via NoNameservers errors — means EDNS rejected
                # If responded = True and we got here, EDNS was accepted
                edns_ok = True
                edns_sz = buf
            score += edns_ok
            parts.append(f"EDNS{'✓' if edns_ok else '✗'}({edns_sz})")
        except Exception:
            parts.append("EDNS✗(0)")

        # 6 · NXD ──────────────────────────────────────────────
        # Test *.invalid 3 times; need 2/3 to pass (range-scout: good >= 2)
        # Tests against .invalid TLD not the tunnel domain (avoids hijacking check on real domain)
        try:
            good = 0
            for _ in range(3):
                rnd_label = random.randbytes(6).hex()
                responded, nxd, _, _ = await _resolve(
                    ip, f"{rnd_label}.invalid", "A", timeout)
                if responded and nxd:
                    good += 1
            nxd_ok = good >= 2
            score += nxd_ok
            parts.append("NXD" + ("✓" if nxd_ok else "✗"))
        except Exception:
            parts.append("NXD✗")

        # Score threshold: 4/6 minimum (balanced — range-scout default is 2,
        # but for Iran tunnel we need at minimum RND+DPI+EDNS working)
        # Show ALL resolvers that survived Phase 1 (responded to warmup).
        # We score them but don't filter here — E2E is the real gate.
        # A resolver scoring 2/6 might still work perfectly in MasterDNS.
        passes = True   # always show; E2E phase is the actual filter
        return ip, score, 6, ms_out, "  ".join(parts), passes


# ── Master scan (2-phase) ─────────────────────────────────────────
async def run_scan(ips, domain, concurrency, timeout_s, target,
                   on_progress, on_result, on_done, stop_ev):
    """
    Phase 1: quick warmup alive check on all IPs.
    Phase 2: full 6-check (range-scout algorithm) on survivors.

    Phase 2 uses a separate, tighter semaphore (concurrency // 4) because
    each _full_check task can open up to 6 UDP sockets simultaneously.
    Running concurrency * 6 sockets at once causes kernel panics on macOS
    Intel when scanning large pools (200k+).
    """
    # Phase 1: 1 socket per task — use full concurrency
    sem_p1    = asyncio.Semaphore(concurrency)
    # Phase 2: up to 6 sockets per task — cap at concurrency // 4
    p2_conc   = max(20, concurrency // 4)
    sem_p2    = asyncio.Semaphore(p2_conc)

    total_p1  = len(ips)
    survivors = []
    tested_p1 = 0
    found     = 0
    quick_to  = min(timeout_s, 2.0)

    # ── Phase 1 ──────────────────────────────────────────────
    tasks, idx = [], 0
    while (tasks or idx < total_p1) and not stop_ev.is_set():
        while len(tasks) < concurrency and idx < total_p1:
            tasks.append(asyncio.create_task(
                _quick_alive(ips[idx], domain, quick_to, sem_p1)))
            idx += 1
        if not tasks:
            break
        done, pending = await asyncio.wait(
            tasks, return_when=asyncio.FIRST_COMPLETED, timeout=0.5)
        tasks = list(pending)
        for t in done:
            try:
                ip, alive, ms = t.result()
            except Exception:
                tested_p1 += 1; continue
            tested_p1 += 1
            if alive:
                survivors.append(ip)
            pct = tested_p1 / total_p1 * 50 if total_p1 else 0
            on_progress(tested_p1, total_p1, found, pct,
                f"Phase 1/2 — alive scan  {tested_p1:,}/{total_p1:,}"
                f"  alive: {len(survivors)}")
    for t in tasks:
        t.cancel()

    if stop_ev.is_set() or not survivors:
        on_done(tested_p1, 0)
        return

    # ── Phase 2 ──────────────────────────────────────────────
    total_p2  = len(survivors)
    tested_p2 = 0
    tasks, idx = [], 0
    while (tasks or idx < total_p2) and not stop_ev.is_set():
        while len(tasks) < p2_conc and idx < total_p2:
            tasks.append(asyncio.create_task(
                _full_check(survivors[idx], domain, timeout_s, sem_p2)))
            idx += 1
        if not tasks:
            break
        done, pending = await asyncio.wait(
            tasks, return_when=asyncio.FIRST_COMPLETED, timeout=0.5)
        tasks = list(pending)
        for t in done:
            try:
                ip, score, max_s, ms, detail, passes = t.result()
            except Exception:
                tested_p2 += 1; continue
            tested_p2 += 1
            if passes:
                found += 1
                on_result(ip, score, max_s, ms, detail)
            pct = 50 + (tested_p2 / total_p2 * 50 if total_p2 else 0)
            on_progress(tested_p2, total_p2, found, pct,
                f"Phase 2/2 — deep check  {tested_p2:,}/{total_p2:,}"
                f"  verified: {found}")
            if found >= target:
                stop_ev.set(); break
    for t in tasks:
        t.cancel()
    on_done(tested_p1 + tested_p2, found)


# ═══════════════════════════════════════════════════════════════
#  PHASE 3: E2E VERIFICATION via bundled SlipNet binary
#  Runs the actual MasterDNS tunnel test on DNS-verified resolvers.
#  This is the ONLY way to confirm a resolver actually works for
#  MasterDNS — DNS checks alone are not enough.
# ═══════════════════════════════════════════════════════════════

def run_e2e_verify(found_ips: list, domain: str, timeout_s: float,
                   on_log, on_verified, on_e2e_done, stop_ev):
    """
    Pipe found_ips through the bundled SlipNet binary's DNS scanner.
    SlipNet option 2 (DNS Scanner) will test each IP against the real
    MasterDNS protocol including MTU negotiation — the actual tunnel test.

    Writes a temp resolvers file → launches slipnet binary → parses output.
    """
    import subprocess, tempfile, os, re

    bin_path = get_masterdns_exe()
    if not bin_path:
        on_log("⚠  SlipNet binary not found — skipping E2E verification")
        on_e2e_done(found_ips)   # return all found IPs unfiltered
        return

    # Write IPs to a temp file
    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False) as f:
        f.write("\n".join(found_ips) + "\n")
        tmp_path = f.name

    on_log(f"Phase 3 — E2E verify via SlipNet: {len(found_ips)} resolvers → {bin_path.name}")

    try:
        # Build the interactive input sequence:
        # Select option 2 (DNS Scanner)
        # Enter domain
        # Select option 1 (File)
        # Enter file path
        # Accept defaults for concurrency/timeout/querysize
        stdin_input = "\n".join([
            "2",           # DNS Scanner
            domain,        # tunnel domain
            "1",           # File source
            tmp_path,      # path to our temp file
            "",            # concurrency default
            "",            # timeout default
            "",            # query size default
            "n",           # don't save results
        ]) + "\n"

        result = subprocess.run(
            [str(bin_path)],
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=max(30, timeout_s * len(found_ips) + 30),
        )
        output = result.stdout + result.stderr

        # Parse working resolvers from SlipNet output
        # Format: *  IP_ADDRESS   score/6   Xms  details
        import ipaddress as _ipa
        # Strict octet match: each octet is 0-255. Avoids matching e.g. "999.999.999.999"
        _octet = r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)'
        _ip_re = re.compile(
            rf'[*\s]\s+({_octet}(?:\.{_octet}){{3}})\s+(\d)/6\s+(\d+)ms'
        )
        verified = []
        for line in output.splitlines():
            # Lines with * prefix = fully compatible (6/6)
            # Lines without * but with score = partially compatible
            m = _ip_re.search(line)
            if m:
                ip    = m.group(1)
                # Final sanity check — the regex is strict but never trust input
                try:
                    _ipa.IPv4Address(ip)
                except ValueError:
                    continue
                score = int(m.group(2))
                ms    = int(m.group(3))
                if ip in found_ips:   # include any ip slipnet accepts
                    verified.append(ip)
                    icon = "★" if score == 6 else "◆" if score >= 4 else "▸"
                    on_verified(ip, score, ms, f"{icon} E2E {score}/6")

        if verified:
            on_log(f"E2E verified: {len(verified)}/{len(found_ips)} resolvers pass real tunnel test")
        else:
            on_log(f"⚠  E2E: no resolvers passed real tunnel test — returning DNS-verified list")
            verified = found_ips   # fallback: use DNS-verified list

        on_e2e_done(verified)

    except subprocess.TimeoutExpired:
        on_log("⚠  E2E verification timed out — using DNS-verified resolvers")
        on_e2e_done(found_ips)
    except Exception as e:
        on_log(f"⚠  E2E error: {e} — using DNS-verified resolvers")
        on_e2e_done(found_ips)
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════
#  DoH / DoT SCANNER  (port 443 / port 853 resolvers)
# ═══════════════════════════════════════════════════════════════
#
# Why DoH/DoT scanning exists alongside the UDP scanner:
#
# Iran's DPI has been getting steadily better at flagging plain UDP/53
# traffic, including the kind generated by DNS tunnels. DoH (port 443)
# and DoT (port 853) ride on top of TLS, so the DPI sees an opaque
# TLS handshake to a foreign IP — much harder to fingerprint as
# tunnel traffic specifically. The tradeoff:
#
#   DoH (port 443):  hardest to block (looks like HTTPS), slowest per query
#   DoT (port 853):  faster than DoH, but port 853 sometimes blocked outright
#   UDP (port 53):   fastest, easiest to fingerprint, becoming less reliable
#
# Unlike the UDP scan which probes ~200k IPs from Iran ranges, this scans
# a small curated list of well-known DoH/DoT endpoints (one round-trip
# each). The output feeds VayDNS, which natively supports both transports.


def get_doh_endpoints() -> list[str]:
    """Return the list of DoH endpoint URLs to test."""
    text = _read_data_lines("doh_endpoints.txt", "")
    return [l.strip() for l in text.splitlines()
            if l.strip() and not l.strip().startswith("#")]


def get_dot_endpoints() -> list[str]:
    """Return the list of DoT host:port endpoints to test."""
    text = _read_data_lines("dot_endpoints.txt", "")
    return [l.strip() for l in text.splitlines()
            if l.strip() and not l.strip().startswith("#")]


async def _probe_doh(endpoint: str, timeout: float) -> tuple[bool, float]:
    """Send a real DNS query over DoH; return (ok, elapsed_ms).

    Uses a benign query (cloudflare.com A) so the resolver actually has
    to do work — a more honest reachability + latency test than just a
    TCP connect. Runs the sync dns.query.https call in a thread executor
    because dnspython's async DoH support is uneven across versions and
    a thread offload is portable.
    """
    import dns.message, dns.query
    q = dns.message.make_query("cloudflare.com", "A")
    t0 = time.perf_counter()
    try:
        loop = asyncio.get_running_loop()
        # dns.query.https blocks; run in default executor with our timeout.
        await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: dns.query.https(q, endpoint, timeout=timeout),
            ),
            timeout=timeout + 1.0,
        )
        return True, (time.perf_counter() - t0) * 1000
    except Exception:
        return False, 0.0


async def _probe_dot(endpoint: str, timeout: float) -> tuple[bool, float]:
    """Send a real DNS query over DoT; return (ok, elapsed_ms).

    Endpoint is host[:port] — default port 853 when omitted."""
    import dns.message, dns.query
    host, _, port_s = endpoint.partition(":")
    try:
        port = int(port_s) if port_s else 853
    except ValueError:
        return False, 0.0
    q = dns.message.make_query("cloudflare.com", "A")
    t0 = time.perf_counter()
    try:
        loop = asyncio.get_running_loop()
        await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: dns.query.tls(q, host, port=port, timeout=timeout),
            ),
            timeout=timeout + 1.0,
        )
        return True, (time.perf_counter() - t0) * 1000
    except Exception:
        return False, 0.0


async def run_doh_dot_scan(transport: str, endpoints: list[str],
                            concurrency: int, timeout_s: float,
                            on_progress, on_result, on_done, stop_ev):
    """Probe each endpoint once and stream results back via callbacks.

    transport: "doh" or "dot". concurrency is capped low (max 10) because
    each probe holds a TLS connection open — too many parallel TLS handshakes
    against the same provider can trigger rate limits."""
    sem = asyncio.Semaphore(min(max(2, concurrency), 10))
    total = len(endpoints)
    tested = 0
    found  = 0
    probe  = _probe_doh if transport == "doh" else _probe_dot

    async def _one(ep):
        async with sem:
            ok, ms = await probe(ep, timeout_s)
            return ep, ok, ms

    tasks = [asyncio.create_task(_one(ep)) for ep in endpoints]
    for fut in asyncio.as_completed(tasks):
        if stop_ev.is_set():
            for t in tasks:
                t.cancel()
            break
        try:
            ep, ok, ms = await fut
        except Exception:
            tested += 1
            continue
        tested += 1
        if ok:
            found += 1
            on_result(ep, ms)
        pct = tested / total * 100 if total else 0
        on_progress(tested, total, found, pct,
                    f"DoH/DoT scan  {tested}/{total}  alive: {found}")
    on_done(tested, found)


#  DESIGN TOKENS
# ═══════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════
#  BIDI FIX — Persian/Arabic text rendering
# ═══════════════════════════════════════════════════════════════
# ── Linux: install bundled Vazirmatn font so tkinter/fontconfig can use it ───
if sys.platform == "linux":
    def _install_bundled_font() -> None:
        import shutil, subprocess
        search = [app_dir()]
        if getattr(sys, "frozen", False):
            search.append(Path(getattr(sys, "_MEIPASS", "")))
        for base in search:
            src = base / "Vazirmatn-Regular.ttf"
            if src.exists():
                fonts_dir = Path.home() / ".fonts"
                fonts_dir.mkdir(exist_ok=True)
                dst = fonts_dir / "Vazirmatn-Regular.ttf"
                if not dst.exists():
                    shutil.copy2(src, dst)
                    subprocess.run(["fc-cache", "-f", str(fonts_dir)],
                                   capture_output=True, timeout=10)
                break
    try:
        _install_bundled_font()
    except Exception:
        pass

# ── Windows: register bundled Vazirmatn into GDI before Tk initialises ───
if sys.platform == "win32":
    def _install_bundled_font_windows() -> None:
        import ctypes
        search = [app_dir()]
        if getattr(sys, "frozen", False):
            search.append(Path(getattr(sys, "_MEIPASS", "")))
        for base in search:
            src = base / "Vazirmatn-Regular.ttf"
            if src.exists():
                # FR_PRIVATE (0x10): visible only to this process, auto-cleaned on exit
                ctypes.windll.gdi32.AddFontResourceExW(str(src), 0x10, 0)
                break
    try:
        _install_bundled_font_windows()
    except Exception:
        pass

# Tkinter on Windows AND Linux does not auto-join Arabic/Persian characters
# or reorder RTL text. Fix: use arabic_reshaper + python-bidi.
# macOS has native CoreText BiDi — excluded.
#
# Two bidi helpers are defined:
#
#  _bidi(s)        — for Tk widgets (Label, Button, Text, Treeview…).
#                    On Windows: reshape + get_display + LRO…PDF wrapper so
#                    GDI renders the already-visual-ordered string as-is.
#                    On Linux: reshape + get_display (FreeType renders as-is).
#                    Multi-line strings: each line processed independently.
#
#  _bidi_native(s) — for native Win32 dialogs (messagebox, window titles).
#                    Win32's Uniscribe/DirectWrite already handles shaping
#                    and BiDi from logical-order text.  Only a U+200F (RLM)
#                    prefix is needed to signal RTL direction; applying our
#                    own get_display would double-reverse the text.
#                    On Linux (Tk dialogs, not native): same as _bidi.

# Safe no-op fallback — overridden on Windows/Linux below.
# Always defined so show_help and other module-level code can call _bidi()
# on any platform without a NameError (macOS uses CoreText natively).
def _bidi(s: str) -> str:          # type: ignore[misc]
    return s
def _bidi_native(s: str) -> str:   # type: ignore[misc]
    return s

_needs_bidi_fix = sys.platform in ("win32", "linux")
if _needs_bidi_fix:
    try:
        import arabic_reshaper as _ar
        from bidi.algorithm import get_display as _bidi_display

        if sys.platform == "win32":
            def _bidi_line(s: str) -> str:
                if any("\u0600" <= c <= "\u06ff" for c in s):
                    # LRO…PDF prevents GDI from double-applying BiDi on
                    # the already-visual-ordered presentation forms
                    return "\u202d" + _bidi_display(_ar.reshape(s)) + "\u202c"
                return s

            def _bidi(s: str) -> str:
                if isinstance(s, str) and any("\u0600" <= c <= "\u06ff" for c in s):
                    if "\n" in s:
                        return "\n".join(_bidi_line(ln) for ln in s.split("\n"))
                    return _bidi_line(s)
                return s

            def _bidi_native(s: str) -> str:
                """Win32 native dialogs: RLM prefix only, Uniscribe handles the rest."""
                if isinstance(s, str) and any("\u0600" <= c <= "\u06ff" for c in s):
                    return "\u200f" + s
                return s

        else:  # linux — Tk uses FreeType which renders chars in string order
            def _bidi_line(s: str) -> str:
                if any("\u0600" <= c <= "\u06ff" for c in s):
                    return _bidi_display(_ar.reshape(s))
                return s

            def _bidi(s: str) -> str:  # type: ignore[misc]
                if isinstance(s, str) and any("\u0600" <= c <= "\u06ff" for c in s):
                    if "\n" in s:
                        return "\n".join(_bidi_line(ln) for ln in s.split("\n"))
                    return _bidi_line(s)
                return s

            _bidi_native = _bidi  # Linux Tk dialogs need same full processing

    except ImportError:
        _RLM = "\u200f"
        def _bidi(s: str) -> str:  # type: ignore[misc]
            if isinstance(s, str) and not s.startswith(_RLM):
                if any("\u0600" <= c <= "\u06ff" for c in s):
                    return _RLM + s
            return s
        _bidi_native = _bidi  # type: ignore[misc]

    def _patch_widget(cls):
        _oi = cls.__init__
        _oc = cls.configure

        def _ni(self, master=None, cnf={}, **kw):
            if "text" in kw: kw["text"] = _bidi(kw["text"])
            _oi(self, master, cnf, **kw)

        def _nc(self, cnf=None, **kw):
            if "text" in kw: kw["text"] = _bidi(kw["text"])
            return _oc(self, cnf, **kw)

        cls.__init__  = _ni
        cls.configure = _nc
        cls.config    = _nc

    for _c in (tk.Label, tk.Button, tk.Checkbutton, tk.Radiobutton):
        _patch_widget(_c)

    _oc_ttk = ttk.Label.configure
    def _nc_ttk(self, **kw):
        if "text" in kw: kw["text"] = _bidi(kw["text"])
        return _oc_ttk(self, **kw)
    ttk.Label.configure = ttk.Label.config = _nc_ttk

    # ── ttk.Label.__init__ ───────────────────────────────────────
    _orig_ttk_label_init = ttk.Label.__init__
    def _ttk_label_init(self, master=None, **kw):
        if "text" in kw and isinstance(kw["text"], str):
            kw["text"] = _bidi(kw["text"])
        _orig_ttk_label_init(self, master, **kw)
    ttk.Label.__init__ = _ttk_label_init

    # ── tk.Text.insert (activity log / scrolledtext) ─────────────
    _orig_text_insert = tk.Text.insert
    def _text_insert(self, index, chars, *args):
        if isinstance(chars, str):
            chars = _bidi(chars)
        return _orig_text_insert(self, index, chars, *args)
    tk.Text.insert = _text_insert

    # ── ttk.Treeview: profile names and detail strings ───────────
    _orig_tree_insert = ttk.Treeview.insert
    def _tree_insert(self, parent, index, iid=None, **kw):
        if "text" in kw and isinstance(kw["text"], str):
            kw["text"] = _bidi(kw["text"])
        if "values" in kw:
            kw["values"] = tuple(
                _bidi(v) if isinstance(v, str) else v for v in kw["values"])
        return _orig_tree_insert(self, parent, index, iid=iid, **kw)
    ttk.Treeview.insert = _tree_insert

    _orig_tree_item = ttk.Treeview.item
    def _tree_item_patch(self, item, option=None, **kw):
        if "text" in kw and isinstance(kw["text"], str):
            kw["text"] = _bidi(kw["text"])
        if "values" in kw:
            kw["values"] = tuple(
                _bidi(v) if isinstance(v, str) else v for v in kw["values"])
        return _orig_tree_item(self, item, option, **kw)
    ttk.Treeview.item = _tree_item_patch

    # ── messagebox: native Win32 dialogs need _bidi_native ───────
    # (Win32 MessageBoxW uses Uniscribe for shaping+BiDi from logical
    # order; applying get_display would double-reverse the text)
    import tkinter.messagebox as _tkm
    for _mb_fn in ("showinfo", "showwarning", "showerror",
                   "askokcancel", "askyesno", "askretrycancel", "askquestion"):
        _mb_orig = getattr(_tkm, _mb_fn, None)
        if _mb_orig:
            def _make_mb_wrapper(_orig):
                def _wrapper(title=None, message=None, **kw):
                    return _orig(
                        _bidi_native(title)   if isinstance(title,   str) else title,
                        _bidi_native(message) if isinstance(message, str) else message,
                        **kw)
                return _wrapper
            setattr(_tkm, _mb_fn, _make_mb_wrapper(_mb_orig))

    # ── simpledialog.askstring: Tk-rendered dialog, use full _bidi ─
    import tkinter.simpledialog as _tksd
    _sd_orig = _tksd.askstring
    def _sd_askstring(title=None, prompt=None, **kw):
        return _sd_orig(
            _bidi_native(title)  if isinstance(title,  str) else title,
            _bidi(prompt) if isinstance(prompt, str) else prompt,
            **kw)
    _tksd.askstring = _sd_askstring


# ═══════════════════════════════════════════════════════════════
#  DESIGN TOKENS — warm, modern, user-friendly palette
# ═══════════════════════════════════════════════════════════════
BG     = "#1a1f2e"       # deep navy — easy on eyes
PANEL  = "#141824"       # top bar / footer
CARD   = "#212840"       # card surfaces
BORDER = "#2e3a54"       # borders
ACCENT = "#00c9a7"       # teal — scan button
BLUE   = "#5b8ff9"       # periwinkle — save button
GREEN  = "#2ecc71"       # vivid green — success
WARN   = "#f5a623"       # amber — scanning
DANGER = "#e74c3c"       # red — stop
PURPLE = "#7c3aed"       # purple — connect / e2e verified
TEXT   = "#eef2ff"       # near-white
MUTED  = "#7b8db5"       # cool grey labels
INPUT  = "#0f1320"       # input background
HINT   = "#4e5f80"       # secondary hint text

# All button text is always pure black — max readability on any bg
BTN_TEXT = "#000000"
SCAN_FG  = "#000000"
STOP_FG  = "#000000"
SAVE_FG  = "#000000"
CLEAR_FG = "#000000"
BTN_FG   = "#000000"

# Disabled state — clearly off but still readable
DIS_BG   = "#252d42"
DIS_FG   = "#4a5a7a"

# Legacy aliases kept for compatibility
CONN_BG  = PURPLE
CONN_DIS = "#1a0a3a"


def F(size=11, weight="normal"):
    for fam in ("Segoe UI","SF Pro Display","Helvetica Neue","Ubuntu","Arial"):
        if fam in tkfont.families():
            return (fam, size, weight)
    return ("TkDefaultFont", size, weight)

def FM(size=11):
    for fam in ("Consolas","JetBrains Mono","Fira Code","Courier New","Courier"):
        if fam in tkfont.families():
            return (fam, size, "normal")
    return ("TkFixedFont", size, "normal")

def FA(size=11, weight="normal"):
    for fam in ("Vazirmatn","Tahoma","Arial","TkDefaultFont"):
        if fam in tkfont.families():
            return (fam, size, weight)
    return ("TkDefaultFont", size, weight)

# ═══════════════════════════════════════════════════════════════
#  HELP DIALOG
# ═══════════════════════════════════════════════════════════════
HELP = {
    "fa": ("راهنمای استفاده — KevinNet DNS", [
        ("KevinNet چیست؟",
         "KevinNet یک برنامه کاربر-پسند است که تانل DNS را برای شما راه‌اندازی می‌کند.\n"
         "تانل DNS اینترنت شما را از طریق یک سرور شخصی در خارج از ایران عبور می‌دهد\n"
         "بدون اینکه فیلترینگ DPI ایران بتواند آن را تشخیص دهد.\n\n"
         "دو موتور پشتیبانی می‌شود:\n"
         "• MasterDNS — DNS tunnel با Resolver‌های متعدد، بهترین برای ایران\n"
         "• VayDNS    — DNS tunnel با DoH/DoT/UDP، رمزنگاری Noise پروتکل"),

        ("پیش‌نیاز: سرور و دامنه",
         "۱. یک VPS لینوکسی خارج از ایران (Hetzner، DigitalOcean و...)\n"
         "۲. یک دامنه با دو رکورد DNS:\n"
         "   • رکورد A  — ns.yourdomain.com  →  IP سرور (glue record)\n"
         "   • رکورد NS — v.yourdomain.com   →  ns.yourdomain.com\n"
         "   دامنه تانل شما v.yourdomain.com می‌شود\n\n"
         "۳. نصب VPN روی سرور (راهنما در README)\n\n"
         "MasterDNS: بعد از نصب فایل encrypt_key.txt روی سرور دارید\n"
         "           → محتوای آن کلید ۳۲ کاراکتری است\n\n"
         "VayDNS:    بعد از نصب فایل server.pub روی سرور دارید\n"
         "           → روی سرور cat server.pub بزنید\n"
         "           → رشته hex 64 کاراکتری که می‌بینید کلید عمومی است"),

        ("۱  نوع VPN را انتخاب کنید",
         "MasterDNS:  اگر سرور MasterDnsVPN نصب کرده‌اید\n"
         "VayDNS:     اگر سرور VayDNS نصب کرده‌اید\n\n"
         "هر نوع فیلدهای خودش را نشان می‌دهد و فقط دکمه ذخیره همان نوع فعال می‌شود."),

        ("۲  نام کشور / پوشه را وارد کنید",
         "یک نام دلخواه برای این پیکربندی — مثلاً  Iran  یا  Turkey\n"
         "پوشه‌ای با این نام کنار برنامه ساخته می‌شود که:\n"
         "• فایل‌های تنظیمات VPN درون آن ذخیره می‌شود\n"
         "• فایل اجرایی VPN هم در همان پوشه کپی می‌شود\n"
         "• می‌توانید چندین پروفایل با نام‌های مختلف داشته باشید"),

        ("۳  دامنه تانل را وارد کنید",
         "ساب‌دامینی که NS آن به سرور شما اشاره دارد.\n"
         "مثال:  v.example.com\n"
         "این را از تنظیمات سرورتان بگیرید.\n\n"
         "نکته: نام کوتاه‌تر = فضای بیشتر برای داده در هر پکت DNS"),

        ("۴  کلید را وارد کنید",
         "MasterDNS:  کلید ۳۲ کاراکتری از فایل encrypt_key.txt روی سرور\n"
         "VayDNS:     کلید عمومی ۶۴ کاراکتری hex از فایل server.pub روی سرور\n\n"
         "این کلید باید دقیقاً با سرور مطابقت داشته باشد."),

        ("۵  تنظیمات اسکن را انتخاب کنید",
         "هدف (Target): چند Resolver می‌خواهید — پیشنهاد: 100\n"
         "همزمانی: بالاتر از 100 نروید در ایران — بهترین: 80\n"
         "Timeout: شبکه‌های ایران کند — پیشنهاد: 3 ثانیه\n"
         "پول: هر چه بیشتر، Resolver بیشتر — پیشنهاد: 200 (یعنی ۲۰۰ هزار IP)\n\n"
         "→ کم پیدا شد؟ Pool را به 300 یا 500 افزایش دهید\n"
         "→ اسکن را 2-3 بار تکرار کنید — هر بار IP‌های مختلفی تست می‌شود"),

        ("۶  روی ▶ شروع اسکن کلیک کنید",
         "مرحله ۱ (سریع): بررسی زنده بودن همه IP‌های پول\n"
         "مرحله ۲ (دقیق): تست ۶ معیاره — ★6/6 ◆4-5 ▸2-3 ·0-1\n"
         "مرحله ۳ (واقعی): تأیید E2E از طریق باینری VPN\n\n"
         "نتایج رنگی معنایشان است: سبز = عالی، زرد = خوب، نارنجی = ضعیف"),

        ("۷  ذخیره در پروفایل‌ها",
         "MasterDNS: روی '💾 ذخیره در MasterDNS' کلیک کنید\n"
         "VayDNS:    روی '💾 ذخیره در VayDNS' کلیک کنید\n\n"
         "پروفایل با تنظیمات پیش‌فرض ذخیره می‌شود. برای تغییر تنظیمات:\n"
         "→ تب مربوطه را باز کنید → پروفایل را انتخاب کنید → ویرایش کنید"),

        ("۸  اتصال از تب پروفایل‌ها",
         "به تب MasterDNS Profiles یا VayDNS Profiles بروید.\n"
         "پروفایل ذخیره‌شده را از لیست انتخاب کنید.\n"
         "روی 🚀 اتصال کلیک کنید — ترمینال باز می‌شود و VPN شروع به کار می‌کند.\n\n"
         "می‌توانید قبل از اتصال تنظیمات را تغییر داده و ذخیره کنید.\n"
         "با 📋 کپی می‌توانید از یک پروفایل چند نسخه با تنظیمات متفاوت داشته باشید."),

        ("🔧  مقادیر بهینه MasterDNS برای ایران",
         "روش رمزنگاری:    1 — XOR          کمترین سربار در پکت‌های DNS\n"
         "استراتژی بالانس: 3 — Least Loss   ایران افت پکت بالا دارد\n"
         "تکرار بسته:      2 یا 3           افزونگی در شبکه پر افت\n"
         "Max Upload MTU:  80–100           query کوچک‌تر = کمتر DPI trigger\n"
         "Max Download MTU: 700            جلوگیری از fragmentation ISP\n"
         "Min Upload MTU:  38              بیشترین تعداد Resolver در pool\n"
         "Min Download MTU: 400           Resolverهای مرزی را نگه می‌دارد"),

        ("🔧  مقادیر بهینه VayDNS برای ایران",
         "Transport:       UDP             مستقیم‌ترین حالت از ایران\n"
         "Resolver:        خالی            همه Resolverهای اسکن‌شده امتحان می‌شوند\n"
         "Max QNAME Len:   101             ایمن برای اکثر Resolverها\n"
         "Idle Timeout:    10s             اگر قطعی مکرر دارید: 30s\n"
         "Record Type:     txt             بیشترین سازگاری با DPI\n"
         "UDP Workers:     100             اگر خطای socket داشتید: 50\n"
         "Resolver Timeout: 60s           اگر بعد از ۶۰ ثانیه وصل نشد به Resolver بعدی می‌رود"),

        ("تست دوباره و مقایسه",
         "اگر اتصال خوب نبود این مراحل را امتحان کنید:\n"
         "۱. در تب پروفایل، پروفایل را کپی کنید (📋 Duplicate)\n"
         "۲. در نسخه کپی، یک تنظیم را تغییر دهید (مثلاً MTU)\n"
         "۳. هر دو را ذخیره کنید و هر کدام را تست کنید\n"
         "۴. نسخه بهتر را نگه دارید، بقیه را حذف کنید\n\n"
         "برای MasterDNS می‌توانید اسکن را تکرار کنید — هر بار Resolverهای جدید"),

        ("📁  پوشه‌های برنامه — مهم",
         "KevinNet همه پروفایل‌ها را در پوشه‌های خودش کنار برنامه ذخیره می‌کند:\n"
         "• masterdns_profiles/ — پروفایل‌های MasterDNS\n"
         "• vaydns_profiles/    — پروفایل‌های VayDNS\n"
         "• Iran/ یا Turkey/    — فایل‌های اجرایی VPN\n\n"
         "لطفاً این پوشه‌ها را دستی جابجا یا حذف نکنید.\n"
         "برای دسترسی به همه پروفایل‌ها فقط برنامه را باز کنید —\n"
         "همه چیز در تب MasterDNS یا VayDNS Profiles قابل مشاهده است."),
        ("مک — مشکل 'damaged' یا 'cannot be verified'",
         "در ترمینال این دو دستور را بزنید:\n"
         "chmod +x KevinNet_macOS_Universal\n"
         "xattr -d com.apple.quarantine KevinNet_macOS_Universal"),
    ]),
    "en": ("How to use — KevinNet DNS", [
        ("What is KevinNet?",
         "KevinNet is a user-friendly app that sets up a DNS tunnel for you.\n"
         "A DNS tunnel routes your internet through a personal server outside Iran\n"
         "without Iran's DPI filtering being able to detect or block it.\n\n"
         "Two engines are supported:\n"
         "• MasterDNS — DNS tunnel with multiple resolvers, best for Iran\n"
         "• VayDNS    — DNS tunnel with DoH/DoT/UDP, Noise protocol encryption"),

        ("Prerequisite: server and domain",
         "1. A Linux VPS outside Iran (Hetzner, DigitalOcean, etc.)\n"
         "2. A domain with two DNS records:\n"
         "   • A record  — ns.yourdomain.com  →  your server IP  (glue)\n"
         "   • NS record — v.yourdomain.com   →  ns.yourdomain.com\n"
         "   Your tunnel domain is v.yourdomain.com\n\n"
         "3. VPN server installed on the VPS (see README for guides)\n\n"
         "MasterDNS: after install you have encrypt_key.txt on the server\n"
         "           → its contents is your 32-char key\n\n"
         "VayDNS:    after install you have server.pub on the server\n"
         "           → run: cat server.pub\n"
         "           → the 64-char hex string you see is your public key"),

        ("1  Choose VPN type",
         "MasterDNS:  if you installed MasterDnsVPN on your server\n"
         "VayDNS:     if you installed VayDNS on your server\n\n"
         "Each type shows its own fields. Only the matching save button is active."),

        ("2  Enter country / folder name",
         "Any name for this configuration — e.g.  Iran  or  Turkey\n"
         "A folder with this name is created next to the app, containing:\n"
         "• The VPN config files\n"
         "• A copy of the VPN binary\n"
         "You can have multiple profiles with different names."),

        ("3  Enter your tunnel domain",
         "The subdomain whose NS record points to your server.\n"
         "e.g.  v.example.com\n"
         "Get this from your server setup.\n\n"
         "Tip: shorter names leave more room for data inside each DNS packet."),

        ("4  Enter your key",
         "MasterDNS:  32-char key from encrypt_key.txt on the server\n"
         "VayDNS:     64-char hex public key from server.pub on the server\n\n"
         "This must match the server exactly."),

        ("5  Choose scan settings",
         "Target: how many resolvers to find — recommended: 100\n"
         "Concurrency: do not go above 100 inside Iran — best: 80\n"
         "Timeout: Iranian networks are slow — recommended: 3s\n"
         "Pool ×1000: more IPs scanned = more resolvers found — try: 200\n\n"
         "→ Finding very few? Increase Pool to 300 or 500\n"
         "→ Run 2-3 times — each run tests different IPs"),

        ("6  Click ▶ Start Scan",
         "Phase 1 (fast): alive check on all IPs in the pool\n"
         "Phase 2 (deep): 6-check scoring — ★6/6 ◆4-5 ▸2-3 ·0-1\n"
         "Phase 3 (real): E2E tunnel test via the VPN binary\n\n"
         "Green = excellent, Yellow = good, Orange = weak"),

        ("7  Save to Profiles",
         "MasterDNS: click '💾 Save to MasterDNS Profiles'\n"
         "VayDNS:    click '💾 Save to VayDNS Profiles'\n\n"
         "Saved with default settings. To change settings:\n"
         "→ Open the relevant tab → select the profile → edit"),

        ("8  Connect from the Profiles tab",
         "Go to the MasterDNS Profiles or VayDNS Profiles tab.\n"
         "Select your saved profile from the list.\n"
         "Click 🚀 Launch VPN — a terminal opens and the VPN starts.\n\n"
         "You can edit settings before launching and save the changes.\n"
         "Use 📋 Duplicate to make copies with different settings for A/B testing."),

        ("🔧  MasterDNS optimal values for Iran",
         "Encryption Method:    1 — XOR          lowest overhead in DNS packets\n"
         "Balancing Strategy:   3 — Least Loss    Iran has high packet loss\n"
         "Packet Duplication:   2 or 3            redundancy on lossy paths\n"
         "Max Upload MTU:       80–100            smaller queries = less DPI trigger\n"
         "Max Download MTU:     700               avoids ISP fragmentation\n"
         "Min Upload MTU:       38                keeps maximum resolver pool\n"
         "Min Download MTU:     400               keeps marginal resolvers"),

        ("🔧  VayDNS optimal values for Iran",
         "Transport:       UDP             most direct path from Iran\n"
         "Resolver:        (empty)         tries all scanned resolvers in order\n"
         "Max QNAME Len:   101             safe for most resolvers\n"
         "Idle Timeout:    10s             increase to 30s if you see reconnects\n"
         "Record Type:     txt             most compatible under DPI\n"
         "UDP Workers:     100             lower to 50 if you see socket errors\n"
         "Resolver Timeout: 60s           moves to next resolver if stuck for 60s"),

        ("Testing and comparing settings",
         "If the connection is unstable, try these steps:\n"
         "1. In the Profiles tab, duplicate the profile (📋 Duplicate)\n"
         "2. In the copy, change one setting (e.g. Max Upload MTU)\n"
         "3. Save both and test each one\n"
         "4. Keep the better one, delete the rest\n\n"
         "For MasterDNS, repeat the scan to get fresh resolvers — each run finds different IPs."),

        ("📁  App folders — important",
         "KevinNet stores all profiles in folders next to the app:\n"
         "• masterdns_profiles/ — MasterDNS profiles\n"
         "• vaydns_profiles/    — VayDNS profiles\n"
         "• Iran/ or Turkey/    — VPN output files\n\n"
         "Do not move or delete these folders manually.\n"
         "To access all your profiles, just open the app —\n"
         "everything is visible in the MasterDNS or VayDNS Profiles tab."),
        ("macOS — 'damaged' or 'cannot be verified' error",
         "Run these two commands in Terminal:\n"
         "chmod +x KevinNet_macOS_Universal\n"
         "xattr -d com.apple.quarantine KevinNet_macOS_Universal"),
    ]),
}


def show_help(parent, lang, *, allow_dismiss: bool = False):
    """Render the help dialog.

    When `allow_dismiss=True` a "don't show again" checkbox is shown, and
    ticking it persists `help_dismissed=True` in settings so the dialog
    doesn't auto-open on the next launch. The checkbox is hidden when the
    user explicitly opens the help (header button) — they obviously want
    to see it then.
    """
    title, steps = HELP[lang]
    d = tk.Toplevel(parent)
    d.title(title)
    d.configure(bg=PANEL)
    d.resizable(True, True)
    d.grab_set()
    ff = FA if lang == "fa" else F

    tk.Label(d, text=title, bg=PANEL, fg=ACCENT,
             font=ff(14, "bold"), pady=16, padx=24).pack(fill="x")
    tk.Frame(d, bg=BORDER, height=1).pack(fill="x", padx=24)

    scroll_frame = tk.Frame(d, bg=PANEL)
    scroll_frame.pack(fill="both", expand=True)

    canvas   = tk.Canvas(scroll_frame, bg=PANEL, bd=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical",
                               command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    body    = tk.Frame(canvas, bg=PANEL)
    body_win = canvas.create_window((0, 0), window=body, anchor="nw")

    def _on_body_configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
    def _on_canvas_resize(e):
        canvas.itemconfig(body_win, width=e.width)
    body.bind("<Configure>", _on_body_configure)
    canvas.bind("<Configure>", _on_canvas_resize)

    def _on_mousewheel(e):
        if sys.platform == "darwin":
            canvas.yview_scroll(-1 * int(e.delta), "units")
        elif sys.platform == "win32":
            canvas.yview_scroll(-1 * int(e.delta / 120), "units")
        else:
            canvas.yview_scroll(-1 if e.num == 4 else 1, "units")
    canvas.bind("<MouseWheel>", _on_mousewheel)
    canvas.bind("<Button-4>",   _on_mousewheel)
    canvas.bind("<Button-5>",   _on_mousewheel)
    body.bind("<MouseWheel>",   _on_mousewheel)

    inner = tk.Frame(body, bg=PANEL)
    inner.pack(fill="x", padx=24, pady=10)

    # Bind touchpad scroll on every widget inside the canvas
    inner.bind("<Configure>", lambda e: (
        canvas.configure(scrollregion=canvas.bbox("all")),
        bind_mousewheel_recursive(inner, canvas)
    ), add="+")

    for step_title, step_body in steps:
        row = tk.Frame(inner, bg=CARD,
                       highlightbackground=BORDER, highlightthickness=1)
        row.pack(fill="x", pady=4, ipady=6, ipadx=8)
        tk.Label(row, text=step_title, bg=CARD, fg=ACCENT,
                 font=ff(11, "bold"), anchor="w", padx=12,
                 wraplength=520, justify="left").pack(fill="x")
        tk.Label(row, text=step_body,
                 bg=CARD, fg=TEXT, font=ff(10),
                 anchor="w", padx=20, justify="left",
                 wraplength=510).pack(fill="x")

    tk.Frame(d, bg=BORDER, height=1).pack(fill="x", padx=24)

    btn_row = tk.Frame(d, bg=PANEL)
    btn_row.pack(fill="x", pady=14)

    # "Don't show again" — only on the auto-open at startup
    dismiss_var = tk.BooleanVar(value=False)
    if allow_dismiss:
        cb_text = ("دیگر نشان نده" if lang == "fa"
                   else "Don't show again on startup")
        tk.Checkbutton(
            btn_row, text=cb_text, variable=dismiss_var,
            bg=PANEL, fg=MUTED, font=ff(10),
            activebackground=PANEL, activeforeground=TEXT,
            selectcolor=INPUT, bd=0,
        ).pack(side="left", padx=24)

    def _close():
        if allow_dismiss and dismiss_var.get():
            try:
                s = load_settings()
                s["help_dismissed"] = True
                save_settings(s)
            except Exception:
                pass
        d.destroy()

    tk.Button(btn_row,
              text=_bidi("✓  متوجه شدم") if lang == "fa" else "Got it  ✓",
              bg=ACCENT, fg="#000000", font=ff(11, "bold"),
              relief="flat", bd=0, pady=11, padx=30, cursor="hand2",
              activebackground="#00bfa5", activeforeground="#000000",
              command=_close).pack(side="right", padx=24)

    d.update_idletasks()
    screen_h = d.winfo_screenheight()
    screen_w = d.winfo_screenwidth()
    dlg_w    = min(620, screen_w - 80)
    dlg_h    = min(d.winfo_reqheight(), int(screen_h * 0.88))
    px = parent.winfo_x() + parent.winfo_width()  // 2
    py = parent.winfo_y() + parent.winfo_height() // 2
    d.geometry(f"{dlg_w}x{dlg_h}+{px - dlg_w//2}+{py - dlg_h//2}")
    d.minsize(480, 400)


# ═══════════════════════════════════════════════════════════════
#  PROFILES — persist scan results + key config options
# ═══════════════════════════════════════════════════════════════

PROFILE_DEFAULTS: dict = {
    "listen_port":        18000,
    "encryption_method":  1,
    "balancing_strategy": 2,
    "packet_duplication": 2,
    "min_upload_mtu":     38,
    "max_upload_mtu":     150,
    "min_download_mtu":   500,
    "max_download_mtu":   900,
    "log_level":          "INFO",
}

ENC_LABELS = [
    "0 — None", "1 — XOR", "2 — ChaCha20",
    "3 — AES-128-GCM", "4 — AES-192-GCM", "5 — AES-256-GCM",
]
BAL_LABELS = [
    "1 — Random", "2 — Round Robin",
    "3 — Least Loss", "4 — Lowest Latency",
]
LOG_LABELS = ["DEBUG", "INFO", "WARN", "ERROR"]


def profiles_dir() -> Path:
    new_d = app_dir() / "masterdns_profiles"
    old_d = app_dir() / "profiles"
    # Migrate old "profiles" folder to "masterdns_profiles" on first run
    if old_d.exists() and not new_d.exists():
        try:
            old_d.rename(new_d)
        except Exception:
            pass
    new_d.mkdir(parents=True, exist_ok=True)
    return new_d


def load_all_profiles() -> dict:
    import json as _json
    result = {}
    files = sorted(
        profiles_dir().glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for f in files:
        try:
            data = _json.loads(f.read_text(encoding="utf-8"))
            result[f.stem] = data
        except Exception:
            pass
    return result


def _safe_profile_stem(name: str, default: str = "profile") -> str:
    """Build a filesystem-safe filename stem from a user-supplied profile name.

    Falls back to `default` when the input is empty or contains only special
    characters (which would otherwise produce a stem that starts with "_").
    """
    safe = "".join(
        c if c.isalnum() or c in "-_ " else "_"
        for c in name
    ).strip().replace(" ", "_").strip("_")
    return safe or default


def _profile_filename(safe_stem: str, prefix: str = "") -> str:
    """Construct a unique-ish profile filename.

    Adds a 4-char random suffix after the timestamp so two saves within the
    same second don't collide (the timestamp resolution is one second).
    """
    import secrets
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    salt = secrets.token_hex(2)  # 4 hex chars
    if prefix:
        return f"{prefix}{safe_stem}_{ts}_{salt}.json"
    return f"{safe_stem}_{ts}_{salt}.json"


def _write_profile_json(path: Path, profile: dict):
    """Write a profile JSON with restrictive permissions (Unix).

    Profiles may contain the MasterDNS shared encryption key — limit read
    access to the current user. On Windows, the user-profile ACLs already
    restrict this; on Unix the default umask is too permissive.
    """
    import json as _json
    path.write_text(
        _json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if sys.platform != "win32":
        try:
            path.chmod(0o600)
        except Exception:
            pass


def save_new_profile(profile: dict) -> str:
    safe  = _safe_profile_stem(profile.get("name", "profile"))
    fname = _profile_filename(safe)
    _write_profile_json(profiles_dir() / fname, profile)
    return fname[:-5]


def update_profile(stem: str, profile: dict):
    _write_profile_json(profiles_dir() / f"{stem}.json", profile)


def delete_profile(stem: str):
    path = profiles_dir() / f"{stem}.json"
    country_folder = None
    if path.exists():
        try:
            import json as _json
            data = _json.loads(path.read_text(encoding="utf-8"))
            country_folder = data.get("country", "")
        except Exception:
            pass
        path.unlink()
    return country_folder


def _toml_str_escape(value: str) -> str:
    """Escape a string value for embedding inside a TOML basic string.

    TOML basic strings use the same escape syntax as JSON for double quotes,
    backslashes, and control characters. Routing through json.dumps and then
    stripping the surrounding quotes gives us a reliable escape — TOML is a
    superset of this part of JSON's string spec.
    """
    import json as _json
    return _json.dumps(value, ensure_ascii=False)[1:-1]


def build_config_from_profile(profile: dict) -> str:
    opts = {**PROFILE_DEFAULTS, **profile.get("options", {})}
    ts   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Domain and key go inside TOML strings — escape special characters so a
    # stray " or \ in user input doesn't break the resulting client_config.toml
    domain = _toml_str_escape(profile.get("domain", ""))
    key    = _toml_str_escape(profile.get("key", ""))
    cfg  = (CONFIG_TEMPLATE
            .replace("{domain}",    domain)
            .replace("{key}",       key)
            .replace("{timestamp}", ts))
    for k, v in opts.items():
        cfg = cfg.replace(f"{{{k}}}", str(v))
    return cfg


def write_profile_files(profile: dict):
    import shutil as _sh
    country = profile.get("country", "output")
    folder  = app_dir() / country
    folder.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config_path = folder / "client_config.toml"
    config_path.write_text(
        build_config_from_profile(profile), encoding="utf-8"
    )
    # Config contains the shared encryption key — restrict file permissions
    # so other users on the machine can't read it (Unix only; Windows ACLs
    # default to the user's profile being unreadable by other users anyway).
    if sys.platform != "win32":
        try:
            config_path.chmod(0o600)
        except Exception:
            pass
    hdr = (RESOLVER_HEADER
           .replace("{timestamp}", ts)
           .replace("{country}",   country))
    resolvers = profile.get("resolvers", [])
    (folder / "client_resolvers.txt").write_text(
        hdr + "\n".join(resolvers) + "\n", encoding="utf-8"
    )
    exe_src = get_masterdns_exe()
    if exe_src:
        exe_dst = folder / exe_src.name
        try:
            _sh.copy2(str(exe_src), str(exe_dst))
            if sys.platform != "win32":
                exe_dst.chmod(exe_dst.stat().st_mode | 0o111)
        except Exception:
            pass
    return folder


# ═══════════════════════════════════════════════════════════════
#  VAYDNS PROFILES
# ═══════════════════════════════════════════════════════════════

VAYDNS_DEFAULTS: dict = {
    # Transport
    "transport":        "udp",
    "custom_resolver":  "",        # UDP IP, DoH URL, or DoT host:port

    # Local listener
    "listen_port":      7000,

    # QNAME / upstream MTU
    "max_qname_len":    101,       # 101 = ~50 byte MTU with short domains; use 253 for dnstt-compat
    "max_num_labels":   0,         # 0 = unlimited; set to 1 for most DNS-like behaviour

    # Session / reconnect
    "idle_timeout":     "10s",     # must match server; dnstt-compat default is 2m
    "keepalive":        "2s",      # must be < idle_timeout; dnstt-compat default is 10s
    "reconnect_min":    "1s",
    "reconnect_max":    "30s",
    "max_streams":      0,         # 0 = unlimited

    # DNS record type (must match server)
    "record_type":      "txt",     # txt is most compatible; try null for slightly higher throughput

    # Queue / KCP
    "queue_size":       512,
    "kcp_window_size":  0,         # 0 = queue_size/2

    # UDP-specific
    "udp_workers":      100,
    "udp_shared_socket": False,

    # Rate limiting
    "rps":              0,         # 0 = unlimited queries/sec

    # Script resolver timeout (seconds per resolver before trying next)
    "resolver_timeout": 60,

    # Other
    "log_level":        "info",
}

# Iran-recommended VayDNS defaults (shown as hints in the UI)
VAYDNS_IRAN_HINTS: dict = {
    "max_qname_len":    "101  (default — safe for most resolvers)",
    "idle_timeout":     "10s  (increase to 30s if you see frequent reconnects)",
    "keepalive":        "2s   (keep well below idle_timeout)",
    "record_type":      "txt  (most compatible under DPI)",
    "queue_size":       "512  (increase to 1024 on fast connections)",
    "udp_workers":      "100  (lower to 50 if you see socket errors)",
    "rps":              "0    (set to 50 if your resolver rate-limits you)",
}

VAYDNS_TRANSPORT_LABELS = [
    "udp — Plaintext UDP  (port 53)",
    "doh — DNS over HTTPS",
    "dot — DNS over TLS   (port 853)",
]
VAYDNS_RECORD_LABELS = ["txt", "null", "cname", "a", "aaaa", "ns", "mx"]
VAYDNS_LOG_LABELS    = ["debug", "info", "warning", "error"]


def vaydns_profiles_dir() -> Path:
    d = app_dir() / "vaydns_profiles"
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_all_vaydns_profiles() -> dict:
    import json as _json
    result = {}
    files  = sorted(
        vaydns_profiles_dir().glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for f in files:
        try:
            result[f.stem] = _json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            pass
    return result


def save_new_vaydns_profile(profile: dict) -> str:
    safe  = _safe_profile_stem(profile.get("name", "vaydns"), default="vaydns")
    fname = _profile_filename(safe, prefix="vd_")
    _write_profile_json(vaydns_profiles_dir() / fname, profile)
    return fname[:-5]


def update_vaydns_profile(stem: str, profile: dict):
    _write_profile_json(vaydns_profiles_dir() / f"{stem}.json", profile)


def delete_vaydns_profile(stem: str) -> str | None:
    path = vaydns_profiles_dir() / f"{stem}.json"
    country = None
    if path.exists():
        try:
            import json as _json
            country = _json.loads(path.read_text(encoding="utf-8")).get("country", "")
        except Exception:
            pass
        path.unlink()
    return country


def build_vaydns_command(profile: dict, resolver: str,
                          bin_name: str | None = None) -> str:
    """Return the full vaydns-client shell command for a single resolver.

    bin_name defaults to the arch-specific name found by get_vaydns_exe(),
    falling back to the generic name. Pass it explicitly when you already
    know the copied filename.

    Pubkey and domain come from user input — quote them via shlex on Unix
    so a stray space or quote in user paste can't break the command or
    inject an extra flag. On Windows the same script runs in cmd.exe which
    uses different quoting; for now we rely on input validation there.
    The `resolver` argument is left as-is because the caller may pass
    `"$RESOLVER"` (shell variable expansion) for multi-resolver scripts.
    """
    import shlex as _shlex
    opts      = {**VAYDNS_DEFAULTS, **profile.get("options", {})}
    domain    = profile.get("domain", "")
    pubkey    = profile.get("pubkey", "")
    transport = opts["transport"]
    listen    = f"127.0.0.1:{opts['listen_port']}"

    if sys.platform != "win32":
        # Defence in depth — input validation should already reject bad chars
        # but shlex.quote guarantees no shell-meta surprises.
        pubkey_q = _shlex.quote(pubkey)
        domain_q = _shlex.quote(domain)
    else:
        pubkey_q = pubkey
        domain_q = domain

    if bin_name is None:
        src = get_vaydns_exe()
        if src:
            bin_name = f"./{src.name}"
        elif sys.platform == "win32":
            bin_name = "vaydns-client.exe"
        else:
            bin_name = "./vaydns-client"

    if transport == "udp":
        transport_flag = f"-udp {resolver}"
    elif transport == "doh":
        transport_flag = f"-doh {resolver}"
    else:  # dot
        transport_flag = f"-dot {resolver}"

    parts = [
        bin_name,
        transport_flag,
        f"-pubkey {pubkey_q}",
        f"-domain {domain_q}",
        f"-listen {listen}",
        f"-max-qname-len {opts['max_qname_len']}",
        f"-idle-timeout {opts['idle_timeout']}",
        f"-keepalive {opts['keepalive']}",
        f"-reconnect-min {opts['reconnect_min']}",
        f"-reconnect-max {opts['reconnect_max']}",
        f"-record-type {opts['record_type']}",
        f"-queue-size {opts['queue_size']}",
        f"-log-level {opts['log_level']}",
    ]
    if opts.get("max_num_labels", 0):
        parts.append(f"-max-num-labels {opts['max_num_labels']}")
    if opts.get("max_streams", 0):
        parts.append(f"-max-streams {opts['max_streams']}")
    if opts.get("kcp_window_size", 0):
        parts.append(f"-kcp-window-size {opts['kcp_window_size']}")
    if opts.get("rps", 0):
        parts.append(f"-rps {opts['rps']}")
    if transport == "udp":
        parts.append(f"-udp-workers {opts.get('udp_workers', 100)}")
        if opts.get("udp_shared_socket", False):
            parts.append("-udp-shared-socket")
    return " ".join(parts)


def write_vaydns_launch_script(profile: dict) -> Path:
    """Write run.sh (or run.bat) to the profile folder and return its path."""
    import shutil as _sh
    opts      = {**VAYDNS_DEFAULTS, **profile.get("options", {})}
    country   = profile.get("country", "vaydns_output")
    resolvers = profile.get("resolvers", [])
    transport = opts["transport"]
    folder    = app_dir() / country
    # NOTE: folder.mkdir is called BELOW, only right before we write files.
    # This prevents empty folders appearing if the function is called speculatively.

    # Build resolver address list
    # For UDP transport: use scanned resolvers (all of them, not just 20).
    # Fall back to 8.8.8.8 only if the profile has zero resolvers AND no custom_resolver.
    custom_resolver = opts.get("custom_resolver", "").strip()
    if transport == "udp":
        if custom_resolver:
            # User specified a single resolver — use only that
            resolver_addrs = [
                custom_resolver if ":" in custom_resolver else f"{custom_resolver}:53"
            ]
        else:
            # Use all scanned resolvers so script can fall through if one fails
            resolver_addrs = [
                r if ":" in r else f"{r}:53"
                for r in resolvers
            ] or ["8.8.8.8:53"]
    else:
        # DoH / DoT: user must provide resolver URL or address in options
        resolver_addrs = [custom_resolver] if custom_resolver else [""]

    # Now create folder and copy binary
    folder.mkdir(parents=True, exist_ok=True)

    # Copy vaydns-client binary if present — keep arch-specific name
    bin_src = get_vaydns_exe()
    bin_copy_error = None
    if bin_src:
        try:
            dst = folder / bin_src.name
            _sh.copy2(str(bin_src), str(dst))
            if sys.platform != "win32":
                dst.chmod(dst.stat().st_mode | 0o111)
        except Exception as _copy_err:
            bin_copy_error = str(_copy_err)

    # Determine the actual binary name that was copied into the folder
    if bin_src:
        sh_bin_name  = f"./{bin_src.name}"
        bat_bin_name = bin_src.name  # no ./ on Windows
    elif sys.platform == "win32":
        sh_bin_name  = "vaydns-client.exe"
        bat_bin_name = "vaydns-client.exe"
    else:
        sh_bin_name  = "./vaydns-client"
        bat_bin_name = "vaydns-client"

    # --- Shell script (macOS / Linux) ---
    if sys.platform != "win32":
        lines = [
            "#!/bin/bash",
            "# Auto-generated by KevinNet DNS — VayDNS launcher",
            f"# Profile: {profile.get('name','')}",
            f"# Domain:  {profile.get('domain','')}",
            f"# Transport: {transport}",
            "#",
            "# NOTE: These resolvers were scanned from inside Iran.",
            "# They are Iranian public DNS servers — they only work correctly",
            "# when connecting FROM inside Iran. Testing from outside Iran",
            "# (Australia, Europe, etc.) will show NXDOMAIN and handshake",
            "# timeouts because the resolvers can't reach your tunnel server",
            "# from that network path.",
            "",
            "# Trap Ctrl+C and termination signals — kill the background",
            "# vaydns-client process so it doesn't become a zombie.",
            "VD_PID=",
            "cleanup() {",
            "  [ -n \"$VD_PID\" ] && kill $VD_PID 2>/dev/null && wait $VD_PID 2>/dev/null",
            "  exit 0",
            "}",
            "trap cleanup INT TERM",
            "",
        ]
        if transport == "udp":
            if len(resolver_addrs) == 1:
                # Single resolver — run directly, let vaydns-client handle retries
                lines += [
                    f'echo "[vaydns] using resolver: {resolver_addrs[0]}"',
                    build_vaydns_command(profile, resolver_addrs[0], sh_bin_name),
                ]
            else:
                # Multiple scanned resolvers.
                # vaydns-client NEVER exits on its own — it retries the same resolver
                # forever with exponential back-off. We run each as a background
                # process and kill it after RESOLVER_TIMEOUT seconds if it hasn't
                # stayed connected. No external tools (timeout/gtimeout) needed.
                lines += [
                    "RESOLVERS=(",
                    *[f'  "{r}"' for r in resolver_addrs],
                    ")", "",
                    "# Seconds to wait per resolver before giving up and trying the next one.",
                    "# Change in the VayDNS Profiles tab → Resolver Timeout option.",
                    f"RESOLVER_TIMEOUT={opts.get('resolver_timeout', 60)}",
                    "",
                    'for RESOLVER in "${RESOLVERS[@]}"; do',
                    '  echo "[vaydns] ▶ trying resolver: $RESOLVER  (timeout: ${RESOLVER_TIMEOUT}s)"',
                    "",
                    f"  {build_vaydns_command(profile, '"$RESOLVER"', sh_bin_name)} &",
                    "  VD_PID=$!",
                    "  ELAPSED=0",
                    "",
                    "  # Wait until the process exits on its own OR the timeout is reached",
                    "  while [ $ELAPSED -lt $RESOLVER_TIMEOUT ] && kill -0 $VD_PID 2>/dev/null; do",
                    "    sleep 2",
                    "    ELAPSED=$((ELAPSED + 2))",
                    "  done",
                    "",
                    "  if kill -0 $VD_PID 2>/dev/null; then",
                    '    # Still running after timeout — resolver is stuck, kill and try next',
                    '    echo "[vaydns] ✗ resolver $RESOLVER stuck for ${RESOLVER_TIMEOUT}s, trying next..."',
                    "    kill $VD_PID 2>/dev/null",
                    "    wait $VD_PID 2>/dev/null",
                    "  else",
                    "    wait $VD_PID",
                    "    EXIT_CODE=$?",
                    "    if [ $EXIT_CODE -eq 0 ]; then",
                    '      echo "[vaydns] ✓ session ended cleanly"',
                    "      exit 0",
                    "    fi",
                    '    echo "[vaydns] ✗ resolver $RESOLVER exited (code $EXIT_CODE), trying next..."',
                    "  fi",
                    "done",
                    "",
                    'echo "[vaydns] all resolvers exhausted — check your pubkey, domain, and server"',
                    "exit 1",
                ]
        else:
            # DoH or DoT — single resolver address, run directly
            addr = resolver_addrs[0] if resolver_addrs[0] else ""
            if not addr:
                lines += [f'echo "ERROR: set a resolver address in the VayDNS Profiles tab for {transport} transport"']
            else:
                lines += [build_vaydns_command(profile, addr, sh_bin_name)]

        script_path = folder / "run.sh"
        script_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        script_path.chmod(script_path.stat().st_mode | 0o111)
        return script_path

    # --- Batch script (Windows) ---
    lines = [
        "@echo off",
        "REM Auto-generated by KevinNet DNS — VayDNS launcher",
        f"REM Profile: {profile.get('name','')}",
        f"REM Transport: {transport}",
        "",
    ]
    if transport == "udp":
        if len(resolver_addrs) == 1:
            lines.append(f"echo Using resolver: {resolver_addrs[0]}")
            lines.append(build_vaydns_command(profile, resolver_addrs[0], bat_bin_name))
        else:
            # Windows: start each in a new window with a timeout via WMIC or timeout command
            # Simplest portable approach: run sequentially, vaydns exits non-zero on failure
            # The user can re-run the script to try the next resolver.
            # For a proper fallthrough, PowerShell would be needed — use run.ps1 instead.
            lines += [
                f"SET RESOLVER_TIMEOUT={opts.get('resolver_timeout', 60)}",
                "",
            ]
            for i, r in enumerate(resolver_addrs):
                lines += [
                    f"echo [vaydns] trying resolver {i+1}/{len(resolver_addrs)}: {r}",
                    f"start /B /WAIT {build_vaydns_command(profile, r, bat_bin_name)}",
                    "if %ERRORLEVEL% == 0 goto :done",
                    f"echo [vaydns] resolver {r} failed, trying next...",
                ]
            lines += ["echo [vaydns] all resolvers exhausted", "goto :eof", ":done"]
    else:
        addr = resolver_addrs[0] if resolver_addrs[0] else ""
        if addr:
            lines.append(build_vaydns_command(profile, addr, bat_bin_name))
        else:
            lines.append(f"echo ERROR: set a resolver address for {transport} transport")
    lines += ["pause"]
    script_path = folder / "run.bat"
    script_path.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")
    return script_path


def get_vaydns_exe() -> Path | None:
    """
    Find the vaydns-client binary next to the app or in _MEIPASS.

    Expected file names (place any one of these next to the KevinNet app):

        Windows x64   : vaydns-client_windows_amd64.exe
        Windows ARM64 : vaydns-client_windows_arm64.exe
        macOS Intel   : vaydns-client_darwin_amd64
        macOS ARM64   : vaydns-client_darwin_arm64
        Linux x64     : vaydns-client_linux_amd64
        Linux ARM64   : vaydns-client_linux_arm64

    Generic fallbacks (also accepted):
        Windows       : vaydns-client.exe
        macOS / Linux : vaydns-client
    """
    import platform as _platform

    machine = _platform.machine().lower()
    is_arm  = machine in ("arm64", "aarch64", "armv8l")
    arch    = "arm64" if is_arm else "amd64"

    if sys.platform == "win32":
        candidates = [
            f"vaydns-client_windows_{arch}.exe",   # underscore style
            f"vaydns-client-windows-{arch}.exe",   # dash style
            "vaydns-client.exe",
        ]
    elif sys.platform == "darwin":
        candidates = [
            f"vaydns-client-darwin-{arch}",        # dash style (actual files)
            f"vaydns-client_darwin_{arch}",         # underscore style
            "vaydns-client",
        ]
    else:  # Linux + anything else
        candidates = [
            f"vaydns-client-linux-{arch}",         # dash style (actual files)
            f"vaydns-client_linux_{arch}",          # underscore style
            "vaydns-client",
        ]

    search_dirs = [app_dir()]
    if getattr(sys, "frozen", False):
        search_dirs.append(Path(getattr(sys, "_MEIPASS", "")))

    # Platform keywords used to filter glob results so a darwin binary
    # bundled in _MEIPASS is never returned on Windows/Linux and vice versa.
    if sys.platform == "win32":
        plat_keywords = ("windows", "win")
        reject_keywords = ("darwin", "linux", "macos", "mac")
    elif sys.platform == "darwin":
        plat_keywords = ("darwin", "macos", "mac")
        reject_keywords = ("windows", "win", "linux")
    else:
        plat_keywords = ("linux",)
        reject_keywords = ("darwin", "macos", "mac", "windows", "win")

    for d in search_dirs:
        # 1. Try exact candidate names first
        for fname in candidates:
            p = d / fname
            if p.exists():
                return p
        # 2. Glob fallback — catch naming variants, but only for the right platform
        for p in sorted(d.glob("vaydns-client*")):
            name_lower = p.name.lower()
            if p.suffix in (".zip", ".gz", ".tar", ".txt", ".md", ".json"):
                continue
            # Reject binaries explicitly for another platform
            if any(kw in name_lower for kw in reject_keywords):
                continue
            # On Windows require a platform match or .exe; on others accept generic
            if sys.platform == "win32":
                if not (any(kw in name_lower for kw in plat_keywords) or p.suffix == ".exe"):
                    continue
            return p
    return None

# ═══════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        # DPI awareness BEFORE super().__init__()
        if sys.platform == "win32":
            try:
                import ctypes
                try:
                    ctypes.windll.shcore.SetProcessDpiAwareness(2)
                except Exception:
                    ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

        super().__init__()
        self.title("KevinNet DNS")
        self.configure(bg=BG)
        self.minsize(900, 680)   # minimum — all buttons always visible

        self._lang      = "fa"
        self._found_ips : list[str] = []
        self._stop_ev   = threading.Event()
        self._scanning  = False
        self._W         : dict = {}
        self._q         = queue.Queue()   # thread-safe result queue

        # MasterDNS Profiles tab state
        self._profiles         : dict = {}
        self._sel_profile      : str | None = None
        self._pname_var        : tk.StringVar | None = None
        self._popt_vars        : dict = {}
        self._auto_saved_stem  : str | None = None

        # VayDNS Profiles tab state
        self._vd_profiles      : dict = {}
        self._vd_sel_profile   : str | None = None
        self._vd_pname_var     : tk.StringVar | None = None
        self._vd_popt_vars     : dict = {}
        self._vd_pubkey_var    : tk.StringVar | None = None  # scanner field

        self._build_ui()
        self._set_icon()
        # Restore persisted preferences (last domain, country, mode, lang)
        self._apply_settings_on_startup()
        self.after(50,  self._maximize)
        self.after(100, self._poll_q)     # start polling queue
        # Auto-open the help dialog unless the user previously ticked
        # "don't show again". When opened from the header button later
        # the checkbox isn't shown — they obviously want help then.
        if not load_settings().get("help_dismissed", False):
            self.after(700, lambda: show_help(self, self._lang, allow_dismiss=True))

    def _apply_settings_on_startup(self):
        """Repopulate Domain / Country / VPN mode from the previous session."""
        s = load_settings()
        try:
            mode = s.get("last_mode")
            if mode in ("masterdns", "vaydns") and hasattr(self, "_vpn_mode"):
                self._vpn_mode.set(mode)
                # _set_vpn_mode toggles visibility of mode-specific fields
                if hasattr(self, "_set_vpn_mode"):
                    self._set_vpn_mode(mode)
        except Exception:
            pass
        try:
            if s.get("last_domain") and hasattr(self, "_domain_var"):
                self._domain_var.set(s["last_domain"])
        except Exception:
            pass
        try:
            if s.get("last_country") and hasattr(self, "_country_var"):
                self._country_var.set(s["last_country"])
        except Exception:
            pass

    def _set_icon(self):
        """Embed app icon from base64 — works on all platforms."""
        try:
            import base64, io
            from PIL import Image, ImageTk
            data  = base64.b64decode(ICON_B64)
            img   = Image.open(io.BytesIO(data))
            photo = ImageTk.PhotoImage(img)
            self.wm_iconphoto(True, photo)
            self._icon_ref = photo          # prevent GC
        except Exception:
            pass                            # icon is cosmetic; never crash

    def _maximize(self):
        """Open maximized on every platform."""
        if sys.platform == "win32":
            self.state("zoomed")
        elif sys.platform == "darwin":
            # macOS: fill the screen (excluding menu/dock)
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            self.geometry(f"{sw}x{sh}+0+0")
        else:
            # Linux / other Unix
            try:
                self.attributes("-zoomed", True)
            except Exception:
                sw = self.winfo_screenwidth()
                sh = self.winfo_screenheight()
                self.geometry(f"{sw}x{sh}+0+0")

    def _center(self):
        pass   # window is maximized; kept for compatibility

    def _poll_q(self):
        """Drain result queue on main thread — fully thread-safe."""
        try:
            while True:
                item = self._q.get_nowait()
                kind = item[0]
                if kind == "prog":
                    _, tested, total, found, pct, label = item
                    self._on_progress(tested, total, found, pct, label)
                elif kind == "res":
                    _, ip, score, max_s, ms, detail = item
                    self._on_result(ip, score, max_s, ms, detail)
                elif kind == "done":
                    _, tested, found = item
                    self._on_done(tested, found)
                elif kind == "log":
                    _, msg = item
                    self._log(msg)
                elif kind == "e2e_res":
                    # E2E verified resolver — highlight purple in tree
                    _, ip, score, ms, detail = item
                    W = self._W
                    for row in W["tree"].get_children():
                        vals = W["tree"].item(row, "values")
                        if vals and vals[0] == ip:
                            W["tree"].item(row, values=(ip, f"{score}/6", str(ms), detail))
                            W["tree"].item(row, tags=("e2e",))
                            W["tree"].tag_configure("e2e", foreground="#a78bfa")
                            break
                    else:
                        W["tree"].insert("", "end",
                                         values=(ip, f"{score}/6", str(ms), detail),
                                         tags=("e2e",))
                        W["tree"].tag_configure("e2e", foreground="#a78bfa")
                elif kind == "e2e_done":
                    _, verified = item
                    fa = self._lang == "fa"
                    self._found_ips = list(verified)
                    self._W["btn_scan"].config(state="normal",  bg=ACCENT,  fg="#000000", disabledforeground=DIS_FG)
                    if verified:
                        mode = self._vpn_mode.get()
                        if mode == "masterdns":
                            self._W["btn_save"].config(state="normal", bg=BLUE, fg="#000000", disabledforeground=DIS_FG)
                        else:
                            self._W["btn_vd_save"].config(state="normal", bg=PURPLE, fg=BTN_TEXT, disabledforeground=DIS_FG)
                    if self._found_ips:
                        self._W["btn_export"].config(state="normal", bg=WARN, fg=BTN_TEXT,
                                                     cursor="hand2", disabledforeground=DIS_FG)
                    n = len(verified)
                    self._W["badge"].config(
                        text=f"{n}  {'تأیید E2E' if fa else 'E2E verified'}")
                    self._W["status_lbl"].config(
                        text=f"● {'کامل' if fa else 'Done'}  —  {n} {'تأیید شده' if fa else 'E2E verified'}",
                        fg=GREEN)
                    self._log(
                        f"{'✓ مرحله ۳ کامل:' if fa else '✓ Phase 3 done:'} "
                        f"{n} {'resolver تأیید E2E شده' if fa else 'E2E-verified resolvers'} "
                        f"{'آماده ذخیره هستند' if fa else 'ready to save'}")
                elif kind == "doh_res":
                    # DoH endpoint responded — show as a teal row with a 🔒 icon
                    _, endpoint, ms = item
                    self._W["tree"].insert(
                        "", "end",
                        values=(endpoint, "DoH", f"{ms:.0f}", "🔒 reachable"),
                        tags=("doh",))
                    self._W["tree"].tag_configure("doh", foreground="#5eead4")
                    self._log(f"🔒  DoH  {endpoint}  {ms:.0f}ms")
                elif kind == "dot_res":
                    _, endpoint, ms = item
                    self._W["tree"].insert(
                        "", "end",
                        values=(endpoint, "DoT", f"{ms:.0f}", "🔒 reachable"),
                        tags=("dot",))
                    self._W["tree"].tag_configure("dot", foreground="#a5b4fc")
                    self._log(f"🔒  DoT  {endpoint}  {ms:.0f}ms")
                elif kind == "doh_dot_done":
                    _, tested, found = item
                    fa = self._lang == "fa"
                    self._scanning = False
                    self._W["btn_scan"].config(
                        state="normal", bg=ACCENT, fg="#000000",
                        disabledforeground=DIS_FG)
                    self._W["btn_doh_scan"].config(
                        state="normal", bg=PURPLE, fg=BTN_TEXT,
                        disabledforeground=DIS_FG)
                    self._W["btn_stop"].config(
                        state="disabled", bg=DIS_BG, fg=DIS_FG,
                        disabledforeground=DIS_FG)
                    self._W["status_lbl"].config(
                        text=f"● {'DoH/DoT کامل' if fa else 'DoH/DoT done'}"
                             f"  —  {found}/{tested} reachable",
                        fg=GREEN)
                    self._log(
                        f"{'✓ DoH/DoT کامل:' if fa else '✓ DoH/DoT done:'} "
                        f"{found}/{tested} reachable")

        except queue.Empty:
            pass
        except Exception:
            pass
        self.after(40, self._poll_q)

    # ── TOP BAR ─────────────────────────────────────────────────
    def _build_ui(self):
        W = self._W

        topbar = tk.Frame(self, bg=PANEL, height=60)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="KevinNet DNS", bg=PANEL, fg=ACCENT,
                 font=F(18, "bold")).pack(side="left", padx=(20, 8))
        tk.Label(topbar, text="·  DNS Resolver Scanner", bg=PANEL, fg=MUTED,
                 font=F(11)).pack(side="left")
        tk.Label(topbar, text="by Kevin Haji", bg=PANEL, fg=HINT,
                 font=F(10)).pack(side="left", padx=(10,0))

        btn_fr = tk.Frame(topbar, bg=PANEL)
        btn_fr.pack(side="right", padx=16)

        def top_btn(parent, wkey, text, fg_c, command):
            """Label-based button — reliable on macOS and Windows alike."""
            fr = tk.Frame(parent, bg=BORDER,
                          highlightbackground=BORDER, highlightthickness=1)
            fr.pack(side="right", padx=(6, 0))
            lbl = tk.Label(fr, text=text, bg=BORDER, fg=fg_c,
                           font=FA(10, "bold"), padx=14, pady=7,
                           cursor="hand2")
            lbl.pack()
            def on_enter(e):  lbl.config(bg=ACCENT, fg="#000000"); fr.config(bg=ACCENT)
            def on_leave(e):  lbl.config(bg=BORDER, fg=fg_c);    fr.config(bg=BORDER)
            def on_click(e):  command()
            lbl.bind("<Enter>",   on_enter)
            lbl.bind("<Leave>",   on_leave)
            lbl.bind("<Button-1>",on_click)
            W[wkey] = lbl

        top_btn(btn_fr, "btn_help", "؟  راهنما",
                TEXT, lambda: show_help(self, self._lang))
        top_btn(btn_fr, "btn_lang", "English",
                ACCENT, self._toggle_lang)

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # ── TAB BAR ──────────────────────────────────────────────
        tab_bar = tk.Frame(self, bg=PANEL, height=44)
        tab_bar.pack(fill="x")
        tab_bar.pack_propagate(False)

        def make_tab(wkey, en_text, fa_text, cmd):
            lbl = tk.Label(tab_bar,
                           text=fa_text if self._lang == "fa" else en_text,
                           bg=PANEL, fg=MUTED,
                           font=F(13, "bold"),
                           padx=26, pady=12, cursor="hand2")
            lbl.pack(side="left")
            lbl.bind("<Button-1>", lambda e: cmd())
            W[wkey] = lbl

        make_tab("tab_scanner",  "🔍  Scanner",      "🔍  اسکنر",      self._show_scanner)
        make_tab("tab_profiles",    "📋  MasterDNS Profiles", "📋  MasterDNS",  self._show_profiles)
        make_tab("tab_vd_profiles", "📋  VayDNS Profiles",    "📋  VayDNS",      self._show_vd_profiles)

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # ── CONTENT AREA — three views, only one shown at a time ─
        self._scanner_view    = tk.Frame(self, bg=BG)
        self._profiles_view   = tk.Frame(self, bg=BG)
        self._vd_profiles_view = tk.Frame(self, bg=BG)

        # ── Scanner view (original layout) ───────────────────────
        body = self._scanner_view

        # Scrollable left panel — buttons always accessible even on small screens
        left_outer = tk.Frame(body, bg=BG, width=420)
        left_outer.pack(side="left", fill="y", padx=(12, 6), pady=10)
        left_outer.pack_propagate(False)

        left_canvas = tk.Canvas(left_outer, bg=BG, bd=0,
                                highlightthickness=0, width=400)
        left_scroll = ttk.Scrollbar(left_outer, orient="vertical",
                                    command=left_canvas.yview)
        left_scroll.pack(side="right", fill="y")
        left_canvas.pack(side="left", fill="both", expand=True)

        left = tk.Frame(left_canvas, bg=BG)
        left_win = left_canvas.create_window((0, 0), window=left,
                                              anchor="nw", width=395)

        def _on_left_configure(e):
            left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        def _on_canvas_resize(e):
            left_canvas.itemconfig(left_win, width=e.width)
        left.bind("<Configure>", _on_left_configure)
        left_canvas.bind("<Configure>", _on_canvas_resize)

        # Mouse wheel scroll
        def _on_mousewheel(e):
            if sys.platform == "darwin":
                left_canvas.yview_scroll(-1 * int(e.delta), "units")
            elif sys.platform == "win32":
                left_canvas.yview_scroll(-1 * int(e.delta / 120), "units")
            else:
                if e.num == 4:
                    left_canvas.yview_scroll(-1, "units")
                else:
                    left_canvas.yview_scroll(1, "units")

        left_canvas.bind("<MouseWheel>", _on_mousewheel)
        left_canvas.bind("<Button-4>",   _on_mousewheel)
        left_canvas.bind("<Button-5>",   _on_mousewheel)
        left.bind("<MouseWheel>",        _on_mousewheel)

        self._build_left(left)
        # After left panel is built, bind scroll on all child widgets
        left.bind("<Configure>", lambda e: bind_mousewheel_recursive(left, left_canvas), add="+")

        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True,
                   padx=(0, 16), pady=14)
        self._build_right(right)

        # ── Profiles views ───────────────────────────────────────
        self._build_profiles_tab(self._profiles_view)
        self._build_vd_profiles_tab(self._vd_profiles_view)

        # Start on Scanner tab
        self._show_scanner()

        # ── FOOTER — credit in ONE place only ──
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
        footer = tk.Frame(self, bg=PANEL, height=36)
        footer.pack(fill="x")
        footer.pack_propagate(False)
        tk.Label(
            footer,
            text="Designed & developed by  Kevin Haji  ·  kevinhaji.com"
                 "  ·  kevin.fullstack.dev@gmail.com",
            bg=PANEL, fg=MUTED, font=F(9)).pack(side="left", padx=16)
        W["status_lbl"] = tk.Label(
            footer, text="● Ready", bg=PANEL, fg=GREEN, font=F(9))
        W["status_lbl"].pack(side="right", padx=16)


    # ── TAB SWITCHING ────────────────────────────────────────────
    def _show_scanner(self):
        self._profiles_view.pack_forget()
        self._vd_profiles_view.pack_forget()
        self._scanner_view.pack(fill="both", expand=True)
        self._W["tab_scanner"].config(bg=ACCENT, fg="#000000")
        self._W["tab_profiles"].config(bg=PANEL, fg=MUTED)
        self._W["tab_vd_profiles"].config(bg=PANEL, fg=MUTED)

    def _show_profiles(self):
        self._scanner_view.pack_forget()
        self._vd_profiles_view.pack_forget()
        self._profiles_view.pack(fill="both", expand=True)
        self._W["tab_scanner"].config(bg=PANEL, fg=MUTED)
        self._W["tab_profiles"].config(bg=ACCENT, fg="#000000")
        self._W["tab_vd_profiles"].config(bg=PANEL, fg=MUTED)
        self._refresh_profiles_list()

    def _show_vd_profiles(self):
        self._scanner_view.pack_forget()
        self._profiles_view.pack_forget()
        self._vd_profiles_view.pack(fill="both", expand=True)
        self._W["tab_scanner"].config(bg=PANEL, fg=MUTED)
        self._W["tab_profiles"].config(bg=PANEL, fg=MUTED)
        self._W["tab_vd_profiles"].config(bg=ACCENT, fg="#000000")
        self._vd_refresh_profiles_list()

    # ── PROFILES TAB ─────────────────────────────────────────────
    def _build_profiles_tab(self, parent):
        W  = self._W
        fa = self._lang == "fa"

        cols = tk.Frame(parent, bg=BG)
        cols.pack(fill="both", expand=True, padx=16, pady=14)

        # Left: list
        list_frame = tk.Frame(cols, bg=CARD, width=230,
                              highlightbackground=BORDER, highlightthickness=1)
        list_frame.pack(side="left", fill="y", padx=(0, 12))
        list_frame.pack_propagate(False)

        tk.Label(list_frame,
                 text="پروفایل‌ها" if fa else "Saved Profiles",
                 bg=BORDER, fg=MUTED, font=F(9, "bold"),
                 padx=12, pady=7, anchor="w").pack(fill="x")

        list_canvas = tk.Canvas(list_frame, bg=CARD, bd=0, highlightthickness=0)
        list_scroll = ttk.Scrollbar(list_frame, orient="vertical",
                                    command=list_canvas.yview)
        list_scroll.pack(side="right", fill="y")
        list_canvas.pack(side="left", fill="both", expand=True)

        self._plist_inner = tk.Frame(list_canvas, bg=CARD)
        self._plist_win   = list_canvas.create_window(
            (0, 0), window=self._plist_inner, anchor="nw")

        def _lcfg(e): list_canvas.configure(scrollregion=list_canvas.bbox("all"))
        def _lrsz(e): list_canvas.itemconfig(self._plist_win, width=e.width)
        self._plist_inner.bind("<Configure>", _lcfg)
        list_canvas.bind("<Configure>", _lrsz)
        self._plist_inner.bind("<Map>", lambda e: bind_mousewheel_recursive(self._plist_inner, list_canvas), add="+")
        W["plist_canvas"] = list_canvas

        # Right: detail
        detail_outer = tk.Frame(cols, bg=BG)
        detail_outer.pack(side="left", fill="both", expand=True)

        W["pdetail_empty"] = tk.Label(
            detail_outer,
            text="یک پروفایل انتخاب کنید" if fa else "Select a profile to view or edit",
            bg=BG, fg=MUTED, font=F(12))
        W["pdetail_empty"].pack(expand=True)

        det_canvas = tk.Canvas(detail_outer, bg=BG, bd=0, highlightthickness=0)
        det_scroll = ttk.Scrollbar(detail_outer, orient="vertical",
                                   command=det_canvas.yview)
        det_scroll.pack(side="right", fill="y")
        det_canvas.pack(side="left", fill="both", expand=True)

        detail = tk.Frame(det_canvas, bg=BG)
        det_win = det_canvas.create_window((0, 0), window=detail, anchor="nw")

        def _dcfg(e): det_canvas.configure(scrollregion=det_canvas.bbox("all"))
        def _drsz(e): det_canvas.itemconfig(det_win, width=e.width)
        detail.bind("<Configure>", _dcfg)
        det_canvas.bind("<Configure>", _drsz)
        detail.bind("<Map>", lambda e: bind_mousewheel_recursive(detail, det_canvas), add="+")

        W["pdetail_scroll"]    = det_canvas
        W["pdetail_frame"]     = detail
        W["pdetail_scrollbar"] = det_scroll
        det_canvas.pack_forget()
        det_scroll.pack_forget()

        # Card helper
        def card(parent, en_hdr, fa_hdr, col=ACCENT):
            c = tk.Frame(parent, bg=CARD,
                         highlightbackground=BORDER, highlightthickness=1)
            c.pack(fill="x", pady=(0, 10))
            tk.Label(c, text=fa_hdr if fa else en_hdr,
                     bg=BORDER, fg=col, font=F(10, "bold"),
                     padx=12, pady=6, anchor="w").pack(fill="x")
            inner = tk.Frame(c, bg=CARD)
            inner.pack(fill="x", padx=14, pady=8)
            return inner

        meta = card(detail, "⚙  Profile Info", "⚙  اطلاعات پروفایل")

        tk.Label(meta, text="نام پروفایل" if fa else "Profile Name",
                 bg=CARD, fg=MUTED, font=F(9), anchor="w").pack(fill="x")
        self._pname_var = tk.StringVar()
        tk.Entry(meta, textvariable=self._pname_var,
                 bg=INPUT, fg=TEXT, insertbackground=ACCENT,
                 relief="flat", bd=0, font=FM(11),
                 highlightbackground=BORDER, highlightthickness=1,
                 highlightcolor=ACCENT).pack(fill="x", ipady=8, pady=(2, 6))

        W["pmeta_info"] = tk.Label(meta, text="", bg=CARD, fg=MUTED,
                                   font=F(9), anchor="w", justify="left")
        W["pmeta_info"].pack(fill="x")

        # Options card
        opt = card(detail, "🔧  Key Options", "🔧  تنظیمات کلیدی", BLUE)
        popt = {}

        def opt_row(wkey, en_lbl, fa_lbl, widget_builder):
            row = tk.Frame(opt, bg=CARD)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=fa_lbl if fa else en_lbl,
                     bg=CARD, fg=TEXT,
                     font=FA(9) if fa else F(9),
                     anchor="w", width=24).pack(side="left")
            widget_builder(row, wkey)

        def spinbox_b(lo, hi, default):
            def make(parent, wkey):
                var = tk.IntVar(value=default)
                tk.Spinbox(parent, from_=lo, to=hi, textvariable=var,
                           bg=INPUT, fg=TEXT, insertbackground=ACCENT,
                           buttonbackground=BORDER, relief="flat", bd=0,
                           font=FM(10), width=9,
                           highlightbackground=BORDER, highlightthickness=1,
                           highlightcolor=ACCENT).pack(side="left")
                popt[wkey] = var
            return make

        def combo_b(values, default):
            def make(parent, wkey):
                var = tk.StringVar(value=default)
                cb = ttk.Combobox(parent, textvariable=var,
                                  values=values, state="readonly",
                                  width=26, font=FM(10))
                cb.pack(side="left")
                popt[wkey] = var
            return make

        opt_row("listen_port",        "Listen Port",         "پورت محلی",
                spinbox_b(1024, 65535, 18000))
        opt_row("encryption_method",  "Encryption Method",   "روش رمزنگاری",
                combo_b(ENC_LABELS, ENC_LABELS[1]))
        opt_row("balancing_strategy", "Balancing Strategy",  "استراتژی بالانس",
                combo_b(BAL_LABELS, BAL_LABELS[1]))
        opt_row("packet_duplication", "Packet Duplication",  "تکرار بسته",
                spinbox_b(1, 8, 2))
        opt_row("min_upload_mtu",     "Min Upload MTU",       "حداقل MTU آپلود",
                spinbox_b(10, 500, 38))
        opt_row("max_upload_mtu",     "Max Upload MTU",       "حداکثر MTU آپلود",
                spinbox_b(10, 500, 150))
        opt_row("min_download_mtu",   "Min Download MTU",     "حداقل MTU دانلود",
                spinbox_b(100, 2000, 500))
        opt_row("max_download_mtu",   "Max Download MTU",     "حداکثر MTU دانلود",
                spinbox_b(100, 2000, 900))
        opt_row("log_level",          "Log Level",            "سطح لاگ",
                combo_b(LOG_LABELS, "INFO"))

        self._popt_vars = popt

        # Action buttons
        btn_row = tk.Frame(detail, bg=BG)
        btn_row.pack(fill="x", pady=(4, 14))

        def act_btn(wkey, en, fa_t, bg_c, fg_c, cmd):
            b = tk.Button(btn_row, text=fa_t if fa else en,
                          bg=bg_c, fg=fg_c,
                          font=F(10, "bold"), relief="flat", bd=0,
                          padx=14, pady=9, cursor="hand2",
                          activebackground=bg_c, activeforeground=fg_c,
                          command=cmd)
            b.pack(side="left", padx=(0, 6))
            W[wkey] = b

        act_btn("pbtn_save",   "💾 Save Changes",  "💾 ذخیره تغییرات",
                BLUE,   "#000000", self._profile_save_changes)
        act_btn("pbtn_launch", "🚀 Launch VPN",    "🚀 اتصال",
                PURPLE, BTN_TEXT,  self._profile_launch)
        act_btn("pbtn_dupe",   "📋 Duplicate",      "📋 کپی پروفایل",
                ACCENT, "#000000", self._profile_duplicate)
        act_btn("pbtn_delete", "🗑 Delete",          "🗑 حذف",
                DANGER, "#000000", self._profile_delete)

    def _show_profile_detail(self, show: bool):
        W = self._W
        if show:
            W["pdetail_empty"].pack_forget()
            W["pdetail_scroll"].pack(side="left", fill="both", expand=True)
            W["pdetail_scrollbar"].pack(side="right", fill="y")
        else:
            W["pdetail_scroll"].pack_forget()
            W["pdetail_scrollbar"].pack_forget()
            W["pdetail_empty"].pack(expand=True)

    def _refresh_profiles_list(self):
        self._profiles = load_all_profiles()
        inner = self._plist_inner
        for w in inner.winfo_children():
            w.destroy()
        fa = self._lang == "fa"

        if not self._profiles:
            tk.Label(inner,
                     text="هنوز پروفایلی وجود ندارد\nابتدا اسکن انجام دهید" if fa
                          else "No profiles yet.\nRun a scan first.",
                     bg=CARD, fg=MUTED,
                     font=FA(9) if fa else F(9),
                     justify="center", padx=12, pady=20).pack()
            self._sel_profile = None
            self._show_profile_detail(False)
            return

        for stem, p in self._profiles.items():
            self._make_profile_row(inner, stem, p)

        if self._sel_profile and self._sel_profile in self._profiles:
            self._select_profile(self._sel_profile)
        elif self._profiles:
            self._select_profile(next(iter(self._profiles)))

    def _make_profile_row(self, parent, stem, p):
        fa   = self._lang == "fa"
        name = p.get("name", stem)
        date = p.get("date", "")[:10]
        cnt  = p.get("resolver_count", len(p.get("resolvers", [])))
        launched_str = _format_last_launched(p.get("last_launched", ""), fa)

        row = tk.Frame(parent, bg=CARD, cursor="hand2")
        row.pack(fill="x")
        sel_bar = tk.Frame(row, bg=CARD, width=3)
        sel_bar.pack(side="left", fill="y")
        info = tk.Frame(row, bg=CARD)
        info.pack(side="left", fill="x", expand=True, padx=8, pady=8)
        name_lbl = tk.Label(info, text=name, bg=CARD, fg=TEXT,
                            font=F(12, "bold"), anchor="w")
        name_lbl.pack(fill="x")
        # Compose subline: date · N resolvers · last launched X
        meta_parts = [date, f"{cnt} resolvers"]
        if launched_str:
            meta_parts.append(launched_str)
        tk.Label(info, text="  ·  ".join(meta_parts),
                 bg=CARD, fg=MUTED, font=F(10), anchor="w").pack(fill="x")
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x")

        def _on_click(e, s=stem):
            self._select_profile(s)
        for w in (row, sel_bar, info, name_lbl):
            w.bind("<Button-1>", _on_click)

        row._stem     = stem
        row._sel_bar  = sel_bar
        row._name_lbl = name_lbl

    def _select_profile(self, stem: str):
        self._sel_profile = stem
        p   = self._profiles.get(stem, {})
        fa  = self._lang == "fa"
        W   = self._W

        for row in self._plist_inner.winfo_children():
            if isinstance(row, tk.Frame) and hasattr(row, "_stem"):
                if row._stem == stem:
                    row._sel_bar.config(bg=ACCENT)
                    row._name_lbl.config(fg=ACCENT)
                else:
                    row._sel_bar.config(bg=CARD)
                    row._name_lbl.config(fg=TEXT)

        opts = {**PROFILE_DEFAULTS, **p.get("options", {})}
        cnt  = p.get("resolver_count", len(p.get("resolvers", [])))
        date = p.get("date", "")

        self._pname_var.set(p.get("name", stem))
        domain_lbl = "دامنه" if fa else "Domain"
        folder_lbl = "پوشه"  if fa else "Folder"
        saved_lbl  = "تاریخ" if fa else "Saved"
        W["pmeta_info"].config(
            text=(f"{domain_lbl}: {p.get("domain","")}\n"
                  f"{folder_lbl}: {p.get("country","")}\n"
                  f"Resolvers: {cnt}    {saved_lbl}: {date}"))



        popt = self._popt_vars
        popt["listen_port"].set(opts.get("listen_port", 18000))
        enc_match = next((l for l in ENC_LABELS
                          if l.startswith(str(opts.get("encryption_method", 1)))),
                         ENC_LABELS[1])
        popt["encryption_method"].set(enc_match)
        bal_match = next((l for l in BAL_LABELS
                          if l.startswith(str(opts.get("balancing_strategy", 2)))),
                         BAL_LABELS[1])
        popt["balancing_strategy"].set(bal_match)
        popt["packet_duplication"].set(opts.get("packet_duplication", 2))
        popt["min_upload_mtu"].set(opts.get("min_upload_mtu", 38))
        popt["max_upload_mtu"].set(opts.get("max_upload_mtu", 150))
        popt["min_download_mtu"].set(opts.get("min_download_mtu", 500))
        popt["max_download_mtu"].set(opts.get("max_download_mtu", 900))
        log_val = opts.get("log_level", "INFO")
        popt["log_level"].set(log_val if log_val in LOG_LABELS else "INFO")

        self._show_profile_detail(True)

    def _read_popt_vars(self) -> dict:
        popt = self._popt_vars
        return {
            "listen_port":        popt["listen_port"].get(),
            "encryption_method":  int(popt["encryption_method"].get()[0]),
            "balancing_strategy": int(popt["balancing_strategy"].get()[0]),
            "packet_duplication": popt["packet_duplication"].get(),
            "min_upload_mtu":     popt["min_upload_mtu"].get(),
            "max_upload_mtu":     popt["max_upload_mtu"].get(),
            "min_download_mtu":   popt["min_download_mtu"].get(),
            "max_download_mtu":   popt["max_download_mtu"].get(),
            "log_level":          popt["log_level"].get(),
        }

    def _profile_save_changes(self):
        stem = self._sel_profile
        if not stem:
            return
        p      = dict(self._profiles[stem])
        fa     = self._lang == "fa"
        import shutil as _sh

        old_country = p.get("country", "")
        new_name    = self._pname_var.get().strip() or p.get("name", stem)

        p["name"]    = new_name
        p["options"] = self._read_popt_vars()

        # If the user changed the profile name, use it as the new folder name too
        # (only if old_country matched the old name, meaning it was auto-named)
        old_name = self._profiles[stem].get("name", stem)
        if old_name == old_country and new_name != old_country:
            new_country = new_name
        else:
            new_country = old_country

        # ── Rename output folder if country changed ───────────────
        if new_country != old_country:
            old_folder = app_dir() / old_country
            new_folder = app_dir() / new_country
            if old_folder.exists() and not new_folder.exists():
                try:
                    old_folder.rename(new_folder)
                    self._log(
                        f"{'پوشه تغییر نام یافت:' if fa else 'Folder renamed:'} "
                        f"{old_country} → {new_country}")
                except Exception as e:
                    self._log(
                        f"{'خطا در تغییر نام پوشه:' if fa else 'Folder rename error:'} {e}")
                    new_country = old_country  # revert if rename failed

        p["country"] = new_country
        update_profile(stem, p)

        # ── Rewrite config files with new options ─────────────────
        try:
            folder = write_profile_files(p)
            self._log(f"{'پروفایل بروزرسانی شد:' if fa else 'Profile updated:'} {folder}")
        except Exception as e:
            self._log(f"{'خطا:' if fa else 'Error:'} {e}")

        self._profiles[stem] = p
        self._refresh_profiles_list()
        messagebox.showinfo(
            "Saved" if not fa else "ذخیره شد",
            "تغییرات ذخیره شد" if fa else "Changes saved")

    def _profile_launch(self):
        stem = self._sel_profile
        if not stem:
            return
        p  = self._profiles[stem]
        fa = self._lang == "fa"
        # Always regenerate files so current options are applied
        # even if the user didn't click Save Changes first
        try:
            folder = write_profile_files(p)
        except Exception as e:
            messagebox.showerror("", str(e))
            return
        self._saved_folder = folder
        # Record the launch time on the profile JSON — used by the profile
        # list to show "last launched X ago" so users can find their
        # current/active profile in a long list.
        try:
            p["last_launched"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_profile(stem, p)
            self._profiles[stem] = p
            self._refresh_profiles_list()
        except Exception:
            pass
        self._launch_vpn()

    def _profile_duplicate(self):
        stem = self._sel_profile
        if not stem:
            return
        fa      = self._lang == "fa"
        src     = dict(self._profiles[stem])
        import shutil as _sh, copy as _copy

        # Ask for a new name
        new_name = simpledialog.askstring(
            "Duplicate" if not fa else "کپی پروفایل",
            ("New profile name:" if not fa else "نام پروفایل جدید:"),
            initialvalue=src.get("name", stem) + (" (copy)" if not fa else " (کپی)"),
            parent=self)
        if not new_name or not new_name.strip():
            return
        new_name = new_name.strip()

        # Build new profile dict
        new_profile              = _copy.deepcopy(src)
        new_profile["name"]      = new_name
        new_profile["country"]   = new_name
        new_profile["date"]      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Duplicate output folder
        src_folder = app_dir() / src.get("country", stem)
        dst_folder = app_dir() / new_name
        if src_folder.exists():
            try:
                _sh.copytree(str(src_folder), str(dst_folder))
                self._log(
                    f"{'پوشه کپی شد:' if fa else 'Folder duplicated:'} {dst_folder}")
            except Exception as e:
                self._log(
                    f"{'خطا در کپی پوشه:' if fa else 'Folder copy error:'} {e}")
        else:
            # No folder yet — just write fresh files
            try:
                write_profile_files(new_profile)
            except Exception as e:
                self._log(f"{'خطا در نوشتن فایل‌ها:' if fa else 'File write error:'} {e}")

        # Save the new profile JSON
        new_stem = save_new_profile(new_profile)
        self._log(
            f"{'پروفایل کپی شد:' if fa else 'Profile duplicated:'} {new_name}")

        self._refresh_profiles_list()
        # Select the new profile
        self._profiles = load_all_profiles()
        if new_stem in self._profiles:
            self._select_profile(new_stem)

    def _profile_delete(self):
        stem = self._sel_profile
        if not stem:
            return
        fa   = self._lang == "fa"
        name = self._profiles[stem].get("name", stem)
        if not messagebox.askyesno(
                "Delete" if not fa else "حذف",
                f"{'حذف پروفایل' if fa else 'Delete profile'} '{name}'?"):
            return
        country_folder = delete_profile(stem)
        if country_folder:
            folder_path = app_dir() / country_folder
            if folder_path.exists():
                if messagebox.askyesno(
                        "Delete folder?" if not fa else "حذف پوشه؟",
                        f"{'پوشه خروجی هم حذف شود؟' if fa else 'Also delete output folder?'}"
                        f"\n{folder_path}"):
                    import shutil as _sh
                    try:
                        _sh.rmtree(str(folder_path))
                    except Exception as e:
                        self._log(f"{'خطا در حذف پوشه:' if fa else 'Folder delete error:'} {e}")
        self._sel_profile = None
        self._show_profile_detail(False)
        self._refresh_profiles_list()


    # ── VAYDNS PROFILES TAB ──────────────────────────────────────
    def _build_vd_profiles_tab(self, parent):
        W  = self._W
        fa = self._lang == "fa"

        cols = tk.Frame(parent, bg=BG)
        cols.pack(fill="both", expand=True, padx=16, pady=14)

        # ── Left: profile list ────────────────────────────────────
        list_frame = tk.Frame(cols, bg=CARD, width=230,
                              highlightbackground=BORDER, highlightthickness=1)
        list_frame.pack(side="left", fill="y", padx=(0, 12))
        list_frame.pack_propagate(False)

        tk.Label(list_frame,
                 text="پروفایل‌های VayDNS" if fa else "VayDNS Profiles",
                 bg=BORDER, fg=MUTED, font=F(9, "bold"),
                 padx=12, pady=7, anchor="w").pack(fill="x")

        lc = tk.Canvas(list_frame, bg=CARD, bd=0, highlightthickness=0)
        ls = ttk.Scrollbar(list_frame, orient="vertical", command=lc.yview)
        ls.pack(side="right", fill="y")
        lc.pack(side="left", fill="both", expand=True)

        self._vd_plist_inner = tk.Frame(lc, bg=CARD)
        self._vd_plist_win   = lc.create_window((0,0), window=self._vd_plist_inner, anchor="nw")
        self._vd_plist_inner.bind("<Configure>", lambda e: lc.configure(scrollregion=lc.bbox("all")))
        lc.bind("<Configure>", lambda e: lc.itemconfig(self._vd_plist_win, width=e.width))
        self._vd_plist_inner.bind("<Map>", lambda e: bind_mousewheel_recursive(self._vd_plist_inner, lc), add="+")
        W["vd_plist_canvas"] = lc

        # ── Right: detail ─────────────────────────────────────────
        det_outer = tk.Frame(cols, bg=BG)
        det_outer.pack(side="left", fill="both", expand=True)

        W["vd_pdetail_empty"] = tk.Label(
            det_outer,
            text="یک پروفایل VayDNS انتخاب کنید" if fa
                 else "Select a VayDNS profile to view or edit",
            bg=BG, fg=MUTED, font=F(12))
        W["vd_pdetail_empty"].pack(expand=True)

        dc = tk.Canvas(det_outer, bg=BG, bd=0, highlightthickness=0)
        ds = ttk.Scrollbar(det_outer, orient="vertical", command=dc.yview)
        ds.pack(side="right", fill="y")
        dc.pack(side="left", fill="both", expand=True)

        detail  = tk.Frame(dc, bg=BG)
        det_win = dc.create_window((0,0), window=detail, anchor="nw")
        detail.bind("<Configure>", lambda e: dc.configure(scrollregion=dc.bbox("all")))
        dc.bind("<Configure>", lambda e: dc.itemconfig(det_win, width=e.width))
        detail.bind("<Map>", lambda e: bind_mousewheel_recursive(detail, dc), add="+")

        W["vd_pdetail_scroll"]    = dc
        W["vd_pdetail_frame"]     = detail
        W["vd_pdetail_scrollbar"] = ds
        dc.pack_forget(); ds.pack_forget()

        def card(parent, en_hdr, fa_hdr, col=ACCENT):
            c = tk.Frame(parent, bg=CARD,
                         highlightbackground=BORDER, highlightthickness=1)
            c.pack(fill="x", pady=(0, 10))
            tk.Label(c, text=fa_hdr if fa else en_hdr,
                     bg=BORDER, fg=col, font=F(10, "bold"),
                     padx=12, pady=6, anchor="w").pack(fill="x")
            inner = tk.Frame(c, bg=CARD)
            inner.pack(fill="x", padx=14, pady=8)
            return inner

        # Card: info
        meta = card(detail, "⚙  Profile Info", "⚙  اطلاعات پروفایل")
        tk.Label(meta, text="نام پروفایل" if fa else "Profile Name",
                 bg=CARD, fg=MUTED, font=F(9), anchor="w").pack(fill="x")
        self._vd_pname_var = tk.StringVar()
        tk.Entry(meta, textvariable=self._vd_pname_var,
                 bg=INPUT, fg=TEXT, insertbackground=ACCENT,
                 relief="flat", bd=0, font=FM(11),
                 highlightbackground=BORDER, highlightthickness=1,
                 highlightcolor=ACCENT).pack(fill="x", ipady=8, pady=(2,6))
        W["vd_pmeta_info"] = tk.Label(meta, text="", bg=CARD, fg=MUTED,
                                       font=F(9), anchor="w", justify="left")
        W["vd_pmeta_info"].pack(fill="x")

        # Card: VayDNS options
        opt = card(detail, "🔧  VayDNS Options", "🔧  تنظیمات VayDNS", BLUE)
        vd_opt = {}

        def opt_row(wkey, en_lbl, fa_lbl, widget_builder):
            row = tk.Frame(opt, bg=CARD)
            row.pack(fill="x", pady=3)
            lbl = tk.Label(row, text=fa_lbl if fa else en_lbl,
                           bg=CARD, fg=TEXT,
                           font=FA(9) if fa else F(9),
                           anchor="w", wraplength=180, justify="left")
            lbl.pack(side="left", fill="x", expand=True)
            widget_builder(row, wkey)

        def spinbox_b(lo, hi, default):
            def make(parent, wkey):
                var = tk.IntVar(value=default)
                tk.Spinbox(parent, from_=lo, to=hi, textvariable=var,
                           bg=INPUT, fg=TEXT, insertbackground=ACCENT,
                           buttonbackground=BORDER, relief="flat", bd=0,
                           font=FM(10), width=9,
                           highlightbackground=BORDER, highlightthickness=1,
                           highlightcolor=ACCENT).pack(side="left")
                vd_opt[wkey] = var
            return make

        def combo_b(values, default):
            def make(parent, wkey):
                var = tk.StringVar(value=default)
                ttk.Combobox(parent, textvariable=var, values=values,
                             state="readonly", width=28, font=FM(10)).pack(side="left")
                vd_opt[wkey] = var
            return make

        def entry_b(default, width=20):
            def make(parent, wkey):
                var = tk.StringVar(value=default)
                tk.Entry(parent, textvariable=var, bg=INPUT, fg=TEXT,
                         insertbackground=ACCENT, relief="flat", bd=0,
                         font=FM(10), width=width,
                         highlightbackground=BORDER, highlightthickness=1,
                         highlightcolor=ACCENT).pack(side="left", ipady=4)
                vd_opt[wkey] = var
            return make

        # ── Transport ──
        opt_row("transport",        "Transport",                    "نوع انتقال",
                combo_b(VAYDNS_TRANSPORT_LABELS, VAYDNS_TRANSPORT_LABELS[0]))
        opt_row("custom_resolver",
                "Resolver  (leave empty = use all scanned IPs)",
                "Resolver  (خالی = همه IP‌های اسکن‌شده)",
                entry_b("", width=30))
        # Hint label for the resolver field
        hint_row = tk.Frame(opt, bg=CARD)
        hint_row.pack(fill="x", pady=(0, 4))
        tk.Label(hint_row,
                 text="↑ خالی = همه IP‌ها  |  IP وارد کنید = فقط آن یک Resolver  |  DoH: URL کامل  |  DoT: host:853" if fa else "↑ Empty = try all scanned IPs in order  |  Enter IP = use only that one  |  DoH: full URL  |  DoT: host:853",
                 bg=CARD, fg=MUTED,
                 font=FA(8) if fa else F(8),
                 anchor="w", justify="left",
                 padx=4, wraplength=340).pack(fill="x")

        # ── Local ──
        opt_row("listen_port",      "Listen Port",                  "پورت محلی",
                spinbox_b(1024, 65535, 7000))

        # ── QNAME / MTU ──
        opt_row("max_qname_len",    "Max QNAME Len  [50–253]",      "Max QNAME",
                spinbox_b(50, 253, 101))
        opt_row("max_num_labels",   "Max Labels  (0=unlimited)",    "Max Labels",
                spinbox_b(0, 128, 0))

        # ── Session ──
        opt_row("idle_timeout",     "Idle Timeout  (match server)", "Idle Timeout",
                entry_b("10s", width=8))
        opt_row("keepalive",        "Keepalive  (< idle_timeout)",  "Keepalive",
                entry_b("2s", width=8))
        opt_row("reconnect_min",    "Reconnect Min",                "Reconnect Min",
                entry_b("1s", width=8))
        opt_row("reconnect_max",    "Reconnect Max",                "Reconnect Max",
                entry_b("30s", width=8))
        opt_row("max_streams",      "Max Streams  (0=unlimited)",   "Max Streams",
                spinbox_b(0, 256, 0))

        # ── DNS / Protocol ──
        opt_row("record_type",      "Record Type  (match server)",  "نوع رکورد",
                combo_b(VAYDNS_RECORD_LABELS, "txt"))

        # ── Queue / KCP ──
        opt_row("queue_size",       "Queue Size",                   "Queue Size",
                spinbox_b(64, 4096, 512))
        opt_row("kcp_window_size",  "KCP Window  (0=queue/2)",      "KCP Window",
                spinbox_b(0, 4096, 0))

        # ── UDP ──
        opt_row("udp_workers",      "UDP Workers",                  "UDP Workers",
                spinbox_b(1, 500, 100))
        opt_row("udp_shared_socket","Shared UDP Socket",            "Shared Socket",
                combo_b(["False", "True"], "False"))

        # ── Script ──
        opt_row("resolver_timeout", "Resolver Timeout (s)",         "Timeout هر Resolver",
                spinbox_b(10, 600, 60))

        # ── Rate limit ──
        opt_row("rps",              "Rate Limit  req/s  (0=off)",   "Rate Limit",
                spinbox_b(0, 1000, 0))

        # ── Logging ──
        opt_row("log_level",        "Log Level",                    "سطح لاگ",
                combo_b(VAYDNS_LOG_LABELS, "info"))

        self._vd_popt_vars = vd_opt

        # Action buttons
        btn_row = tk.Frame(detail, bg=BG)
        btn_row.pack(fill="x", pady=(4, 14))

        def act_btn(wkey, en, fa_t, bg_c, fg_c, cmd):
            b = tk.Button(btn_row, text=fa_t if fa else en,
                          bg=bg_c, fg=fg_c,
                          font=F(10, "bold"), relief="flat", bd=0,
                          padx=14, pady=9, cursor="hand2",
                          activebackground=bg_c, activeforeground=fg_c,
                          command=cmd)
            b.pack(side="left", padx=(0, 6))
            W[wkey] = b

        act_btn("vd_pbtn_save",   "💾 Save Changes",  "💾 ذخیره",       BLUE,   "#000000", self._vd_profile_save_changes)
        act_btn("vd_pbtn_launch", "🚀 Launch VPN",    "🚀 اتصال",        PURPLE, BTN_TEXT,  self._vd_profile_launch)
        act_btn("vd_pbtn_dupe",   "📋 Duplicate",      "📋 کپی",          ACCENT, "#000000", self._vd_profile_duplicate)
        act_btn("vd_pbtn_delete", "🗑 Delete",          "🗑 حذف",          DANGER, "#000000", self._vd_profile_delete)

    def _vd_show_detail(self, show: bool):
        W = self._W
        if show:
            W["vd_pdetail_empty"].pack_forget()
            W["vd_pdetail_scroll"].pack(side="left", fill="both", expand=True)
            W["vd_pdetail_scrollbar"].pack(side="right", fill="y")
        else:
            W["vd_pdetail_scroll"].pack_forget()
            W["vd_pdetail_scrollbar"].pack_forget()
            W["vd_pdetail_empty"].pack(expand=True)

    def _vd_refresh_profiles_list(self):
        self._vd_profiles = load_all_vaydns_profiles()
        inner = self._vd_plist_inner
        for w in inner.winfo_children():
            w.destroy()
        fa = self._lang == "fa"

        if not self._vd_profiles:
            tk.Label(inner,
                     text="هنوز پروفایل VayDNS ندارید\nابتدا اسکن انجام دهید" if fa
                          else "No VayDNS profiles yet.\nRun a scan first.",
                     bg=CARD, fg=MUTED, font=FA(9) if fa else F(9),
                     justify="center", padx=12, pady=20).pack()
            self._vd_sel_profile = None
            self._vd_show_detail(False)
            return

        for stem, p in self._vd_profiles.items():
            self._vd_make_profile_row(inner, stem, p)

        target = self._vd_sel_profile if self._vd_sel_profile in self._vd_profiles else next(iter(self._vd_profiles))
        self._vd_select_profile(target)

    def _vd_make_profile_row(self, parent, stem, p):
        fa   = self._lang == "fa"
        name = p.get("name", stem)
        date = p.get("date", "")[:10]
        cnt  = p.get("resolver_count", len(p.get("resolvers", [])))
        opts = p.get("options", {})
        transport = opts.get("transport", "udp")
        launched_str = _format_last_launched(p.get("last_launched", ""), fa)

        row     = tk.Frame(parent, bg=CARD, cursor="hand2")
        row.pack(fill="x")
        sel_bar = tk.Frame(row, bg=CARD, width=3)
        sel_bar.pack(side="left", fill="y")
        info    = tk.Frame(row, bg=CARD)
        info.pack(side="left", fill="x", expand=True, padx=8, pady=8)
        name_lbl = tk.Label(info, text=name, bg=CARD, fg=TEXT,
                            font=F(12, "bold"), anchor="w")
        name_lbl.pack(fill="x")
        meta_parts = [date, f"{cnt} resolvers", transport]
        if launched_str:
            meta_parts.append(launched_str)
        tk.Label(info, text="  ·  ".join(meta_parts),
                 bg=CARD, fg=MUTED, font=F(10), anchor="w").pack(fill="x")
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x")

        def _click(e, s=stem):
            self._vd_select_profile(s)
        for w in (row, sel_bar, info, name_lbl):
            w.bind("<Button-1>", _click)

        row._stem = stem; row._sel_bar = sel_bar; row._name_lbl = name_lbl

    def _vd_select_profile(self, stem: str):
        self._vd_sel_profile = stem
        p   = self._vd_profiles.get(stem, {})
        fa  = self._lang == "fa"
        W   = self._W
        opts = {**VAYDNS_DEFAULTS, **p.get("options", {})}
        cnt  = p.get("resolver_count", len(p.get("resolvers", [])))

        for row in self._vd_plist_inner.winfo_children():
            if isinstance(row, tk.Frame) and hasattr(row, "_stem"):
                sel = row._stem == stem
                row._sel_bar.config(bg=ACCENT if sel else CARD)
                row._name_lbl.config(fg=ACCENT if sel else TEXT)

        self._vd_pname_var.set(p.get("name", stem))
        domain_lbl = "دامنه" if fa else "Domain"
        saved_lbl  = "تاریخ" if fa else "Saved"
        W["vd_pmeta_info"].config(
            text=(f"{domain_lbl}: {p.get('domain','')}\n"
                  f"Pubkey: {p.get('pubkey','')[:16]}...\n"
                  f"Resolvers: {cnt}    {saved_lbl}: {p.get('date','')}"))

        vo = self._vd_popt_vars
        transport = opts.get("transport", "udp")
        t_match   = next((l for l in VAYDNS_TRANSPORT_LABELS
                          if l.startswith(transport)), VAYDNS_TRANSPORT_LABELS[0])
        vo["transport"].set(t_match)
        vo["custom_resolver"].set(opts.get("custom_resolver", ""))
        vo["listen_port"].set(opts.get("listen_port", 7000))
        vo["max_qname_len"].set(opts.get("max_qname_len", 101))
        vo["max_num_labels"].set(opts.get("max_num_labels", 0))
        vo["idle_timeout"].set(opts.get("idle_timeout", "10s"))
        vo["keepalive"].set(opts.get("keepalive", "2s"))
        vo["reconnect_min"].set(opts.get("reconnect_min", "1s"))
        vo["reconnect_max"].set(opts.get("reconnect_max", "30s"))
        vo["max_streams"].set(opts.get("max_streams", 0))
        rtype = opts.get("record_type", "txt")
        vo["record_type"].set(rtype if rtype in VAYDNS_RECORD_LABELS else "txt")
        vo["queue_size"].set(opts.get("queue_size", 512))
        vo["kcp_window_size"].set(opts.get("kcp_window_size", 0))
        vo["udp_workers"].set(opts.get("udp_workers", 100))
        vo["udp_shared_socket"].set("True" if opts.get("udp_shared_socket", False) else "False")
        vo["rps"].set(opts.get("rps", 0))
        vo["resolver_timeout"].set(opts.get("resolver_timeout", 60))
        loglvl = opts.get("log_level", "info")
        vo["log_level"].set(loglvl if loglvl in VAYDNS_LOG_LABELS else "info")

        self._vd_show_detail(True)

    def _vd_read_opt_vars(self) -> dict:
        vo = self._vd_popt_vars
        transport_str = vo["transport"].get()
        transport_key = transport_str.split(" — ")[0].strip()
        return {
            "transport":         transport_key,
            "custom_resolver":   vo["custom_resolver"].get().strip(),
            "listen_port":       vo["listen_port"].get(),
            "max_qname_len":     vo["max_qname_len"].get(),
            "max_num_labels":    vo["max_num_labels"].get(),
            "idle_timeout":      vo["idle_timeout"].get().strip(),
            "keepalive":         vo["keepalive"].get().strip(),
            "reconnect_min":     vo["reconnect_min"].get().strip(),
            "reconnect_max":     vo["reconnect_max"].get().strip(),
            "max_streams":       vo["max_streams"].get(),
            "record_type":       vo["record_type"].get(),
            "queue_size":        vo["queue_size"].get(),
            "kcp_window_size":   vo["kcp_window_size"].get(),
            "udp_workers":       vo["udp_workers"].get(),
            "udp_shared_socket": vo["udp_shared_socket"].get() == "True",
            "rps":               vo["rps"].get(),
            "resolver_timeout":  vo["resolver_timeout"].get(),
            "log_level":         vo["log_level"].get(),
        }

    def _vd_profile_save_changes(self):
        stem = self._vd_sel_profile
        if not stem: return
        p  = dict(self._vd_profiles[stem])
        fa = self._lang == "fa"
        p["name"]    = self._vd_pname_var.get().strip() or p.get("name", stem)
        p["options"] = self._vd_read_opt_vars()
        update_vaydns_profile(stem, p)
        try:
            script = write_vaydns_launch_script(p)
            self._log(f"{'VayDNS پروفایل بروزرسانی شد:' if fa else 'VayDNS profile updated:'} {script.parent}")
        except Exception as e:
            self._log(f"{'خطا:' if fa else 'Error:'} {e}")
        self._vd_profiles[stem] = p
        self._vd_refresh_profiles_list()
        messagebox.showinfo("Saved" if not fa else "ذخیره شد",
                            "تغییرات ذخیره شد" if fa else "Changes saved and launch script regenerated.")

    def _vd_profile_launch(self):
        stem = self._vd_sel_profile
        if not stem: return
        p      = self._vd_profiles[stem]
        fa     = self._lang == "fa"
        opts   = {**VAYDNS_DEFAULTS, **p.get("options", {})}
        folder = app_dir() / p.get("country", "vaydns_output")

        # Regenerate script with latest options
        try:
            script = write_vaydns_launch_script(p)
        except Exception as e:
            messagebox.showerror("", str(e)); return

        if not script.exists():
            messagebox.showerror("", f"Script not found: {script}"); return

        # Record launch time before doing the actual launch — useful even
        # if the terminal opens and the user closes it quickly.
        try:
            p["last_launched"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_vaydns_profile(stem, p)
            self._vd_profiles[stem] = p
            self._vd_refresh_profiles_list()
        except Exception:
            pass

        # Check that a vaydns-client binary exists in the output folder.
        # Use glob so any naming variant is accepted.
        # If not there, try copying it now from next to the app.
        def _find_bin_in_folder(f):
            if sys.platform == "win32":
                reject_kw = ("darwin", "linux", "macos", "mac")
                accept_kw = ("windows", "win")
            elif sys.platform == "darwin":
                reject_kw = ("windows", "win", "linux")
                accept_kw = ("darwin", "macos", "mac")
            else:
                reject_kw = ("darwin", "macos", "mac", "windows", "win")
                accept_kw = ("linux",)
            for p in sorted(f.glob("vaydns-client*")):
                n = p.name.lower()
                if p.suffix in (".zip", ".gz", ".tar", ".txt", ".md", ".json"):
                    continue
                if any(kw in n for kw in reject_kw):
                    continue
                if sys.platform == "win32":
                    if not (any(kw in n for kw in accept_kw) or p.suffix == ".exe"):
                        continue
                return p
            return None

        bin_in_folder = _find_bin_in_folder(folder)
        if not bin_in_folder:
            src_bin = get_vaydns_exe()
            if src_bin:
                # Binary exists next to app but wasn't copied — copy it now
                try:
                    import shutil as _sh2
                    dst = folder / src_bin.name
                    _sh2.copy2(str(src_bin), str(dst))
                    if sys.platform != "win32":
                        dst.chmod(dst.stat().st_mode | 0o111)
                    bin_in_folder = dst
                    self._log(f"{'باینری کپی شد:' if fa else 'Binary copied:'} {dst}")
                except Exception as _e:
                    messagebox.showerror("",
                        f"{'خطا در کپی باینری:' if fa else 'Binary copy failed:'} {_e}")
                    return
            else:
                app_folder = app_dir()
                fa_msg = (
                    f"فایل vaydns-client پیدا نشد.\n\n"
                    f"فایل اجرایی را در کنار برنامه KevinNet قرار دهید:\n{app_folder}\n\n"
                    f"هر فایلی که با vaydns-client شروع شود قبول می‌شود.\n"
                    f"مثال: vaydns-client-darwin-arm64"
                )
                en_msg = (
                    f"vaydns-client binary not found.\n\n"
                    f"Place the binary next to the KevinNet app:\n{app_folder}\n\n"
                    f"Any file starting with 'vaydns-client' is accepted.\n"
                    f"Example: vaydns-client-darwin-arm64"
                )
                messagebox.showerror(
                    "vaydns-client not found" if not fa else "فایل اجرایی پیدا نشد",
                    en_msg if not fa else fa_msg)
                return


        import subprocess, shlex
        folder_q  = shlex.quote(str(folder))
        script_q  = shlex.quote(script.name)
        try:
            if sys.platform == "win32":
                subprocess.Popen(["cmd", "/c", "start", "", str(script)], cwd=str(folder))
            elif sys.platform == "darwin":
                as_script = (
                    'tell application "Terminal"\n'
                    '    activate\n'
                    f'    do script "cd {folder_q} && bash {script_q}"\n'
                    'end tell'
                )
                subprocess.Popen(["osascript", "-e", as_script])
            else:
                launched = False
                for term, args in [
                    ("gnome-terminal", ["--working-directory", str(folder), "--", "bash", str(script)]),
                    ("xterm",          ["-e", f"cd {folder_q} && bash {script_q}"]),
                    ("konsole",        ["--workdir", str(folder), "-e", "bash", str(script)]),
                    ("xfce4-terminal", ["--working-directory", str(folder), "-e", str(script)]),
                ]:
                    try:
                        subprocess.Popen([term] + args); launched = True; break
                    except FileNotFoundError: continue
                if not launched:
                    subprocess.Popen(["bash", str(script)], cwd=str(folder))
            self._log(f"{'VayDNS راه‌اندازی شد:' if fa else 'VayDNS launched:'} {script}")
        except Exception as e:
            messagebox.showerror("", str(e))

    def _vd_profile_duplicate(self):
        stem = self._vd_sel_profile
        if not stem: return
        fa  = self._lang == "fa"
        src = dict(self._vd_profiles[stem])
        import copy as _copy, shutil as _sh

        new_name = simpledialog.askstring(
            "Duplicate" if not fa else "کپی پروفایل",
            "New profile name:" if not fa else "نام پروفایل جدید:",
            initialvalue=src.get("name", stem) + (" (copy)" if not fa else " (کپی)"),
            parent=self)
        if not new_name or not new_name.strip(): return

        new_profile = _copy.deepcopy(src)
        new_profile["name"]    = new_name.strip()
        new_profile["country"] = new_name.strip()
        new_profile["date"]    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        src_folder = app_dir() / src.get("country", stem)
        dst_folder = app_dir() / new_name.strip()
        if src_folder.exists():
            try:
                _sh.copytree(str(src_folder), str(dst_folder))
            except Exception as e:
                self._log(f"Folder copy error: {e}")
        else:
            try: write_vaydns_launch_script(new_profile)
            except Exception as e: self._log(f"Script write error: {e}")

        new_stem = save_new_vaydns_profile(new_profile)
        self._log(f"{'VayDNS پروفایل کپی شد:' if fa else 'VayDNS profile duplicated:'} {new_name}")
        self._vd_profiles = load_all_vaydns_profiles()
        self._vd_refresh_profiles_list()
        if new_stem in self._vd_profiles:
            self._vd_select_profile(new_stem)

    def _vd_profile_delete(self):
        stem = self._vd_sel_profile
        if not stem: return
        fa   = self._lang == "fa"
        name = self._vd_profiles[stem].get("name", stem)
        if not messagebox.askyesno(
                "Delete" if not fa else "حذف",
                f"{'حذف پروفایل VayDNS' if fa else 'Delete VayDNS profile'} '{name}'?"): return

        country = delete_vaydns_profile(stem)
        if country:
            fp = app_dir() / country
            if fp.exists() and messagebox.askyesno(
                    "Delete folder?" if not fa else "حذف پوشه؟",
                    f"{'پوشه خروجی هم حذف شود؟' if fa else 'Also delete output folder?'}\n{fp}"):
                import shutil as _sh
                try: _sh.rmtree(str(fp))
                except Exception as e: self._log(f"Folder delete error: {e}")

        self._vd_sel_profile = None
        self._vd_show_detail(False)
        self._vd_refresh_profiles_list()


    # ── VPN MODE SWITCH ──────────────────────────────────────────
    def _set_vpn_mode(self, mode: str):
        """Switch between masterdns and vaydns mode in the scanner."""
        self._vpn_mode.set(mode)
        W  = self._W
        fa = self._lang == "fa"

        if mode == "masterdns":
            # Pill highlight
            W["pill_master"].config(bg=BLUE, fg="#000000")
            W["pill_vaydns"].config(bg=BORDER, fg=MUTED)
            # Show MasterDNS key, hide VayDNS key
            self._vd_key_frame.pack_forget()
            self._md_key_frame.pack(fill="x")
            # Show MasterDNS save button, hide VayDNS save
            W["btn_vd_save"].pack_forget()
            W["btn_save"].pack(fill="x", padx=2)
        else:  # vaydns
            # Pill highlight
            W["pill_master"].config(bg=BORDER, fg=MUTED)
            W["pill_vaydns"].config(bg=PURPLE, fg=BTN_TEXT)
            # Show VayDNS key, hide MasterDNS key
            self._md_key_frame.pack_forget()
            self._vd_key_frame.pack(fill="x")
            # Show VayDNS save button, hide MasterDNS save
            W["btn_save"].pack_forget()
            W["btn_vd_save"].pack(fill="x", padx=2)

        # Reset scan state whenever mode changes
        self._found_ips.clear()
        for row in self._W.get("tree", tk.Frame()).winfo_children():
            try: row.destroy()
            except Exception: pass

    # ── LEFT PANEL ──────────────────────────────────────────────
    def _build_left(self, parent):
        W  = self._W
        fa = self._lang == "fa"

        # helper: section card header
        def card_hdr(fr, key, en, pfa, col=ACCENT):
            lbl = tk.Label(fr, text=pfa if fa else en,
                           bg=BORDER, fg=col,
                           font=FA(10, "bold") if fa else F(10, "bold"),
                           padx=12, pady=6, anchor="w")
            lbl.pack(fill="x")
            W[key] = lbl

        # helper: labelled entry
        def entry_field(parent, wkey_lbl, wkey_ent, wkey_hint,
                        en_lbl, fa_lbl, en_hint, fa_hint,
                        var=None, show=None):
            fr = tk.Frame(parent, bg=CARD)
            fr.pack(fill="x", padx=14, pady=(10, 4))
            lbl = tk.Label(fr, text=fa_lbl if fa else en_lbl,
                           bg=CARD, fg=TEXT,
                           font=FA(11) if fa else F(11), anchor="w")
            lbl.pack(fill="x")
            if var is None:
                var = tk.StringVar()
            kw = dict(textvariable=var, bg=INPUT, fg=TEXT,
                      insertbackground=ACCENT, relief="flat", bd=0,
                      font=FM(12),
                      highlightbackground=BORDER, highlightthickness=1,
                      highlightcolor=ACCENT)
            if show:
                kw["show"] = show
            ent = tk.Entry(fr, **kw)
            ent.pack(fill="x", ipady=10, pady=(3, 0))
            hint = tk.Label(fr, text=fa_hint if fa else en_hint,
                            bg=CARD, fg=MUTED,
                            font=FA(9) if fa else F(9), anchor="w")
            hint.pack(fill="x")
            W[wkey_lbl]  = lbl
            W[wkey_ent]  = ent
            W[wkey_hint] = hint
            return var

        # ── Card 1: Config ──
        c1 = tk.Frame(parent, bg=CARD,
                      highlightbackground=BORDER, highlightthickness=1)
        c1.pack(fill="x", pady=(0, 10))
        card_hdr(c1, "c1_hdr", "⚙  Tunnel Config", "⚙  تنظیمات تانل", ACCENT)

        # ── VPN Mode selector ──────────────────────────────────────
        mode_frame = tk.Frame(c1, bg=CARD)
        mode_frame.pack(fill="x", padx=14, pady=(10, 0))

        tk.Label(mode_frame,
                 text="نوع VPN" if fa else "VPN Type",
                 bg=CARD, fg=TEXT,
                 font=FA(11) if fa else F(11),
                 anchor="w").pack(fill="x")

        pill_row = tk.Frame(mode_frame, bg=CARD)
        pill_row.pack(fill="x", pady=(6, 4))

        self._vpn_mode = tk.StringVar(value="masterdns")

        def make_pill(wkey, en, fa_t, value):
            is_sel = (value == "masterdns")
            b = tk.Button(pill_row,
                          text=fa_t if fa else en,
                          bg=BLUE if is_sel else BORDER,
                          fg="#000000" if is_sel else MUTED,
                          font=F(10, "bold"), relief="flat", bd=0,
                          padx=20, pady=8, cursor="hand2",
                          activebackground=BLUE, activeforeground="#000000",
                          command=lambda v=value: self._set_vpn_mode(v))
            b.pack(side="left", padx=(0, 6))
            W[wkey] = b

        make_pill("pill_master", "MasterDNS", "MasterDNS", "masterdns")
        make_pill("pill_vaydns", "VayDNS",    "VayDNS",    "vaydns")

        # ── MasterDNS key field (shown when masterdns selected) ──
        self._md_key_frame = tk.Frame(c1, bg=CARD)
        self._key_var = entry_field(
            self._md_key_frame, "key_lbl", "key_ent", "key_hint",
            "MasterDNS Encryption Key",  "کلید رمزنگاری MasterDNS",
            "32-char key from server  (encrypt_key.txt)",
            "کلید ۳۲ کاراکتری از سرور  (فایل encrypt_key.txt)")
        # Key frame packed AFTER country/domain — see _set_vpn_mode

        # ── VayDNS key field (shown when vaydns selected) ────────
        self._vd_key_frame = tk.Frame(c1, bg=CARD)
        self._vd_pubkey_var = entry_field(
            self._vd_key_frame, "vd_key_lbl", "vd_key_ent", "vd_key_hint",
            "VayDNS Public Key",  "کلید عمومی VayDNS",
            "64-char hex pubkey from server  (server.pub)",
            "کلید عمومی ۶۴ کاراکتری hex از سرور  (server.pub)")
        self._vd_key_frame.pack_forget()    # hidden by default

        # Country comes before domain in the UI
        self._country_var = entry_field(
            c1, "country_lbl", "country_ent", "country_hint",
            "Country / Folder", "نام کشور / پوشه",
            "output folder name  e.g. Iran  Turkey  etc.",
            "نام پوشه خروجی  مثال: Iran  Turkey")

        self._domain_var = entry_field(
            c1, "domain_lbl", "domain_ent", "domain_hint",
            "Tunnel Domain",  "دامنه تانل",
            "subdomain pointing to your server  e.g. v.example.com",
            "ساب‌دامین که به سرور اشاره دارد  مثال: v.example.com")
        self._md_key_frame.pack(fill="x")  # default: MasterDNS selected

        tk.Frame(c1, bg=CARD, height=10).pack()

        # ── Card 2: Scan Options ──
        c2 = tk.Frame(parent, bg=CARD,
                      highlightbackground=BORDER, highlightthickness=1)
        c2.pack(fill="x", pady=(0, 10))
        card_hdr(c2, "c2_hdr", "🔍  Scan Options", "🔍  تنظیمات اسکن", BLUE)

        # Two rows of spinboxes so nothing gets cut off on narrow screens
        spin_row1 = tk.Frame(c2, bg=CARD)
        spin_row1.pack(fill="x", padx=14, pady=(10, 4))
        spin_row2 = tk.Frame(c2, bg=CARD)
        spin_row2.pack(fill="x", padx=14, pady=(0, 6))

        def spin_col(parent, wlbl, wsp, en, pfa, lo, hi, default):
            col = tk.Frame(parent, bg=CARD)
            col.pack(side="left", fill="x", expand=True, padx=(0, 8))
            lbl = tk.Label(col, text=pfa if fa else en, bg=CARD, fg=MUTED,
                           font=FA(9) if fa else F(9), anchor="w")
            lbl.pack(fill="x")
            var = tk.IntVar(value=default)
            sp  = tk.Spinbox(col, from_=lo, to=hi, textvariable=var,
                             bg=INPUT, fg=TEXT, insertbackground=ACCENT,
                             buttonbackground=BORDER, relief="flat", bd=0,
                             font=FM(11),
                             highlightbackground=BORDER, highlightthickness=1,
                             highlightcolor=ACCENT, width=5)
            sp.pack(fill="x", ipady=8)
            W[wlbl] = lbl
            W[wsp]  = sp
            return var

        # Row 1: Target  Concurrency  Timeout
        self._target_var  = spin_col(spin_row1, "t_lbl",  "t_sp",  "Target",       "هدف",             5,    500,  100)
        self._conc_var    = spin_col(spin_row1, "c_lbl",  "c_sp",  "Concurrency",  "همزمانی",         10,   500,  100)
        self._timeout_var = spin_col(spin_row1, "to_lbl", "to_sp", "Timeout (s)",  "Timeout (ثانیه)", 1,    10,     3)
        # Row 2: Pool (full width so label is readable)
        self._pool_var    = spin_col(spin_row2, "p_lbl",  "p_sp",  "Pool ×1000 IPs", "پول ×۱۰۰۰ IP",  10, 1000,  200)
        # Add empty spacers to balance row 2 visually
        tk.Frame(spin_row2, bg=CARD).pack(side="left", fill="x", expand=True, padx=(0,8))
        tk.Frame(spin_row2, bg=CARD).pack(side="left", fill="x", expand=True)

        tk.Frame(c2, bg=CARD, height=6).pack()

        # ── Buttons ──
        bf = tk.Frame(parent, bg=BG)
        bf.pack(fill="x", pady=(2, 0))

        def mk_btn(wkey, en, pfa, bg_c, fg_c, cmd, state="normal"):
            act_bg = bg_c if state == "normal" else DIS_BG
            act_fg = BTN_TEXT if state == "normal" else DIS_FG
            wrapper = tk.Frame(bf, bg=BG)
            wrapper.pack(fill="x", pady=(0, 5))
            b = tk.Button(wrapper,
                          text=pfa if fa else en,
                          bg=act_bg, fg=act_fg,
                          font=FA(12, "bold") if fa else F(12, "bold"),
                          relief="flat", bd=0,
                          padx=18, pady=11,
                          cursor="hand2" if state == "normal" else "arrow",
                          state=state,
                          activebackground=bg_c,
                          activeforeground=BTN_TEXT,
                          disabledforeground=DIS_FG,
                          command=cmd)
            b.pack(fill="x", padx=2)
            W[wkey] = b

        mk_btn("btn_scan",    "▶  Start Scan",  "▶  شروع اسکن", ACCENT, SCAN_FG, self._start_scan)
        mk_btn("btn_stop",    "■  Stop",         "■  توقف",       DANGER, "#000000", self._stop_scan, "disabled")
        # DoH/DoT scan — alternative encrypted transports. Slower but harder
        # for Iranian DPI to fingerprint than plain UDP/53. Lower-key colour
        # so the primary "Start Scan" remains visually dominant.
        mk_btn("btn_doh_scan", "🔒  Scan DoH/DoT", "🔒  اسکن DoH/DoT",
               PURPLE, BTN_TEXT, self._start_doh_dot_scan)

        # Save button frame — only the active VPN mode's button is visible
        self._save_btn_frame = tk.Frame(bf, bg=BG)
        self._save_btn_frame.pack(fill="x", pady=(0, 5))

        def mk_save_btn(wkey, en, pfa, bg_c, fg_c, cmd):
            b = tk.Button(self._save_btn_frame,
                          text=pfa if fa else en,
                          bg=DIS_BG, fg=DIS_FG,
                          font=FA(12, "bold") if fa else F(12, "bold"),
                          relief="flat", bd=0,
                          padx=18, pady=11,
                          cursor="arrow",
                          state="disabled",
                          activebackground=bg_c,
                          activeforeground=fg_c,
                          disabledforeground=DIS_FG,
                          command=cmd)
            b.pack(fill="x", padx=2)
            W[wkey] = b

        mk_save_btn("btn_save",    "💾  Save to MasterDNS Profiles", "💾  ذخیره در MasterDNS",
                    BLUE,   SAVE_FG, self._save_configs)
        mk_save_btn("btn_vd_save", "💾  Save to VayDNS Profiles",    "💾  ذخیره در VayDNS",
                    PURPLE, BTN_TEXT, self._save_vaydns_profile)

        # Show only the MasterDNS save button initially
        W["btn_vd_save"].pack_forget()

        mk_btn("btn_export",  "📤  Export DNS List", "📤  خروجی لیست DNS", WARN, BTN_TEXT, self._export_dns, "disabled")
        mk_btn("btn_clear",   "🗑  Clear",  "🗑  پاک کردن", BORDER, CLEAR_FG, self._clear)

    # ── RIGHT PANEL ─────────────────────────────────────────────
    def _build_right(self, parent):
        W = self._W

        # Progress row
        prog_top = tk.Frame(parent, bg=BG)
        prog_top.pack(fill="x", pady=(0, 6))
        W["prog_lbl"] = tk.Label(prog_top, text="Ready",
                                  bg=BG, fg=MUTED, font=F(10))
        W["prog_lbl"].pack(side="left")
        W["badge"] = tk.Label(prog_top, text="0  found",
                               bg=CARD, fg=GREEN,
                               font=F(10, "bold"), padx=12, pady=4,
                               relief="flat",
                               highlightbackground=GREEN,
                               highlightthickness=1)
        W["badge"].pack(side="right")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("G.Horizontal.TProgressbar",
                        troughcolor=BORDER, background=ACCENT,
                        bordercolor=BORDER, thickness=14,
                        lightcolor=ACCENT, darkcolor=ACCENT)
        W["progress"] = ttk.Progressbar(parent,
                                         style="G.Horizontal.TProgressbar",
                                         mode="determinate", maximum=100)
        W["progress"].pack(fill="x", pady=(0, 10))

        # Results card
        res = tk.Frame(parent, bg=CARD,
                       highlightbackground=BORDER, highlightthickness=1)
        res.pack(fill="both", expand=True, pady=(0, 8))

        res_hdr_fr = tk.Frame(res, bg=BORDER)
        res_hdr_fr.pack(fill="x")
        W["res_hdr"] = tk.Label(res_hdr_fr,
                                 text="🟢  Found Resolvers",
                                 bg=BORDER, fg=GREEN,
                                 font=F(10, "bold"), padx=12, pady=6,
                                 anchor="w")
        W["res_hdr"].pack(side="left", fill="x", expand=True)
        W["res_count"] = tk.Label(res_hdr_fr, text="",
                                   bg=BORDER, fg=MUTED,
                                   font=F(9), padx=10, pady=6)
        W["res_count"].pack(side="right")

        style.configure("R.Treeview",
                        background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=32,
                        font=FM(11),
                        borderwidth=0, relief="flat")
        style.configure("R.Treeview.Heading",
                        background="#0d1526", foreground=ACCENT,
                        font=F(10, "bold"), padding=(8, 6))
        style.map("R.Treeview",
                  background=[("selected", "#1e3a60")],
                  foreground=[("selected", "#ffffff")])

        tv_fr = tk.Frame(res, bg=CARD)
        tv_fr.pack(fill="both", expand=True)

        W["tree"] = ttk.Treeview(tv_fr, columns=("ip", "score", "ms", "detail"),
                                  show="headings", style="R.Treeview")
        W["tree"].heading("ip",     text="IP Address")
        W["tree"].heading("score",  text="Score")
        W["tree"].heading("ms",     text="ms")
        W["tree"].heading("detail", text="Checks")
        W["tree"].column("ip",     width=150, anchor="w")
        W["tree"].column("score",  width=60,  anchor="center")
        W["tree"].column("ms",     width=70,  anchor="center")
        W["tree"].column("detail", width=380, anchor="w")
        vsb = ttk.Scrollbar(tv_fr, orient="vertical",
                             command=W["tree"].yview)
        W["tree"].configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        W["tree"].pack(side="left", fill="both", expand=True)

        # Right-click context menu — Copy IP, Copy all IPs, Open in browser.
        # Right-click on macOS is Button-2 (single-button mice) or Button-3
        # (multi-button + trackpad two-finger). Bind both.
        self._tree_menu = tk.Menu(self, tearoff=False, bg=CARD, fg=TEXT,
                                  activebackground=ACCENT,
                                  activeforeground="#000000")
        self._tree_menu.add_command(
            label="Copy IP", command=self._tree_copy_selected_ip)
        self._tree_menu.add_command(
            label="Copy all IPs", command=self._tree_copy_all_ips)
        self._tree_menu.add_separator()
        self._tree_menu.add_command(
            label="Open output folder", command=self._open_saved_folder)

        def _on_right_click(event):
            iid = W["tree"].identify_row(event.y)
            if iid:
                W["tree"].selection_set(iid)
            try:
                self._tree_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self._tree_menu.grab_release()

        W["tree"].bind("<Button-3>", _on_right_click)   # Linux / Windows / mac multi-button
        W["tree"].bind("<Button-2>", _on_right_click)   # macOS single-button
        # Control-click on macOS also brings up context menu
        W["tree"].bind("<Control-Button-1>", _on_right_click)

        # Log card
        log_card = tk.Frame(parent, bg=CARD,
                            highlightbackground=BORDER, highlightthickness=1)
        log_card.pack(fill="x")
        tk.Label(log_card, text="📋  Log",
                 bg=BORDER, fg=MUTED,
                 font=F(10, "bold"), padx=12, pady=5, anchor="w").pack(fill="x")
        W["log"] = scrolledtext.ScrolledText(
            log_card, height=7,
            bg="#0a0f1e", fg="#7a9cc0",
            insertbackground=ACCENT,
            font=FM(10), relief="flat", bd=0, state="disabled")
        W["log"].pack(fill="both", padx=2, pady=2)

    # ── LANGUAGE ────────────────────────────────────────────────
    def _toggle_lang(self):
        self._lang = "en" if self._lang == "fa" else "fa"
        self._refresh_lang()

    def _refresh_lang(self):
        fa = self._lang == "fa"
        W  = self._W
        ff = FA if fa else F

        W["btn_lang"].config(text="English" if fa else "فارسی",
                             fg=ACCENT, font=FA(10, "bold"))
        W["btn_help"].config(text="؟  راهنما" if fa else "?  Help",
                             fg=TEXT,   font=FA(10, "bold"))

        W["c1_hdr"].config(text="⚙  تنظیمات تانل"   if fa else "⚙  Tunnel Config",
                           font=ff(10, "bold"))
        W["c2_hdr"].config(text="🔍  تنظیمات اسکن"  if fa else "🔍  Scan Options",
                           font=ff(10, "bold"))

        for wlbl, whin, fa_t, en_t, fa_h, en_h in [
            ("domain_lbl",  "domain_hint",
             "دامنه تانل",     "Tunnel Domain",
             "مثال:  v.example.com", "e.g.  v.example.com"),
            ("key_lbl",     "key_hint",
             "کلید رمزنگاری",  "Encryption Key",
             "کلید ۳۲ کاراکتری", "32-char key"),
            ("country_lbl", "country_hint",
             "نام کشور / پوشه", "Country / Folder",
             "مثال:  Iran",    "e.g.  Iran"),
        ]:
            W[wlbl].config(text=fa_t if fa else en_t, font=ff(11))
            W[whin].config(text=fa_h if fa else en_h, font=ff(9))

        for wlbl, fa_t, en_t in [
            ("t_lbl",  "هدف",            "Target"),
            ("c_lbl",  "همزمانی",         "Concurrency"),
            ("to_lbl", "Timeout (ثانیه)", "Timeout (s)"),
            ("p_lbl",  "پول (×۱۰۰۰)",    "Pool (x1000)"),
        ]:
            W[wlbl].config(text=fa_t if fa else en_t, font=ff(9))

        h_fa = "پیشنهاد ایران: Target=100  Concurrency<=80  Timeout=3s  Pool=200-500\n"                "Resolver kam? Pool raa bala bebrid ya eskan chand bar ejra konid"
        h_en = "Iran recommended: Target=100  Concurrency<=80  Timeout=3s  Pool=200-500\n"                "Finding few resolvers? Increase Pool or run scan multiple times"
        if "scan_hint" in W:
            W["scan_hint"].config(text=h_fa if fa else h_en, font=ff(8))
        if "log_hdr_lbl" in W:
            W["log_hdr_lbl"].config(text="📋  گزارش فعالیت" if fa else "📋  Activity Log",
                                    font=ff(10, "bold"))

        for wkey, fa_t, en_t in [
            ("btn_scan",    "▶  شروع اسکن",           "▶  Start Scan"),
            ("btn_stop",    "■  توقف",                "■  Stop"),
            ("btn_save",    "💾  ذخیره در MasterDNS", "💾  Save to MasterDNS Profiles"),
            ("btn_vd_save", "💾  ذخیره در VayDNS",    "💾  Save to VayDNS Profiles"),
            ("btn_export",  "📤  خروجی لیست DNS",     "📤  Export DNS List"),
            ("vd_key_lbl",  "کلید عمومی VayDNS",      "VayDNS Public Key"),
            ("pill_master", "MasterDNS",               "MasterDNS"),
            ("pill_vaydns", "VayDNS",                  "VayDNS"),
            ("btn_clear",   "🗑  پاک کردن",            "🗑  Clear"),
        ]:
            W[wkey].config(text=fa_t if fa else en_t,
                           font=ff(12, "bold"))

        n = len(self._found_ips)
        W["res_hdr"].config(
            text="🟢  Resolver های تایید شده (۵/۶ یا ۶/۶)" if fa else "🟢  Verified Resolvers (5/6 or 6/6)")
        W["badge"].config(text=f"{n}  {'یافت‌شده' if fa else 'found'}")

    # ── LOG ─────────────────────────────────────────────────────
    def _log(self, msg):
        log = self._W.get("log")
        if not log:
            return
        ts   = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}]  {msg}\n"
        if   msg.startswith("★"):                                    tag = "star"
        elif msg.startswith("◆"):                                    tag = "diamond"
        elif msg.startswith("▸"):                                    tag = "arrow"
        elif any(x in msg for x in ("⚠","ERROR","error","خطا")):    tag = "warn"
        elif any(x in msg for x in ("E2E","Phase 3","مرحله ۳","تأیید E2E")): tag = "e2e"
        elif any(x in msg for x in ("Saved","ذخیره","copied","کپی","SUCCESS","SUCCESS")): tag = "star"
        elif any(x in msg for x in ("Phase","مرحله","Pool","Settings","تنظیمات","پایگاه")): tag = "info"
        else:                                                         tag = "muted"
        log.config(state="normal")
        log.insert("end", line, tag)
        log.see("end")
        log.config(state="disabled")

    # ── SCAN ────────────────────────────────────────────────────
    def _start_scan(self):
        if not DNS_AVAILABLE:
            messagebox.showerror(
                "Error", "dnspython not installed.\nRun:  pip install dnspython")
            return

        domain  = self._domain_var.get().strip()
        key     = self._key_var.get().strip()
        country = self._country_var.get().strip()
        fa      = self._lang == "fa"

        mode = self._vpn_mode.get()

        # Validate inputs upfront. Bad input here causes confusing TOML
        # parse errors or silent failures later — much better to reject early.
        ok, err = validate_domain(domain)
        if not ok:
            messagebox.showwarning(
                "", ("دامنه نامعتبر است. " if fa else "Invalid domain. ") + err)
            return

        ok, err = validate_folder_name(country)
        if not ok:
            messagebox.showwarning(
                "", ("نام پوشه نامعتبر است. " if fa else "Invalid folder name. ") + err)
            return

        # Validate the key for the selected VPN mode
        if mode == "masterdns":
            ok, err = validate_masterdns_key(key)
            if not ok:
                messagebox.showwarning(
                    "", ("کلید MasterDNS نامعتبر است. " if fa
                         else "Invalid MasterDNS key. ") + err)
                return
            pubkey = ""
        else:  # vaydns
            pubkey = (self._vd_pubkey_var.get() if self._vd_pubkey_var else "").strip()
            ok, err = validate_vaydns_pubkey(pubkey)
            if not ok:
                messagebox.showwarning(
                    "", ("کلید عمومی VayDNS نامعتبر است. " if fa
                         else "Invalid VayDNS public key. ") + err)
                return

        # Persist last-used inputs so a restart resumes where the user left off
        try:
            settings = load_settings()
            settings["last_mode"]    = mode
            settings["last_domain"]  = domain
            settings["last_country"] = country
            save_settings(settings)
        except Exception:
            pass

        # Reset UI
        self._found_ips.clear()
        self._auto_saved_stem = None
        for row in self._W["tree"].get_children():
            self._W["tree"].delete(row)
        self._stop_ev.clear()
        self._scanning = True
        self._W["btn_scan"].config(state="disabled", bg=DIS_BG, fg=DIS_FG, disabledforeground=DIS_FG)
        self._W["btn_stop"].config(state="normal",   bg=DANGER, fg="#000000", disabledforeground=DIS_FG)
        self._W["btn_save"].config(state="disabled", bg=DIS_BG, fg=DIS_FG, disabledforeground=DIS_FG)
        self._W["progress"]["value"] = 0
        self._W["status_lbl"].config(text="● Scanning…", fg=WARN)

        target  = self._target_var.get()
        conc    = self._conc_var.get()
        timeout = float(self._timeout_var.get())
        builtin_ips = get_builtin_resolvers()           # 376 known public
        pool_size   = self._pool_var.get() * 1000
        iran_ips    = get_iran_sample(pool_size)            # user-defined pool size
        # Combine: built-in first (tested first), then Iran sample
        seen = set()
        ips  = []
        for ip in builtin_ips + iran_ips:
            if ip not in seen:
                seen.add(ip)
                ips.append(ip)

        self._log(
            f"{'پایگاه داده:' if fa else 'Pool:'} "
            f"{len(builtin_ips)} {'resolver شناخته‌شده' if fa else 'known resolvers'} + "
            f"{len(iran_ips)} {'IP ایران (مثل SlipNet)' if fa else 'Iran IPs (same scale as SlipNet)'} "
            f"= {len(ips):,} {'کل' if fa else 'total'}")
        self._log(
            f"{'مرحله ۱: اسکن سریع  →  مرحله ۲: امتیازدهی (همه نشان داده می‌شن)  →  مرحله ۳: تأیید E2E واقعی' if fa else 'Phase 1: alive scan  →  Phase 2: scoring (all shown)  →  Phase 3: E2E real tunnel verify'}")
        self._log(
            f"{'★=6/6  ◆=4-5  ▸=2-3  ·=0-1  — همه در مرحله E2E تست می‌شن' if fa else '★=6/6  ◆=4-5  ▸=2-3  ·=0-1  — all go to E2E phase, real tunnel is the final filter'}")
        self._log(
            f"{'تنظیمات:' if fa else 'Settings:'} "
            f"concurrency={conc}  timeout={timeout}s  target={target}")

        # Callbacks (thread-safe via after())
        def _prog(tested, total, found, pct, label=""):
            self._q.put(("prog", tested, total, found, pct, label))

        def _res(ip, score, max_score, ms, detail_str):
            self._q.put(("res", ip, score, max_score, ms, detail_str))

        def _done(tested, found):
            self._q.put(("done", tested, found))

        # ── Safe concurrency cap ──────────────────────────────
        # macOS/Linux default fd limit is 256.
        # Each DNS query opens a UDP socket → cap to avoid silent failures.
        # Phase 1 (quick): safe_conc  Phase 2 (6-check): safe_conc // 4
        # because each Phase-2 task opens up to 6 sockets simultaneously.
        if sys.platform == "darwin":
            # Try to raise the fd limit first.
            # IMPORTANT: safe_conc caps Phase 1. Phase 2 uses safe_conc // 4
            # internally (see run_scan). On Intel Macs, Phase 2 opens up to 6
            # sockets per task — too high a cap causes kernel panics at 200k+
            # pool sizes. 150 is the safe ceiling for Intel; ARM tolerates more.
            try:
                import resource, platform as _plat
                soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
                target_fd  = min(hard, 4096)
                resource.setrlimit(resource.RLIMIT_NOFILE, (target_fd, hard))
                # Apple Silicon can handle higher concurrency than Intel
                is_arm = _plat.machine() in ("arm64", "aarch64")
                mac_cap = 250 if is_arm else 150
                safe_conc = min(conc, mac_cap)
            except Exception:
                safe_conc  = min(conc, 80)
        elif sys.platform == "win32":
            safe_conc = min(conc, 200)   # Windows handles more sockets
        else:
            safe_conc = min(conc, 150)   # Linux — generous but safe

        safe_conc = max(safe_conc, 20)   # never go below 20

        if safe_conc != conc:
            self._log(
                f"{'محدودیت سیستمی: همزمانی از' if fa else 'OS socket limit: concurrency capped'} "
                f"{conc} → {safe_conc}  "
                f"({'مرحله ۲:' if fa else 'Phase 2:'} {max(20, safe_conc // 4)})")

        # Background thread with correct event loop
        def _run():
            loop = (asyncio.SelectorEventLoop()
                    if sys.platform == "win32"
                    else asyncio.new_event_loop())
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(
                    run_scan(ips, domain, safe_conc, timeout,
                             target, _prog, _res, _done, self._stop_ev))
            finally:
                loop.close()

        threading.Thread(target=_run, daemon=True).start()

    def _on_progress(self, tested, total, found, pct, label=""):
        fa = self._lang == "fa"
        self._W["progress"]["value"] = min(pct, 100)
        if label:
            txt = label
        else:
            txt = (f"تست‌شده: {tested:,}  |  یافت: {found}  |  پیشرفت: {pct:.1f}%"
                   if fa else
                   f"Tested: {tested:,}  |  Found: {found}  |  {pct:.1f}%")
        self._W["prog_lbl"].config(text=txt)
        n = len(self._found_ips)
        self._W["badge"].config(
            text=f"{n}  {'یافت‌شده' if fa else 'found'}")

    def _on_result(self, ip, score, max_score, ms, detail_str):
        fa = self._lang == "fa"
        self._found_ips.append(ip)
        n = len(self._found_ips)
        if "res_count" in self._W:
            self._W["res_count"].config(
                text=f"{n} {'یافت‌شده' if fa else 'found'}")
        # Color by score — all shown, sorted visually
        if score == 6:
            tag, icon = "s6", "★"   # bright green  — perfect
        elif score >= 4:
            tag, icon = "s4", "◆"   # yellow        — good
        elif score >= 2:
            tag, icon = "s2", "▸"   # orange        — weak but possible
        else:
            tag, icon = "s0", "·"   # muted         — very weak
        self._W["tree"].insert("", "end",
                               values=(ip,
                                       f"{score}/{max_score}",
                                       f"{ms:.0f}",
                                       detail_str),
                               tags=(tag,))
        self._W["tree"].tag_configure("s6", foreground="#34d399")
        self._W["tree"].tag_configure("s4", foreground="#fbbf24")
        self._W["tree"].tag_configure("s2", foreground="#fb923c")
        self._W["tree"].tag_configure("s0", foreground="#64748b")
        self._log(f"{icon}  {ip}   {score}/{max_score}   {ms:.0f}ms   {detail_str}")
        n = len(self._found_ips)
        self._W["badge"].config(
            text=f"{n}  {'یافت‌شده' if fa else 'found'}")

    def _on_done(self, tested, found):
        fa = self._lang == "fa"
        self._scanning = False
        self._W["btn_scan"].config(state="disabled", bg=DIS_BG, fg=DIS_FG, disabledforeground=DIS_FG)
        self._W["btn_stop"].config(state="disabled", bg=DIS_BG, fg=DIS_FG, disabledforeground=DIS_FG)
        self._W["btn_save"].config(state="disabled", bg=DIS_BG, fg=DIS_FG, disabledforeground=DIS_FG)
        self._log(f"{'اسکن DNS کامل شد — تست: ' if fa else 'DNS scan done — tested: '}{tested:,}  {'یافت: ' if fa else 'found: '}{found}")

        if found and not self._stop_ev.is_set():
            # Auto-start Phase 3 E2E immediately
            self._W["status_lbl"].config(
                text=f"● {'مرحله ۳: تأیید واقعی تانل…' if fa else 'Phase 3: E2E tunnel verify…'}",
                fg="#a78bfa")
            self._log(
                f"{'مرحله ۳ شروع شد — تأیید واقعی تانل با SlipNet…' if fa else 'Phase 3 started — real tunnel verify via SlipNet…'}")
            self._run_e2e_auto()
        else:
            # No results or stopped — just enable save if anything found
            self._W["btn_scan"].config(state="normal",  bg=ACCENT,  fg="#000000", disabledforeground=DIS_FG)
            if found:
                mode = self._vpn_mode.get()
                if mode == "masterdns":
                    self._W["btn_save"].config(state="normal", bg=BLUE, fg="#000000", disabledforeground=DIS_FG)
                else:
                    self._W["btn_vd_save"].config(state="normal", bg=PURPLE, fg=BTN_TEXT, disabledforeground=DIS_FG)
            self._W["status_lbl"].config(
                text=f"● {'اتمام' if fa else 'Done'}  —  {found} {'یافت‌شده' if fa else 'found'}",
                fg=GREEN)

    def _run_e2e_auto(self):
        """Auto Phase 3 — triggered automatically after Phase 2."""
        fa     = self._lang == "fa"
        domain = self._domain_var.get().strip()

        if not domain or not self._found_ips:
            self._W["btn_scan"].config(state="normal",  bg=ACCENT,  fg="#000000", disabledforeground=DIS_FG)
            if self._found_ips:
                self._W["btn_save"].config(state="normal",  bg=BLUE,   fg="#000000", disabledforeground=DIS_FG)
            return

        timeout = float(self._timeout_var.get())
        ips_to_test = list(self._found_ips)

        def _on_log(msg):
            self._q.put(("log", msg))

        def _on_verified(ip, score, ms, detail):
            self._q.put(("e2e_res", ip, score, ms, detail))

        def _on_e2e_done(verified_ips):
            self._q.put(("e2e_done", verified_ips))

        def _run():
            run_e2e_verify(
                ips_to_test, domain, timeout,
                _on_log, _on_verified, _on_e2e_done, self._stop_ev)

        threading.Thread(target=_run, daemon=True).start()

    def _start_doh_dot_scan(self):
        """Probe the curated DoH and DoT endpoint lists.

        Unlike the UDP scan this doesn't require a tunnel domain — it's a
        pure reachability + latency check from the user's network. Useful
        for picking a `custom_resolver` value to paste into a VayDNS DoH
        or DoT profile when plain UDP isn't surviving DPI any more.
        """
        if not DNS_AVAILABLE:
            messagebox.showerror(
                "Error", "dnspython not installed.\nRun:  pip install dnspython")
            return
        fa = self._lang == "fa"
        endpoints_doh = get_doh_endpoints()
        endpoints_dot = get_dot_endpoints()
        if not (endpoints_doh or endpoints_dot):
            messagebox.showwarning(
                "",
                "هیچ endpoint برای DoH/DoT تعریف نشده." if fa
                else "No DoH/DoT endpoints configured.")
            return

        # Reset visible state
        for row in self._W["tree"].get_children():
            self._W["tree"].delete(row)
        self._W["progress"]["value"] = 0
        self._stop_ev.clear()
        self._scanning = True
        self._W["btn_scan"].config(state="disabled", bg=DIS_BG, fg=DIS_FG, disabledforeground=DIS_FG)
        self._W["btn_doh_scan"].config(state="disabled", bg=DIS_BG, fg=DIS_FG, disabledforeground=DIS_FG)
        self._W["btn_stop"].config(state="normal", bg=DANGER, fg="#000000", disabledforeground=DIS_FG)
        self._W["status_lbl"].config(
            text="● DoH/DoT scanning…", fg=WARN)
        self._log(
            f"{'شروع اسکن DoH/DoT…' if fa else 'DoH/DoT scan starting…'} "
            f"{len(endpoints_doh)} DoH + {len(endpoints_dot)} DoT")

        timeout = float(self._timeout_var.get())

        def _prog(tested, total, found, pct, label=""):
            self._q.put(("prog", tested, total, found, pct, label))

        def _res_doh(endpoint, ms):
            self._q.put(("doh_res", endpoint, ms))

        def _res_dot(endpoint, ms):
            self._q.put(("dot_res", endpoint, ms))

        def _done(tested, found):
            self._q.put(("doh_dot_done", tested, found))

        def _run():
            loop = (asyncio.SelectorEventLoop()
                    if sys.platform == "win32"
                    else asyncio.new_event_loop())
            asyncio.set_event_loop(loop)
            try:
                # Scan DoH first, then DoT — display interleaves naturally
                # because results stream as they arrive.
                if endpoints_doh and not self._stop_ev.is_set():
                    loop.run_until_complete(
                        run_doh_dot_scan(
                            "doh", endpoints_doh, 8, timeout,
                            _prog, _res_doh,
                            lambda t, f: None,    # intermediate done is no-op
                            self._stop_ev))
                if endpoints_dot and not self._stop_ev.is_set():
                    loop.run_until_complete(
                        run_doh_dot_scan(
                            "dot", endpoints_dot, 8, timeout,
                            _prog, _res_dot, _done, self._stop_ev))
                else:
                    _done(0, 0)
            finally:
                loop.close()

        threading.Thread(target=_run, daemon=True).start()

    def _stop_scan(self):
        self._stop_ev.set()
        self._W["btn_stop"].config(state="disabled", bg=DIS_BG, fg=DIS_FG, disabledforeground=DIS_FG)
        self._W["btn_scan"].config(state="normal",   bg=ACCENT,  fg="#000000", disabledforeground=DIS_FG)
        if "btn_doh_scan" in self._W:
            self._W["btn_doh_scan"].config(
                state="normal", bg=PURPLE, fg=BTN_TEXT,
                disabledforeground=DIS_FG)
        self._log("⏹  Stopped.")

    def _clear(self):
        self._stop_ev.set()
        self._found_ips.clear()
        for row in self._W["tree"].get_children():
            self._W["tree"].delete(row)
        log = self._W["log"]
        log.config(state="normal")
        log.delete("1.0", "end")
        log.config(state="disabled")
        self._W["progress"]["value"] = 0
        self._W["prog_lbl"].config(text="Ready")
        fa = self._lang == "fa"
        self._W["badge"].config(text=f"0  {'یافت‌شده' if fa else 'found'}")
        self._W["status_lbl"].config(text="● Ready", fg=GREEN)
        self._W["btn_save"].config(state="disabled",    bg="#1a2a4a")
        self._W["btn_vd_save"].config(state="disabled", bg=DIS_BG, fg=DIS_FG, disabledforeground=DIS_FG)
        self._W["btn_export"].config(state="disabled",  bg=DIS_BG, fg=DIS_FG, cursor="arrow", disabledforeground=DIS_FG)
        self._W["btn_scan"].config(state="normal",       bg=ACCENT)
        self._W["btn_stop"].config(state="disabled",     bg=DIS_BG, fg=DIS_FG, disabledforeground=DIS_FG)
        if "btn_doh_scan" in self._W:
            self._W["btn_doh_scan"].config(
                state="normal", bg=PURPLE, fg=BTN_TEXT,
                disabledforeground=DIS_FG)
        self._saved_folder = None

    # ── Context menu actions on the resolver tree ────────────────
    def _tree_copy_selected_ip(self):
        """Copy the selected resolver's IP to the OS clipboard."""
        sel = self._W["tree"].selection()
        if not sel:
            return
        vals = self._W["tree"].item(sel[0], "values")
        if not vals:
            return
        ip = str(vals[0])
        try:
            self.clipboard_clear()
            self.clipboard_append(ip)
            self.update()         # required on some platforms to commit
            self._log(f"{'کپی شد:' if self._lang == 'fa' else 'Copied:'} {ip}")
        except Exception:
            pass

    def _tree_copy_all_ips(self):
        """Copy every resolver IP currently in the tree to the clipboard,
        one per line. Order matches what the user is seeing."""
        ips = []
        for row in self._W["tree"].get_children():
            vals = self._W["tree"].item(row, "values")
            if vals:
                ips.append(str(vals[0]))
        if not ips:
            return
        try:
            self.clipboard_clear()
            self.clipboard_append("\n".join(ips))
            self.update()
            fa = self._lang == "fa"
            self._log(
                f"{'کپی شد:' if fa else 'Copied:'} {len(ips)} "
                f"{'آی‌پی' if fa else 'IPs'}")
        except Exception:
            pass

    def _open_saved_folder(self):
        """Reveal the most recently saved output folder in the OS file manager.

        Falls back to opening the app directory if no folder has been saved
        yet in this session."""
        folder = getattr(self, "_saved_folder", None) or app_dir()
        if not folder.exists():
            return
        try:
            import subprocess
            if sys.platform == "win32":
                # explorer needs the path as one argument; spaces in country
                # folder names are handled correctly by Popen with a list.
                subprocess.Popen(["explorer", str(folder)])
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(folder)])
            else:
                subprocess.Popen(["xdg-open", str(folder)])
        except Exception as e:
            self._log(f"{'خطا در باز کردن پوشه:' if self._lang == 'fa' else 'Open folder error:'} {e}")

    def _export_dns(self):
        """Export the scanned DNS resolver list to a plain-text file."""
        fa = self._lang == "fa"
        if not self._found_ips:
            messagebox.showinfo(
                "KevinNet DNS",
                "هیچ نتیجه‌ای برای خروجی وجود ندارد." if fa else "No DNS results to export.",
                parent=self)
            return
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(
            parent=self,
            title="ذخیره لیست DNS" if fa else "Export DNS List",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="dns_resolvers.txt")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("# KevinNet DNS — Scanned Resolvers\n")
                f.write(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Total: {len(self._found_ips)}\n\n")
                f.write("\n".join(self._found_ips) + "\n")
            messagebox.showinfo(
                "KevinNet DNS",
                f"{'خروجی ذخیره شد:' if fa else 'Exported successfully:'}\n{path}",
                parent=self)
        except Exception as e:
            messagebox.showerror("KevinNet DNS", str(e), parent=self)

    def _save_vaydns_profile(self):
        """Save a VayDNS profile from the current scan results."""
        if not self._found_ips:
            messagebox.showwarning("", "هیچ Resolver یافت نشد." if self._lang == "fa"
                                   else "No resolvers found.")
            return
        domain  = self._domain_var.get().strip()
        pubkey  = (self._vd_pubkey_var.get() if self._vd_pubkey_var else "").strip().lower()
        country = self._country_var.get().strip()
        fa      = self._lang == "fa"

        ok, err = validate_domain(domain)
        if not ok:
            messagebox.showwarning(
                "", ("دامنه نامعتبر است. " if fa else "Invalid domain. ") + err)
            return
        ok, err = validate_vaydns_pubkey(pubkey)
        if not ok:
            messagebox.showwarning(
                "", ("کلید عمومی VayDNS نامعتبر است. " if fa
                     else "Invalid VayDNS public key. ") + err)
            return
        ok, err = validate_folder_name(country)
        if not ok:
            messagebox.showwarning(
                "", ("نام پوشه نامعتبر است. " if fa else "Invalid folder name. ") + err)
            return

        ts      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        profile = {
            "name":           country,
            "date":           ts,
            "domain":         domain,
            "pubkey":         pubkey,
            "country":        country,
            "resolver_count": len(self._found_ips),
            "resolvers":      list(self._found_ips),
            "options":        dict(VAYDNS_DEFAULTS),
        }
        try:
            script = write_vaydns_launch_script(profile)
            save_new_vaydns_profile(profile)
            self._log(f"{'✓ VayDNS پروفایل ذخیره شد — تب VayDNS Profiles را ببینید' if fa else '✓ VayDNS profile saved — see VayDNS Profiles tab'}")
            messagebox.showinfo(
                "Saved",
                f"{'VayDNS پروفایل ذخیره شد:' if fa else 'VayDNS profile saved to:'}"
                f"\n{script.parent}\n"
                f"\n• {script.name}  (launch script)"
                f"\n• vaydns-client\n\n"
                f"{'برای تغییر تنظیمات به تب VayDNS Profiles بروید' if fa else 'Go to VayDNS Profiles tab to edit options'}.")
        except Exception as e:
            messagebox.showerror("", str(e))

    def _save_configs_silent(self):
        """Auto-save with defaults immediately after scan — no dialog.
        Creates the profile and output files so Launch VPN works straight away."""
        if not self._found_ips:
            return
        domain  = self._domain_var.get().strip()
        key     = self._key_var.get().strip()
        country = self._country_var.get().strip()
        if not domain or not country:
            return
        fa = self._lang == "fa"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        profile = {
            "name":           country,
            "date":           ts,
            "domain":         domain,
            "key":            key,
            "country":        country,
            "resolver_count": len(self._found_ips),
            "resolvers":      list(self._found_ips),
            "options":        dict(PROFILE_DEFAULTS),
        }
        try:
            folder = write_profile_files(profile)
            self._auto_saved_stem = save_new_profile(profile)
            self._saved_folder    = folder
            self._log(
                f"{'✓ ذخیره خودکار با پیش‌فرض — برای تغییر MTU به تب پروفایل‌ها بروید' if fa else '✓ Auto-saved with defaults — go to MasterDNS Profiles tab to edit MTU and options'}")
        except Exception as e:
            self._log(f"{'خطا در ذخیره خودکار:' if fa else 'Auto-save error:'} {e}")

        # ── SAVE ────────────────────────────────────────────────────
    def _launch_vpn(self):
        """Launch MasterDnsVPN from the saved country folder in a terminal."""
        fa     = self._lang == "fa"
        folder = self._saved_folder

        if not folder or not folder.exists():
            messagebox.showwarning("",
                "ابتدا فایل‌ها را ذخیره کنید." if fa
                else "Save the config files first.")
            return

        bin_name = "MasterDnsVPN.exe" if sys.platform == "win32" else "MasterDnsVPN"
        bin_path = folder / bin_name

        if not bin_path.exists():
            no_bin = "فایل اجرایی پیدا نشد:" if fa else "Binary not found:"
            hint   = "مطمئن شوید MasterDnsVPN در کنار برنامه قرار دارد." if fa else "Make sure MasterDnsVPN is placed next to this app."
            messagebox.showerror("", f"{no_bin}\n{bin_path}\n\n{hint}")
            return

        try:
            import subprocess, shlex
            # Quote the folder path so spaces in profile names (e.g. "Turkey 2") work
            folder_q   = shlex.quote(str(folder))
            bin_path_q = shlex.quote(str(bin_path))

            if sys.platform == "win32":
                # Windows Popen with cwd handles spaces natively — no quoting needed
                subprocess.Popen(
                    ["cmd", "/c", "start", "", str(bin_path)],
                    cwd=str(folder)
                )
            elif sys.platform == "darwin":
                # AppleScript: wrap path in single quotes inside the do script string
                script = (
                    'tell application "Terminal"\n'
                    '    activate\n'
                    f'    do script "cd {folder_q} && ./{bin_name}"\n'
                    'end tell'
                )
                subprocess.Popen(["osascript", "-e", script])
            else:
                launched = False
                for term, args in [
                    # gnome-terminal / konsole / xfce4 pass cwd as argument — safe with spaces
                    ("gnome-terminal", ["--working-directory", str(folder), "--", str(bin_path)]),
                    # xterm uses -e with a shell string — must quote
                    ("xterm",          ["-e", f"cd {folder_q} && {bin_path_q}"]),
                    ("konsole",        ["--workdir", str(folder), "-e", str(bin_path)]),
                    ("xfce4-terminal", ["--working-directory", str(folder), "-e", str(bin_path)]),
                    ("x-terminal-emulator", ["-e", str(bin_path)]),
                ]:
                    try:
                        subprocess.Popen([term] + args)
                        launched = True
                        break
                    except FileNotFoundError:
                        continue
                if not launched:
                    subprocess.Popen([str(bin_path)], cwd=str(folder))

            self._log(
                f"{'MasterDNSVPN راه‌اندازی شد از:' if fa else 'MasterDNSVPN launched from:'} {folder}")
            self._W["status_lbl"].config(
                text=f"● {'در حال اتصال…' if fa else 'Connecting…'}", fg=GREEN)

        except Exception as e:
            err = "خطا در راه‌اندازی:" if fa else "Launch error:"
            messagebox.showerror("Error", f"{err}\n{e}")
            self._log(f"Launch error: {e}")

    def _save_configs(self):
        if not self._found_ips:
            messagebox.showwarning(
                "", "هیچ Resolver یافت نشد." if self._lang == "fa"
                    else "No resolvers found.")
            return

        domain  = self._domain_var.get().strip()
        key     = self._key_var.get().strip()
        country = self._country_var.get().strip()
        ts      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fa      = self._lang == "fa"

        profile = {
            "name":           country,
            "date":           ts,
            "domain":         domain,
            "key":            key,
            "country":        country,
            "resolver_count": len(self._found_ips),
            "resolvers":      list(self._found_ips),
            "options":        dict(PROFILE_DEFAULTS),
        }

        # Write all output files via shared helper (uses build_config_from_profile
        # which correctly substitutes ALL option placeholders in the TOML)
        try:
            folder = write_profile_files(profile)
        except Exception as e:
            messagebox.showerror("", str(e))
            return

        # Save or update profile JSON — update auto-saved one if it exists,
        # otherwise create new (prevents duplicate profiles per scan)
        try:
            if self._auto_saved_stem:
                profile["date"] = ts
                update_profile(self._auto_saved_stem, profile)
                self._log(f"{'پروفایل بروزرسانی شد' if fa else 'Profile updated'}")
            else:
                self._auto_saved_stem = save_new_profile(profile)
                self._log(f"{'پروفایل ذخیره شد' if fa else 'Profile saved'}")
        except Exception as e:
            self._log(f"{'خطا در ذخیره پروفایل:' if fa else 'Profile save error:'} {e}")

        self._saved_folder = folder
        self._W["status_lbl"].config(
            text=f"● {'ذخیره شد' if fa else 'Saved'}", fg=ACCENT)
        self._log(f"Saved  →  {folder}")
        messagebox.showinfo(
            "Saved",
            f"{'فایل‌ها ذخیره شدند:' if fa else 'Files saved to:'}"
            f"\n{folder}\n"
            f"\n• client_config.toml"
            f"\n• client_resolvers.txt\n\n"
            f"{'برای تغییر MTU به تب پروفایل‌ها بروید' if fa else 'Go to the Profiles tab to edit MTU and other options'}.")


# ═══════════════════════════════════════════════════════════════
def main():
    App().mainloop()

if __name__ == "__main__":
    main()
