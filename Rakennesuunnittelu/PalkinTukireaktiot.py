# Bergman-M PalkinTukireaktiot.py
# Ohjelma laskee yksiaukkoisen palkin tukireaktiot tasaiselle kuormalle ja/tai pistekuormalle.

import raportointi
import io_cli
import laskenta

def main():
    #  Pääohjelma
    print("Tervetuloa palkin tukireaktioiden laskuriin!")
    while True:
        L = io_cli.Lähtöarvot()
        tasaiset_kuormat, pistekuormat = io_cli.kuormat(L)
        R1, R2, koottu_tasaiset_kuormat, koottu_pistekuormat = laskenta.palkin_tukireaktiot(L, tasaiset_kuormat, pistekuormat)
        raportointi.vaikutusraportti(koottu_tasaiset_kuormat, koottu_pistekuormat)
        laskenta.tarkista_tasapainoyhtälö(R1, R2, tasaiset_kuormat, pistekuormat)
        # sisaiset_kuormat(R1, R2, L, tasaiset_kuormat, pistekuormat)

        print(f"""\nPalkin tukireaktiot ovat:
        Vasen tukireaktio (R1): {R1:.2f} kN
        Oikea tukireaktio (R2): {R2:.2f} kN""")

        if not io_cli.Jatketaanko():
            return
    

if __name__ == "__main__":
    #   Suoritetaan pääohjelma
    main()