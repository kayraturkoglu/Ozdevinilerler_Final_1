
def ikili_topla(a, b):
    """Binary toplama işlemi."""
    a = a[::-1]
    b = b[::-1]
    elde = 0
    sonuc = ""

    for i in range(max(len(a), len(b))):
        bit_a = int(a[i]) if i < len(a) else 0
        bit_b = int(b[i]) if i < len(b) else 0
        toplam = bit_a + bit_b + elde
        sonuc = str(toplam % 2) + sonuc
        elde = toplam // 2

    if elde:
        sonuc = "1" + sonuc
    return sonuc


class TuringMakinesi:
    def __init__(self, bant_verisi):
        self.bant = list(bant_verisi)
        self.kafa = 0
        self.durum = "q0"
        self.carpilan = ""
        self.carpan = ""
        self.sonuc = "0"

    def adim_yazdir(self, eski, okunan, yazilan, hareket, yeni):
        print(f"({eski}, {okunan}) -> ({yeni}, {yazilan}, {hareket})")

    def bant_goster(self):
        print("Bant:", ''.join(self.bant))
        print("      " + " " * self.kafa + "^")

    # ---------------------------------------------------------
    # GİRDİ KONTROLÜ
    # ---------------------------------------------------------
    def girdi_kontrol(self):
        self.durum = "q1"
        print("\nDurum:", self.durum)
        print("Girdi kontrol ediliyor.\n")

        while self.kafa < len(self.bant):
            okunan = self.bant[self.kafa]
            if okunan in ["0", "1", "*", "="]:
                self.adim_yazdir("q1", okunan, okunan, "R", "q1")
                self.kafa += 1
            else:
                self.adim_yazdir("q1", okunan, okunan, "S", "q_reject")
                print("HATA: Geçersiz sembol.")
                return False

        if self.bant.count("*") != 1 or self.bant.count("=") != 1:
            print("HATA: Bant formatı hatalı (* ve = eksik).")
            return False

        if self.bant[-1] != "=":
            print("HATA: Bant '=' ile bitmelidir.")
            return False

        self.durum = "q_return"
        while self.kafa > 0:
            self.adim_yazdir("q_return", self.bant[self.kafa - 1], self.bant[self.kafa - 1], "L", "q_return")
            self.kafa -= 1

        print("Head bandın başına döndü.\n")
        return True

    # ---------------------------------------------------------
    # OPERAND AYIRMA
    # ---------------------------------------------------------
    def operand_ayir(self):
        print("--- Operand Ayrılıyor ---")
        self.durum = "q2"
        idx = 0
        sol = []
        sag = []

        # sol operand
        while self.bant[idx] != "*":
            self.adim_yazdir("q2", self.bant[idx], self.bant[idx], "R", "q2")
            sol.append(self.bant[idx])
            idx += 1

        # yıldız
        self.adim_yazdir("q2", "*", "*", "R", "q3")
        self.carpilan = ''.join(sol)
        idx += 1
        print("Multiplicand:", self.carpilan)

        # sağ operand
        while self.bant[idx] != "=":
            self.adim_yazdir("q3", self.bant[idx], self.bant[idx], "R", "q3")
            sag.append(self.bant[idx])
            idx += 1

        self.adim_yazdir("q3", "=", "=", "L", "q4")
        self.carpan = ''.join(sag)
        print("Multiplier:", self.carpan)
        print()

        self.kafa = self.bant.index("=") - 1

    # ---------------------------------------------------------
    # ÇARPMA (Shift-Add + X işaretleme)
    # ---------------------------------------------------------
    def carp(self):
        print("--- Çarpma Başladı ---")
        sonuc = "0"
        kaydirma = 0

        while self.bant[self.kafa] != "*":
            bit = self.bant[self.kafa]
            print(f"\nOkunan multiplier biti: {bit}")

            # bit X ile işaretleniyor
            self.adim_yazdir("q6", bit, "X", "L", "q6")
            self.bant[self.kafa] = "X"
            self.bant_goster()

            # bit = 1 ise partial eklenir
            if bit == "1":
                kaydirilmis = self.carpilan + ("0" * kaydirma)
                print("Kaydırılmış partial:", kaydirilmis)
                sonuc = ikili_topla(sonuc, kaydirilmis)
                print("Yeni sonuç:", sonuc)
                print()

            # kaydırma bir sonraki bit için artar
            kaydirma += 1
            self.kafa -= 1

        self.sonuc = sonuc

        print("\n--- Çarpma Tamamlandı ---")
        print("Binary sonuç:", sonuc)
        print("Decimal sonuç:", int(sonuc, 2))

        final = f"{self.carpilan}*{self.carpan}={sonuc}"
        print("SON BANT:", final)
        print("\nDurum: q_accept\n")


# ============================================================
# ANA PROGRAM
# ============================================================

print("Binary çarpmak için iki sayı giriniz.")
sayi1 = input("Birinci sayı: ").strip()
sayi2 = input("İkinci sayı: ").strip()

if not (sayi1.isdigit() and set(sayi1) <= {"0", "1"}):
    print("HATA: Birinci sayı sadece 0 ve 1 içermelidir.")
    exit()

if not (sayi2.isdigit() and set(sayi2) <= {"0", "1"}):
    print("HATA: İkinci sayı sadece 0 ve 1 içermelidir.")
    exit()

bant = f"{sayi1}*{sayi2}="
print("\nOluşturulan bant:", bant)

tm = TuringMakinesi(bant)

if tm.girdi_kontrol():
    tm.operand_ayir()
    tm.carp()
