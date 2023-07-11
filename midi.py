from pygame import midi
import time
midi.init()

deviceIn = midi.Input(1)

NOTAS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
BEMOL = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
MODS = ["", "sus2", "sus4", "sus", "m", "(5b)", "7M", "7", "9", "11"]

def limpar(nota, mod=0):
    if mod == 0:
        for i in MODS:
            nota = nota.replace(i, "")
    else:
        nota = nota.replace("sus2", "").replace("sus4", "").replace("sus", "")

    ind = nota.find("/")
    if ind != -1:
        nota = nota[0:ind]
    return nota

def bemol(acorde):
    a = limpar(acorde)
    return acorde.replace(a, BEMOL[NOTAS.index(a)]).replace("sus2", "9")

def calcularCampHarm(escala, emnotas, menor=0):
    padrão = ["MmmMMmd","mdMmmMM"]
    campo = []
    if emnotas:
        for g in range(1, 7):
            campo.append(calcularAcorde(escala, g))
    else:
        esc = calcularEscala(escala)
        for g in range(7):
            if padrão[menor][g] == "M":    campo.append(esc[g])
            if padrão[menor][g] == "d":    campo.append(esc[g] + "dim")
            if padrão[menor][g] == "m":    campo.append(esc[g] + "m")
                        
    return campo

pressionadas = []
def identificarAcorde():
    global pressionadas
    pressionadas = []
    acorde = "?"
    difp = []
    while True:
        resultado = refresh(15)
        if resultado:
            #Organizar por altura
            alturasA = []
            alturasO = []
            difp = []
            org = []
            for p in pressionadas:
                alturasO.append((NOTAS.index(p[0]))+p[1]*12)
                alturasA.append((NOTAS.index(p[0]))+p[1]*12)
            alturasO.sort()
            for i in alturasO:
                ind = alturasA.index(i)
                org.append(pressionadas[ind])
            pressionadas = org

            for p in pressionadas:
                if p[0] not in difp:
                    difp.append(p[0])

            pos = []

            for a in DICACORDES.keys():
                ac = DICACORDES[a]
                ok = True
                for n in range(len(ac)):
                    if ac[n] not in difp:
                        ok = False
                for n in range(len(difp)):
                    if difp[n] not in ac:
                        ok = False
                if a.find("sus2(5b)") != -1:
                    ok = False
                if ok:
                    pos.append(a)
            if pos.count(acorde) == 0:
                acorde = "?"

            for p in pos:
                if p.find("sus4") != -1:
                    pos.remove(p)
                    break
            
            baixan = pressionadas[0][0]
            
            if len(pos) == 2:
                for p in pos:
                    if baixan == DICACORDES[p][0]:
                        pos = [p]

            if len(pos) == 1:
                acorde = pos[0]
                if baixan != DICACORDES[acorde][0] and baixan != "":
                    acorde = acorde + f"/{baixan}"
                return acorde
                    
def identificarNota(event):
    oitava = int(event[0][1]/12)
    nota = NOTAS[event[0][1] - oitava*12]
    
    return nota, oitava-2, event[0][1]

def toqueAcorde(acorde):
    nts = calcularAcorde(acorde)
    tocarNotas(nts)

def detecção(nota):
    sus2 = 1 if nota.find("sus2") != -1 else 0
    if not sus2:
        sus4 = 1 if nota.find("sus") != -1 else 0
    else:
        sus4 = 0
    menor = 1 if nota.find("m") != -1 else 0
    if menor:
        sus2, sus4 = 0, 0
    qBemol = 1 if nota.find("(5b)") != -1 else 0
    sétima = 1 if nota.find("7") != -1 else 0
    sétima = 2 if nota.find("7M") != -1 else sétima
    nona = 1 if nota.find("9") != -1 else 0
    decimaPrimeira = 1 if nota.find("11") != -1 else 0
    return limpar(nota), menor, sus2, sus4, qBemol, sétima, nona, decimaPrimeira

#o = midi.Output(3)

def tocarNotas(notasPT, oit=2, força=127, duração=1):
    maior = -1
    for n in notasPT:
        if NOTAS.index(n) < maior:
            oit += 1
        o.note_on(NOTAS.index(n) + 12*3 + oit*12, força, 0)
        maior = NOTAS.index(n)
    time.sleep(duração)
    maior = -1
    for n in notasPT:
        if NOTAS.index(n) < maior:
            oit += 1
        o.note_off(NOTAS.index(n) + 12*3 + oit*12, força, 0)
        maior = NOTAS.index(n)

def calcularEscala(nota):
    notas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    padrão = ["WWHWWWH", "WHWWHWW"]

    modo = 1 if nota.find("m") != -1 else 0
    
    p = padrão[modo]
    notaAtual = notas.index(limpar(nota))
    notasEscala = [notas[notaAtual]]
    for x in range(7):
        inter = p[x]
        if inter == "W":    notaAtual += 2
        if inter == "H":    notaAtual += 1
        notasEscala.append(notas[notaAtual%12])
    return notasEscala

força = 0
sustain = False
pP = False
def refresh(buffer=1000):
    global pressionadas
    global sustain, pP
    for event in deviceIn.read(buffer):
        if event[0][0] in [176, 177]:
            sustain = event[0][2] > 0

        if event[0][0] in [144, 145]:
            if event[0][2] > 0:
                pP = False
                força = event[0][2]
                n = identificarNota(event)
                if n not in pressionadas:
                    pressionadas.append(n)
                return n, 1, força
            else:
                pP = True
                if not sustain:
                    n = identificarNota(event)
                    if n in pressionadas:
                        pressionadas.remove(n)
        
        if not sustain and pP:
            for n in pressionadas:
                pressionadas.remove(n)

def calcularAcorde(escala, grau=1):
    padrão = ["MmmMMmd","mdMmmMM"]
    escala, menor, sus2, sus4, qBemol, sétima, nona, decimaPrimeira = detecção(escala)
        
    indexes = [0, 2, 4]
    notas = calcularEscala(escala)
    if padrão[menor][grau-1] == "M":
        notas = calcularEscala(notas[grau-1])
    if padrão[menor][grau-1] == "m":
        notas = calcularEscala(notas[grau-1]+"m")
    if padrão[menor][grau-1] == "d":
        notas = calcularEscala(notas[grau-1]+"m")
    
    n = []
    for i in indexes:
        if i == 4 and padrão[menor][grau-1] == "d":
            n.append(NOTAS[NOTAS.index(notas[i])-1])
        else:
            if i == 2:
                if sus2:
                    n.append(NOTAS[NOTAS.index(notas[i])-2+menor])
                if sus4:
                    n.append(NOTAS[(NOTAS.index(notas[i])+1+menor)%12])
            if not sus2 and not sus4 or i != 2:
                n.append(notas[i])
            if i == 4 and nona:
                n.append(NOTAS[(NOTAS.index(notas[1]))%12])
            if i == 4 and decimaPrimeira:
                    n.append(NOTAS[(NOTAS.index(notas[i])+1+menor)%12])
    if sétima != 0:
        n.append(NOTAS[(NOTAS.index(notas[6])+sétima-2+menor)%12])
    if qBemol:
        n[2] = NOTAS[(NOTAS.index(n[2])-1)%12]
    return n

def organizar(ac):
    res = limpar(ac)
    sM = True if ac.find("7M") != -1 else False
    s4 = True if ac.find("sus4") != -1 and ac.find("m") == -1 else False
    s2 = True if ac.find("sus2") != -1 and ac.find("m") == -1 else False
    ac = ac.replace("sus", "") if ac.find("m") != -1 else ac
    ac = ac.replace("7M", "").replace("sus4", "").replace("sus2", "")
    for mod in ["m", "sus", "(5b)", "7" if not sM else "", "9" if not s2 else "", "11" if not s4 else ""]:
        if ac.find(mod) != -1:
            res += mod
        if mod == '(5b)' and sM:
            res += "7M"
        if mod == 'm' and s2:
            res += "sus2"
        if mod == 'm' and s4:
            res += "sus4"
    return res

def val(ac, mod):
    ac + mod
    ac = ac.replace("sus2", "") if mod in {"sus", "sus4"} else ac
    ac = ac.replace("sus4", "") if mod in {"sus", "sus2"} else ac
    ac = ac.replace("7M", "") if mod == "7" != -1 else ac
    return ac + mod

DICACORDES = {}
for n in NOTAS:
    for mod in MODS:
        #["", "m", "sus2", "sus4", "sus", "(5b)", "7M", "7", "9", "11"]
        ac = n+mod
            
        DICACORDES[ac] = calcularAcorde(ac)
        for mod2 in MODS:
             if ac.find(mod2) == -1:
                ac = val(ac, mod2)
                if mod not in {"7", "7M"} or mod2 not in {"7", "7M"}:
                    if mod not in {"sus2", "sus4", "sus"} or mod2 not in {"sus2", "sus4", "sus"}:
                        ac = ac+mod2
                        o = organizar(ac)
                        DICACORDES[o] = calcularAcorde(o)
    