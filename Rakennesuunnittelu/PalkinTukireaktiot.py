# Bergman-M PalkinTukireaktiot.py
# Ohjelma laskee yksiaukkoisen palkin tukireaktiot tasaiselle kuormalle ja/tai pistekuormalle.


VIRHESYOTE = str("Virheellinen syöte. Yritä uudelleen.")

def palkin_tukireaktiot(L, q, pistekuormat):
    # Lasketaan palkin tukireaktiot yksiaukkoiselle palkille, 
    # jossa on tasainen kuorma q (kN/m) ja pistekuorma F (kN) etäisyydellä a (m) vasemmasta tuesta.

    R1 = - ((q * L) / 2 + sum(F * (L - a) / L for F, a in pistekuormat)) # Tukireaktio vasemmassa päässä
    R2 = - ((q * L) / 2 + sum(F * a / L for F, a in pistekuormat))  # Tukireaktio oikeassa päässä
    return R1, R2

def Kysy_a_etaisyys(L):
    # Kysytään pistekuorman etäisyys vasemmasta tuesta ja tarkistetaan sen kelvollisuus
    while True:
        try:
            a = float(input("Anna etäisyys a vasemmasta tuesta (m): "))
            if a < 0:
                print("Etäisyyden tulee olla positiivinen luku. Yritä uudelleen.")
            elif a > L:
                print("Etäisyyden tulee olla pienempi tai yhtä suuri kuin palkin pituus. Yritä uudelleen.")
            else:
                return a
        except ValueError:
            print("Virheellinen syöte. Yritä uudelleen.")

def tasainen_kuorma():
    # Kysytään tasainen kuorma
    while True:
        try:
            q = float(input("Anna tasainen kuorma (kN/m): "))
            return q
        except ValueError:
            print(VIRHESYOTE)
            continue

def pistekuorma(L):
    # Kysytään pistekuorma ja sen etäisyys vasemmasta tuesta
    while True:
        try:
            F = float(input("Anna pistekuorma (kN) tai paina 0: "))
            if F == 0:
                F = 0
                a = 0
            else:
                a = Kysy_a_etaisyys(L)
        except ValueError:
            print(VIRHESYOTE)
            continue
        return F, a


def kuormat(L):
    # Kysytään kuormatyyppi ja palautetaan vastaava kuorman arvo 
    print("""Valitse kuormatyyppi:
    1. Tasainen kuorma
    2. Pistekuorma etäisyydellä a vasemmasta tuesta
    3. Molemmat kuormat""")

    q = 0   # Tasainen kuorma
    pistekuormat = []

    while True:
            try:
                valinta = int(input("Anna valintasi (1, 2, 3): "))
                if valinta not in [1, 2, 3]:
                    print(VIRHESYOTE)
                    continue
                if valinta == 1:
                    q = tasainen_kuorma()
                elif valinta == 2:
                    while True:
                        F, a = pistekuorma(L)
                        if F == 0 and a == 0:
                            break
                        pistekuormat.append((F, a))
                elif valinta == 3:
                    q = tasainen_kuorma()
                    while True:
                        F, a = pistekuorma(L)
                        if F == 0 and a == 0:
                            break
                        pistekuormat.append((F, a))
                return q, pistekuormat
            except ValueError:
                print(VIRHESYOTE)
                continue

def Lähtöarvot():
    # Kysytään käyttäjältä palkin pituuden ja kuorman arvot
    while True:
        try:
            L = float(input("Anna palkin pituus (m): "))
            if L <= 0:
                print("Pituuden tulee olla positiivinen luku. Yritä uudelleen.")
                continue
        except ValueError:
            print(VIRHESYOTE)
            continue
        return L

def Jatketaanko():
    # Kysytään käyttäjältä jatketaanko ohjelman suorittamista
    while True:
        jatka = input("Lasketaanko toisen palkin tukireaktiot? (k/e): ").lower()
        if jatka not in ["k", "e"]:
            print("Virheellinen syöte. Vastaa 'k' (kyllä) tai 'e' (ei).")
        
        elif jatka == "k":
            return True
        elif jatka == "e":
            print("Kiitos ohjelman käytöstä!")
            return False
        
def tarkista_tasapainoyhtälö(R1, R2, L, q, pistekuormat):
    # Tarkistetaan tukireaktioiden tasapainoyhtälö
    kokonaiskuorma = q * L + sum(F for F, a in pistekuormat)
    tukireaktioiden_summa = R1 + R2

    if abs(kokonaiskuorma + tukireaktioiden_summa) < 0.01:
        print("Tasapainoyhtälö täyttyy.")
    else:
        print("Tasapainoyhtälö ei täyty.")

def main():
    #  Pääohjelma
    print("Tervetuloa palkin tukireaktioiden laskuriin!")

    while True:
        L = Lähtöarvot()
        q, pistekuormat = kuormat(L)
        R1, R2 = palkin_tukireaktiot(L, q, pistekuormat)
        tarkista_tasapainoyhtälö(R1, R2, L, q, pistekuormat)

        print(f"""Palkin tukireaktiot ovat:
        Vasen tukireaktio (R1): {R1:.2f} kN
        Oikea tukireaktio (R2): {R2:.2f} kN""")

        if not Jatketaanko():
            return
    

if __name__ == "__main__":
    #   Suoritetaan pääohjelma
    main()