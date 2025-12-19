# Bergman-M PalkinTukireaktiot.py
# Ohjelma laskee yksiaukkoisen palkin tukireaktiot tasaiselle kuormalle ja/tai pistekuormalle.


VIRHESYOTE = "Virheellinen syöte. Yritä uudelleen."
EPS = 1e-6  # Pieni arvo vertailuihin

def palkin_tukireaktiot(L, tasaiset_kuormat, pistekuormat):
    # Lasketaan palkin tukireaktiot yksiaukkoiselle palkille, 
    # jossa on tasainen kuorma q (kN/m) ja pistekuorma F (kN) etäisyydellä a (m) vasemmasta tuesta.

    R1 = 0  # Vasen tukireaktio
    R2 = 0  # Oikea tukireaktio 

    #  Osakuormat  
    for q,x1,x2 in tasaiset_kuormat:
        W = q * (x2 - x1)  # resultantti tasaisesta kuormasta
        xc = 1/2 * (x1 + x2)  # resultantin vaikutuspisteen etäisyys vasemmasta tuesta
        R1 += - W * (L - xc) / L
        R2 += - W * xc / L

    # Lisätään pistekuormien vaikutus tukireaktioihin
    for F, a in pistekuormat:
        R1 += - F * (L - a) / L
        R2 += - F * a / L

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

def kysy_tasaisen_kuorman_alue(L):
    # Kysytään tasaisen kuorman vaikutusalueen alkupiste ja loppupiste
    while True:
        try:
            x1 = float(input("Anna tasaisen kuorman alkupiste x1 (m): "))
            if x1 < 0 or x1 > L:
                print("Alkupisteen tulee olla välillä 0 - L. Yritä uudelleen.")
                continue
            x2 = float(input("Anna tasaisen kuorman loppupiste x2 (m): "))
            if x2 < x1 or x2 > L:
                print("Loppupisteen tulee olla välillä x1 - L. Yritä uudelleen.")
                continue
            return x1, x2
        except ValueError:
            print("Virheellinen syöte. Yritä uudelleen.")

def tasainen_kuorma(L):
    # Kysytään tasainen kuorma
    while True:
        try:
            q = float(input("Anna tasainen kuorma (kN/m) tai paina 0: "))
            if q == 0:
                q = 0
                x1 = 0
                x2 = 0
            else:
                x1, x2 = kysy_tasaisen_kuorman_alue(L)
        except ValueError:
            print(VIRHESYOTE)
            continue
        return q, x1, x2

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

    tasaiset_kuormat = []   # Tasainen kuorma (q, x1, x2)
    pistekuormat = []  # Lista pistekuormista (F, a)

    while True:
            try:
                valinta = int(input("Anna valintasi (1, 2, 3): "))
                if valinta not in [1, 2, 3]:
                    print(VIRHESYOTE)
                    continue
                if valinta == 1:
                    while True:
                        q, x1, x2 = tasainen_kuorma(L)
                        if q == 0:
                            break
                        tasaiset_kuormat.append((q, x1, x2))
                elif valinta == 2:
                    while True:
                        F, a = pistekuorma(L)
                        if F == 0 and a == 0:
                            break
                        pistekuormat.append((F, a))
                elif valinta == 3:
                    while True:
                        q, x1, x2 = tasainen_kuorma(L)
                        if q == 0:
                            break
                        tasaiset_kuormat.append((q, x1, x2))
                    while True:
                        F, a = pistekuorma(L)
                        if F == 0 and a == 0:
                            break
                        pistekuormat.append((F, a))
                return tasaiset_kuormat, pistekuormat
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
        
def tarkista_tasapainoyhtälö(R1, R2, tasaiset_kuormat, pistekuormat):
    # Tarkistetaan tukireaktioiden tasapainoyhtälö

    kokonaiskuorma = sum(q*(x2-x1) for q, x1, x2 in tasaiset_kuormat) + sum(F for F, a in pistekuormat)
    tukireaktioiden_summa = R1 + R2

    if abs(kokonaiskuorma + tukireaktioiden_summa) < EPS:
        print("Tasapainoyhtälö täyttyy.")
    else:
        print("Tasapainoyhtälö ei täyty.")

def main():
    #  Pääohjelma
    print("Tervetuloa palkin tukireaktioiden laskuriin!")

    while True:
        L = Lähtöarvot()
        tasaiset_kuormat, pistekuormat = kuormat(L)
        R1, R2 = palkin_tukireaktiot(L, tasaiset_kuormat, pistekuormat)
        tarkista_tasapainoyhtälö(R1, R2, tasaiset_kuormat, pistekuormat)

        print(f"""Palkin tukireaktiot ovat:
        Vasen tukireaktio (R1): {R1:.2f} kN
        Oikea tukireaktio (R2): {R2:.2f} kN""")

        if not Jatketaanko():
            return
    

if __name__ == "__main__":
    #   Suoritetaan pääohjelma
    main()