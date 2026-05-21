<div align="right">

[🇮🇷 فارسی](README_FA.md) | 🇬🇧 English

</div>

# 🌐 KevinNet DNS

**A user-friendly GUI client for DNS tunneling  supports MasterDnsVPN and VayDNS**

> KevinNet automatically scans Iranian IP ranges to find working DNS resolvers, then generates ready-to-use config files and launch scripts  with a single click to connect. No config files to edit. No terminal commands to remember.

**Created by Kevin Haji · [kevinhaji.com](https://kevinhaji.com) · [kevin.fullstack.dev@gmail.com](mailto:kevin.fullstack.dev@gmail.com)**

---

## What is KevinNet?

A DNS tunnel disguises your internet traffic as ordinary DNS queries. Iran's DPI filtering cannot easily identify or block it. KevinNet handles all the technical parts  scanning for working resolvers, writing config files, copying binaries, launching the VPN  so you only need to fill in a few fields and click buttons.

Two VPN engines are supported:

- **MasterDNS**  uses multiple resolvers simultaneously for high reliability. Best choice for Iran.
- **VayDNS**  uses Noise protocol encryption with DoH, DoT, or UDP transport. Falls through resolvers automatically.

---

## What's New in 3.3.0

- 🔒  **DoH / DoT scanning** - new button scans a curated list of well-known DNS-over-HTTPS (port 443) and DNS-over-TLS (port 853) endpoints. Because the traffic is TLS, it's much harder for Iranian DPI to fingerprint as tunnel traffic than plain UDP/53.
- 🖱  **Right-click context menu** on the resolver list - Copy IP, Copy all IPs, Open output folder.
- ⏱  **Last-launched indicator** on each profile (`launched 5m ago`, `launched 3h ago`). Easy to spot which profile is currently active.
- 💾  **Remembers your last inputs** - domain, country folder, and VPN mode are restored on next launch.
- ✅  **Input validation** with clear error messages - no more confusing "parse TOML failed" errors when a paste contained a stray character.
- 🔐  **Security hardening** - profile files are created with restrictive permissions on Linux/macOS so other users can't read your encryption keys.
- 🧪  **Test suite** with 87 tests runs in CI before every release build.
- 📜  **SHA-256 checksums** published alongside every release so you can verify downloads.

See [CHANGELOG.md](CHANGELOG.md) for the full list.

---

## 📥 Download KevinNet

Download the latest release from the [**Releases page**](../../releases/latest):

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

> **Linux:** Run `chmod +x KevinNet_Linux_x64` before launching.

### Verifying your download (optional but recommended)

Every release ships with a `SHA256SUMS.txt` file alongside the binaries. To verify the file you downloaded hasn't been tampered with:

```bash
shasum -a 256 -c SHA256SUMS.txt     # macOS / Linux
```
```powershell
Get-FileHash -Algorithm SHA256 KevinNet_Windows_x64.exe  # Windows
```

Compare the output against the line for your platform in `SHA256SUMS.txt`. If they don't match, do not run the file - re-download from the official Releases page.

---

## 🔧 What You Need Before Starting

KevinNet is the **client app**. It connects to a VPN server that you (or someone you know) must set up on a VPS outside Iran.

---

### If you are using MasterDNS

#### 1  A VPS server outside Iran

Any Linux VPS with a public IP address. Popular providers: Hetzner, DigitalOcean, Vultr, Linode.

#### 2  A domain name with NS delegation

MasterDNS acts as an authoritative DNS server, so DNS queries for your tunnel subdomain must be forwarded to your VPS. Create **two DNS records** in your domain provider's control panel:

| Type | Name | Value | Purpose |
|---|---|---|---|
| `A` | `ns` | Your server's IP | Glue record  where your nameserver lives |
| `NS` | `v` | `ns.yourdomain.com` | Delegates `v.yourdomain.com` queries to your server |

Example with domain `example.com` and server IP `1.2.3.4`:
- `ns.example.com` → `1.2.3.4` (A record)
- `v.example.com` → `ns.example.com` (NS record)

Your tunnel domain is `v.example.com`.

> **Cloudflare users:** The `A` record for `ns` must be **DNS only** (grey cloud), not proxied.
> **Tip:** Short names (1–2 chars) leave more room for data per DNS packet → better speed.

#### 3  MasterDnsVPN server installed

Follow the official guide: 👉 [https://github.com/masterking32/MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)

After setup you will have:
- **Tunnel Domain**  e.g. `v.example.com` → enter this in KevinNet
- **32-character Encryption Key**  saved in `encrypt_key.txt` on the server → enter this in KevinNet

> The key must match between client and server. If you lose it, run `cat encrypt_key.txt` on your server.

#### 4  The MasterDnsVPN client binary

Bundled inside KevinNet  copied to your output folder automatically when you save. If missing, see [⚠️ Binary missing?](#-binary-missing) below.

---

### If you are using VayDNS

#### 1  A VPS server outside Iran

Same as MasterDNS  any Linux VPS with a public IP.

#### 2  A domain name with NS delegation

VayDNS also acts as an authoritative DNS server. The DNS setup concept is identical to MasterDNS: one `A` glue record + one `NS` delegation record.

Example with domain `example.com` and server IP `1.2.3.4`:
- `tns.example.com` → `1.2.3.4` (A record  glue)
- `t.example.com` → `tns.example.com` (NS record  delegation)

Your tunnel domain is `t.example.com`.

> **Important:** The glue record name (`tns`) must NOT be a subdomain of the tunnel name (`t`). They must be separate  e.g. `tns` and `t`, not `ns.t`.

#### 3  VayDNS server installed

Follow the official guide: 👉 [https://github.com/net2share/vaydns](https://github.com/net2share/vaydns)

After setup you will have:
- **Tunnel Domain**  e.g. `t.example.com` → enter this in KevinNet
- **`server.pub` file** on the server  contains your public key

#### 4  Your VayDNS Public Key (64-character hex string)

The public key authenticates your server  it proves to the client that it is talking to the right server and not an interceptor. To get it, run on your server:

```bash
cat server.pub
```

You will see a 64-character hex string like:
```
0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b
```

Copy this entire string and paste it into the **VayDNS Public Key** field in KevinNet.

> The public key is safe to share  it only verifies your server's identity. The private key (`server.key`) must stay on the server and never be shared.

#### 5  The vaydns-client binary

Bundled inside KevinNet  copied to your output folder automatically when you save. If missing, see [⚠️ Binary missing?](#-binary-missing) below.

---

## 🚀 How to Use  Step by Step

### Step 1  Choose VPN type

At the top of the Scanner panel, click **MasterDNS** or **VayDNS**. Only the fields and save button for your chosen type will show.

### Step 2  Fill in your details

| Field | MasterDNS | VayDNS |
|---|---|---|
| **Country / Folder** | Any name  e.g. `Iran` | Any name  e.g. `Iran` |
| **Tunnel Domain** | e.g. `v.example.com` | e.g. `t.example.com` |
| **Key** | 32-char key from `encrypt_key.txt` | 64-char hex key from `server.pub` |

### Step 3  Set scan options

| Option | Recommended for Iran | Notes |
|---|---|---|
| **Target** | `100` | How many resolvers to find |
| **Concurrency** | `80` | Do not go above 100 inside Iran |
| **Timeout** | `3s` | Iranian networks are slow |
| **Pool ×1000** | `200` | 200k IPs scanned. Increase to 300–500 if few found |

Run the scan 2–3 times  each run tests a different random set of IPs.

### Step 4  Start the scan

Click **▶ Start Scan**. Three automatic phases:

- **Phase 1**  Quick alive check across all IPs in the pool
- **Phase 2**  Full 6-check scoring: NS→A, TXT, RND, DPI, EDNS, NXD
- **Phase 3**  Real E2E tunnel test through the VPN binary

🟢 6/6 excellent · 🟡 4–5 good · 🟠 2–3 weak · ⚫ ·0–1 very weak

### Step 5  Save to Profiles

- **MasterDNS:** click **💾 Save to MasterDNS Profiles**
- **VayDNS:** click **💾 Save to VayDNS Profiles**

A profile is saved with sensible defaults. The VPN binary is copied into the output folder automatically.

### (Optional) Export DNS List

After any scan, the **📤 Export DNS List** button becomes active regardless of which VPN mode you used. Click it to save the found resolver IPs as a plain `.txt` file - one IP per line. Useful if you want to use the resolver list in another application or script.

### (Optional) DoH / DoT Scan - encrypted transports

The **🔒 Scan DoH/DoT** button (new in 3.3.0) probes a curated list of well-known DNS-over-HTTPS (port 443) and DNS-over-TLS (port 853) endpoints. The traffic looks like normal HTTPS, so it's much harder for Iranian DPI to fingerprint as tunnel traffic than plain UDP/53. Working endpoints stream into the results list with a 🔒 icon - paste any of them into a VayDNS profile as a custom resolver when UDP isn't surviving DPI.

The lists live in `data/doh_endpoints.txt` and `data/dot_endpoints.txt` next to the app. You can edit them to add private endpoints or remove dead ones without rebuilding.

### Tip - right-click any resolver

In the results list, right-click (or two-finger click / Ctrl-click on Mac) to **Copy IP**, **Copy all IPs**, or **Open output folder** in your file manager.

### Step 6  Connect from the Profiles tab

Click **📋 MasterDNS Profiles** or **📋 VayDNS Profiles** at the top.

1. Select your profile from the left list  the **launched 5m ago** indicator helps you find your active profile
2. Optionally edit options and click **💾 Save Changes**
3. Click **🚀 Launch VPN**  a terminal opens and the VPN starts

Set your browser proxy to `SOCKS5 127.0.0.1:18000` (MasterDNS) or `SOCKS5 127.0.0.1:7000` (VayDNS).

---

## 📋 Profiles Tab  Saving, Editing & Re-testing

Every save creates a profile in `masterdns_profiles/` or `vaydns_profiles/` next to the app.

| Button | What it does |
|---|---|
| 💾 Save Changes | Rewrites config files with your current settings |
| 🚀 Launch VPN | Regenerates files and launches the VPN |
| 📋 Duplicate | Copies the profile  great for A/B testing different settings |
| 🗑 Delete | Removes the profile and optionally the output folder |

---

## 🔧 MasterDNS Options  What They Mean & Iran Optimal Values

| Option | Iran optimal | Why |
|---|---|---|
| **Encryption Method** | `1  XOR` | Lowest overhead in small DNS packets. Must match server. |
| **Balancing Strategy** | `3  Least Loss` | Iran has high uneven packet loss  favours the most reliable resolver |
| **Packet Duplication** | `2–3` | Sends each packet via multiple resolvers  redundancy on lossy paths |
| **Max Upload MTU** | `80–100` | Smaller DNS queries look less suspicious to DPI |
| **Max Download MTU** | `700` | Prevents ISP from fragmenting large DNS responses |
| **Min Upload MTU** | `38` | Very conservative  keeps the maximum number of resolvers usable |
| **Min Download MTU** | `400` | Keeps resolvers that return slightly smaller responses |
| **Log Level** | `INFO` | Shows connection events without flooding the terminal |

---

## 🔧 VayDNS Options  What They Mean & Iran Optimal Values

| Option | Iran optimal | Why |
|---|---|---|
| **Transport** | `UDP` | Plaintext UDP on port 53  most direct path from Iran |
| **Resolver** | *(empty)* | Uses all scanned resolvers in order  see note below |
| **Listen Port** | `7000` | The local port your browser proxy connects to |
| **Max QNAME Length** | `101` | ~50 byte upstream MTU, safe for most Iranian resolvers |
| **Idle Timeout** | `10s` | How long before declaring a session dead. Must match server. Increase to `30s` if reconnects are frequent. |
| **Keepalive** | `2s` | How often to ping the server to keep the session alive. Must be less than idle timeout. Must match server. |
| **Record Type** | `txt` | TXT records carry the most data and are most compatible under DPI |
| **Queue Size** | `512` | Internal packet buffer  increase to `1024` on fast connections |
| **UDP Workers** | `100` | Concurrent outgoing queries  lower to `50` if you see socket errors |
| **Resolver Timeout** | `60s` | If a resolver doesn't connect within this many seconds, the script moves to the next one |
| **Log Level** | `info` | Normal operation |

**The Resolver field:**
- **Empty (recommended)**  KevinNet generates a launch script that tries all scanned resolvers in order. If one gets stuck, it moves to the next after `Resolver Timeout` seconds.
- **Single address**  Only that resolver is used. Format: `8.8.8.8:53` for UDP · `https://dns.google/dns-query` for DoH · `dns.google:853` for DoT.

> **Testing from outside Iran:** Scanned resolvers are Iranian public DNS servers. They only work correctly when connecting **from inside Iran**. Testing from Australia, Europe, or anywhere else will show NXDOMAIN errors  those resolvers cannot reach your tunnel server from a foreign network.

---

## ⚠️ Binary missing?

### MasterDnsVPN binary missing

> **KevinNet v3.0.9+ bundles the correct binary automatically for every platform - upgrade first before trying manual steps below.**

Download the client binary from the [MasterDnsVPN releases](https://github.com/masterking32/MasterDnsVPN/releases/latest):

| Platform | Download |
|---|---|
| 🐧 Linux x64 | [MasterDnsVPN_Client_Linux_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Linux_AMD64.zip) |
| 🐧 Linux ARM64 | [MasterDnsVPN_Client_Linux_ARM64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Linux_ARM64.zip) |
| 🐧 Linux x64 (legacy glibc) | [MasterDnsVPN_Client_Linux-Legacy_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Linux-Legacy_AMD64.zip) |
| 🪟 Windows x64 | [MasterDnsVPN_Client_Windows_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Windows_AMD64.zip) |
| 🪟 Windows ARM64 | [MasterDnsVPN_Client_Windows_ARM64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Windows_ARM64.zip) |
| 🍎 macOS (all) | [MasterDnsVPN releases page](https://github.com/masterking32/MasterDnsVPN/releases/latest) |

1. Extract the ZIP
2. Rename the binary to `MasterDnsVPN` (macOS/Linux) or `MasterDnsVPN.exe` (Windows)
3. Place it **next to the KevinNet app**
4. Click **Save to MasterDNS Profiles** again - it copies automatically

### vaydns-client binary missing

Download from the [VayDNS releases page](https://github.com/net2share/vaydns/releases).
Use these exact filenames when placing next to KevinNet:

| Platform | Filename |
|---|---|
| macOS Apple Silicon (M1/M2/M3/M4) | `vaydns-client-darwin-arm64` |
| macOS Intel | `vaydns-client-darwin-amd64` |
| Linux x64 | `vaydns-client-linux-amd64` |
| Linux ARM64 | `vaydns-client-linux-arm64` |
| Windows x64 | `vaydns-client_windows_amd64.exe` |

1. Download and rename to the exact name above
2. Place it **next to the KevinNet app**
3. Click **Save to VayDNS Profiles** again  it copies automatically

---

---

## 🔍 Common Problems & Solutions

### KevinNet app itself

**macOS: "KevinNet is damaged and can't be opened" or "cannot be verified"**
```bash
chmod +x KevinNet_macOS_Universal
xattr -d com.apple.quarantine KevinNet_macOS_Universal
```
Or right-click the app → Open → Open.

**Linux: "Permission denied" when launching**
```bash
chmod +x KevinNet_Linux_x64
./KevinNet_Linux_x64
```

**Windows: antivirus blocks the app**
This is a false positive  PyInstaller-compiled apps trigger some antivirus scanners. Add an exception for the file, or build from source yourself (see BUILD_INSTRUCTIONS.txt).

**Windows: Persian text appears as separate unjoined characters**
v3.1.2+ bundles Vazirmatn and loads it automatically on startup. If you are on an older version, upgrade to the latest release from the [releases page](https://github.com/kamalalhagh/kevinnet-dns/releases/latest).

---

### VPN binary missing from output folder

**After clicking Save, the country folder has no `MasterDnsVPN` or `vaydns-client`**

The binary must be placed **next to the KevinNet app** before saving  KevinNet copies it into the output folder. See [⚠️ Binary missing?](#-binary-missing) for download links and exact filenames.

**macOS: `MasterDnsVPN` is there but won't run  "cannot be opened"**
```bash
chmod +x /path/to/Iran/MasterDnsVPN
xattr -d com.apple.quarantine /path/to/Iran/MasterDnsVPN
```

**macOS: `vaydns-client-darwin-arm64` won't run**
```bash
chmod +x /path/to/Iran/vaydns-client-darwin-arm64
xattr -d com.apple.quarantine /path/to/Iran/vaydns-client-darwin-arm64
```

---

### Scan finds very few or zero resolvers

**Finding 0–5 resolvers even after scanning**

- Increase **Pool ×1000** from `200` to `500`  more IPs scanned = more found
- Run the scan **2–3 times**  each run picks a different random set of IPs
- Lower **Timeout** to `2s` if the scan takes too long (sacrifices some accuracy)
- Increase **Concurrency** slightly  but do not go above `100` inside Iran

**Phase 3 (E2E) passes zero resolvers**

Phase 3 tests the actual tunnel through your server. Zero means either:
- The server is down or misconfigured  check it is running
- The tunnel domain DNS is not resolving  wait up to 48h after creating DNS records
- The encryption key doesn't match the server  double-check `encrypt_key.txt`

---

### VPN connects but internet doesn't work

**Connected but browser shows no internet / pages don't load**

- Make sure your browser proxy is set to `SOCKS5 127.0.0.1:18000` (MasterDNS) or `SOCKS5 127.0.0.1:7000` (VayDNS)
- Try a SOCKS5 proxy extension  Proxy SwitchyOmega for Chrome/Firefox works well
- Check that the VPN terminal is still open and running

**Connected but very slow**

For MasterDNS  try lowering MTU values:
- Set **Max Upload MTU** to `60–80` (smaller packets, less likely to be throttled)
- Set **Max Download MTU** to `600`
- Save changes in the Profiles tab and reconnect

For VayDNS:
- Try setting **Max QNAME Length** to `80` instead of `101`
- Try **Record Type** `null` instead of `txt` (higher throughput on some resolvers)

---

### MasterDNS specific problems

**"parse TOML failed" error when launching MasterDnsVPN**

The config file has an unfilled placeholder. This happens if you launch from the output folder without saving through KevinNet. Always save from the Profiles tab before launching. If the error persists:
1. Delete the country folder
2. Go to the Profiles tab, select the profile
3. Click **💾 Save Changes** to regenerate the files
4. Click **🚀 Launch VPN**

**Frequent disconnections / reconnects**

- Increase **Packet Duplication** to `3`  more redundancy on lossy paths
- Change **Balancing Strategy** to `3  Least Loss`
- Re-scan to get a fresh set of resolvers  old ones may have been blocked

**Only a handful of resolvers work (most are 1–2)**

This is normal  most public DNS servers don't forward DNS queries for custom NS delegations. A score of 10–30 good resolvers from a scan of 200k IPs is a good result.

---

### VayDNS specific problems

**"noise handshake: timeout" repeated in the terminal**

The resolver is returning NXDOMAIN  it can't reach your tunnel server. The script will automatically move to the next resolver after `Resolver Timeout` seconds. If all resolvers fail:
- Your tunnel domain DNS may not be set up correctly  verify NS delegation with `dig v.yourdomain.com NS`
- Try increasing **Resolver Timeout** to `90s` to give each resolver more time

**VPN process keeps running after Ctrl+C**

This was a known issue  fixed in the latest version. The launch script now uses `trap` to clean up background processes on exit. Re-save your profile to get the updated script.

**"all resolvers exhausted" message**

All scanned resolvers failed within the timeout. Solutions:
1. Re-scan to get a fresh set of resolvers (Iranian DNS servers change frequently)
2. Enter a well-known public resolver in the **Resolver** field: `8.8.8.8:53`
3. Check your server is running and the tunnel domain resolves correctly

**Testing from outside Iran  NXDOMAIN on all resolvers**

This is expected behaviour, not a bug. The scanned resolvers are Iranian public DNS servers. They only forward queries for your tunnel domain when accessed from inside Iran. Testing from Europe, Australia, or anywhere outside Iran will always fail.

---

### DNS / domain problems

**"dig v.yourdomain.com NS" shows no results**

DNS propagation can take up to 48 hours. Wait and try again. Also check:
- The NS record value points to the exact same name as the A record (e.g. `ns.yourdomain.com`)
- Cloudflare A record is set to DNS only (grey cloud), not proxied

**Server is running but no resolvers pass Phase 3**

Try verifying the domain manually from your server:
```bash
dig @127.0.0.1 test.v.yourdomain.com A
```
If this returns NXDOMAIN, the server is not receiving DNS queries correctly. Check the firewall (port 53 UDP must be open) and `systemd-resolved` is disabled.

---

## 🖥️ Server Setup

KevinNet is a **client-side app only**. Server installation is covered in the official repos:

- **MasterDNS server:** 👉 [https://github.com/masterking32/MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)
- **VayDNS server:** 👉 [https://github.com/net2share/vaydns](https://github.com/net2share/vaydns)

---

## 🛠️ Build From Source

See [BUILD_INSTRUCTIONS.txt](BUILD_INSTRUCTIONS.txt) (English) or [BUILD_INSTRUCTIONS_FA.txt](BUILD_INSTRUCTIONS_FA.txt) (فارسی) for the full PyInstaller build steps.

### Running the test suite

KevinNet ships with a unit test suite (87 tests) covering input validation, scanner helpers, profile config building, and settings handling. Tests run in CI before every release.

```bash
pip install pytest dnspython pillow
python -m pytest tests/ -v
```

All tests must pass before a release is built - the CI workflow gates the platform-specific builds behind a successful `pytest` run.

### Editing bundled data lists

The Iranian CIDR ranges, public DNS resolvers, WhiteDNS Iran list, and DoH/DoT endpoint lists live as plain text files in `data/`:

| File | Contents |
|---|---|
| `data/iran_cidrs.txt` | Iranian IPv4 CIDR ranges sampled during scanning |
| `data/public_resolvers.txt` | Well-known public DNS resolvers (warm-up set) |
| `data/white_dns_iran.txt` | Pre-verified Iranian DNS resolvers (high-hit-rate seed list) |
| `data/doh_endpoints.txt` | DNS-over-HTTPS endpoints scanned by the 🔒 button |
| `data/dot_endpoints.txt` | DNS-over-TLS endpoints scanned by the 🔒 button |

You can edit these files to add private endpoints or remove dead entries - no rebuild needed. When PyInstaller bundles the binary it copies them inside, and the app also looks for a `data/` folder next to the executable so user edits take priority over the bundled copy.

---

## 🙏 Credits

**MasterDnsVPN** by MasterkinG32 (Amin Mahmoudi)  [GitHub](https://github.com/masterking32/MasterDnsVPN)  MIT License

**VayDNS** by net2share  [GitHub](https://github.com/net2share/vaydns)  fork of dnstt by David Fifield (public domain)

See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) for full license texts.

---

## ⭐ Support This Project

- **⭐ Star this repo**  helps others discover it
- **Share** with anyone in Iran who needs free internet
- **Report bugs** via GitHub Issues

Every star and share helps this tool reach one more family that needs it.

See [CHANGELOG.md](CHANGELOG.md) for what's new in each release.

---

## ⚖️ License & Disclaimer

Copyright © 2026 Kevin Haji  [MIT License](LICENSE)  See [DISCLAIMER.md](DISCLAIMER.md)
