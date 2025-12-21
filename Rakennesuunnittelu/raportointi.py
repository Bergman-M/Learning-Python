# raportointi.py
# Palkin laskennan tulosten raportointi ja esittäminen.
# Tulokset konsolissa, sekä kuvaajat matplotilla.
# y-akselin suunta alas päin positiivinen.

def vaikutusraportti(koottu_tasaiset_kuormat, koottu_pistekuormat):
    # Tulostaa raportin kuormien vaikutuksista

    print("\nKuormien vaikutusraportti:")
    print("-------------------------")
    kuorma_nro = 1

    if koottu_tasaiset_kuormat:
        print("Tasaiset kuormat:")
        for q1, q2, x1, x2, W, xc, dR1, dR2 in koottu_tasaiset_kuormat:
            print(
                f"""\n#{kuorma_nro} Kuorma q1={q1:.2f} kN/m, q2={q2:.2f} kN/m
                Alue [{x1:.2f} m, {x2:.2f} m]
                Resultantti W={W:.2f} kN
                Vaikutuspiste xc={xc:.2f} m
                Kuorman vaikutus tukireaktioihin ΔR1 = {dR1:.2f} kN ja ΔR2 = {dR2:.2f} kN"""
            )
            kuorma_nro += 1
    else:
        print("\nEi tasaisia kuormia.")

    if koottu_pistekuormat:
        print("\nPistekuormat:")
        kuorma_nro = 1
        for F, a, dR1, dR2 in koottu_pistekuormat:
            print(
                f"""\n#{kuorma_nro} Pistekuorma F={F:.2f} kN etäisyydellä a={a:.2f} m
                Kuorman vaikutus tukireaktioihin ΔR1 = {dR1:.2f} kN ja ΔR2 = {dR2:.2f} kN"""
            )
            kuorma_nro += 1
    else:
        print("\nEi pistekuormia.")

    print()


def sisaiset_kuormat_raportti(x_pisteet, Vs, Ms):
    # Tulostaa sisäisten kuormien leikkausvoimat ja momentin.

    print("Pisteet:")
    for x in x_pisteet:
        print(f"piste:{x:.2f}")

    print("\nLeikkausvoimat:")
    for V in Vs:
        print(f"leikkausvoima:{V:.2f}")

    print("\nMomentit:")
    for M in Ms:
        print(f"Momentti:{M:.2f}")

def pistekuorman_epäjatkuvuuden_huomioiminen(x_pisteet, pistekuormat_map, Vs):
    # Pistekuormat aiheuttavat leikkausvoimaan epäjatkuvuushyppyjä.
    # Pystysuora hyppy saadaan lisäämällä sama x kahdesti: ennen ja jälkeen kuorman.

    x_v = [x_pisteet[0]] # x-koordinaatit leikkausvoimakaavioita varten.
    V_v = [Vs[0]] # Vastaavat leikkausvoiman arvot.

    if pistekuormat_map and x_pisteet[0] in pistekuormat_map:
        V0_before = Vs[0] + pistekuormat_map[x_pisteet[0]]
        x_v = [x_pisteet[0], x_pisteet[0]]
        V_v = [V0_before, Vs[0]]

    for i in range(1, len(x_pisteet)):
        x = x_pisteet[i]
        if pistekuormat_map and x in pistekuormat_map:
            V_before = Vs[i] + pistekuormat_map[x]
            x_v.extend([x, x])
            V_v.extend([V_before, Vs[i]])
        else:
            x_v.append(x)
            V_v.append(Vs[i])

    return x_v, V_v


def piirra_sisaiset_kuormat(
    x_pisteet,
    Vs,
    Ms,
    tumma_teema = False,
    otsikko="Sisäiset kuormat",
    tallenna_polku=None,
    pistekuormat_map=None,
):
    # Pirtää Leikkaus- ja momenttikuvaajat.
    # Käyttöliittymän tausta joko tummalla teemalla tai vaalealla teemalla.
    # kuvaajat mahdollista tallentaa pdf-tiedostona.

    try:
        import matplotlib.pyplot as plt
    
        if tumma_teema:
            plt.style.use("dark_background")

        else:
            plt.style.use("default")

    except ImportError:
        print("Matplotlib ei ole asennettuna.")
        return

    if not (len(x_pisteet) == len(Vs) == len(Ms)):
        raise ValueError("x_pisteet, Vs ja Ms pitää olla saman pituisia.")

    fig, (ax_m, ax_v) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
    fig.suptitle(otsikko)

    # Piirretään Momenttikaavio.
    ax_m.plot(x_pisteet, Ms, color="tab:orange")
    ax_m.axhline(0, color="white" if tumma_teema else "black", linewidth=0.8)
    ax_m.set_ylabel("M [kNm]")
    ax_m.grid(True, which="both", alpha=0.3)

    x_v, V_v = pistekuorman_epäjatkuvuuden_huomioiminen(x_pisteet, pistekuormat_map, Vs)  # Huomioidaan leikkausvoiman epäjatkuvuus.

    # Piirretään Leikkauskaavio.
    ax_v.plot(x_v, V_v, color="tab:blue")
    ax_v.axhline(0, color="white" if tumma_teema else "black", linewidth=0.8)
    ax_v.set_ylabel("V [kN]")
    ax_v.set_xlabel("x [m]")
    ax_v.grid(True, which="both", alpha=0.3)

    ax_m.invert_yaxis()
    ax_v.invert_yaxis()

    plt.tight_layout() # Järjestää alakuviot ja marginaalit automaattisesti, jotta eivät  mene päällekkäin.

    if tallenna_polku:
        plt.savefig(tallenna_polku, dpi=300)

    plt.show()
