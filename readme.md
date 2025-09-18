# File Sender App — Repository Skeleton

## Dosya Yapısı
```
file-sender-app/
├─ README.md               # English README
├─ README_TR.md            # Türkçe README
├─ LICENSE                 # MIT License
├─ .gitignore
├─ src/
│  ├─ file_sender_human.py # Main application
│  └─ __init__.py
└─ examples/
   └─ sample_config.md
```

---

## README.md (English)

# File Sender App

## Description
This is a simple desktop application that allows a user to send files via their own email account. By entering SMTP settings, email address, and password (or an application-specific password), the user can send selected files to one or more recipients.

## Features
- Support for SMTP server and port (SSL 465, TLS 587)
- Send email to multiple recipients
- Add, remove, and clear attachments
- Subject and message support
- Simple and user-friendly interface (Tkinter)

## Requirements
- Python 3.8 or higher
- Tkinter (on Linux: `sudo apt install python3-tk`)

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/file-sender-app.git
   cd file-sender-app
   ```
2. Run the application:
   ```bash
   python src/file_sender_human.py
   ```

## Notes
- If you are using Gmail, you may need to create an application password.
- For Outlook, typically `smtp.office365.com` with port `587` works.
- This application is designed only for use with the user’s explicit consent.

---

## README_TR.md (Türkçe)

# Dosya Gönderici Uygulaması

## Açıklama
Bu uygulama, kullanıcının kendi e-posta hesabını kullanarak dosya göndermesini sağlayan basit bir masaüstü programıdır. SMTP bilgilerini, e-posta adresini ve şifreyi (veya uygulama şifresini) girerek seçilen dosyaları bir veya birden fazla alıcıya gönderebilir.

## Özellikler
- SMTP sunucu ve port desteği (SSL 465, TLS 587)
- Birden fazla alıcıya gönderim
- Dosya ekleme, kaldırma ve temizleme
- Konu ve mesaj desteği
- Basit ve kullanıcı dostu arayüz (Tkinter)

## Gereksinimler
- Python 3.8 veya üzeri
- Tkinter (Linux: `sudo apt install python3-tk`)

## Çalıştırma
1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/kullanici_adi/file-sender-app.git
   cd file-sender-app
   ```
2. Uygulamayı çalıştırın:
   ```bash
   python src/file_sender_human.py
   ```

## Notlar
- Gmail kullanıyorsanız uygulama şifresi oluşturmanız gerekebilir.
- Outlook için `smtp.office365.com` ve port `587` genelde çalışır.
- Bu uygulama yalnızca kullanıcının açık rızası ile kullanılmalıdır.

---

## LICENSE (MIT)

MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## .gitignore (suggestion)

```
__pycache__/
*.pyc
dist/
build/
*.egg-info/
.env
.env.*
.vscode/
.DS_Store
```



