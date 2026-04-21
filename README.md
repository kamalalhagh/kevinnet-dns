<div align="right">

[🇮🇷 فارسی](README_FA.md) | 🇬🇧 English

</div>

# 🌐 KevinNet DNS

**Companion tool for [MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)**

> Automatically scans Iranian IP ranges to find DNS resolvers that bypass Iran's DPI filtering, then generates ready-to-use config files for MasterDnsVPN — with a single click to connect.

**Created by Kevin Haji · [kevinhaji.com](https://kevinhaji.com) · [kevin.fullstack.dev@gmail.com](mailto:kevin.fullstack.dev@gmail.com)**

---

## 📥 Download (No installation needed)

Download the latest compiled binary for your platform from the [**Releases page**](../../releases/latest):

| Platform | File |
|---|---|
| 🪟 Windows x64 | `KevinNet_Windows_x64.exe` |
| 🪟 Windows ARM64 | `KevinNet_Windows_ARM64.exe` |
| 🍎 macOS (Intel + Apple Silicon) | `KevinNet_macOS_Universal` |
| 🐧 Linux x64 | `KevinNet_Linux_x64` |
| 🐧 Linux ARM64 | `KevinNet_Linux_ARM64` |

> **macOS:** After downloading, right-click → Open → Open to bypass Gatekeeper.
> **Linux:** Run `chmod +x KevinNet_Linux_x64` before launching.

---

## 🚀 How to Use

### Step 1 — Fill in the settings

| Field | What to enter | Example |
|---|---|---|
| Tunnel Domain | The subdomain pointing to your server | `v.example.com` |
| Encryption Key | 32-character key from your server | `4c8da843709463cab27f...` |
| Country / Folder | Name for the output folder | `Iran` |

### Step 2 — Choose scan settings (recommended for Iran)

| Setting | Recommended for Iran | Notes |
|---|---|---|
| **Target** | `100` | Number of resolvers to find. More = more reliable VPN |
| **Concurrency** | `80–100` | Iran has OS socket limits — don't go above 150 |
| **Timeout** | `2–3s` | 3s is safer on congested Iranian networks |
| **Pool ×1000** | `200` | 200,000 IPs scanned. More = more resolvers found |

> **Tip:** If you find very few resolvers, increase **Pool** to `300` or `500`.
> Do NOT increase Concurrency — it causes silent failures on macOS/Iran connections.
> Run the scan 2–3 times and each run finds different resolvers.

### Step 3 — Start the scan

Click **▶ Start Scan**. The scan runs in 3 automatic phases:

- **Phase 1** — Quick alive check on all IPs in the pool (~5–10 min for 200k)
- **Phase 2** — Full 6-check scoring: NS→A, TXT, RND, DPI, EDNS, NXD (all shown)
- **Phase 3** — Real E2E tunnel test via MasterDnsVPN binary (final filter)

Result colours:
- 🟢 **★ 6/6** — Perfect, passes all checks
- 🟡 **◆ 4–5/6** — Good, likely works
- 🟠 **▸ 2–3/6** — Weak, might work
- ⚫ **· 0–1/6** — Very weak

### Step 4 — Save and Connect

Click **💾 Save Config Files** — creates a folder (e.g. `Iran/`) next to the app with:
- `client_config.toml`
- `client_resolvers.txt`
- `MasterDnsVPN` (or `.exe` on Windows)

Click **🚀 Connect MasterDNSVPN** — opens a terminal and launches the VPN.

---

## ⚠️ MasterDnsVPN binary not in the folder?

If after saving you don't see `MasterDnsVPN` inside the country folder, follow these steps:

### Download MasterDnsVPN manually

| Platform | Download |
|---|---|
| Windows AMD64 | [MasterDnsVPN_Client_Windows_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Windows_AMD64.zip) |
| Windows ARM64 | [MasterDnsVPN_Client_Windows_ARM64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Windows_ARM64.zip) |
| macOS AMD64 | [MasterDnsVPN_Client_MacOS_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_MacOS_AMD64.zip) |

### Place it correctly

1. Extract the downloaded ZIP
2. Find the binary inside (it may be called `MasterDnsVPN_Client` or similar)
3. Rename it to exactly `MasterDnsVPN` (macOS/Linux) or `MasterDnsVPN.exe` (Windows)
4. Place it in **the same folder as the KevinNet app**
5. Run KevinNet again and click **Save Config Files** — it will copy it automatically

**macOS only** — make it executable:
```bash
chmod +x /path/to/MasterDnsVPN
```

After placing it correctly, the next Save will copy it into every country folder automatically.

---

## 🖥️ Section 1 — Server Setup

### 1.1 🌐 Domain Setup (Prerequisite)

To receive DNS requests on your server, you must delegate a subdomain to it.
Create **two DNS records** in your domain provider's control panel:

#### Step 1.1.1 — Create an A Record

| Field | Value |
|---|---|
| Type | `A` |
| Name | `ns` (or any short name) |
| Value | Your server's IPv4 address |

Example: `ns.example.com → 1.2.3.4`

> **Cloudflare users:** Click the orange cloud icon next to the A record so it turns **grey (DNS only)**. It must NOT be proxied.

#### Step 1.1.2 — Create an NS Record

| Field | Value |
|---|---|
| Type | `NS` |
| Name | `v` (your tunnel subdomain) |
| Value | `ns.example.com` |

Example: `v.example.com → ns.example.com`

> **Cloudflare users:** Add the NS record normally. Make sure the `ns` A record is already set to DNS only.

#### 1.1.3 💡 MTU Note

Shorter domain names leave more room for data inside each DNS packet.
Keep names short (1–3 characters) for better throughput.

---

### 1.2 🐧 Linux Server Installation

#### Step 1.2.1 — Automatic Installation

```bash
bash <(curl -Ls https://raw.githubusercontent.com/masterking32/MasterDnsVPN/main/server_linux_install.sh)
```

When finished:
- The server starts automatically
- Your **encryption key** is shown in the terminal
- The key is saved to `encrypt_key.txt` next to the binary

> ⚠️ **Copy and save your encryption key** — clients need it to connect.

#### Step 1.2.2 — Important Notes

**Domain:** Enter the exact subdomain from your NS record (e.g. `v.example.com`).

**DNS propagation:** Wait up to 48 hours after creating DNS records.

**Verify DNS:**
```bash
dig v.example.com NS
dig @ns.example.com v.example.com A
```

**Open firewall port 53 (UDP):**
```bash
# ufw
sudo ufw allow 53/udp && sudo ufw reload

# firewalld
sudo firewall-cmd --add-port=53/udp --permanent && sudo firewall-cmd --reload
```

**Port 53 already in use by systemd-resolved:**
```bash
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved
sudo systemctl restart MasterDnsVPN
```

---

## 🛠️ Build From Source

See [**BUILD_INSTRUCTIONS.txt**](BUILD_INSTRUCTIONS.txt) (English) or [**BUILD_INSTRUCTIONS_FA.txt**](BUILD_INSTRUCTIONS_FA.txt) (فارسی).

### Quick start — macOS
```bash
brew install python@3.12 python-tk@3.12
/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv venv
source venv/bin/activate
pip install dnspython pyinstaller pillow
chmod +x build_mac_universal.sh
./build_mac_universal.sh
```

### Quick start — Windows
```bat
python -m venv venv
venv\Scripts\activate
pip install dnspython pyinstaller pillow
build_windows.bat
```

---

## 🙏 Credits & Acknowledgements

This tool is a companion to **MasterDnsVPN** by **MasterkinG32 (Amin Mahmoudi)**.

- GitHub: [https://github.com/masterking32/MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)
- MasterDnsVPN is used under the **MIT License** — see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)

---

## 💰 Optional Financial Support

- **Website:** [kevinhaji.com](https://kevinhaji.com)
- **Email:** [kevin.fullstack.dev@gmail.com](mailto:kevin.fullstack.dev@gmail.com)

---

## ⚖️ License

Copyright © 2026 Kevin Haji — [MIT License](LICENSE)

## ⚠️ Disclaimer

See [DISCLAIMER.md](DISCLAIMER.md). MasterDnsVPN is provided for educational and research purposes only.
