<div align="left">

[🇬🇧 English](README.md) | 🇮🇷 فارسی

</div>

<div dir="rtl">

# 🌐 KevinNet DNS

**یک برنامه گرافیکی ساده برای DNS Tunnel  پشتیبانی از MasterDnsVPN و VayDNS**

> KevinNet به صورت خودکار IP‌های ایرانی را اسکن می‌کند تا Resolverهای کارآمد پیدا کند، سپس فایل‌های پیکربندی آماده می‌سازد و VPN را با یک کلیک راه‌اندازی می‌کند. بدون ویرایش فایل. بدون دستورات پیچیده ترمینال.

**ساخته شده توسط Kevin Haji · [kevinhaji.com](https://kevinhaji.com) · [kevin.fullstack.dev@gmail.com](mailto:kevin.fullstack.dev@gmail.com)**

---

## 💡 KevinNet چیست؟

یک تانل DNS ترافیک اینترنت شما را به عنوان درخواست‌های DNS معمولی پنهان می‌کند. فیلترینگ DPI ایران نمی‌تواند آن را شناسایی یا مسدود کند. KevinNet تمام بخش‌های فنی را مدیریت می‌کند  اسکن برای Resolverهای کارآمد، نوشتن فایل‌های تنظیمات، کپی باینری‌ها، راه‌اندازی VPN  تنها کاری که باید بکنید پر کردن چند فیلد و کلیک کردن است.

دو موتور VPN پشتیبانی می‌شود:

- **MasterDNS**  از چندین Resolver همزمان استفاده می‌کند. پایداری عالی. بهترین انتخاب برای ایران.
- **VayDNS**  رمزنگاری Noise Protocol با انتقال DoH، DoT یا UDP. به صورت خودکار Resolverها را امتحان می‌کند.

---

## ✨ چه چیزی در نسخه 3.3.0 جدید است؟

- 🔒  **اسکن DoH / DoT** — دکمه جدید برای اسکن لیست منتخبی از endpointهای معروف DNS-over-HTTPS (پورت 443) و DNS-over-TLS (پورت 853). چون ترافیک روی TLS است، تشخیص آن به عنوان ترافیک تونل برای DPI ایران بسیار سخت‌تر از UDP/53 معمولی است.
- 🖱  **منوی راست‌کلیک** روی لیست Resolverها — کپی IP، کپی همه IPها، باز کردن پوشه خروجی.
- ⏱  **زمان آخرین اجرا** روی هر پروفایل (مثلاً `5 دقیقه پیش اجرا شد`). راحت می‌توانید پروفایل فعال فعلی را پیدا کنید.
- 💾  **به یاد می‌سپارد** — دامنه، پوشه کشور و حالت VPN آخرین بار شما در اجرای بعدی بازیابی می‌شوند.
- ✅  **اعتبارسنجی ورودی** با پیام‌های خطای واضح — دیگر خطاهای گیج‌کننده «parse TOML failed» وقتی یک کاراکتر اضافی در دامنه پیست شده باشد، نخواهید دید.
- 🔐  **بهبود امنیتی** — فایل‌های پروفایل با مجوزهای محدود روی Linux/macOS ساخته می‌شوند تا کاربران دیگر سیستم نتوانند کلیدهای رمزنگاری شما را بخوانند.
- 🧪  **مجموعه تست‌ها** با 87 تست در CI قبل از هر build اجرا می‌شود.
- 📜  **چک‌سام SHA-256** همراه هر release منتشر می‌شود تا بتوانید دانلودها را تأیید کنید.

برای فهرست کامل تغییرات [CHANGELOG.md](CHANGELOG.md) را ببینید.

---

## 📥 دانلود KevinNet

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

### تأیید دانلود (اختیاری اما توصیه می‌شود)

هر release یک فایل `SHA256SUMS.txt` کنار باینری‌ها دارد. برای تأیید اینکه فایل دانلود شده دستکاری نشده:

```bash
shasum -a 256 -c SHA256SUMS.txt     # macOS / Linux
```
```powershell
Get-FileHash -Algorithm SHA256 KevinNet_Windows_x64.exe  # Windows
```

خروجی را با خط مربوط به پلتفرم شما در `SHA256SUMS.txt` مقایسه کنید. اگر برابر نبود، فایل را اجرا نکنید — از صفحه Releases رسمی دوباره دانلود کنید.

> ---

### لینوکس: متن فارسی ناخوانا یا حروف جدا از هم نمایش داده می‌شود

**حروف فارسی/عربی به صورت ایزوله، غیرمتصل یا با ترتیب اشتباه نمایش داده می‌شوند**

این مشکل زمانی رخ می‌دهد که سیستم‌عامل فونت عربی/فارسی مناسب نداشته باشد. KevinNet نسخه v3.1.1 به بعد فونت Vazirmatn را به صورت خودکار در اولین اجرا نصب می‌کند. اگر متن هنوز ناخواناست:

```bash
# نصب فونت فارسی به صورت دستی
sudo apt install fonts-noto fonts-noto-extra   # دبیان/اوبونتو
sudo dnf install google-noto-sans-arabic-fonts  # فدورا
sudo pacman -S noto-fonts                        # آرچ
```

سپس KevinNet را دوباره اجرا کنید.

**لینوکس:** قبل از اجرا `chmod +x KevinNet_Linux_x64` بزنید.

---

## 🔧 پیش‌نیازها  قبل از شروع چه چیزی لازم دارید

KevinNet برنامه **سمت کلاینت** است. باید ابتدا یک سرور VPN روی یک VPS خارج از ایران راه‌اندازی شده باشد.

---

### اگر از MasterDNS استفاده می‌کنید

#### ۱  یک سرور VPS خارج از ایران

هر VPS لینوکسی با آدرس IP عمومی کافی است. ارائه‌دهندگان معروف: Hetzner، DigitalOcean، Vultr، Linode.

#### ۲  یک دامنه با تنظیمات NS

MasterDNS به عنوان یک سرور DNS معتبر (Authoritative) عمل می‌کند، پس درخواست‌های DNS برای ساب‌دامین تانل باید به VPS شما هدایت شوند. **دو رکورد DNS** در کنترل پنل دامنه‌تان بسازید:

| نوع | نام | مقدار | هدف |
|---|---|---|---|
| `A` | `ns` | IP سرور | رکورد Glue  آدرس nameserver شما |
| `NS` | `v` | `ns.yourdomain.com` | هدایت درخواست‌های `v.yourdomain.com` به سرور |

مثال با دامنه `example.com` و IP سرور `1.2.3.4`:
- `ns.example.com` → `1.2.3.4` (رکورد A)
- `v.example.com` → `ns.example.com` (رکورد NS)

دامنه تانل شما `v.example.com` می‌شود.

> **کاربران Cloudflare:** رکورد A برای `ns` باید **DNS only** (ابر خاکستری) باشد. نه proxied.
> **نکته:** نام‌های کوتاه (۱-۲ کاراکتر) فضای بیشتری برای داده در هر پکت DNS دارند = سرعت بهتر.

#### ۳  نصب سرور MasterDnsVPN روی VPS

راهنمای رسمی: 👉 [https://github.com/masterking32/MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)

بعد از نصب دارید:
- **دامنه تانل**  مثلاً `v.example.com` → این را در KevinNet وارد کنید
- **کلید رمزنگاری ۳۲ کاراکتری**  در فایل `encrypt_key.txt` روی سرور → این را در KevinNet وارد کنید

> کلید باید بین کلاینت و سرور یکسان باشد. اگر گم شد، روی سرور `cat encrypt_key.txt` بزنید.

#### ۴  باینری MasterDnsVPN

درون KevinNet بسته‌بندی شده و به صورت خودکار در پوشه خروجی کپی می‌شود. اگر نبود، بخش [⚠️ باینری نیست؟](#-باینری-نیست) را ببینید.

---

### اگر از VayDNS استفاده می‌کنید

#### ۱  یک سرور VPS خارج از ایران

همان MasterDNS  هر VPS لینوکسی با IP عمومی.

#### ۲  یک دامنه با تنظیمات NS

VayDNS هم به عنوان سرور DNS معتبر عمل می‌کند. مفهوم راه‌اندازی DNS دقیقاً مانند MasterDNS است: یک رکورد A برای Glue و یک رکورد NS برای delegation.

مثال با دامنه `example.com` و IP سرور `1.2.3.4`:
- `tns.example.com` → `1.2.3.4` (رکورد A  glue)
- `t.example.com` → `tns.example.com` (رکورد NS  delegation)

دامنه تانل شما `t.example.com` می‌شود.

> **مهم:** نام رکورد glue (مثلاً `tns`) نباید زیرشاخه tunnel subdomain (مثلاً `t`) باشد. باید مجزا باشند  مثلاً `tns` و `t`، نه `ns.t`.

#### ۳  نصب سرور VayDNS روی VPS

راهنمای رسمی: 👉 [https://github.com/net2share/vaydns](https://github.com/net2share/vaydns)

بعد از نصب دارید:
- **دامنه تانل**  مثلاً `t.example.com` → این را در KevinNet وارد کنید
- **فایل `server.pub`** روی سرور  حاوی کلید عمومی شماست

#### ۴  کلید عمومی VayDNS (رشته hex 64 کاراکتری)

کلید عمومی هویت سرور شما را تأیید می‌کند  به کلاینت ثابت می‌کند که با سرور درست صحبت می‌کند. برای دریافت آن، روی سرور بزنید:

```bash
cat server.pub
```

یک رشته ۶۴ کاراکتری مانند این خواهید دید:
```
0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b
```

این رشته کامل ۶۴ کاراکتری را کپی کنید و در فیلد **VayDNS Public Key** در KevinNet بچسبانید.

> کلید عمومی برای اشتراک‌گذاری ایمن است  فقط هویت سرور را تأیید می‌کند. کلید خصوصی (`server.key`) باید فقط روی سرور بماند و هرگز به اشتراک گذاشته نشود.

#### ۵  باینری vaydns-client

درون KevinNet بسته‌بندی شده و به صورت خودکار در پوشه خروجی کپی می‌شود. اگر نبود، بخش [⚠️ باینری نیست؟](#-باینری-نیست) را ببینید.

---

## 🚀 نحوه استفاده  گام به گام

### مرحله ۱  نوع VPN را انتخاب کنید

روی **MasterDNS** یا **VayDNS** در بالای پنل اسکنر کلیک کنید. فقط فیلدها و دکمه ذخیره همان نوع نشان داده می‌شود.

### مرحله ۲  مشخصات را وارد کنید

| فیلد | MasterDNS | VayDNS |
|---|---|---|
| **نام کشور / پوشه** | هر نامی  مثلاً `Iran` | هر نامی  مثلاً `Iran` |
| **دامنه تانل** | مثلاً `v.example.com` | مثلاً `t.example.com` |
| **کلید** | کلید ۳۲ کاراکتری از `encrypt_key.txt` | کلید hex 64 کاراکتری از `server.pub` |

### مرحله ۳  تنظیمات اسکن

| گزینه | پیشنهاد برای ایران | توضیح |
|---|---|---|
| **هدف** | `100` | تعداد Resolver مورد نظر |
| **همزمانی** | `80` | بالاتر از ۱۰۰ نروید |
| **Timeout** | `3 ثانیه` | شبکه‌های ایران کند هستند |
| **پول ×۱۰۰۰** | `200` | ۲۰۰ هزار IP اسکن. اگر کم بود: ۳۰۰–۵۰۰ |

اسکن را ۲-۳ بار تکرار کنید  هر بار IP‌های تصادفی مختلفی تست می‌شود.

### مرحله ۴  شروع اسکن

روی **▶ شروع اسکن** کلیک کنید. سه مرحله خودکار:

- **مرحله ۱**  بررسی سریع زنده بودن همه IP‌ها
- **مرحله ۲**  امتیازدهی ۶ معیاره: ★6/6 ◆4-5 ▸2-3 ·0-1
- **مرحله ۳**  تست E2E واقعی از طریق باینری VPN

🟢 عالی · 🟡 خوب · 🟠 ضعیف · ⚫ خیلی ضعیف

### مرحله ۵  ذخیره در پروفایل‌ها

- **MasterDNS:** روی **💾 ذخیره در MasterDNS** کلیک کنید
- **VayDNS:** روی **💾 ذخیره در VayDNS** کلیک کنید

پروفایل با تنظیمات پیش‌فرض ذخیره می‌شود. باینری VPN به صورت خودکار کپی می‌شود.

### (اختیاری) خروجی لیست DNS

بعد از هر اسکن، دکمه **📤 خروجی لیست DNS** فعال می‌شود — بدون توجه به اینکه MasterDNS یا VayDNS انتخاب کرده‌اید. با کلیک روی آن می‌توانید لیست Resolver های پیدا شده را به عنوان یک فایل `.txt` ساده (یک IP در هر خط) ذخیره کنید. اگر می‌خواهید از این لیست در برنامه دیگری استفاده کنید مفید است.

### (اختیاری) اسکن DoH / DoT — انتقال‌های رمزنگاری شده

دکمه **🔒 اسکن DoH/DoT** (جدید در 3.3.0) لیست منتخبی از endpointهای معروف DNS-over-HTTPS (پورت 443) و DNS-over-TLS (پورت 853) را تست می‌کند. ترافیک شبیه HTTPS معمولی است، پس DPI ایران به سختی می‌تواند آن را به عنوان ترافیک تونل تشخیص دهد. endpointهای کارآمد با آیکون 🔒 در لیست نتایج نمایش داده می‌شوند — هر کدام را می‌توانید به عنوان custom resolver در پروفایل VayDNS استفاده کنید وقتی UDP کار نمی‌کند.

لیست‌ها در فایل‌های `data/doh_endpoints.txt` و `data/dot_endpoints.txt` کنار برنامه قرار دارند. می‌توانید آن‌ها را ویرایش کنید تا endpointهای خصوصی اضافه یا موارد مرده را حذف کنید — نیازی به ساخت دوباره برنامه نیست.

### نکته — راست‌کلیک روی هر Resolver

در لیست نتایج، راست‌کلیک کنید (یا با دو انگشت / Ctrl-کلیک روی مک) تا منوی **کپی IP**، **کپی همه IPها** یا **باز کردن پوشه خروجی** ظاهر شود.

### مرحله ۶  اتصال از تب پروفایل‌ها

روی **📋 MasterDNS Profiles** یا **📋 VayDNS Profiles** در بالای برنامه کلیک کنید.

۱. پروفایل را از لیست انتخاب کنید  نشانگر **5 دقیقه پیش اجرا شد** کمک می‌کند پروفایل فعال فعلی را پیدا کنید
۲. در صورت نیاز تنظیمات را ویرایش کنید و **💾 ذخیره تغییرات** بزنید
۳. روی **🚀 اتصال** کلیک کنید  ترمینال باز می‌شود و VPN شروع می‌کند

پروکسی مرورگر را روی `SOCKS5 127.0.0.1:18000` (MasterDNS) یا `SOCKS5 127.0.0.1:7000` (VayDNS) تنظیم کنید.

---

## 📋 تب پروفایل‌ها  ذخیره، ویرایش و آزمایش مجدد

هر ذخیره یک پروفایل در `masterdns_profiles/` یا `vaydns_profiles/` کنار برنامه می‌سازد.

| دکمه | کار |
|---|---|
| 💾 ذخیره تغییرات | فایل‌های تنظیمات با گزینه‌های فعلی بازنویسی می‌شود |
| 🚀 اتصال | فایل‌ها را بازتولید می‌کند و VPN را راه‌اندازی می‌کند |
| 📋 کپی | پروفایل را کپی می‌کند  برای تست A/B تنظیمات مختلف |
| 🗑 حذف | پروفایل و اختیاراً پوشه خروجی را حذف می‌کند |

---

## 🔧 تنظیمات MasterDNS  معنی هر کدام و مقدار بهینه برای ایران

| تنظیم | بهینه | چرا |
|---|---|---|
| **روش رمزنگاری** | `1  XOR` | کمترین سربار در پکت‌های کوچک DNS. باید با سرور یکسان باشد. |
| **استراتژی بالانس** | `3  Least Loss` | ایران افت پکت بالا و نامتعادل دارد  بهترین Resolver را ترجیح می‌دهد |
| **تکرار بسته** | `2–3` | هر پکت از چند Resolver فرستاده می‌شود  اگر یکی drop کرد، دیگری می‌رسد |
| **Max Upload MTU** | `80–100` | query کوچک‌تر به DPI مشکوک‌تر به نظر نمی‌رسد |
| **Max Download MTU** | `700` | از fragmentation پاسخ‌های DNS توسط ISP جلوگیری می‌کند |
| **Min Upload MTU** | `38` | بیشترین تعداد Resolver را در pool نگه می‌دارد |
| **Min Download MTU** | `400` | Resolverهایی که پاسخ کمی کوچک‌تر برمی‌گردانند حفظ می‌شوند |
| **سطح لاگ** | `INFO` | رویدادهای اتصال را نشان می‌دهد بدون اینکه ترمینال پر شود |

---

## 🔧 تنظیمات VayDNS  معنی هر کدام و مقدار بهینه برای ایران

| تنظیم | بهینه | چرا |
|---|---|---|
| **Transport** | `UDP` | UDP ساده روی پورت ۵۳  مستقیم‌ترین مسیر از ایران |
| **Resolver** | *(خالی)* | همه Resolverهای اسکن‌شده به ترتیب امتحان می‌شوند |
| **Listen Port** | `7000` | پورت محلی که مرورگر/پروکسی به آن وصل می‌شود |
| **Max QNAME Length** | `101` | ~۵۰ بایت MTU upstream، ایمن برای اکثر Resolverهای ایران |
| **Idle Timeout** | `10s` | مدت زمانی که صبر می‌کند تا session را مرده بداند. باید با سرور یکسان باشد. اگر قطعی مکرر دارید `30s` کنید. |
| **Keepalive** | `2s` | هر چند ثانیه یک ping به سرور می‌فرستد. باید کمتر از idle timeout باشد. باید با سرور یکسان باشد. |
| **Record Type** | `txt` | رکورد TXT بیشترین ظرفیت داده و سازگاری با DPI را دارد |
| **Queue Size** | `512` | بافر داخلی پکت  روی اتصال‌های سریع `1024` کنید |
| **UDP Workers** | `100` | تعداد query های UDP همزمان  اگر خطای socket داشتید `50` کنید |
| **Resolver Timeout** | `60s` | اگر یک Resolver در این مدت session برقرار نکرد به بعدی می‌رود |
| **سطح لاگ** | `info` | عملکرد عادی |

**فیلد Resolver:**
- **خالی (توصیه‌شده)**  KevinNet یک اسکریپت launch می‌سازد که همه Resolverهای اسکن‌شده را به ترتیب امتحان می‌کند. اگر یکی گیر کند، بعد از `Resolver Timeout` ثانیه به بعدی می‌رود.
- **یک آدرس**  فقط همان Resolver استفاده می‌شود. فرمت: `8.8.8.8:53` برای UDP · `https://dns.google/dns-query` برای DoH · `dns.google:853` برای DoT.

> **تست از خارج ایران:** Resolverهای اسکن‌شده سرورهای DNS عمومی ایرانی هستند. فقط از **داخل ایران** درست کار می‌کنند. تست از استرالیا، اروپا یا هر جای دیگر خارج از ایران خطاهای NXDOMAIN نشان می‌دهد  آن Resolverها از شبکه خارجی نمی‌توانند به سرور تانل شما دسترسی داشته باشند.

---

## ⚠️ باینری نیست؟

### باینری MasterDnsVPN نیست

> **KevinNet نسخه v3.1.1 به بعد باینری مناسب هر پلتفرم را به صورت خودکار بسته‌بندی می‌کند — ابتدا KevinNet را آپدیت کنید.**

کلاینت را از [صفحه releases مستر](https://github.com/masterking32/MasterDnsVPN/releases/latest) دانلود کنید:

| پلتفرم | لینک |
|---|---|
| 🐧 لینوکس x64 | [MasterDnsVPN_Client_Linux_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Linux_AMD64.zip) |
| 🐧 لینوکس ARM64 | [MasterDnsVPN_Client_Linux_ARM64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Linux_ARM64.zip) |
| 🐧 لینوکس x64 (glibc قدیمی) | [MasterDnsVPN_Client_Linux-Legacy_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Linux-Legacy_AMD64.zip) |
| 🪟 ویندوز AMD64 | [MasterDnsVPN_Client_Windows_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Windows_AMD64.zip) |
| 🪟 ویندوز ARM64 | [MasterDnsVPN_Client_Windows_ARM64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_Windows_ARM64.zip) |
| 🍎 مک Apple Silicon | [MasterDnsVPN_Client_MacOS_ARM64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_MacOS_ARM64.zip) |
| 🍎 مک Intel | [MasterDnsVPN_Client_MacOS_AMD64.zip](https://github.com/masterking32/MasterDnsVPN/releases/latest/download/MasterDnsVPN_Client_MacOS_AMD64.zip) |

۱. ZIP را باز کنید
۲. باینری را به `MasterDnsVPN` (مک/لینوکس) یا `MasterDnsVPN.exe` (ویندوز) تغییر نام دهید
۳. **کنار برنامه KevinNet** بگذارید
۴. دوباره **ذخیره در MasterDNS** کلیک کنید — به صورت خودکار کپی می‌شود

### باینری vaydns-client نیست

از [صفحه releases VayDNS](https://github.com/net2share/vaydns/releases) دانلود کنید.
این نام‌های دقیق را هنگام قرار دادن کنار KevinNet استفاده کنید:

| پلتفرم | نام فایل |
|---|---|
| مک Apple Silicon (M1/M2/M3/M4) | `vaydns-client-darwin-arm64` |
| مک Intel | `vaydns-client-darwin-amd64` |
| لینوکس x64 | `vaydns-client-linux-amd64` |
| لینوکس ARM64 | `vaydns-client-linux-arm64` |
| ویندوز x64 | `vaydns-client_windows_amd64.exe` |

۱. دانلود کنید و به نام دقیق بالا تغییر نام دهید
۲. **کنار برنامه KevinNet** بگذارید
۳. دوباره **ذخیره در VayDNS** کلیک کنید  به صورت خودکار کپی می‌شود

---

---

## 🔍 مشکلات رایج و راه‌حل‌ها

### مشکلات خود برنامه KevinNet

**مک: "KevinNet is damaged and can't be opened" یا "cannot be verified"**
```bash
chmod +x KevinNet_macOS_Universal
xattr -d com.apple.quarantine KevinNet_macOS_Universal
```
یا راست‌کلیک روی برنامه → Open → Open.

**لینوکس: "Permission denied" هنگام اجرا**
```bash
chmod +x KevinNet_Linux_x64
./KevinNet_Linux_x64
```

**ویندوز: آنتی‌ویروس برنامه را مسدود کرد**
این یک false positive است  برنامه‌های کامپایل‌شده با PyInstaller گاهی این مشکل را دارند. یک exception برای فایل اضافه کنید یا از سورس کامپایل کنید (ببینید BUILD_INSTRUCTIONS_FA.txt).

**ویندوز: متن فارسی به صورت حروف جدا از هم نمایش داده می‌شود**
نسخه v3.1.2 به بعد فونت Vazirmatn را به صورت خودکار بارگذاری می‌کند. اگر مشکل داشتید، آخرین نسخه را از [صفحه releases](https://github.com/kamalalhagh/kevinnet-dns/releases/latest) دانلود کنید.

---

### باینری VPN در پوشه نیست

**بعد از ذخیره، پوشه کشور `MasterDnsVPN` یا `vaydns-client` ندارد**

باینری باید **کنار برنامه KevinNet** قرار داشته باشد  KevinNet آن را به پوشه خروجی کپی می‌کند. برای لینک دانلود و نام دقیق فایل‌ها بخش [⚠️ باینری نیست؟](#-باینری-نیست) را ببینید.

**مک: `MasterDnsVPN` هست اما اجرا نمی‌شود**
```bash
chmod +x /path/to/Iran/MasterDnsVPN
xattr -d com.apple.quarantine /path/to/Iran/MasterDnsVPN
```

**مک: `vaydns-client-darwin-arm64` اجرا نمی‌شود**
```bash
chmod +x /path/to/Iran/vaydns-client-darwin-arm64
xattr -d com.apple.quarantine /path/to/Iran/vaydns-client-darwin-arm64
```

---

### اسکن Resolver کم یا صفر پیدا می‌کند

**بعد از اسکن 0 تا 5 Resolver پیدا شد**

- **Pool ×1000** را از `200` به `500` افزایش دهید  IP‌های بیشتر = Resolver بیشتر
- اسکن را **2-3 بار تکرار کنید**  هر بار IP‌های تصادفی مختلفی تست می‌شود
- اگر اسکن خیلی طول می‌کشد، **Timeout** را به `2` ثانیه کاهش دهید
- **Concurrency** را کمی افزایش دهید  اما بالاتر از `100` نروید

**مرحله ۳ (E2E) صفر Resolver تأیید کرد**

مرحله ۳ تانل واقعی را از طریق سرور تست می‌کند. صفر یعنی:
- سرور خاموش یا نادرست تنظیم شده  بررسی کنید در حال اجراست
- DNS دامنه تانل هنوز propagate نشده  تا ۴۸ ساعت صبر کنید
- کلید رمزنگاری با سرور مطابقت ندارد  `encrypt_key.txt` را دوباره بررسی کنید

---

### VPN وصل می‌شود اما اینترنت کار نمی‌کند

**وصل شد اما مرورگر اینترنت ندارد**

- پروکسی مرورگر را روی `SOCKS5 127.0.0.1:18000` (MasterDNS) یا `SOCKS5 127.0.0.1:7000` (VayDNS) تنظیم کنید
- از افزونه Proxy SwitchyOmega در Chrome/Firefox استفاده کنید
- بررسی کنید ترمینال VPN هنوز باز و در حال اجراست

**وصل شد اما خیلی کند است**

برای MasterDNS  مقادیر MTU را کاهش دهید:
- **Max Upload MTU** را به `60–80` کاهش دهید
- **Max Download MTU** را به `600` کاهش دهید
- در تب Profiles ذخیره کنید و دوباره وصل شوید

برای VayDNS:
- **Max QNAME Length** را به `80` کاهش دهید
- **Record Type** را به `null` تغییر دهید (throughput بالاتر در بعضی Resolver‌ها)

---

### مشکلات خاص MasterDNS

**خطای "parse TOML failed" هنگام اجرای MasterDnsVPN**

فایل config دارای placeholder پر نشده است. همیشه از طریق تب Profiles ذخیره کنید. اگر مشکل ادامه داشت:
۱. پوشه کشور را حذف کنید
۲. به تب Profiles بروید و پروفایل را انتخاب کنید
۳. **💾 ذخیره تغییرات** بزنید تا فایل‌ها بازتولید شوند
۴. **🚀 اتصال** بزنید

**قطع و وصل مکرر**

- **Packet Duplication** را به `3` افزایش دهید
- **Balancing Strategy** را به `3  Least Loss` تغییر دهید
- اسکن جدیدی اجرا کنید  Resolver‌های قدیمی ممکن است block شده باشند

**اکثر Resolver‌ها ★1–2 هستند**

این طبیعی است  اکثر DNS عمومی، query های NS delegation سفارشی را forward نمی‌کنند. ۱۰-۳۰ Resolver خوب از اسکن ۲۰۰ هزار IP نتیجه خوبی است.

---

### مشکلات خاص VayDNS

**"noise handshake: timeout" مکرر در ترمینال**

Resolver مقدار NXDOMAIN برمی‌گرداند  نمی‌تواند به سرور تانل دسترسی داشته باشد. اسکریپت بعد از `Resolver Timeout` ثانیه به Resolver بعدی می‌رود. اگر همه Resolver‌ها fail شدند:
- تنظیمات NS دامنه را با `dig v.yourdomain.com NS` بررسی کنید
- **Resolver Timeout** را به `90` ثانیه افزایش دهید

**بعد از Ctrl+C پروسه همچنان در حال اجراست**

این یک مشکل شناخته‌شده بود که در آخرین نسخه برطرف شد. اسکریپت launch اکنون از `trap` برای پاک‌سازی پروسه‌های background استفاده می‌کند. پروفایل را دوباره ذخیره کنید تا اسکریپت به‌روز شود.

**پیام "all resolvers exhausted"**

همه Resolver‌ها در مدت timeout fail شدند:
۱. اسکن جدید اجرا کنید  Resolver‌های DNS ایرانی مرتباً تغییر می‌کنند
۲. در فیلد **Resolver** یک Resolver شناخته‌شده وارد کنید: `8.8.8.8:53`
۳. بررسی کنید سرور در حال اجراست و دامنه تانل درست resolve می‌شود

**تست از خارج ایران  همه Resolver‌ها NXDOMAIN می‌دهند**

این رفتار طبیعی است، نه باگ. Resolver‌های اسکن‌شده سرورهای DNS عمومی ایرانی هستند و فقط از داخل ایران درست کار می‌کنند.

---

### مشکلات DNS و دامنه

**`dig v.yourdomain.com NS` نتیجه‌ای نشان نمی‌دهد**

DNS propagation تا ۴۸ ساعت طول می‌کشد. همچنین بررسی کنید:
- مقدار رکورد NS دقیقاً به همان نامی که رکورد A دارد اشاره کند
- رکورد A در Cloudflare روی DNS only (ابر خاکستری) تنظیم شده باشد

**سرور در حال اجراست اما هیچ Resolver‌ای مرحله ۳ را رد نمی‌کند**

از روی سرور بررسی کنید:
```bash
dig @127.0.0.1 test.v.yourdomain.com A
```
اگر NXDOMAIN برگرداند، سرور درخواست‌های DNS دریافت نمی‌کند. فایروال (پورت ۵۳ UDP باز باشد) و غیرفعال بودن `systemd-resolved` را بررسی کنید.

---

## 🖥️ راه‌اندازی سرور

KevinNet فقط ابزار **سمت کلاینت** است. نصب سرور در ریپوهای رسمی توضیح داده شده:

- **سرور MasterDNS:** 👉 [https://github.com/masterking32/MasterDnsVPN](https://github.com/masterking32/MasterDnsVPN)
- **سرور VayDNS:** 👉 [https://github.com/net2share/vaydns](https://github.com/net2share/vaydns)

---

## 🛠️ کامپایل از سورس

برای مراحل کامل ساخت با PyInstaller ببینید [BUILD_INSTRUCTIONS.txt](BUILD_INSTRUCTIONS.txt) (انگلیسی) یا [BUILD_INSTRUCTIONS_FA.txt](BUILD_INSTRUCTIONS_FA.txt) (فارسی).

### اجرای مجموعه تست‌ها

KevinNet با یک مجموعه تست یونیت (۸۷ تست) که اعتبارسنجی ورودی، توابع کمکی اسکنر، ساخت فایل پیکربندی پروفایل و ماژول تنظیمات را پوشش می‌دهد عرضه می‌شود. تست‌ها در CI قبل از هر release اجرا می‌شوند.

```bash
pip install pytest dnspython pillow
python -m pytest tests/ -v
```

همه تست‌ها باید قبل از ساخت release موفق باشند — workflow CI ساخت‌های مختص پلتفرم را پشت یک اجرای موفق `pytest` نگه می‌دارد.

### ویرایش لیست‌های داده

محدوده‌های CIDR ایران، Resolverهای DNS عمومی، لیست WhiteDNS ایران و لیست‌های endpoint های DoH/DoT به صورت فایل‌های متنی ساده در پوشه `data/` قرار دارند:

| فایل | محتوا |
|---|---|
| `data/iran_cidrs.txt` | محدوده‌های IPv4 ایران که هنگام اسکن نمونه‌گیری می‌شوند |
| `data/public_resolvers.txt` | Resolverهای DNS عمومی معروف (مجموعه گرمایش) |
| `data/white_dns_iran.txt` | Resolverهای ایرانی از قبل تأیید شده (لیست شروع با نرخ موفقیت بالا) |
| `data/doh_endpoints.txt` | endpoint های DNS-over-HTTPS که با دکمه 🔒 اسکن می‌شوند |
| `data/dot_endpoints.txt` | endpoint های DNS-over-TLS که با دکمه 🔒 اسکن می‌شوند |

می‌توانید این فایل‌ها را برای اضافه کردن endpointهای خصوصی یا حذف موارد مرده ویرایش کنید — نیازی به ساخت دوباره نیست. PyInstaller هنگام ساخت آن‌ها را داخل باینری کپی می‌کند، و برنامه همچنین به دنبال یک پوشه `data/` کنار فایل اجرایی می‌گردد تا ویرایش‌های کاربر بر کپی بسته‌بندی شده اولویت داشته باشند.

---

## 🙏 تقدیر و تشکر

**MasterDnsVPN** توسط MasterkinG32 (Amin Mahmoudi)  [GitHub](https://github.com/masterking32/MasterDnsVPN)  مجوز MIT

**VayDNS** توسط net2share  [GitHub](https://github.com/net2share/vaydns)  فورک از dnstt توسط David Fifield (دامنه عمومی)

برای متن کامل مجوزها ببینید [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

---

## ⭐ حمایت از این پروژه

- **⭐ ستاره بدید**  به دیگران کمک می‌کند پیداش کنند
- **اشتراک بگذارید** با کسانی که در ایران به اینترنت آزاد نیاز دارند
- **باگ گزارش کنید** از طریق GitHub Issues

هر ستاره و اشتراک‌گذاری به رسیدن این ابزار به یک خانواده دیگر کمک می‌کند.

---

## ⚖️ مجوز و سلب مسئولیت

حق چاپ © ۲۰۲۶ Kevin Haji  [مجوز MIT](LICENSE)  ببینید [DISCLAIMER_FA.md](DISCLAIMER_FA.md)

</div>
