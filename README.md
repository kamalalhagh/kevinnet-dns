<div align="right">

[🇮🇷 فارسی](README_FA.md) | 🇬🇧 English

</div>

# 🌐 KevinNet DNS

**A user-friendly GUI client for DNS tunneling — supports MasterDnsVPN and VayDNS**

> KevinNet automatically scans Iranian IP ranges to find working DNS resolvers, then generates ready-to-use config files and launch scripts for your VPN — with a single click to connect. No config files to edit. No terminal commands to remember.

**Created by Kevin Haji · [kevinhaji.com](https://kevinhaji.com) · [kevin.fullstack.dev@gmail.com](mailto:kevin.fullstack.dev@gmail.com)**

---

## 💡 What is this?

A DNS tunnel disguises your internet traffic as ordinary DNS queries. Iranian DPI filtering cannot easily identify or block it. KevinNet handles all the technical parts — finding working resolvers, writing config files, launching the VPN — so you only need to click a few buttons.

**Supported VPN engines:**
- **MasterDNS** ([MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)) — DNS tunnel with multiple simultaneous resolvers. Excellent stability for Iran.
- **VayDNS** ([VayDNS](https://github.com/net2share/vaydns)) — DNS tunnel with DoH/DoT/UDP transport and Noise protocol end-to-end encryption.

---

## 📥 Download

Download the latest release for your platform from the [**Releases page**](../../releases/latest):

| Platform | File |
|---|---|
| 🪟 Windows x64 | `KevinNet_Windows_x64.exe` |
| 🍎 macOS (Intel + Apple Silicon) | `KevinNet_macOS_Universal` |
| 🐧 Linux x64 | `KevinNet_Linux_x64` |
| 🐧 Linux ARM64 | `KevinNet_Linux_ARM64` |

> **macOS:** After downloading, run in Terminal:
> ```bash
> chmod +x KevinNet_macOS_Universal
> xattr -d com.apple.quarantine KevinNet_macOS_Universal
> ```
> Or right-click → Open → Open.

> **Linux:** Run `chmod +x KevinNet_Linux_x64` before launching.

---

## 🔧 Prerequisites

You need a **VPS server outside Iran** with the VPN server software installed. Have these ready before opening KevinNet:

| | MasterDNS | VayDNS |
|---|---|---|
| Tunnel domain | `v.example.com` | `v.example.com` |
| Key | 32-char encryption key (from `encrypt_key.txt`) | 64-char hex public key (from `server.pub`) |

See the [Server Setup](#-server-setup) section below for installation instructions.

---

## 🚀 How to Use — Step by Step

### Step 1 — Choose VPN type

Click **MasterDNS** or **VayDNS** at the top of the Scanner panel. Only the fields and save button for your chosen type will be shown.

### Step 2 — Fill in your details

| Field | What to enter |
|---|---|
| **Country / Folder** | A name for this config — e.g. `Iran` or `Turkey` |
| **Tunnel Domain** | The subdomain pointing to your server — e.g. `v.example.com` |
| **Key** | Your 32-char (MasterDNS) or 64-char hex (VayDNS) key from the server |

### Step 3 — Set scan options

| Option | Recommended for Iran | Notes |
|---|---|---|
| **Target** | `100` | Resolvers to find. More = more stable VPN |
| **Concurrency** | `80` | Do not go above 100 inside Iran |
| **Timeout** | `3s` | Iranian networks are slow |
| **Pool ×1000** | `200` | 200,000 IPs scanned. More = more resolvers |

> Finding very few resolvers? Increase Pool to `300` or `500` and scan again.
> Run the scan 2–3 times — each run tests different random IPs.

### Step 4 — Start the scan

Click **▶ Start Scan**. Three automatic phases run:

- **Phase 1** — Quick alive check across all IPs in the pool
- **Phase 2** — Full 6-check scoring: NS→A, TXT, RND, DPI, EDNS, NXD
- **Phase 3** — Real E2E tunnel test through the VPN binary

Result colours: 🟢 ★6/6 excellent · 🟡 ◆4–5 good · 🟠 ▸2–3 weak · ⚫ ·0–1 very weak

### Step 5 — Save to Profiles

- **MasterDNS:** click **💾 Save to MasterDNS Profiles**
- **VayDNS:** click **💾 Save to VayDNS Profiles**

The profile is saved with sensible defaults. The VPN binary is copied into the output folder automatically (if it is next to the KevinNet app).

### Step 6 — Connect from the Profiles tab

Click the **📋 MasterDNS Profiles** or **📋 VayDNS Profiles** tab at the top.

1. Select your saved profile from the left list
2. Optionally edit settings (MTU, timeouts, etc.) and click **💾 Save Changes**
3. Click **🚀 Launch VPN** — a terminal opens and the VPN starts

---

## 📋 Profiles Tab — Managing Saved Configurations

Every save creates a profile stored in `masterdns_profiles/` or `vaydns_profiles/` next to the app. You can revisit any profile without scanning again.

| Button | What it does |
|---|---|
| 💾 Save Changes | Rewrites config files / launch script with current options |
| 🚀 Launch VPN | Regenerates files and launches the VPN |
| 📋 Duplicate | Copies the profile and its folder — great for A/B testing settings |
| 🗑 Delete | Removes the profile (and optionally the output folder) |

---

## 🔧 MasterDNS Key Options — What They Mean & Iran Optimal Values

These are edited in the MasterDNS Profiles tab.

| Option | Iran optimal | Why |
|---|---|---|
| **Encryption Method** | `1 — XOR` | Lowest overhead inside small DNS packets |
| **Balancing Strategy** | `3 — Least Loss` | Iran has high and uneven packet loss |
| **Packet Duplication** | `2–3` | Redundancy on lossy paths |
| **Max Upload MTU** | `80–100` | Smaller queries are less likely to trigger DPI |
| **Max Download MTU** | `700` | Prevents ISP fragmentation |
| **Min Upload MTU** | `38` | Keeps the maximum number of resolvers usable |
| **Min Download MTU** | `400` | Keeps marginal resolvers in the pool |
| **Log Level** | `INFO` | Normal operation |

---

## 🔧 VayDNS Key Options — What They Mean & Iran Optimal Values

These are edited in the VayDNS Profiles tab.

| Option | Iran optimal | Why |
|---|---|---|
| **Transport** | `UDP` | Most direct path from Iran |
| **Resolver** | *(empty)* | Tries all scanned resolvers in order |
| **Listen Port** | `7000` | Local port for your browser/app |
| **Max QNAME Length** | `101` | Safe for most resolvers (~50 byte MTU) |
| **Idle Timeout** | `10s` | Increase to `30s` if you see frequent reconnects |
| **Keepalive** | `2s` | Must be less than idle timeout |
| **Record Type** | `txt` | Most compatible under DPI filtering |
| **Queue Size** | `512` | Increase to `1024` on fast connections |
| **UDP Workers** | `100` | Lower to `50` if you see socket errors |
| **Resolver Timeout** | `60s` | Moves to next resolver if stuck for this long |
| **Log Level** | `info` | Normal operation |

**Resolver field explained:**
- **Empty** — KevinNet generates a launch script that tries all scanned resolvers in order. If one is stuck for longer than `Resolver Timeout` seconds, it automatically moves to the next one.
- **Single IP/URL** — only that resolver is used (e.g. `8.8.8.8:53` for UDP, `https://dns.google/dns-query` for DoH).

> **Important:** The scanned resolvers are Iranian public DNS servers. They only work correctly when connecting **from inside Iran**. Testing from Australia, Europe, or other countries will show NXDOMAIN responses because those resolvers can't reach your tunnel server from outside Iran.

---

## ⚠️ VPN binary missing from folder?

If after saving you don't see `MasterDnsVPN` or `vaydns-client` inside the country folder:

1. Download the binary for your platform (see links below)
2. Rename it to exactly `MasterDnsVPN` or the correct `vaydns-client-*` name
3. **Place it next to the KevinNet app** (not inside the country folder)
4. Click Save again — it copies automatically

**MasterDnsVPN downloads:**
| Platform | Link |
|---|---|
| Windows AMD64 | [MasterDnsVPN_Client_Windows_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Windows_AMD64.zip) |
| macOS AMD64 | [MasterDnsVPN_Client_MacOS_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_MacOS_AMD64.zip) |

**VayDNS binary names** (place next to KevinNet app):
| Platform | File name |
|---|---|
| macOS Apple Silicon | `vaydns-client-darwin-arm64` |
| macOS Intel | `vaydns-client-darwin-amd64` |
| Linux x64 | `vaydns-client-linux-amd64` |
| Linux ARM64 | `vaydns-client-linux-arm64` |
| Windows x64 | `vaydns-client_windows_amd64.exe` |

---

## 🖥️ Server Setup

### MasterDNS Server

See the full guide at [MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN).

**Quick DNS setup** — create two records in your domain provider:

| Type | Name | Value |
|---|---|---|
| `A` | `ns` | Your server IPv4 address |
| `NS` | `v` | `ns.example.com` |

> Cloudflare users: the `A` record must be **DNS only** (grey cloud), not proxied.

**Install on Linux:**
```bash
bash <(curl -Ls https://raw.githubusercontent.com/masterking32/MasterDnsVPN/main/server_linux_install.sh)
```

Your encryption key is shown at the end and saved to `encrypt_key.txt`.

**Open firewall port 53 (UDP):**
```bash
sudo ufw allow 53/udp && sudo ufw reload
```

If port 53 is in use by `systemd-resolved`:
```bash
sudo systemctl stop systemd-resolved && sudo systemctl disable systemd-resolved
sudo systemctl restart MasterDnsVPN
```

---

### VayDNS Server

See the full guide at [VayDNS](https://github.com/net2share/vaydns).

**Quick DNS setup** — same as MasterDNS: one `A` record for the glue, one `NS` record for the tunnel subdomain.

**Build and generate keys:**
```bash
go build -o vaydns-server ./vaydns-server
./vaydns-server -gen-key -privkey-file server.key -pubkey-file server.pub
```

Copy `server.pub` to your client machine. The hex string inside it is your VayDNS public key.

**Run the server:**
```bash
./vaydns-server -udp :53 -privkey-file server.key \
  -domain t.example.com -upstream 127.0.0.1:8000
```

You need something for the server to forward to. For SOCKS5 via SSH:
```bash
ssh -N -D 127.0.0.1:8000 -o NoHostAuthenticationForLocalhost=yes 127.0.0.1
```

**Redirect port 53 (run as non-root):**
```bash
sudo iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300
./vaydns-server -udp :5300 -privkey-file server.key -domain t.example.com -upstream 127.0.0.1:8000
```

---

## 🛠️ Build From Source

See [BUILD_INSTRUCTIONS.txt](BUILD_INSTRUCTIONS.txt) or [BUILD_INSTRUCTIONS_FA.txt](BUILD_INSTRUCTIONS_FA.txt).

**macOS quick start:**
```bash
brew install python@3.12 python-tk@3.12
/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv venv
source venv/bin/activate
pip install dnspython pyinstaller pillow
./build_mac_universal.sh
```

---

## 🙏 Credits & Acknowledgements

KevinNet would not exist without these excellent projects:

**MasterDnsVPN** by MasterkinG32 (Amin Mahmoudi)
- GitHub: [https://github.com/masterking32/MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)
- Used under the MIT License

**VayDNS** by net2share
- GitHub: [https://github.com/net2share/vaydns](https://github.com/net2share/vaydns)
- A fork of dnstt by David Fifield (public domain)

See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) for full license texts.

---

## ⭐ Support This Project

The best way to support KevinNet is to help it reach people who need it:

- **Star this repository** on GitHub — it helps others discover the tool
- **Share it** with anyone in Iran who needs a reliable internet connection
- **Report bugs** and suggest improvements via GitHub Issues
- **Spread the word** in communities that could benefit from it

Every star and share helps this tool reach one more family that needs it.

---

## ⚖️ License & Disclaimer

Copyright © 2026 Kevin Haji — [MIT License](LICENSE)

See [DISCLAIMER.md](DISCLAIMER.md). This tool is provided for educational and research purposes. Use responsibly and in accordance with the laws of your jurisdiction.
