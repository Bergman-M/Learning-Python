import constants

def palkin_tukireaktiot(L, tasaiset_kuormat, pistekuormat):
    # Lasketaan palkin tukireaktiot yksiaukkoiselle palkille, 
    # jossa on tasainen kuorma q (kN/m) ja pistekuorma F (kN) etäisyydellä a (m) vasemmasta tuesta.

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
            print(f"Pistekuorman etäisyys a={a:.2f} m on palkin pituutta L={L:.2f} suurempi tai negatiivinen. Ohitetaan kuorma F ={F:.2f} kN.")
            continue  # Ohitetaan virheelliset etäisyydet

        dR1 = - F * (L - a) / L
        dR2 = - F * a / L
        R1 += dR1
        R2 += dR2
        koottu_pistekuormat.append((F, a, dR1, dR2))

    return R1, R2, koottu_tasaiset_kuormat, koottu_pistekuormat


def tarkista_tasapainoyhtälö(R1, R2, tasaiset_kuormat, pistekuormat):
    # Tarkistetaan tukireaktioiden tasapainoyhtälö

    kokonaiskuorma = sum(0.5*(q1+q2)*(x2-x1) for q1, q2, x1, x2 in tasaiset_kuormat) + sum(F for F, a in pistekuormat)
    tukireaktioiden_summa = R1 + R2

    if abs(kokonaiskuorma + tukireaktioiden_summa) < constants.EPS:
        print("Tasapainoyhtälö täyttyy.")
    else:
        print("Tasapainoyhtälö ei täyty.")


def w(x, tasaiset_kuormat):
    # Laskee pisteessä x vaikuttavan kuormaintensiteetin
    w_summa = 0

    for q1, q2, x1, x2 in tasaiset_kuormat:
        if x1 <= x <= x2 and x2 - x1 > constants.EPS:
            # Lineaarinen interpolointi kuorman arvosta
            qx = q1 + (q2 - q1) * (x - x1) / (x2 - x1)
            w_summa += qx
    return w_summa

'''
def sisaiset_kuormat(R1, R2, L, tasaiset_kuormat, pistekuormat):
    pass
    #TODO : Toteuta sisäisten kuormien laskenta ja tarvittaessa palauta tai tulosta tulokset
    #Lasketaan Leikkaus- ja Taivutusmomenttikuormat palkin pituudella

    pakolliset_sijainnit = [0, L] # Pisteet, joissa kuormat vaikuttavat

    for q1, q2, x1, x2 in tasaiset_kuormat: # Lisätään tasaisen kuorman alkupisteet ja loppupisteet
        pakolliset_sijainnit.append(x1)
        pakolliset_sijainnit.append(x2)

    for F, a in pistekuormat:
        pakolliset_sijainnit.append(a) 

    R1_up = -R1  # Tukireaktioiden suunta ylös
    num_points = 1000  # Pisteiden määrä palkin pituudella
    dx = L / (num_points - 1)   # Väli pisteiden välillä  
    grid = [i * dx for i in range(num_points)]  # Pisteet palkin pituudella

    xs = pakolliset_sijainnit + grid  # Yhdistetään pakolliset pisteet ja tasainen ruudukko
    xs = [0 if x < 0 else L if x > L else x for x in xs]  # Rajataan pisteet palkin sisäll
    xs.sort()  # Järjestetään pisteet
    xs_siistitty = [xs[0]] # Aloitetaan siisti pistelista ensimmäisellä pisteellä
    
    for x in xs[1:]: # Käydään pisteet läpi yksi kerrallaan ja lisätään vain, jos etäisyys edelliseen on suurempi kuin EPS
        if abs(x - xs_siistitty[-1]) > constants.EPS:
            xs_siistitty.append(x)
    xs = xs_siistitty

    V = R1_up  # Leikkausvoima vasemmassa päässä
    M = 0      # Taivutusmomentti vasemmassa päässä

    Vs = [V]
    Ms = [M]

    for i in range(1, len(xs)):
        x_prev = xs[i-1]
        x_curr = xs[i]
        dx = x_curr - x_prev

        # Päivitetään leikkausvoima kuormien vaikutuksella välillä [x_prev, x_curr]
        w_avg = 0.5 * (w(x_prev, tasaiset_kuormat) + w(x_curr, tasaiset_kuormat))
        V -= w_avg * dx

        for F, a in pistekuormat:
            if x_prev < a <= x_curr:
                V -= F

        Vs.append(V)

        # Päivitetään taivutusmomentti leikkausvoiman vaikutuksella
        M += V * dx
        Ms.append(M)
'''