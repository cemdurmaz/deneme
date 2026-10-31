"""
Sadece 4 işlem (+, -, *, /) yapabilen modern grafik arayüzlü (Tkinter) hesap makinesi uygulaması.
"""

import tkinter as tk


class HesapMakinesiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("4 İşlem Hesap Makinesi")
        self.root.geometry("360x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#181825")

        # Pencereyi ekranın ortasında aç
        self.pencereyi_ortala(360, 520)

        self.ifade = ""
        self.gecmis = ""

        # Arayüz bileşenlerini oluştur
        self.arayuz_olustur()

        # Klavye desteğini bağla
        self.root.bind("<Key>", self.klavye_yakala)

    def pencereyi_ortala(self, genislik, yukseklik):
        self.root.update_idletasks()
        ekran_g = self.root.winfo_screenwidth()
        ekran_y = self.root.winfo_screenheight()
        x = (ekran_g - genislik) // 2
        y = (ekran_y - yukseklik) // 2
        self.root.geometry(f"{genislik}x{yukseklik}+{x}+{y}")

    def arayuz_olustur(self):
        # Ekran Çerçevesi
        ekran_kapsayici = tk.Frame(self.root, bg="#11111b", padx=16, pady=16)
        ekran_kapsayici.pack(fill="x", padx=14, pady=(14, 10))

        # Üst Küçük Geçmiş Etiketi
        self.gecmis_degiskeni = tk.StringVar(value="")
        self.gecmis_etiketi = tk.Label(
            ekran_kapsayici,
            textvariable=self.gecmis_degiskeni,
            font=("Segoe UI", 12),
            bg="#11111b",
            fg="#6c7086",
            anchor="e",
        )
        self.gecmis_etiketi.pack(fill="x")

        # Ana Ekran / Sonuç
        self.ekran_degiskeni = tk.StringVar(value="0")
        self.ana_ekran = tk.Label(
            ekran_kapsayici,
            textvariable=self.ekran_degiskeni,
            font=("Segoe UI", 32, "bold"),
            bg="#11111b",
            fg="#cdd6f4",
            anchor="e",
        )
        self.ana_ekran.pack(fill="x", pady=(4, 0))

        # Buton Izgarası Çerçevesi
        izgara = tk.Frame(self.root, bg="#181825", padx=10, pady=5)
        izgara.pack(fill="both", expand=True, padx=4, pady=(0, 10))

        # Buton tanımları: (Metin, Satır, Sütun, Arka Plan, Yazı Rengi, Sütun Genişliği)
        butonlar = [
            ("C", 0, 0, "#f38ba8", "#11111b", 2),
            ("⌫", 0, 2, "#fab387", "#11111b", 1),
            ("÷", 0, 3, "#89b4fa", "#11111b", 1),
            ("7", 1, 0, "#313244", "#cdd6f4", 1),
            ("8", 1, 1, "#313244", "#cdd6f4", 1),
            ("9", 1, 2, "#313244", "#cdd6f4", 1),
            ("×", 1, 3, "#89b4fa", "#11111b", 1),
            ("4", 2, 0, "#313244", "#cdd6f4", 1),
            ("5", 2, 1, "#313244", "#cdd6f4", 1),
            ("6", 2, 2, "#313244", "#cdd6f4", 1),
            ("-", 2, 3, "#89b4fa", "#11111b", 1),
            ("1", 3, 0, "#313244", "#cdd6f4", 1),
            ("2", 3, 1, "#313244", "#cdd6f4", 1),
            ("3", 3, 2, "#313244", "#cdd6f4", 1),
            ("+", 3, 3, "#89b4fa", "#11111b", 1),
            ("0", 4, 0, "#313244", "#cdd6f4", 2),
            (".", 4, 2, "#313244", "#cdd6f4", 1),
            ("=", 4, 3, "#a6e3a1", "#11111b", 1),
        ]

        for i in range(5):
            izgara.rowconfigure(i, weight=1)
        for j in range(4):
            izgara.columnconfigure(j, weight=1)

        self.buton_nesneleri = {}
        for metin, satir, sutun, bg_renk, fg_renk, span in butonlar:
            btn = tk.Button(
                izgara,
                text=metin,
                font=("Segoe UI", 16, "bold"),
                bg=bg_renk,
                fg=fg_renk,
                activebackground="#45475a",
                activeforeground="#ffffff",
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda t=metin: self.butona_tiklandi(t),
            )
            btn.grid(
                row=satir,
                column=sutun,
                columnspan=span,
                sticky="nsew",
                padx=4,
                pady=4,
            )
            self.buton_hover_efekti_ekle(btn, bg_renk)
            self.buton_nesneleri[metin] = btn

    def buton_hover_efekti_ekle(self, buton, normal_renk):
        # Hover parlama efekti
        hover_renk = "#585b70" if normal_renk == "#313244" else normal_renk
        buton.bind("<Enter>", lambda e: buton.config(bg=hover_renk))
        buton.bind("<Leave>", lambda e: buton.config(bg=normal_renk))

    def klavye_yakala(self, event):
        tus = event.char
        sembol_eslestirme = {
            "/": "÷",
            "*": "×",
            "\r": "=",
            "\x08": "⌫",
            "\x1b": "C",
        }

        if tus in "0123456789+-.",:
            if tus == ",":
                tus = "."
            self.butona_tiklandi(tus)
        elif tus in sembol_eslestirme:
            self.butona_tiklandi(sembol_eslestirme[tus])
        elif event.keysym in ("Return", "KP_Enter"):
            self.butona_tiklandi("=")
        elif event.keysym == "BackSpace":
            self.butona_tiklandi("⌫")
        elif event.keysym == "Escape":
            self.butona_tiklandi("C")

    def butona_tiklandi(self, tus):
        if tus == "C":
            self.ifade = ""
            self.gecmis = ""
            self.gecmis_degiskeni.set("")
            self.ekran_degiskeni.set("0")

        elif tus == "⌫":
            if self.ifade:
                self.ifade = self.ifade[:-1]
                self.ekran_degiskeni.set(self.ifade if self.ifade else "0")

        elif tus == "=":
            self.hesapla()

        elif tus in ["+", "-", "×", "÷"]:
            if not self.ifade:
                if tus == "-":
                    self.ifade = "-"
                    self.ekran_degiskeni.set(self.ifade)
                return

            if self.ifade[-1] in ["+", "-", "×", "÷"]:
                self.ifade = self.ifade[:-1] + tus
            else:
                self.ifade += tus
            self.ekran_degiskeni.set(self.ifade)

        elif tus == ".":
            # Son sayı segmentinde zaten nokta olup olmadığını kontrol et
            parcalar = (
                self.ifade.replace("+", " ")
                .replace("-", " ")
                .replace("×", " ")
                .replace("÷", " ")
                .split()
            )
            son_sayi = parcalar[-1] if parcalar else ""
            if "." not in son_sayi:
                self.ifade += "." if self.ifade and self.ifade[-1].isdigit() else "0."
                self.ekran_degiskeni.set(self.ifade)

        else:  # Rakamlar (0-9)
            if self.ekran_degiskeni.get() == "0" and tus != ".":
                self.ifade = tus
            else:
                self.ifade += tus
            self.ekran_degiskeni.set(self.ifade)

    def hesapla(self):
        if not self.ifade:
            return

        # İfadeyi Python'ın eval edebileceği formata çevir (+, -, *, /)
        ifade_hesap = self.ifade.replace("×", "*").replace("÷", "/")

        # Sonda kalan işlem operatörlerini temizle
        ifade_hesap = ifade_hesap.rstrip("+-*/")
        if not ifade_hesap:
            return

        try:
            # 0'a bölme kontrolü
            if "/0" in ifade_hesap.replace(" ", ""):
                parcalar = ifade_hesap.split("/")
                for p in parcalar[1:]:
                    temiz_p = p.strip()
                    if temiz_p == "0" or (
                        temiz_p.startswith("0") and not temiz_p.startswith("0.")
                    ):
                        raise ZeroDivisionError

            # Güvenli eval: yalnızca sayılar ve 4 işlem sembolleri
            if any(c not in "0123456789+-*/. " for c in ifade_hesap):
                raise ValueError("Geçersiz sembol")

            sonuc = eval(ifade_hesap, {"__builtins__": None}, {})

            if isinstance(sonuc, float) and sonuc.is_integer():
                sonuc = int(sonuc)

            self.gecmis = self.ifade + " ="
            self.gecmis_degiskeni.set(self.gecmis)

            self.ifade = str(sonuc)
            self.ekran_degiskeni.set(self.ifade)

        except ZeroDivisionError:
            self.gecmis_degiskeni.set(self.ifade + " =")
            self.ekran_degiskeni.set("0'a bölünemez")
            self.ifade = ""
        except Exception:
            self.ekran_degiskeni.set("Hata")
            self.ifade = ""


if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = HesapMakinesiGUI(pencere)
    pencere.mainloop()
