import os
import re
import threading
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import scrolledtext
from pathlib import Path
from send2trash import send2trash

class KopyaTemizleyiciApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulut Disk Kopyaları Temizleyici - Pro")
        self.root.geometry("700x640")
        self.root.resizable(False, False)

        # --- Klasör Seçimi ---
        tk.Label(root, text="Kök Klasör:", font=("Arial", 10, "bold")).place(x=20, y=20)
        self.klasor_yolu = tk.StringVar()
        self.klasor_entry = tk.Entry(root, textvariable=self.klasor_yolu, width=55, state="readonly")
        self.klasor_entry.place(x=105, y=20)
        tk.Button(root, text="Gözat...", command=self.klasor_sec).place(x=450, y=16)

        # --- Uzantı ve Paket Seçimi ---
        tk.Label(root, text="Uzantılar:", font=("Arial", 10, "bold")).place(x=20, y=60)
        
        self.uzanti_yolu = tk.StringVar()
        self.uzanti_entry = tk.Entry(root, textvariable=self.uzanti_yolu, width=40)
        self.uzanti_entry.place(x=105, y=60)
        
        # Hariç Tut Checkbox'ı
        self.haric_tut_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Hariç Tut", variable=self.haric_tut_var, font=("Arial", 9, "bold"), fg="red").place(x=360, y=58)

        # Hazır Paketler Combobox'ı
        tk.Label(root, text="Hazır Paket:", font=("Arial", 9, "bold")).place(x=450, y=60)
        self.paket_secim = ttk.Combobox(root, values=[
            "Manuel Giriş", 
            "İmaj Dosyaları", 
            "Video Dosyaları", 
            "İmaj + Video"
        ], state="readonly", width=15)
        self.paket_secim.current(0)
        self.paket_secim.place(x=530, y=60)
        self.paket_secim.bind("<<ComboboxSelected>>", self.paket_degisti)

        tk.Label(root, text="(Örn: pdf, txt, jpg - Tüm dosyalar için boş bırakın)", font=("Arial", 8), fg="gray").place(x=105, y=85)

        # --- Güvenlik Ayarları ---
        tk.Label(root, text="Ayarlar:", font=("Arial", 10, "bold")).place(x=20, y=120)
        
        self.orijinal_sart = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Orijinal dosyası (parantezsiz hali) aynı klasörde bulunmak zorunda", variable=self.orijinal_sart).place(x=100, y=120)

        self.boyut_sart = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Boyutlar (byte) tamamen aynı olmak zorunda", variable=self.boyut_sart).place(x=100, y=145)

        # --- Sorumluluk Reddi (Disclaimer) ---
        self.onay_var = tk.BooleanVar(value=False)
        onay_metni = "Olası veri kayıplarından geliştiricinin sorumlu olmadığını ve tüm sorumluluğun bana ait olduğunu kabul ediyorum."
        self.onay_cb = tk.Checkbutton(root, text=onay_metni, variable=self.onay_var, font=("Arial", 9, "bold"), fg="#d32f2f")
        self.onay_cb.place(x=20, y=180)

        # --- Butonlar ---
        self.baslat_btn = tk.Button(root, text="Temizlemeyi Başlat", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", command=self.islem_baslat)
        self.baslat_btn.place(x=160, y=215, width=160, height=35)

        self.durdur_btn = tk.Button(root, text="Durdur", font=("Arial", 10, "bold"), bg="#f44336", fg="white", state="disabled", command=self.islem_durdur)
        self.durdur_btn.place(x=340, y=215, width=160, height=35)

        # --- Durum ve Animasyon Etiketi ---
        self.durum_etiketi = tk.Label(root, text="Hazır", font=("Arial", 9, "bold"), fg="green")
        self.durum_etiketi.place(x=240, y=260)
        self.islem_suruyor = False
        self.iptal_edildi = False
        self.animasyon_sayaci = 0

        # --- Log Ekranı ---
        tk.Label(root, text="İşlem Geçmişi:", font=("Arial", 10, "bold")).place(x=20, y=265)
        self.log_ekrani = scrolledtext.ScrolledText(root, width=80, height=14, font=("Consolas", 9))
        self.log_ekrani.place(x=20, y=290)

        # --- GELİŞTİRİCİ / REKLAM ALANI ---
        ttk.Separator(root, orient='horizontal').place(x=0, y=590, relwidth=1)
        
        tk.Label(root, text="Geliştirici: hgumuskaya", font=("Arial", 9, "italic"), fg="#555555").place(x=20, y=605)
        
        self.link_etiketi = tk.Label(root, text="GitHub Proje Sayfası", font=("Arial", 9, "bold"), fg="blue", cursor="hand2")
        self.link_etiketi.place(x=520, y=605)
        self.link_etiketi.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/hgumuskaya/bulut-disk-kopyalari-temizleyici"))
        self.link_etiketi.bind("<Enter>", lambda e: self.link_etiketi.config(font=("Arial", 9, "bold", "underline")))
        self.link_etiketi.bind("<Leave>", lambda e: self.link_etiketi.config(font=("Arial", 9, "bold")))

    def klasor_sec(self):
        secilen = filedialog.askdirectory(title="Kök Klasörü Seçin")
        if secilen:
            self.klasor_yolu.set(secilen)

    def paket_degisti(self, event):
        secim = self.paket_secim.get()
        if secim == "İmaj Dosyaları":
            self.uzanti_yolu.set("jpg, jpeg, png, gif, bmp, tiff, tif, webp")
        elif secim == "Video Dosyaları":
            self.uzanti_yolu.set("mp4, avi, mkv, mov, wmv, flv, webm")
        elif secim == "İmaj + Video":
            self.uzanti_yolu.set("jpg, jpeg, png, gif, bmp, tiff, tif, webp, mp4, avi, mkv, mov, wmv, flv, webm")
        elif secim == "Manuel Giriş":
            self.uzanti_yolu.set("")

    def log_yaz(self, mesaj):
        self.log_ekrani.insert(tk.END, mesaj + "\n")
        self.log_ekrani.see(tk.END)

    def animasyon_oynat(self):
        if self.islem_suruyor and not self.iptal_edildi:
            noktalar = "." * (self.animasyon_sayaci % 4)
            self.durum_etiketi.config(text=f"İşlem devam ediyor, lütfen bekleyiniz{noktalar}", fg="red")
            self.animasyon_sayaci += 1
            self.root.after(500, self.animasyon_oynat)

    def islem_durdur(self):
        self.iptal_edildi = True
        self.durdur_btn.config(state="disabled", bg="gray")
        self.durum_etiketi.config(text="Durduruluyor...", fg="orange")
        self.log_yaz(">>> DURDURMA İSTEĞİ ALINDI, MEVCUT İŞLEMLER KESİLİYOR... <<<")

    def islem_baslat(self):
        klasor = self.klasor_yolu.get()
        if not klasor:
            messagebox.showwarning("Uyarı", "Lütfen önce bir kök klasör seçin!")
            return
            
        if not self.onay_var.get():
            messagebox.showerror("Onay Gerekli", "Lütfen işleme başlamadan önce sorumluluk reddi bildirimini onaylayın!")
            return

        self.baslat_btn.config(state="disabled", bg="gray")
        self.durdur_btn.config(state="normal", bg="#f44336")
        self.onay_cb.config(state="disabled")
        
        self.log_ekrani.delete(1.0, tk.END) 
        
        self.islem_suruyor = True
        self.iptal_edildi = False
        self.animasyon_sayaci = 0
        self.animasyon_oynat()

        threading.Thread(target=self.kopyalari_cope_at, args=(klasor,), daemon=True).start()

    def kopyalari_cope_at(self, kok_klasor):
        ham_uzantilar = self.uzanti_yolu.get().strip()
        gecerli_uzantilar = []
        if ham_uzantilar:
            parcalar = [u.strip().lower() for u in ham_uzantilar.split(',')]
            for u in parcalar:
                if u:
                    if not u.startswith('.'):
                        u = f".{u}"
                    gecerli_uzantilar.append(u)

        haric_tut = self.haric_tut_var.get()
        desen = re.compile(r' \(\d+\)$')
        temizlenen_dosya_sayisi = 0

        self.log_yaz(f"Tarama başlatıldı: {kok_klasor}")
        
        if gecerli_uzantilar:
            mod_metni = "HARİÇ TUTULANLAR" if haric_tut else "SADECE DAHİL EDİLENLER"
            self.log_yaz(f"Filtre Modu: {mod_metni} -> {', '.join(gecerli_uzantilar)}")
        else:
            self.log_yaz("Filtre Modu: TÜM DOSYALAR")
            
        self.log_yaz("-" * 50)

        # Klasör erişim hatalarını yakalayan callback fonksiyonu
        def klasor_hata_yakala(error):
            self.log_yaz(f"[UYARI/ATLANDI] Erişim engellendi: {error.filename}")

        # Windows sistem korumalı dizinleri
        atlanacak_dizinler = {"$recycle.bin", "system volume information", "recovery"}

        try:
            # os.walk kullanarak hataları yakalayıp taramaya devam ediyoruz
            for kok, dizinler, dosyalar in os.walk(kok_klasor, onerror=klasor_hata_yakala):
                if self.iptal_edildi:
                    self.log_yaz("-" * 50)
                    self.log_yaz("KULLANICI İŞLEMİ İPTAL ETTİ!")
                    break

                # Sistem korumalı klasörleri tarama dışı bırak
                dizinler[:] = [d for d in dizinler if d.lower() not in atlanacak_dizinler]

                for dosya_adi_tam in dosyalar:
                    if self.iptal_edildi:
                        break

                    dosya_yolu = Path(kok) / dosya_adi_tam
                    dosya_uzantisi = dosya_yolu.suffix.lower()

                    if gecerli_uzantilar:
                        if haric_tut and (dosya_uzantisi in gecerli_uzantilar):
                            continue
                        elif not haric_tut and (dosya_uzantisi not in gecerli_uzantilar):
                            continue

                    dosya_kok_adi = dosya_yolu.stem
                    eslesme = desen.search(dosya_kok_adi)

                    if eslesme:
                        orijinal_isim = dosya_kok_adi[:eslesme.start()] + dosya_yolu.suffix
                        orijinal_yol = dosya_yolu.parent / orijinal_isim

                        silme_izni = True

                        try:
                            # 1. Kural: Orijinal dosya şartı
                            if self.orijinal_sart.get() and not orijinal_yol.exists():
                                silme_izni = False

                            # 2. Kural: Boyut şartı
                            if silme_izni and self.boyut_sart.get():
                                if orijinal_yol.exists():
                                    kopya_boyut = os.path.getsize(dosya_yolu)
                                    orijinal_boyut = os.path.getsize(orijinal_yol)
                                    if kopya_boyut != orijinal_boyut:
                                        silme_izni = False
                                else:
                                    silme_izni = False

                            if silme_izni:
                                send2trash(str(dosya_yolu))
                                self.log_yaz(f"[SİLİNDİ] {dosya_yolu.name}")
                                temizlenen_dosya_sayisi += 1

                        except PermissionError:
                            self.log_yaz(f"[HATA - YETKİ YOK] {dosya_yolu.name} silinemedi (Erişim engellendi).")
                        except Exception as e:
                            self.log_yaz(f"[HATA] {dosya_yolu.name}: {e}")

            self.log_yaz("-" * 50)
            if self.iptal_edildi:
                self.log_yaz(f"İptal edilene kadar toplam {temizlenen_dosya_sayisi} dosya çöp kutusuna taşındı.")
                messagebox.showinfo("İptal Edildi", f"İşlem durduruldu!\nO ana kadar {temizlenen_dosya_sayisi} adet dosya temizlendi.")
            else:
                self.log_yaz(f"İşlem tamamlandı! Toplam {temizlenen_dosya_sayisi} dosya çöp kutusuna taşındı.")
                messagebox.showinfo("Tamamlandı", f"İşlem bitti!\n{temizlenen_dosya_sayisi} adet dosya çöp kutusuna taşındı.")

        except Exception as e:
            self.log_yaz(f"Beklenmeyen bir hata oluştu: {e}")
        finally:
            self.islem_suruyor = False
            self.baslat_btn.config(state="normal", bg="#4CAF50")
            self.durdur_btn.config(state="disabled", bg="gray")
            self.onay_cb.config(state="normal")

            if self.iptal_edildi:
                self.durum_etiketi.config(text="İptal Edildi", fg="orange")
            else:
                self.durum_etiketi.config(text="Tamamlandı!", fg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = KopyaTemizleyiciApp(root)
    root.mainloop()
