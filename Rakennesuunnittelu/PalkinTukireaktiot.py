# Bergman-M PalkinTukireaktiot.py
# Ohjelma laskee yksiaukkoisen palkin tukireaktiot tasaisilla kuormalla ja/tai pistekuormalla.
# Oletuksena, että tuet palkin päissä ja palkit niveltuettuja (momentti vapautettu päistä).
# Palkilla ei ole omaa painoa.


import raportointi
import io_cli
import laskenta
import constants

def main():
    #  Pääohjelma
    print("Tervetuloa palkin tukireaktioiden laskuriin!")
    while True:
        L = io_cli.lahtoarvot()
        tasaiset_kuormat, pistekuormat = io_cli.kuormat(L)
        R1, R2, koottu_tasaiset_kuormat, koottu_pistekuormat = laskenta.palkin_tukireaktiot(L, tasaiset_kuormat, pistekuormat)
        raportointi.vaikutusraportti(koottu_tasaiset_kuormat, koottu_pistekuormat)
        laskenta.tarkista_tasapainoyhtälö(R1, R2, tasaiset_kuormat, pistekuormat)
        x_pisteet, Vs, Ms = laskenta.sisaiset_kuormat(R1, R2, L, tasaiset_kuormat, pistekuormat)
        raportointi.sisaiset_kuormat_raportti(x_pisteet, Vs, Ms)

        if io_cli.piirretaanko():
            pistekuormat_map = laskenta.pistekuormat_kartta(pistekuormat, x_pisteet, tol=constants.X_TOL)
            tumma_teema = io_cli.teema()
            raportointi.piirra_sisaiset_kuormat(x_pisteet, Vs, Ms,tumma_teema, pistekuormat_map=pistekuormat_map)

        print(f"""\nPalkin tukireaktiot ovat:
        Vasen tukireaktio (R1): {R1:.2f} kN
        Oikea tukireaktio (R2): {R2:.2f} kN""")

        if not io_cli.Jatketaanko():
            return
    

if __name__ == "__main__":
    #   Suoritetaan pääohjelma
    main()
