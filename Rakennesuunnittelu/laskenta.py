# laskenta.py
# staattinen laskenta palkille
# tukireaktiot
# kuormaintensiteetti w(x)
# leikkausvoima- ja momenttijakauma V(x), M(x)

# Oletukset:
# Yksiaukkoinen palkki
# lineaariset tasaiset kuormat
# pistekuormat mallinnetaan epäjatkuvuuden hyppyinä

# Sisäiset rasitukset lasketaan rakenteiden mekaniikan perusyhtälöillä.
# Laskenta perustuu palkkiteorian differentiaaliyhtälöihin.

import constants

def palkin_tukireaktiot(L, tasaiset_kuormat, pistekuormat):
    # Lasketaan palkin tukireaktiot yksiaukkoiselle palkille, 
    # jossa on tasainen kuorma q (kN/m) ja pistekuorma F (kN) etäisyydellä a (m) vasemmasta tuesta.

    if L is None or L <= constants.EPS:
        raise ValueError("Palkin pituus L pitää olla positiivinen.")

    R1 = 0  # Vasen tukireaktio
    R2 = 0  # Oikea tukireaktio 

    koottu_tasaiset_kuormat = []    # Lista kuormista ja niiden resultanteista
    koottu_pistekuormat = []         # Lista pistekuormista

    #  Osakuormat  
    for q1, q2, x1, x2 in tasaiset_kuormat:
        Lk = x2 - x1  # kuorman pituus
        if Lk <= 0:
            continue  # Ohitetaan negatiiviset tai nollapituudet

        # Resultantin laskenta (trapezoidi)
        W = 0.5 * (q1 + q2) * Lk # resultantti tasaisesta kuormasta
        if abs(W) < constants.EPS:
            continue  # Ohitetaan nollakuormat
        
        # Vaikutuspiste (trapezoidin painopiste)
        jakaja = (q1 + q2)
        if abs(jakaja) < constants.EPS:
            continue # Vältetään jakaminen nollalla
        
        x_lokaali = Lk * (q1 + 2*q2) / (3*jakaja)  # etäisyys kuorman alkupisteestä
        xc = x1 + x_lokaali # etäisyys vasemmasta tuesta

        # Tukireaktiot (oletetaan alaspäin positiiviseksi)
        dR1 = - W * (L - xc) / L
        dR2 = - W * xc / L
        R1 += dR1
        R2 += dR2
        koottu_tasaiset_kuormat.append((q1, q2, x1, x2, W, xc, dR1, dR2))

    # Lisätään pistekuormien vaikutus tukireaktioihin
    for F, a in pistekuormat:
        if a > L or a < 0:
            print(f"""Pistekuorman etäisyys a={a:.2f} m on palkin pituutta L={L:.2f} suurempi tai negatiivinen. 
            Ohitetaan kuorma F ={F:.2f} kN."""
            )
            continue  # Ohitetaan virheelliset etäisyydet

        dR1 = - F * (L - a) / L
        dR2 = - F * a / L
        R1 += dR1
        R2 += dR2
        koottu_pistekuormat.append((F, a, dR1, dR2))

    return R1, R2, koottu_tasaiset_kuormat, koottu_pistekuormat


def tarkista_tasapainoyhtälö(R1, R2, tasaiset_kuormat, pistekuormat):
    # Tarkistetaan pytysuuntaisen voiman tasapainoyhtälö annetuille tukireaktioille ja kuormille.
    # Oletukset: 
    # - Kuormat ovat alaspäin negatiivisia ja reaktiot positiivisia ylös.
    # Tarkistetaan, että |kuormat + Vasentuki (R1) + Oikeatuki (R2)| < EPS (virhemarginaali float-lukujen  vuoksi).

    def _iter_tasaiset_kuormat_4(kuormat):
        # Normalisoi tasaiset kuormat muotoon (q1, q2, x1, x2).
        # Sallii useamman listan sisällön (supersetit), mutta vaatii vähintään neljä ensimmäistä aroa, eli:
        #   q1, q2 = kuorman intensiteetti (kN/m)
        #   x1, x2 = vaikutusalueen rajat (m)
        # Luovuttaa (yieldaa) aina neljä arvoa, jotta laskenta pysyy siistinä.

        for kuorma in kuormat:
            if len(kuorma) < 4:
                raise ValueError("Tasaisen kuorman muodon pitää olla (q1, q2, x1, x2) (tai superset).")
            yield kuorma[0], kuorma[1], kuorma[2], kuorma[3]

    def _iter_pistekuormat_2(kuormat):
        # Normalisoi pistekuormat muotoon (F, a)
        # Sallii useammat listan arvon (supersetit), mutta luovuttaa (yieldaa) vähintään kaksi arvoa:
        #   F = pistekuorma (kN)
        #   a = sijainti (m)
        
        for kuorma in kuormat:
            if len(kuorma) < 2:
                raise ValueError("Pistekuorman muodon pitää olla (F, a) (tai superset).")
            yield kuorma[0], kuorma[1]

    # Tasainen (lineaarisesti vaihtelevan) kuorman resultanttivoima = trapezoidin pinta-ala
    # = 0.5*(q1 + q2) * (x2 - x1)
    tasaiset_summa = sum(0.5 * (q1 + q2) * (x2 - x1)
            for q1, q2, x1, x2 in _iter_tasaiset_kuormat_4(tasaiset_kuormat))

    # Pistekuormien summa (a:ta ei tarvita tarkastukseen)
    piste_summa = sum(F for F, _a in _iter_pistekuormat_2(pistekuormat))

    kokonaiskuorma = tasaiset_summa + piste_summa
    tukireaktioiden_summa = R1 + R2

    if abs(kokonaiskuorma + tukireaktioiden_summa) < constants.EPS:
        print("Tasapainoyhtälö täyttyy.")
    else:
        print("Tasapainoyhtälö ei täyty.")


def w(x, tasaiset_kuormat):
    # Palauttaa kuormaintensiteetin w(x) [kN/m] pisteessä x.
    # Huomioi useat päällekkäiset lineaariset tasaiset kuormat.
    w_summa = 0

    for q1, q2, x1, x2 in tasaiset_kuormat:
        if x1 <= x <= x2 and x2 - x1 > constants.EPS:
            # Lineaarinen interpolointi kuorman arvosta
            qx = q1 + (q2 - q1) * (x - x1) / (x2 - x1)
            w_summa += qx
    return w_summa


def x_laskentapisteet(L, tasaiset_kuormat, pistekuormat):
    # Palauttaa palkin välillä laskettavat solmupisteet. 
    # Huomioi hyvin lähellä olevat pisteet yhdeksi laskentasolmuksi

    pakolliset_sijainnit = [0, L] # Pisteet, joissa kuormat vaikuttavat

    for q1, q2, x1, x2 in tasaiset_kuormat: # Lisätään tasaisen kuorman alkupisteet ja loppupisteet
        pakolliset_sijainnit.append(x1)
        pakolliset_sijainnit.append(x2)

    for F, a in pistekuormat:
        pakolliset_sijainnit.append(a) 

    if L is None or L <= constants.EPS:
        raise ValueError("Palkin pituus L pitää olla positiivinen.")
    


    grid = [i * constants.DX for i in range(int(L / constants.DX) + 1)]  # Pisteet palkin pituudella

    x_pisteet = pakolliset_sijainnit + grid  # Yhdistetään pakolliset pisteet ja solmupisteruudukko
    x_pisteet = [0 if x < 0 else L if x > L else x for x in x_pisteet]  # Rajataan pisteet palkin sisällä
    x_pisteet.sort()  # Järjestetään pisteet
    x_pisteet_siistitty = [x_pisteet[0]] # Aloitetaan siisti pistelista ensimmäisellä pisteellä
    
    for x in x_pisteet[1:]: # Käydään pisteet läpi yksi kerrallaan ja lisätään vain, jos etäisyys edelliseen on suurempi kuin EPS
        if abs(x - x_pisteet_siistitty[-1]) > constants.EPS:
            x_pisteet_siistitty.append(x)
    x_pisteet = x_pisteet_siistitty

    return x_pisteet

def pistekuormat_kartta(pistekuormat, x_pisteet, tol):
    # Palauttaa sanakirjan {x_piste : F_summa}
    # x_piste on aina arvo x_pisteet-listasta (snäppäys), jotta float-vertailu on ok

    kartta = {}

    for F, a in pistekuormat:
        # Etsi lähin laskentapiste
        x_lahin = min(x_pisteet, key = lambda x: abs(x - a))

        # Tarkistus
        if abs(x_lahin - a) > tol:
            print(f"Varoitus: pistekuorma a={a:.6f} ei osunut x-pisteeseen"
                  f"(lähin {x_lahin:.6f})")
            
        
        kartta[x_lahin] = kartta.get(x_lahin, 0.0) + F # Summaa kuormat samaan pisteeseen

    return kartta

def sisaiset_kuormat(R1, R2, L, tasaiset_kuormat, pistekuormat):
    #Lasketaan Leikkaus- ja Taivutusmomenttikuormat palkin pituudella

    x_pisteet = x_laskentapisteet(L, tasaiset_kuormat, pistekuormat)

    R1_up = -R1  # Tukireaktioiden suunta ylös
    V = R1_up  # Leikkausvoima vasemmassa päässä
    M = 0      # Taivutusmomentti vasemmassa päässä

    pistekuormat_map = pistekuormat_kartta(pistekuormat, x_pisteet, tol = constants.X_TOL) 

    # pistekuormat kohdassa x=0 vaikuttavat heti V:hen (x=0+)
    F0 = pistekuormat_map.pop(x_pisteet[0], 0.0)
    V -= F0

    Vs = [V]
    Ms = [M]


    for i in range(1, len(x_pisteet)):
        x_prev = x_pisteet[i-1]
        x_curr = x_pisteet[i]
        dx = x_curr - x_prev #Integrointiväli leikkaus- ja momenttilaskentaan

        # ennen loopissa: V on arvo kohdassa x_prev (oikealta)
        V_prev = V

        # Päivitetään leikkausvoima kuormien vaikutuksella välillä [x_prev, x_curr]
        # Käytetään "raja-arvoja" kuorman epäjatkuvuuskohdissa (x1/x2),
        # jotta segmentit juuri ennen/ jälkeen alkua/loppua eivät saa puolikasta kuormaa.
        if dx <= 2 * constants.EPS:
            w_avg = w(0.5 * (x_prev + x_curr), tasaiset_kuormat)
        else:
            x_prev_eval = min(L, max(0.0, x_prev + constants.EPS))
            x_curr_eval = min(L, max(0.0, x_curr - constants.EPS))
            w_avg = 0.5 * (w(x_prev_eval, tasaiset_kuormat) + w(x_curr_eval, tasaiset_kuormat))
        V_left = V_prev - w_avg * dx  # leikkaus juuri ennen x_curr

        # momentti on jatkuva -> integroi välillä [x_prev, x_curr]
        M += 0.5 * (V_prev + V_left) * dx  # trapezoidi, parempi kuin M += V*dx

        # nyt siirry kohtaan x_curr ja tee pistekuorman hyppy
        V = V_left
        if x_curr in pistekuormat_map:
            V -= pistekuormat_map[x_curr]

        Vs.append(V)
        Ms.append(M)

    return x_pisteet, Vs, Ms 
