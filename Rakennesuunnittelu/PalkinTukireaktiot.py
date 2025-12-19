# Bergman-M PalkinTukireaktiot.py
# Ohjelma laskee yksiaukkoisen palkin tukireaktiot tasaiselle kuormalle ja/tai pistekuormalle keskellä palkkia.

def palkin_tukireaktiot(L, q, F, a):
    # Lasketaan palkin tukireaktiot yksiaukkoiselle palkille, 
    # jossa on tasainen kuorma q (kN/m) ja/tai pistekuorma F (kN) keskellä palkkia pituudella L (m) 

    R1 = (q * L) / 2 + F * (L- a)/L # Tukireaktio vasemmassa päässä
    R2 = (q * L) / 2 + F * a/L  # Tukireaktio oikeassa päässä
    return R1, R2


def kuormat(L):
    # Kysytään kuormatyyppi ja palautetaan vastaava kuorman arvo 
    print("""Valitse kuormatyyppi:
    1. Tasainen kuorma
    2. Pistekuorma keskellä palkkia
    3. Molemmat kuormat""")

    q = 0   # Tasainen kuorma
    F = 0   # Pistekuorma
    a = 0   # Etäisyys vasemmasta tuesta
    try:
        valinta = int(input("Anna valintasi (1, 2, 3): "))
        if valinta not in [1, 2, 3]:
            print("Virheellinen valinta. Yritä uudelleen.")
            return kuormat()
        try:
            if valinta == 1:
                q = float(input("Anna tasainen kuorma (kN/m): "))
            elif valinta == 2:
                F = float(input("Anna pistekuorma (kN): "))
                a = float(input("Anna etäisyys vasemmasta tuesta (m): "))
                while a < 0 or a > L:
                    if a < 0:
                        print("Etäisyyden tulee olla positiivinen luku. Yritä uudelleen.")
                    elif a > L:
                        print("Etäisyyden tulee olla pienempi tai yhtä suuri kuin palkin pituus. Yritä uudelleen.")
                    a = float(input("Anna etäisyys vasemmasta tuesta (m): "))
            elif valinta == 3:
                q = float(input("Anna tasainen kuorma (kN/m): "))
                F = float(input("Anna pistekuorma (kN): "))
                a = float(input("Anna etäisyys vasemmasta tuesta (m): "))
                while a < 0 or a > L:
                    if a < 0:
                        print("Etäisyyden tulee olla positiivinen luku. Yritä uudelleen.")
                    elif a > L:
                        print("Etäisyyden tulee olla pienempi tai yhtä suuri kuin palkin pituus. Yritä uudelleen.")
                    a = float(input("Anna etäisyys vasemmasta tuesta (m): "))
            return q , F, a
        except ValueError:
            print("Virheellinen syöte. Yritä uudelleen.")
            return kuormat()
    except ValueError:
        print("Virheellinen syöte. Yritä uudelleen.")
        return kuormat()
    

def lähtöarvot():
    # Kysytään käyttäjältä palkin pituuden ja kuorman arvot
    try:
        L = float(input("Anna palkin pituus (m): "))
        if L <= 0:
            print("Pituuden tulee olla positiivinen luku. Yritä uudelleen.")
            return lähtöarvot() 
    except ValueError:
        print("Virheellinen syöte. Yritä uudelleen.")
        return lähtöarvot()
    return L

def jatketaanko():
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


def main():

    #  Pääohjelma
    print("Tervetuloa palkin tukireaktioiden laskuriin!")

    while True:
        L = lähtöarvot()
        q, F, a = kuormat(L)
        R1, R2 = palkin_tukireaktiot(L, q, F, a)

        print(f"""Palkin tukireaktiot ovat:
        Vasen tukireaktio (R1): {R1:.2f} kN
        Oikea tukireaktio (R2): {R2:.2f} kN""")

        if not jatketaanko():
            return
    

if __name__ == "__main__":
    #   Suoritetaan pääohjelma
    main() 