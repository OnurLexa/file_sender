import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from email.message import EmailMessage
import smtplib
import ssl
import os
from typing import List


# ---------------------------
# Helper / Util fonksiyonları
# ---------------------------
def human_readable_filename(path: str) -> str:
    try:
        return os.path.basename(path)
    except Exception:
        return path


def validate_port(value: str) -> int:
    try:
        p = int(value.strip())
        if p <= 0 or p > 65535:
            raise ValueError("Port aralığı 1-65535 olmalı.")
        return p
    except Exception as e:
        raise ValueError(f"Geçersiz port: {e}")


def split_recipients(raw: str) -> List[str]:
    return [r.strip() for r in raw.split(",") if r.strip()]


# ---------------------------
# Temel gönderme işlemi
# ---------------------------
def send_mail_via_smtp(
    smtp_host: str,
    smtp_port: int,
    sender: str,
    password: str,
    recipients: List[str],
    subject: str,
    body: str,
    attachments: List[str],
    timeout: int = 30,
):
    """SMTP üzerinden e-posta gönderir. Hata fırlatırsa çağıran yakalar."""
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject or "(No Subject)"
    msg.set_content(body or "")

    # Ekleri ekle
    for p in attachments:
        try:
            with open(p, "rb") as fh:
                data = fh.read()
            # tipi basitçe application/octet-stream olarak ekliyoruz
            filename = human_readable_filename(p)
            msg.add_attachment(data, maintype="application", subtype="octet-stream", filename=filename)
        except Exception as e:
            raise RuntimeError(f"Ek dosya okunamadı: {p}  —  {e}")

    # Bağlantı ve gönderim
    if smtp_port == 465:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=timeout) as server:
            server.login(sender, password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=timeout) as server:
            server.ehlo()
            # STARTTLS var mı kontrol et, varsa güvenli hale getir
            if server.has_extn("STARTTLS"):
                context = ssl.create_default_context()
                server.starttls(context=context)
                server.ehlo()
            server.login(sender, password)
            server.send_message(msg)


# ---------------------------
# GUI: Tkinter uygulaması
# ---------------------------
class FileSenderGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Dosya Gönderici")
        root.geometry("700x520")
        root.minsize(640, 480)

        self._attachments: List[str] = []

        # Üst alan: SMTP ve kimlik
        top = tk.Frame(root, padx=10, pady=8)
        top.pack(fill="x")

        tk.Label(top, text="SMTP Sunucu:").grid(row=0, column=0, sticky="w")
        self.smtp_entry = tk.Entry(top)
        self.smtp_entry.insert(0, "smtp.gmail.com")
        self.smtp_entry.grid(row=0, column=1, sticky="we", padx=6)

        tk.Label(top, text="Port (SSL=465/TLS=587):").grid(row=1, column=0, sticky="w")
        self.port_entry = tk.Entry(top)
        self.port_entry.insert(0, "465")
        self.port_entry.grid(row=1, column=1, sticky="we", padx=6)

        tk.Label(top, text="Gönderen e-posta:").grid(row=2, column=0, sticky="w")
        self.from_entry = tk.Entry(top)
        self.from_entry.grid(row=2, column=1, sticky="we", padx=6)

        tk.Label(top, text="Parola / Uygulama şifresi:").grid(row=3, column=0, sticky="w")
        self.pass_entry = tk.Entry(top, show="*")
        self.pass_entry.grid(row=3, column=1, sticky="we", padx=6)

        top.columnconfigure(1, weight=1)

        # Orta bölüm: alıcı, konu, mesaj
        mid = tk.Frame(root, padx=10, pady=6)
        mid.pack(fill="both", expand=False)

        tk.Label(mid, text="Alıcı(lar) (virgülle ayır):").pack(anchor="w")
        self.to_entry = tk.Entry(mid)
        self.to_entry.pack(fill="x", pady=3)

        tk.Label(mid, text="Konu:").pack(anchor="w", pady=(6,0))
        self.subject_entry = tk.Entry(mid)
        self.subject_entry.pack(fill="x", pady=3)

        tk.Label(mid, text="Mesaj:").pack(anchor="w", pady=(6,0))
        self.msg_text = scrolledtext.ScrolledText(mid, height=8)
        self.msg_text.pack(fill="both", pady=3)

        # Ekler listesi ve butonlar
        attach_frame = tk.Frame(root, padx=10, pady=6)
        attach_frame.pack(fill="both", expand=False)

        self.attach_listbox = tk.Listbox(attach_frame, height=7)
        self.attach_listbox.pack(side="left", fill="both", expand=True)

        right_buttons = tk.Frame(attach_frame)
        right_buttons.pack(side="right", fill="y", padx=8)

        tk.Button(right_buttons, text="Dosya Ekle", width=16, command=self._on_add_files).pack(pady=4)
        tk.Button(right_buttons, text="Seçiliyi Kaldır", width=16, command=self._on_remove_selected).pack(pady=4)
        tk.Button(right_buttons, text="Tümünü Temizle", width=16, command=self._on_clear).pack(pady=4)

        # Gönder butonu
        action_frame = tk.Frame(root, padx=10, pady=8)
        action_frame.pack(fill="x")
        tk.Button(action_frame, text="Gönder", height=2, command=self._on_send).pack(fill="x")

        # Durum satırı
        self.status = tk.Label(root, text="Hazır", anchor="w", relief="sunken")
        self.status.pack(fill="x", padx=10, pady=(6,10))

    # -------------
    # GUI eventleri
    # -------------
    def _on_add_files(self):
        paths = filedialog.askopenfilenames(title="Göndermek istediğiniz dosyaları seçin")
        if not paths:
            return
        added = 0
        for p in paths:
            if p not in self._attachments:
                self._attachments.append(p)
                self.attach_listbox.insert("end", human_readable_filename(p))
                added += 1
        if added:
            self._set_status(f"{added} dosya eklendi.")

    def _on_remove_selected(self):
        sel = list(self.attach_listbox.curselection())
        if not sel:
            return
        for i in reversed(sel):
            del self._attachments[i]
            self.attach_listbox.delete(i)
        self._set_status("Seçili ekler kaldırıldı.")

    def _on_clear(self):
        if not self._attachments:
            return
        if messagebox.askyesno("Onay", "Tüm ekleri kaldırmak istiyor musunuz?"):
            self._attachments.clear()
            self.attach_listbox.delete(0, "end")
            self._set_status("Ekler temizlendi.")

    def _set_status(self, text: str):
        self.status.config(text=text)
        self.root.update_idletasks()

    def _on_send(self):
        # Bilgileri al
        smtp = self.smtp_entry.get().strip()
        port_raw = self.port_entry.get().strip()
        sender = self.from_entry.get().strip()
        password = self.pass_entry.get()
        recipients_raw = self.to_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.msg_text.get("1.0", "end").strip()

        # Basit doğrulamalar
        try:
            port = validate_port(port_raw)
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            return

        recipients = split_recipients(recipients_raw)
        if not smtp or not sender or not password or not recipients:
            messagebox.showerror("Hata", "SMTP, gönderici, parola ve en az bir alıcı bilgisi gerekli.")
            return

        if not self._attachments:
            if not messagebox.askyesno("Onay", "Ek dosya yok — yine de gönderilsin mi?"):
                return

        # Kullanıcı onayı (kısa)
        ok = messagebox.askyesno("Gönderimi Onayla", f"{len(self._attachments)} ek ile e-posta gönderilsin mi?")
        if not ok:
            return

        # Gönderme işlemi
        self._set_status("Gönderiliyor...")
        try:
            send_mail_via_smtp(
                smtp_host=smtp,
                smtp_port=port,
                sender=sender,
                password=password,
                recipients=recipients,
                subject=subject,
                body=body,
                attachments=self._attachments,
            )
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Kimlik Hatası", "E-posta kimlik doğrulaması başarısız. Parola/uygulama şifresini kontrol edin.")
            self._set_status("Hazır")
            return
        except Exception as e:
            messagebox.showerror("Gönderim Hatası", f"E-posta gönderilemedi:\n{e}")
            self._set_status("Hazır")
            return

        self._set_status("Gönderildi.")
        messagebox.showinfo("Tamamlandı", "E-posta başarıyla gönderildi.")
        # istersen ekleri temizleyebilirsin:
        # self._on_clear()


def main():
    root = tk.Tk()
    app = FileSenderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
