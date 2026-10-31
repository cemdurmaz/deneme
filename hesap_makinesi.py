"""
Sadece 4 işlem (Toplama, Çıkarma, Çarpma, Bölme) yapabilen hesap makinesi uygulaması.
"""


def topla(a: float, b: float) -> float:
    """İki sayıyı toplar."""
    return a + b


def cikar(a: float, b: float) -> float:
    """İlk sayıdan ikinci sayıyı çıkarır."""
    return a - b


def carp(a: float, b: float) -> float:
    """İki sayıyı çarpar."""
    return a * b


def bol(a: float, b: float) -> float:
    """İlk sayıyı ikinci sayıya böler."""
    if b == 0:
        raise ZeroDivisionError("Bir sayı 0'a bölünemez!")
    return a / b


def format_sayi(sayi: float):
    """Sayı tamsayı ise tamsayı formatında gösterir, değilse float bırakır."""
    return int(sayi) if sayi.is_integer() else sayi


def sayi_al(mesaj: str) -> float:
    """Kullanıcıdan geçerli bir sayı girmesini ister."""
    while True:
        try:
            deger = input(mesaj).strip().replace(",", ".")
            return float(deger)
        except ValueError:
            print("Hata: Lütfen geçerli bir sayı giriniz.")


def ana_menu():
    """Kullanıcı arayüzü ve işlem döngüsü."""
    print("=" * 40)
    print("       4 İŞLEM HESAP MAKİNESİ")
    print("=" * 40)
    print("İşlemler:")
    print("  1 veya + : Toplama")
    print("  2 veya - : Çıkarma")
    print("  3 veya * : Çarpma")
    print("  4 veya / : Bölme")
    print("  q veya 5 : Çıkış")
    print("=" * 40)

    while True:
        secim = input("\nYapmak istediğiniz işlemi seçin: ").strip().lower()

        if secim in ["q", "5", "çıkış", "exit"]:
            print("Hesap makinesi kapatılıyor. İyi günler!")
            break

        if secim not in ["1", "2", "3", "4", "+", "-", "*", "/"]:
            print("Geçersiz seçim! Lütfen 1, 2, 3, 4 ya da (+, -, *, /) giriniz.")
            continue

        sayi1 = sayi_al("1. Sayıyı girin: ")
        sayi2 = sayi_al("2. Sayıyı girin: ")

        try:
            if secim in ["1", "+"]:
                sonuc = topla(sayi1, sayi2)
                sembol = "+"
            elif secim in ["2", "-"]:
                sonuc = cikar(sayi1, sayi2)
                sembol = "-"
            elif secim in ["3", "*"]:
                sonuc = carp(sayi1, sayi2)
                sembol = "*"
            elif secim in ["4", "/"]:
                sonuc = bol(sayi1, sayi2)
                sembol = "/"

            print(f"\n>> Sonuç: {format_sayi(sayi1)} {sembol} {format_sayi(sayi2)} = {format_sayi(sonuc)}")

        except ZeroDivisionError as e:
            print(f"\nHata: {e}")


if __name__ == "__main__":
    ana_menu()
