# bulut-disk-kopyalari-temizleyici
Bulut Disk Kopyaları Temizleyici (Cloud Duplicate Cleaner)

☁️ Bulut Disk Kopyaları Temizleyici (Cloud Duplicate Cleaner)

Google Drive, OneDrive, Dropbox, iCloud vb. bulut depolama servislerinin senkronizasyon çatışmaları veya tekrarlı indirmeler sonucu oluşturduğu kopya dosyaları (dosya (1).txt, resim (2).jpg) akıllı filtreleme ve güvenlik kurallarıyla tespit edip Geri Dönüşüm Kutusu'na taşıyan masaüstü aracı.

📸 Genel Bakış

Dosyaları kalıcı olarak silmez; send2trash kütüphanesi sayesinde güvenle işletim sisteminin çöp kutusuna taşır.

Tkinter tabanlı sade, kilitlenmeyen (multi-thread) Windows grafik arayüzü sunar.

⚡ Temel Özellikler

Çift Katmanlı Doğrulama:

Orijinal Dosya Şartı: dosya (1).ext dosyasının silinmesi için aynı dizinde mutlaka parantezsiz orijinal hali (dosya.ext) aranır.

Birebir Boyut Eşleşmesi (Opsiyonel): İsteğe bağlı olarak kopya dosya ile ana dosyanın bayt cinsinden tam eşleşmesi şart koşulabilir.

Gelişmiş Uzantı Filtresi:

Dahil Et Modu: Sadece belirtilen uzantıları arar (Örn: pdf, txt).

Hariç Tut Modu: Belirtilen uzantılara dokunmaz, kalan tüm dosyaları tarar (Örn: exe, sys, dll).

Hazır Dosya Paketleri:

İmaj Dosyaları: jpg, jpeg, png, gif, bmp, tiff, tif, webp

Video Dosyaları: mp4, avi, mkv, mov, wmv, flv, webm

İmaj + Video: Tüm görsel ve video formatlarını tek tıkla yükler.

Güvenlik ve Kontrol:

Canlı Durum Animasyonu & Konsol: Taranan ve silinen her dosyayı anlık olarak listeler.

Anında Durdurma (İptal): İstendiğinde tarama ve temizleme işlemi güvenle yarıda kesilebilir.

Sorumluluk Bildirimi Onayı: Yanlışlıkla işlem başlatılmasını önleyen zorunlu kullanıcı onay mekanizması.

🚀 Kurulum ve Çalıştırma

1. Python ile Çalıştırma

Depoyu klonlayın:

git clone https://github.com/hgumuskaya/bulut-disk-kopyalari-temizleyici.git
cd bulut-disk-kopyalari-temizleyici


Gerekli bağımlılığı yükleyin:

pip install send2trash


Uygulamayı başlatın:

python main.py


📦 Tek Parça (.exe) Olarak Paketleme

Python kurulu olmayan bilgisayarlarda doğrudan çalıştırmak için PyInstaller ile derleyebilirsiniz:

pip install pyinstaller
pyinstaller --noconsole --onefile main.py


Derleme tamamlandığında oluşan bağımsız çalıştırılabilir dosya dist/main.exe yolunda yer alacaktır.

⚠️ Sorumluluk Reddi (Disclaimer)

Bu yazılım açık kaynaklıdır ve "olduğu gibi" sağlanır. Dosyalar her ne kadar doğrudan yok edilmeyip çöp kutusuna taşınsa da, işlem başlatmadan önce kritik verilerinizin yedeğini almanız önerilir. Olası veri kayıplarından yazılım geliştiricisi sorumlu tutulamaz.

📄 Lisans

Bu proje MIT Lisansı altında dağıtılmaktadır. Dilediğiniz gibi kullanabilir, değiştirebilir ve geliştirebilirsiniz.
