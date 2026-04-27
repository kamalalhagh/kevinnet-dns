<div align="left">

[🇬🇧 English](README.md) | 🇮🇷 فارسی

</div>

<div dir="rtl">

# 🌐 KevinNet DNS

**یک برنامه گرافیکی ساده برای DNS Tunnel — پشتیبانی از MasterDnsVPN و VayDNS**

> KevinNet به صورت خودکار IP‌های ایرانی را اسکن می‌کند تا Resolverهای کارآمد پیدا کند، سپس فایل‌های پیکربندی آماده می‌سازد و VPN را با یک کلیک راه‌اندازی می‌کند. بدون ویرایش فایل تنظیمات. بدون دستورات پیچیده ترمینال.

**ساخته شده توسط Kevin Haji · [kevinhaji.com](https://kevinhaji.com) · [kevin.fullstack.dev@gmail.com](mailto:kevin.fullstack.dev@gmail.com)**

---

## 💡 این برنامه چیست؟

یک تانل DNS ترافیک اینترنت شما را به عنوان درخواست‌های DNS معمولی پنهان می‌کند. فیلترینگ DPI ایران نمی‌تواند آن را شناسایی یا مسدود کند. KevinNet تمام بخش‌های فنی را مدیریت می‌کند — پیدا کردن Resolverهای کارآمد، نوشتن فایل‌های تنظیمات، راه‌اندازی VPN — تنها کاری که باید بکنید کلیک کردن است.

**موتورهای VPN پشتیبانی‌شده:**
- **MasterDNS** ([MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)) — DNS tunnel با چندین Resolver همزمان. پایداری عالی برای ایران.
- **VayDNS** ([VayDNS](https://github.com/net2share/vaydns)) — DNS tunnel با انتقال DoH/DoT/UDP و رمزنگاری Noise Protocol.

---

## 📥 دانلود

آخرین نسخه را از صفحه [**Releases**](../../releases/latest) دانلود کنید:

| پلتفرم | فایل |
|---|---|
| 🪟 ویندوز x64 | `KevinNet_Windows_x64.exe` |
| 🍎 مک (Intel + Apple Silicon) | `KevinNet_macOS_Universal` |
| 🐧 لینوکس x64 | `KevinNet_Linux_x64` |
| 🐧 لینوکس ARM64 | `KevinNet_Linux_ARM64` |

> **مک:** بعد از دانلود در ترمینال بزنید:
> ```bash
> chmod +x KevinNet_macOS_Universal
> xattr -d com.apple.quarantine KevinNet_macOS_Universal
> ```
> یا راست‌کلیک ← Open ← Open.

> **لینوکس:** قبل از اجرا `chmod +x KevinNet_Linux_x64` بزنید.

---

## 🔧 پیش‌نیاز

به یک **سرور VPS خارج از ایران** با نصب نرم‌افزار سرور VPN نیاز دارید. قبل از باز کردن KevinNet این‌ها را آماده کنید:

| | MasterDNS | VayDNS |
|---|---|---|
| دامنه تانل | `v.example.com` | `v.example.com` |
| کلید | کلید رمزنگاری ۳۲ کاراکتری (از `encrypt_key.txt`) | کلید عمومی ۶۴ کاراکتری hex (از `server.pub`) |

برای نصب سرور بخش [راه‌اندازی سرور](#-راه‌اندازی-سرور) را ببینید.

---

## 🚀 نحوه استفاده — گام به گام

### مرحله ۱ — نوع VPN را انتخاب کنید

روی **MasterDNS** یا **VayDNS** در بالای پنل اسکنر کلیک کنید. فقط فیلدها و دکمه ذخیره همان نوع نمایش داده می‌شود.

### مرحله ۲ — مشخصات را وارد کنید

| فیلد | چی وارد کنید |
|---|---|
| **نام کشور / پوشه** | یک نام برای این پیکربندی — مثلاً `Iran` یا `Turkey` |
| **دامنه تانل** | ساب‌دامینی که به سرور اشاره دارد — مثلاً `v.example.com` |
| **کلید** | کلید ۳۲ کاراکتری (MasterDNS) یا ۶۴ کاراکتری hex (VayDNS) از سرور |

### مرحله ۳ — تنظیمات اسکن

| گزینه | پیشنهاد برای ایران | توضیح |
|---|---|---|
| **هدف (Target)** | `100` | تعداد Resolver مورد نظر |
| **همزمانی** | `80` | بالاتر از ۱۰۰ نروید |
| **Timeout** | `3 ثانیه` | شبکه‌های ایران کند هستند |
| **پول ×۱۰۰۰** | `200` | ۲۰۰ هزار IP اسکن می‌شود |

> کم پیدا شد؟ Pool را به ۳۰۰ یا ۵۰۰ افزایش دهید.
> اسکن را ۲-۳ بار تکرار کنید — هر بار IP‌های تصادفی مختلفی تست می‌شود.

### مرحله ۴ — شروع اسکن

روی **▶ شروع اسکن** کلیک کنید. سه مرحله خودکار اجرا می‌شود:

- **مرحله ۱** (سریع) — بررسی زنده بودن همه IP‌ها
- **مرحله ۲** (دقیق) — امتیازدهی ۶ معیاره: ★6/6 ◆4-5 ▸2-3 ·0-1
- **مرحله ۳** (واقعی) — تست E2E از طریق باینری VPN

رنگ‌بندی: 🟢 عالی · 🟡 خوب · 🟠 ضعیف · ⚫ خیلی ضعیف

### مرحله ۵ — ذخیره در پروفایل‌ها

- **MasterDNS:** روی **💾 ذخیره در MasterDNS** کلیک کنید
- **VayDNS:** روی **💾 ذخیره در VayDNS** کلیک کنید

پروفایل با تنظیمات پیش‌فرض ذخیره می‌شود. باینری VPN به صورت خودکار در پوشه خروجی کپی می‌شود.

### مرحله ۶ — اتصال از تب پروفایل‌ها

روی تب **📋 MasterDNS Profiles** یا **📋 VayDNS Profiles** کلیک کنید.

۱. پروفایل ذخیره‌شده را از لیست انتخاب کنید
۲. در صورت نیاز تنظیمات را ویرایش کرده و **💾 ذخیره تغییرات** بزنید
۳. روی **🚀 اتصال** کلیک کنید — ترمینال باز می‌شود و VPN شروع به کار می‌کند

---

## 📋 تب پروفایل‌ها — مدیریت پیکربندی‌های ذخیره‌شده

هر ذخیره یک پروفایل در پوشه `masterdns_profiles/` یا `vaydns_profiles/` کنار برنامه می‌سازد.

| دکمه | کار |
|---|---|
| 💾 ذخیره تغییرات | فایل‌های تنظیمات با گزینه‌های فعلی بازنویسی می‌شود |
| 🚀 اتصال | فایل‌ها را بازتولید می‌کند و VPN را راه‌اندازی می‌کند |
| 📋 کپی | پروفایل و پوشه را کپی می‌کند — برای تست A/B تنظیمات مختلف |
| 🗑 حذف | پروفایل (و اختیاراً پوشه خروجی) را حذف می‌کند |

---

## 🔧 تنظیمات کلیدی MasterDNS — معنی هر کدام و مقدار بهینه برای ایران

| تنظیم | بهینه برای ایران | چرا |
|---|---|---|
| **روش رمزنگاری** | `1 — XOR` | کمترین سربار در پکت‌های کوچک DNS |
| **استراتژی بالانس** | `3 — Least Loss` | ایران افت پکت بالا و نامتعادل دارد |
| **تکرار بسته** | `2–3` | افزونگی در مسیرهای پر افت |
| **Max Upload MTU** | `80–100` | query کوچک‌تر = کمتر DPI trigger |
| **Max Download MTU** | `700` | جلوگیری از fragmentation ISP |
| **Min Upload MTU** | `38` | بیشترین تعداد Resolver در pool |
| **Min Download MTU** | `400` | Resolverهای مرزی را نگه می‌دارد |
| **سطح لاگ** | `INFO` | عملکرد عادی |

---

## 🔧 تنظیمات کلیدی VayDNS — معنی هر کدام و مقدار بهینه برای ایران

| تنظیم | بهینه برای ایران | چرا |
|---|---|---|
| **Transport** | `UDP` | مستقیم‌ترین مسیر از ایران |
| **Resolver** | *(خالی)* | همه Resolverهای اسکن‌شده به ترتیب امتحان می‌شوند |
| **Listen Port** | `7000` | پورت محلی برای مرورگر/برنامه |
| **Max QNAME Length** | `101` | ایمن برای اکثر Resolver‌ها |
| **Idle Timeout** | `10s` | اگر قطعی مکرر دارید: `30s` |
| **Record Type** | `txt` | بیشترین سازگاری با DPI |
| **UDP Workers** | `100` | اگر خطای socket داشتید: `50` |
| **Resolver Timeout** | `60s` | اگر ۶۰ ثانیه وصل نشد به Resolver بعدی می‌رود |
| **Log Level** | `info` | عملکرد عادی |

**فیلد Resolver:**
- **خالی** — اسکریپت launch همه Resolverهای اسکن‌شده را به ترتیب امتحان می‌کند. اگر یکی بعد از `Resolver Timeout` ثانیه هنوز وصل نشده، به بعدی می‌رود.
- **یک IP یا URL** — فقط همان Resolver استفاده می‌شود (مثال UDP: `8.8.8.8:53`، مثال DoH: `https://dns.google/dns-query`).

> **مهم:** Resolverهای اسکن‌شده سرورهای DNS عمومی ایرانی هستند. آن‌ها فقط از **داخل ایران** درست کار می‌کنند. تست از خارج از ایران (استرالیا، اروپا و...) نتایج NXDOMAIN نشان می‌دهد.

---

## ⚠️ فایل اجرایی VPN در پوشه نیست؟

اگر بعد از ذخیره `MasterDnsVPN` یا `vaydns-client` را در پوشه نمی‌بینید:

۱. فایل را برای پلتفرم خودتان دانلود کنید (لینک‌ها پایین)
۲. نام آن را به نام دقیق موردنیاز تغییر دهید
۳. **کنار برنامه KevinNet** بگذارید (نه داخل پوشه کشور)
۴. دوباره ذخیره کنید — به صورت خودکار کپی می‌شود

**نام‌های قابل قبول vaydns-client:**

| پلتفرم | نام فایل |
|---|---|
| مک Apple Silicon | `vaydns-client-darwin-arm64` |
| مک Intel | `vaydns-client-darwin-amd64` |
| لینوکس x64 | `vaydns-client-linux-amd64` |
| لینوکس ARM64 | `vaydns-client-linux-arm64` |
| ویندوز x64 | `vaydns-client_windows_amd64.exe` |

---

## 🖥️ راه‌اندازی سرور

### سرور MasterDNS

راهنمای کامل در [MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN).

**راه‌اندازی DNS** — دو رکورد در کنترل پنل دامنه بسازید:

| نوع | نام | مقدار |
|---|---|---|
| `A` | `ns` | آدرس IPv4 سرور |
| `NS` | `v` | `ns.example.com` |

> کاربران Cloudflare: رکورد A باید **DNS only** (ابر خاکستری) باشد.

**نصب روی لینوکس:**
```bash
bash <(curl -Ls https://raw.githubusercontent.com/masterking32/MasterDnsVPN/main/server_linux_install.sh)
```

کلید رمزنگاری در پایان نمایش داده می‌شود و در `encrypt_key.txt` ذخیره می‌شود.

**باز کردن پورت ۵۳:**
```bash
sudo ufw allow 53/udp && sudo ufw reload
```

اگر پورت ۵۳ در اشغال است:
```bash
sudo systemctl stop systemd-resolved && sudo systemctl disable systemd-resolved
sudo systemctl restart MasterDnsVPN
```

---

### سرور VayDNS

راهنمای کامل در [VayDNS](https://github.com/net2share/vaydns).

**راه‌اندازی DNS** — همان مراحل MasterDNS: یک رکورد A برای NS و یک رکورد NS برای ساب‌دامین تانل.

**ساخت و تولید کلید:**
```bash
go build -o vaydns-server ./vaydns-server
./vaydns-server -gen-key -privkey-file server.key -pubkey-file server.pub
```

فایل `server.pub` را به دستگاه کلاینت منتقل کنید. محتوای hex آن کلید عمومی VayDNS شماست.

**اجرای سرور:**
```bash
./vaydns-server -udp :53 -privkey-file server.key \
  -domain t.example.com -upstream 127.0.0.1:8000
```

برای SOCKS5 از طریق SSH:
```bash
ssh -N -D 127.0.0.1:8000 -o NoHostAuthenticationForLocalhost=yes 127.0.0.1
```

**ریدایرکت پورت ۵۳ (بدون root):**
```bash
sudo iptables -t nat -I PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5300
./vaydns-server -udp :5300 -privkey-file server.key -domain t.example.com -upstream 127.0.0.1:8000
```

---

## 🛠️ کامپایل از سورس

ببینید [BUILD_INSTRUCTIONS.txt](BUILD_INSTRUCTIONS.txt) یا [BUILD_INSTRUCTIONS_FA.txt](BUILD_INSTRUCTIONS_FA.txt).

---

## 🙏 تقدیر و تشکر

KevinNet بدون این پروژه‌های عالی وجود نداشت:

**MasterDnsVPN** توسط MasterkinG32 (Amin Mahmoudi)
- گیت‌هاب: [https://github.com/masterking32/MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)
- تحت مجوز MIT

**VayDNS** توسط net2share
- گیت‌هاب: [https://github.com/net2share/vaydns](https://github.com/net2share/vaydns)
- فورک از dnstt توسط David Fifield (دامنه عمومی)

برای متن کامل مجوزها ببینید [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

---

## ⭐ حمایت از این پروژه

بهترین راه حمایت از KevinNet رساندن آن به کسانی است که به آن نیاز دارند:

- **ستاره دادن** به این مخزن در GitHub — به دیگران کمک می‌کند آن را پیدا کنند
- **اشتراک‌گذاری** با هر کسی در ایران که به اینترنت آزاد نیاز دارد
- **گزارش باگ** و پیشنهاد بهبود از طریق GitHub Issues
- **انتشار** در جوامع و گروه‌هایی که می‌توانند استفاده کنند

هر ستاره و اشتراک‌گذاری به رسیدن این ابزار به یک خانواده دیگر کمک می‌کند.

---

## ⚖️ مجوز و سلب مسئولیت

حق چاپ © ۲۰۲۶ Kevin Haji — [مجوز MIT](LICENSE)

ببینید [DISCLAIMER_FA.md](DISCLAIMER_FA.md). این ابزار صرفاً برای اهداف آموزشی و تحقیقاتی ارائه می‌شود.

</div>
