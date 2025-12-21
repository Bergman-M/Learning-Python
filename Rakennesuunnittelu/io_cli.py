import constants

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
                    print(constants.VIRHESYOTE)
                    continue
                if valinta == 1:
                    while True:
                        q1, q2, x1, x2 = tasainen_kuorma(L)
                        if q1 == 0 and q2 == 0:
                            break
                        tasaiset_kuormat.append((q1,q2, x1, x2))
                elif valinta == 2:
                    while True:
                        F, a = pistekuorma(L)
                        if F == 0 and a == 0:
                            break
                        pistekuormat.append((F, a))
                elif valinta == 3:
                    while True:
                        q1, q2, x1, x2 = tasainen_kuorma(L)
                        if q1 == 0 and q2 == 0:
                            break
                        tasaiset_kuormat.append((q1, q2, x1, x2))
                    while True:
                        F, a = pistekuorma(L)
                        if F == 0 and a == 0:
                            break
                        pistekuormat.append((F, a))
                return tasaiset_kuormat, pistekuormat
            except ValueError:
                print(constants.VIRHESYOTE)
                continue


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


def pistekuorma(L):
    # Kysytään pistekuorma ja sen etäisyys vasemmasta tuesta
    print()
    while True:
        F = input("Anna pistekuorma (kN) tai paina enter: ")
        if not F == "":
            try:
                F = float(F)
                a = Kysy_a_etaisyys(L)
            except ValueError:
                print(constants.VIRHESYOTE)
                continue
        elif F == "":
            F = 0
            a = 0
        return F, a
    

def tasainen_kuorma(L):
    # Kysytään tasainen kuorma
    print()
    while True:
        q1 = input("Anna tasaisen kuorman q1 (kN/m) tai paina enter: ")
        if not q1 == "":
            try:
                q1 = float(q1)
                while True:
                    try:
                        q2 = float(input("Anna tasaisen kuorman q2 (kN/m): "))
                        x1, x2 = kysy_tasaisen_kuorman_alue(L)
                        return q1, q2, x1, x2
                    except ValueError:
                        print(constants.VIRHESYOTE)
                        continue
            except ValueError:
                print(constants.VIRHESYOTE)
                continue
        elif q1 == "":
            q1 = 0
            q2 = 0
            x1 = 0
            x2 = 0
            return q1, q2, x1, x2
        else:
            print(constants.VIRHESYOTE)
            continue


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


def lahtoarvot():
    # Kysytään käyttäjältä palkin pituuden ja kuorman arvot
    while True:
        try:
            L = float(input("Anna palkin pituus (m): "))
            if L <= 0:
                print("Pituuden tulee olla positiivinen luku. Yritä uudelleen.")
                continue
        except ValueError:
            print(constants.VIRHESYOTE)
            continue
        return L


def Jatketaanko():
    # Kysytään käyttäjältä jatketaanko ohjelman suorittamista
    while True:
        jatka = input("\nLasketaanko toisen palkin tukireaktiot? (k/e): ").lower().strip()
        if jatka not in ["k", "e"]:
            print("Virheellinen syöte. Vastaa 'k' (kyllä) tai 'e' (ei).")
        
        elif jatka == "k":
            return True
        elif jatka == "e":
            print("Kiitos ohjelman käytöstä!")
            return False


def piirretaanko():
    # Kysytään käyttäjältä piirretäänkö kuvaajat
    while True:
        valinta = input("\nPiirretäänkö leikkausvoima- ja momenttikuvaajat? (k/e): ").lower().strip()
        if valinta not in ["k", "e"]:
            print("Virheellinen syöte. Vastaa 'k' (kyllä) tai 'e' (ei).")
            continue
        return valinta == "k"
    

def teema():
    # Kysytään käyttäjältä haluaako tumman vai vaalean teeman
    while True:
        teema = input("\nKäytetäänkö tummaa vai vaaleaa teemaa? (t/v): ").lower().strip()
        if teema not in ["t", "v"]:
            print("Virheellinen syöte. Vastaa 't' (tumma) tai 'v' (vaalea).")
            continue
        elif teema == "t":
            return True
        elif teema == "v":
            return False
