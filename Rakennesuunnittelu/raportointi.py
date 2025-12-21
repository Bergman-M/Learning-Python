# raportointi.py

def vaikutusraportti(koottu_tasaiset_kuormat, koottu_pistekuormat):
    # Tulostaa raportin kuormien vaikutuksista
    print("\nKuormien vaikutusraportti:")
    print("-------------------------")
    Kuorma = 1
    if koottu_tasaiset_kuormat:
        print("Tasaiset kuormat:")
        for q1, q2, x1, x2, W, xc, dR1, dR2 in koottu_tasaiset_kuormat:
            print(f"""\n#{Kuorma} Kuorma q1={q1:.2f} kN/m, q2={q2:.2f} kN/m \nAlue [{x1:.2f} m, {x2:.2f} m] \nResultantti W={W:.2f} kN \nvaikutuspiste xc={xc:.2f} m  \nKuorman vaikutus tukireaktioihin ΔR1 = {dR1:.2f} kN ja ΔR2 = {dR2:.2f} kN""")
            Kuorma += 1
    else:
        print("\nEi tasaisia kuormia.")

    if koottu_pistekuormat:
        print("\nPistekuormat:")
        Kuorma = 1
        for F, a, dR1, dR2 in koottu_pistekuormat:
            print(f"""\n#{Kuorma} Pistekuorma F={F:.2f} kN etäisyydellä a={a:.2f} m \nKuorman vaikutus tukireaktioihin ΔR1 = {dR1:.2f} kN ja ΔR2 = {dR2:.2f} kN""")
            Kuorma += 1
    else:
        print("\nEi pistekuormia.")
    print()  # Tyhjä rivi lopuksi