<div align="left">

[🇬🇧 English](README.md) | 🇮🇷 فارسی

</div>

<div dir="rtl">

# 🌐 KevinNet DNS

**ابزار جانبی برای [MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)**

> به صورت خودکار IP‌های ایرانی را اسکن می‌کند تا DNS Resolverهایی که از DPI ایران عبور می‌کنند را پیدا کند — سپس فایل‌های پیکربندی آماده می‌سازد و با یک کلیک وصل می‌شود.

**ساخته شده توسط Kevin Haji · [kevinhaji.com](https://kevinhaji.com) · [kevin.fullstack.dev@gmail.com](mailto:kevin.fullstack.dev@gmail.com)**

---

## 📥 دانلود (نیاز به نصب ندارد)

آخرین نسخه را از صفحه [**Releases**](../../releases/latest) دانلود کنید:

| پلتفرم | فایل |
|---|---|
| 🪟 ویندوز x64 | `KevinNet_Windows_x64.exe` |
| 🪟 ویندوز ARM64 | `KevinNet_Windows_ARM64.exe` |
| 🍎 مک (Intel + Apple Silicon) | `KevinNet_macOS_Universal` |
| 🐧 لینوکس x64 | `KevinNet_Linux_x64` |
| 🐧 لینوکس ARM64 | `KevinNet_Linux_ARM64` |

> **مک:** بعد از دانلود، راست‌کلیک ← Open ← Open کنید تا Gatekeeper دور بزنید.
> **لینوکس:** قبل از اجرا `chmod +x KevinNet_Linux_x64` را بزنید.

---

## 🚀 نحوه استفاده

### مرحله ۱ — وارد کردن تنظیمات

| فیلد | چی وارد کنید | مثال |
|---|---|---|
| دامنه تانل | ساب‌دامینی که به سرور شما اشاره دارد | `v.example.com` |
| کلید رمزنگاری | کلید ۳۲ کاراکتری از سرور | `4c8da843709463cab27f...` |
| نام کشور / پوشه | نام پوشه خروجی | `Iran` |

### مرحله ۲ — انتخاب تنظیمات اسکن (پیشنهادی برای ایران)

| تنظیم | پیشنهاد برای ایران | توضیح |
|---|---|---|
| **هدف (Target)** | `100` | تعداد Resolverهایی که می‌خواهید پیدا کنید. بیشتر = VPN پایدارتر |
| **همزمانی (Concurrency)** | `80–100` | ایران محدودیت socket دارد — بالاتر از ۱۵۰ نروید |
| **Timeout** | `2–3 ثانیه` | ۳ ثانیه برای شبکه‌های شلوغ ایران ایمن‌تر است |
| **پول (Pool ×1000)** | `200` | ۲۰۰,۰۰۰ IP اسکن می‌شود. بیشتر = Resolver بیشتر |

> **نکته:** اگر Resolver کمی پیدا شد، **Pool** را به `300` یا `500` افزایش دهید.
> **Concurrency را زیاد نکنید** — باعث خطاهای پنهان در مک و شبکه‌های ایران می‌شود.
> اسکن را ۲-۳ بار اجرا کنید — هر بار IP‌های تصادفی مختلفی تست می‌شود.

### مرحله ۳ — شروع اسکن

روی **▶ شروع اسکن** کلیک کنید. اسکن در ۳ مرحله خودکار اجرا می‌شود:

- **مرحله ۱** — بررسی سریع زنده بودن (~۵-۱۰ دقیقه برای ۲۰۰ هزار IP)
- **مرحله ۲** — امتیازدهی کامل ۶ معیاره: NS→A، TXT، RND، DPI، EDNS، NXD (همه نشان داده می‌شن)
- **مرحله ۳** — تست واقعی تانل E2E از طریق باینری MasterDnsVPN (فیلتر نهایی)

رنگ‌بندی نتایج:
- 🟢 **★ ۶/۶** — عالی، همه تست‌ها پاس
- 🟡 **◆ ۴-۵/۶** — خوب، احتمالاً کار می‌کند
- 🟠 **▸ ۲-۳/۶** — ضعیف، ممکن است کار کند
- ⚫ **· ۰-۱/۶** — خیلی ضعیف

### مرحله ۴ — ذخیره و اتصال

روی **💾 ذخیره فایل‌ها** کلیک کنید — پوشه‌ای (مثلاً `Iran/`) کنار برنامه ساخته می‌شود:
- `client_config.toml`
- `client_resolvers.txt`
- `MasterDnsVPN` (یا `.exe` در ویندوز)

روی **🚀 اتصال MasterDNSVPN** کلیک کنید — ترمینال باز می‌شود و VPN راه‌اندازی می‌شود.

---

## ⚠️ MasterDnsVPN در پوشه نیست؟

اگر بعد از ذخیره `MasterDnsVPN` را در پوشه کشور نمی‌بینید، این مراحل را دنبال کنید:

### دانلود دستی MasterDnsVPN

| پلتفرم | لینک دانلود |
|---|---|
| ویندوز AMD64 | [MasterDnsVPN_Client_Windows_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Windows_AMD64.zip) |
| ویندوز ARM64 | [MasterDnsVPN_Client_Windows_ARM64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Windows_ARM64.zip) |
| مک AMD64 | [MasterDnsVPN_Client_MacOS_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_MacOS_AMD64.zip) |

### قرار دادن در مکان درست

۱. فایل ZIP را باز کنید
۲. فایل اجرایی داخل را پیدا کنید (ممکن است `MasterDnsVPN_Client` نام داشته باشد)
۳. نام آن را دقیقاً به `MasterDnsVPN` (مک/لینوکس) یا `MasterDnsVPN.exe` (ویندوز) تغییر دهید
۴. آن را در **همان پوشه‌ای که KevinNet قرار دارد** بگذارید
۵. KevinNet را دوباره اجرا کنید و روی **ذخیره فایل‌ها** کلیک کنید — به صورت خودکار کپی می‌شود

**فقط مک** — قابل اجرا کردن:
```bash
chmod +x /path/to/MasterDnsVPN
```

بعد از قرار دادن صحیح، در هر Save بعدی به صورت خودکار داخل پوشه کشور کپی می‌شود.

---

## 🖥️ بخش ۱ — راه‌اندازی سرور

### ۱.۱ 🌐 راه‌اندازی دامنه (پیش‌نیاز)

برای دریافت درخواست‌های DNS روی سرور، باید یک ساب‌دامین به آن delegate کنید.
**دو رکورد DNS** در کنترل پنل دامنه بسازید:

#### مرحله ۱.۱.۱ — ساخت رکورد A

| فیلد | مقدار |
|---|---|
| Type | `A` |
| Name | `ns` (یا هر اسم کوتاه) |
| Value | آدرس IPv4 سرور |

مثال: `ns.example.com → 1.2.3.4`

> **کاربران Cloudflare:** روی آیکون ابر نارنجی کلیک کنید تا **خاکستری (DNS only)** شود. نباید proxied باشد.

#### مرحله ۱.۱.۲ — ساخت رکورد NS

| فیلد | مقدار |
|---|---|
| Type | `NS` |
| Name | `v` (ساب‌دامین تانل) |
| Value | `ns.example.com` |

مثال: `v.example.com → ns.example.com`

> **کاربران Cloudflare:** رکورد NS را عادی اضافه کنید. مطمئن شوید رکورد A روی DNS only است.

#### ۱.۱.۳ 💡 نکته MTU

نام‌های کوتاه‌تر فضای بیشتری برای داده داخل هر پکت DNS باقی می‌گذارند.
نام‌ها را کوتاه نگه دارید (۱-۳ کاراکتر).

---

### ۱.۲ 🐧 نصب سرور لینوکس

#### مرحله ۱.۲.۱ — نصب خودکار

```bash
bash <(curl -Ls https://raw.githubusercontent.com/masterking32/MasterDnsVPN/main/server_linux_install.sh)
```

بعد از اتمام:
- سرور به صورت خودکار شروع می‌کند
- **کلید رمزنگاری** در ترمینال نشان داده می‌شود
- کلید در فایل `encrypt_key.txt` ذخیره می‌شود

> ⚠️ **کلید را ذخیره کنید** — کلاینت‌ها برای اتصال به آن نیاز دارند.

#### مرحله ۱.۲.۲ — نکات مهم

**دامنه:** همان ساب‌دامین رکورد NS را وارد کنید (مثلاً `v.example.com`).

**انتشار DNS:** تا ۴۸ ساعت صبر کنید.

**تأیید DNS:**
```bash
dig v.example.com NS
dig @ns.example.com v.example.com A
```

**باز کردن پورت ۵۳:**
```bash
# ufw
sudo ufw allow 53/udp && sudo ufw reload

# firewalld
sudo firewall-cmd --add-port=53/udp --permanent && sudo firewall-cmd --reload
```

**پورت ۵۳ در اشغال است (systemd-resolved):**
```bash
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved
sudo systemctl restart MasterDnsVPN
```

---

## 🛠️ کامپایل از سورس

ببینید [**BUILD_INSTRUCTIONS.txt**](BUILD_INSTRUCTIONS.txt) (انگلیسی) یا [**BUILD_INSTRUCTIONS_FA.txt**](BUILD_INSTRUCTIONS_FA.txt) (فارسی).

### شروع سریع — macOS
```bash
brew install python@3.12 python-tk@3.12
/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv venv
source venv/bin/activate
pip install dnspython pyinstaller pillow
chmod +x build_mac_universal.sh
./build_mac_universal.sh
```

### شروع سریع — ویندوز
```bat
python -m venv venv
venv\Scripts\activate
pip install dnspython pyinstaller pillow
build_windows.bat
```

---

## 🙏 تقدیر و تشکر

این ابزار یک برنامه جانبی برای **MasterDnsVPN** توسط **MasterkinG32 (Amin Mahmoudi)** است.

- گیت‌هاب: [https://github.com/masterking32/MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)
- MasterDnsVPN تحت **مجوز MIT** استفاده می‌شود — ببینید [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)

---

## 💰 حمایت مالی اختیاری

- **وب‌سایت:** [kevinhaji.com](https://kevinhaji.com)
- **ایمیل:** [kevin.fullstack.dev@gmail.com](mailto:kevin.fullstack.dev@gmail.com)

---

## ⚖️ مجوز

حق چاپ © ۲۰۲۶ Kevin Haji — [مجوز MIT](LICENSE)

## ⚠️ سلب مسئولیت

ببینید [DISCLAIMER_FA.md](DISCLAIMER_FA.md). MasterDnsVPN صرفاً برای اهداف آموزشی و تحقیقاتی ارائه می‌شود.

</div>
