
from math import exp


def palkin_tukireaktiot(L, q, F):
    # Lasketaan palkin tukireaktiot yksinkertaiselle palkille, jossa on tasainen kuorma
    R1 = (q * L) / 2 + F / 2  # Tukireaktio vasemmassa päässä
    R2 = (q * L) / 2 + F / 2  # Tukireaktio oikeassa päässä
    return R1, R2


def kuormat():
    # Kysytään kuormatyyppi ja palautetaan vastaava kuorman arvo 
    print("""Valitse kuormatyyppi:
    1. Tasainen kuorma
    2. Pistekuorma keskellä palkkia""")

    q = 0
    F = 0
    try:
        valinta = int(input("Anna valintasi (1 tai 2): "))
        if valinta not in [1, 2]:
            print("Virheellinen valinta. Yritä uudelleen.")
            return kuormat()
        try:
            if valinta == 1:
                q = float(input("Anna tasainen kuorma (kN/m): "))
            elif valinta == 2:
                F = float(input("Anna pistekuorma (kN): "))
            return q , F
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


def main():
    #  Pääohjelma
    print("Tervetuloa palkin tukireaktioiden laskuriin!")
    L = lähtöarvot()
    q, F = kuormat()
    R1, R2 = palkin_tukireaktiot(L, q, F)
    print(f"""Palkin tukireaktiot ovat:
    Vasen tukireaktio (R1): {R1:.2f} kN
    Oikea tukireaktio (R2): {R2:.2f} kN""")

if __name__ == "__main__":
    #   Suoritetaan pääohjelma
    main()