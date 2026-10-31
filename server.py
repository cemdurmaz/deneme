"""
Hesap makinesi web uygulamasını yerel olarak başlatan Python sunucusu.
"""

import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8000


class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Önbelleğe almayı kapatarak güncellemelerin anında görünmesini sağla
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def log_message(self, format, *args):
        # Temiz konsol çıktısı
        return


def baslat():
    dizin = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dizin)

    sunucu_adresi = ("", PORT)
    try:
        httpd = HTTPServer(sunucu_adresi, CustomHandler)
    except OSError:
        # Eğer 8000 portu meşgulse alternatif bir port dene
        alternatif_port = 8080
        httpd = HTTPServer(("", alternatif_port), CustomHandler)
        url = f"http://localhost:{alternatif_port}"
    else:
        url = f"http://localhost:{PORT}"

    print("=" * 55)
    print("      GÖRSEL 4 İŞLEM HESAP MAKİNESİ SUNUCUSU")
    print("=" * 55)
    print(f">> Uygulama adresi: {url}")
    print(">> Tarayıcınız açılıyor...")
    print(">> Durdurmak için bu pencerede Ctrl + C tuşlayın.")
    print("=" * 55)

    webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu durduruldu.")
        httpd.server_close()


if __name__ == "__main__":
    baslat()
