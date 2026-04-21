# 🌐 KevinNet DNS Config

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

1. **Enter your tunnel domain** — e.g. `v.example.com`
2. **Enter your encryption key** — 32-character key from your server
3. **Enter country / folder name** — e.g. `Iran`
4. **Click ▶ Start Scan** — scans ~60,000 Iranian IPs (~10–15 min)
5. **Click 💾 Save Config Files** — writes configs + copies MasterDnsVPN binary
6. **Click 🚀 Connect MasterDNSVPN** — launches VPN in a terminal, ready to connect

The scan runs in 3 automatic phases:
- **Phase 1** — Quick alive check on all IPs
- **Phase 2** — Full 6-check scoring (NS→A, TXT, RND, DPI, EDNS, NXD)
- **Phase 3** — Real tunnel E2E verification via MasterDnsVPN binary

Only resolvers that pass the actual tunnel test appear in your config.

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

> **Cloudflare users:** Go to DNS settings and click the orange cloud icon next to the A record so it turns **grey (DNS only)**. It must NOT be proxied.

#### Step 1.1.2 — Create an NS Record

| Field | Value |
|---|---|
| Type | `NS` |
| Name | `v` (your tunnel subdomain) |
| Value | `ns.example.com` |

Example: `v.example.com → ns.example.com`

> **Cloudflare users:** Add the NS record normally. Cloudflare does not proxy NS records, but make sure the `ns` A record is already set to DNS only.

#### 1.1.3 💡 MTU Note

Shorter domain names leave more room for data inside each DNS request.
Keep names short (1–3 characters) for better throughput.
If using Cloudflare, keep all relevant records in **DNS only** mode.

---

### 1.2 🐧 Linux Server Installation

#### Step 1.2.1 — Automatic Installation

Run this single command on your Linux server:

```bash
bash <(curl -Ls https://raw.githubusercontent.com/masterking32/MasterDnsVPN/main/server_linux_install.sh)
```

The script handles everything automatically. When it finishes:
- The server starts
- Your **encryption key** is shown in the terminal log
- The key is also saved to `encrypt_key.txt` next to the executable

> ⚠️ **Save your encryption key** — clients need it to connect.

#### Step 1.2.2 — Important Notes After Installation

**Domain:** During installation you will be asked for a domain. Use the exact subdomain you set up in the NS record, e.g. `v.example.com`.

**DNS propagation:** After creating DNS records, wait for them to propagate. This can take a few minutes to 48 hours depending on your DNS provider and TTL.

**Verify DNS setup:**
```bash
dig v.example.com NS
dig @ns.example.com v.example.com A
```

**Open firewall port 53 (UDP):**

For `ufw`:
```bash
sudo ufw allow 53/udp
sudo ufw reload
```

For `firewalld`:
```bash
sudo firewall-cmd --add-port=53/udp --permanent
sudo firewall-cmd --reload
```

**Port 53 already in use?**

If `systemd-resolved` is using port 53:
```bash
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved
sudo systemctl restart MasterDnsVPN
```

---

## 🛠️ Build From Source

See [**BUILD_INSTRUCTIONS.txt**](BUILD_INSTRUCTIONS.txt) (English) or [**BUILD_INSTRUCTIONS_FA.txt**](BUILD_INSTRUCTIONS_FA.txt) (فارسی) for full step-by-step instructions.

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

This tool is a companion to **MasterDnsVPN**, developed by **MasterkinG32 (Amin Mahmoudi)**.

- GitHub: [https://github.com/masterking32/MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)
- All credit for the VPN client goes to MasterkinG32 and contributors.
- MasterDnsVPN is used under the **MIT License** (see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)).

Download the latest MasterDnsVPN client:

| Platform | Link |
|---|---|
| Windows AMD64 | [MasterDnsVPN_Client_Windows_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Windows_AMD64.zip) |
| Windows ARM64 | [MasterDnsVPN_Client_Windows_ARM64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Windows_ARM64.zip) |
| macOS AMD64 | [MasterDnsVPN_Client_MacOS_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_MacOS_AMD64.zip) |

---

## 💰 Optional Financial Support

If this tool has been useful to you, you can support the development:

- **Website:** [kevinhaji.com](https://kevinhaji.com)
- **Email:** [kevin.fullstack.dev@gmail.com](mailto:kevin.fullstack.dev@gmail.com)

Your support helps maintain and improve this project. Thank you! 🙏

---

## ⚖️ License

Copyright © 2026 Kevin Haji. See [LICENSE](LICENSE) for details.

This project is released under the **MIT License**.

---

## ⚠️ Disclaimer

See [DISCLAIMER.md](DISCLAIMER.md) for the full disclaimer.

MasterDnsVPN is provided as an educational and research project only.
The developers accept no responsibility for misuse or violations of local laws.
