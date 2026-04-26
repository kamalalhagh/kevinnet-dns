<div align="right">

[🇮🇷 فارسی](README_FA.md) | 🇬🇧 English

</div>

# 🌐 KevinNet DNS

**Companion tool for [MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)**

> Automatically scans Iranian IP ranges to find DNS resolvers that bypass Iran's DPI filtering, then generates ready-to-use config files for MasterDnsVPN — with a single click to connect.

**Created by Kevin Haji · [kevinhaji.com](https://kevinhaji.com) · [kevin.fullstack.dev@gmail.com](mailto:kevin.fullstack.dev@gmail.com)**

---

## 📥 Download (No installation needed)

Download the latest stable release for your platform from the [**Releases page**](../../releases/latest):

| Platform | File |
|---|---|
| 🪟 Windows x64 | `KevinNet_Windows_x64.exe` |
| 🪟 Windows ARM64 | `KevinNet_Windows_ARM64.exe` |
| 🍎 macOS (Intel + Apple Silicon) | `KevinNet_macOS_Universal` |
| 🐧 Linux x64 | `KevinNet_Linux_x64` |
| 🐧 Linux ARM64 | `KevinNet_Linux_ARM64` |

> **Looking for the beta with the new Profiles tab?** Check the [**Releases page**](../../releases) and download the latest `v2.x.x-beta` release.

> **macOS:** After downloading:
> ```bash
> chmod +x KevinNet_macOS_Universal
> xattr -d com.apple.quarantine KevinNet_macOS_Universal
> ```
> Or right-click → Open → Open to bypass Gatekeeper without the terminal.
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
> Do NOT increase Concurrency above 100 — it causes silent failures on macOS and Iranian connections.
> Run the scan 2–3 times — each run tests a fresh random set of IPs.

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

The profile is also saved to the **Profiles tab** automatically — see below.

Click **🚀 Connect MasterDNSVPN** — opens a terminal and launches the VPN.

---

## 📋 Profiles Tab — Edit Options & Manage Saved Scans

Every time you save after a scan, a **profile** is automatically created and stored in `profiles/` next to the app. You can open any saved profile later — without scanning again — and adjust settings, then save and launch.

### How to use the Profiles tab

1. Click the **📋 Profiles** tab at the top of the app
2. Select a profile from the left list (shows name, date, and resolver count)
3. Edit the name or any of the key options on the right
4. Click **💾 Save Changes** — rewrites `client_config.toml` in the country folder instantly
5. Click **🚀 Launch VPN** — launches directly from the profile
6. Click **🗑 Delete** — removes the profile (and optionally the output folder)

### 🔧 Key Options — What they mean and optimal values for Iran

These options are inside every profile and directly affect how MasterDnsVPN performs under Iran's heavy DPI filtering.

---

#### Listen Port
**Default:** `18000`
**Iran optimal:** `18000` (leave as-is unless another app uses this port)

The local port your browser or app connects to. For example, in your browser proxy settings you'd set SOCKS5 `127.0.0.1:18000`. Only change this if something else on your machine is already using port 18000.

---

#### Encryption Method
**Options:** `0 — None`, `1 — XOR`, `2 — ChaCha20`, `3 — AES-128-GCM`, `4 — AES-192-GCM`, `5 — AES-256-GCM`
**Default:** `1 — XOR`
**Iran optimal:** `1 — XOR`

Encrypts the payload inside each DNS packet. XOR is the best choice for Iran because:
- It adds minimal overhead inside already-small DNS packets
- ChaCha20 or AES are stronger but add bytes that reduce the usable MTU
- The tunnel domain+key already provides a layer of security
- Switch to `2 — ChaCha20` only if you need stronger encryption and accept slightly lower throughput

> **Must match your server's `DATA_ENCRYPTION_METHOD` setting exactly.**

---

#### Balancing Strategy
**Options:** `1 — Random`, `2 — Round Robin`, `3 — Least Loss`, `4 — Lowest Latency`
**Default:** `2 — Round Robin`
**Iran optimal:** `3 — Least Loss`

Controls how the client picks which resolver to send each packet through.

- **Random** — simplest, no feedback
- **Round Robin** — cycles through all resolvers evenly
- **Least Loss** — favours resolvers with the fewest dropped packets — **best for Iran** because Iranian networks have high and uneven packet loss
- **Lowest Latency** — favours the fastest resolver — good if your resolvers are very consistent

---

#### Packet Duplication
**Range:** `1–8`
**Default:** `2`
**Iran optimal:** `2–3`

Sends each packet to this many resolvers simultaneously. If one path drops the packet, another copy arrives via a different resolver. In Iran's lossy network environment, `2` is a solid baseline. Set to `3` if you experience frequent disconnections. Do not go above `4` — it wastes bandwidth without benefit when you already have many resolvers.

---

#### Min Upload MTU
**Range:** `10–500`
**Default:** `38`
**Iran optimal:** `38`

The minimum upload payload size (in bytes) accepted after MTU discovery. Resolvers that can only handle smaller packets than this are rejected. `38` is very conservative — almost no resolver gets filtered out on this. Leave it at `38` for Iran to maximise the number of usable resolvers.

---

#### Max Upload MTU
**Range:** `10–500`
**Default:** `150`
**Iran optimal:** `80–100`

The upper bound for upload MTU discovery. MasterDnsVPN probes each resolver to find the largest packet it accepts. In Iran, DNS traffic is heavily inspected — large DNS queries look suspicious and get dropped more often. Keeping this at `80–100` means the client uses smaller, less conspicuous packets that are less likely to trigger DPI.

---

#### Min Download MTU
**Range:** `100–2000`
**Default:** `500`
**Iran optimal:** `400`

Minimum download payload size. Resolvers that return very small DNS responses are rejected. Lowering to `400` keeps more resolvers in the pool — useful in Iran where many resolvers work but respond conservatively.

---

#### Max Download MTU
**Range:** `100–2000`
**Default:** `900`
**Iran optimal:** `700`

Upper bound for download MTU discovery. Large DNS responses (800–900 bytes) are more likely to be fragmented by Iranian ISPs or trigger DPI. Setting this to `700` keeps download packets in a safer zone where they are less likely to be blocked mid-transfer.

---

#### Log Level
**Options:** `DEBUG`, `INFO`, `WARN`, `ERROR`
**Default:** `INFO`
**Iran optimal:** `INFO`

Controls how much MasterDnsVPN prints to its terminal. `INFO` shows connection events, resolver switches, and errors — enough to know what's happening without flooding the terminal. Use `DEBUG` only when troubleshooting a specific problem; it prints every packet event and will be very noisy.

---

### 📊 Quick reference — Iran-optimised profile

| Option | Iran optimal | Reason |
|---|---|---|
| Listen Port | `18000` | Default — no conflict typically |
| Encryption Method | `1 — XOR` | Lowest overhead inside DNS |
| Balancing Strategy | `3 — Least Loss` | Iran has high uneven packet loss |
| Packet Duplication | `2–3` | Redundancy on lossy paths |
| Min Upload MTU | `38` | Keep maximum resolver pool |
| Max Upload MTU | `80–100` | Smaller queries avoid DPI |
| Min Download MTU | `400` | Keep marginal resolvers |
| Max Download MTU | `700` | Avoid ISP fragmentation |
| Log Level | `INFO` | Normal operation |

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
