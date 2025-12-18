
def palkin_tukireaktiot(L, q):
    # Lasketaan palkin tukireaktiot yksinkertaiselle palkille, jossa on tasainen kuorma
    R1 = (q * L) / 2  # Tukireaktio vasemmassa päässä
    R2 = (q * L) / 2  # Tukireaktio oikeassa päässä
    return R1, R2


def lähtöarvot():
    # Kysytään käyttäjältä palkin pituuden ja kuorman arvot
    try:
        L = float(input("Anna palkin pituus (m): "))
        q = float(input("Anna palkkiin kohdistuva kuorma (kN/m): "))
        return L, q         # L = palkin pituus, q = kuorma
    except ValueError:
        print("Virheellinen syöte. Yritä uudelleen.")
        return lähtöarvot()

def main():
    #  Pääohjelma
    print("Tervetuloa Palkin Tukireaktioiden laskuriin!")
    L, q = lähtöarvot()
    R1, R2 = palkin_tukireaktiot(L, q)
    print(f"""Palkin tukireaktiot ovat:
    Vasen tukireaktio (R1): {R1:.2f} kN
    Oikea tukireaktio (R2): {R2:.2f} kN""")

if __name__ == "__main__":
    #   Suoritetaan pääohjelma
    main()