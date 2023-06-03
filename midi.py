from pygame import midi
import time
midi.init()

deviceIn = midi.Input(1)
#eviceOut = midi.Output(3)

NOTAS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MODS = ["", "m", "2", "4", "(5b)", "7M", "7", "9"]

def limpar(nota):
    for i in MODS:
        nota = nota.replace(i, "")
    return nota

def calcularCampHarm(escala, emnotas):
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
    refresh()
    acorde = "?"
    while True:
        resultado = refresh(5)
        if resultado:    
            pos = []
            for a in DICACORDES.keys():
                ac = DICACORDES[a]
                ok = True
                for nn in pressionadas:
                    if ac.count(nn) == 0 or len(ac) > len(pressionadas):
                        ok = False
                if ok:
                    pos.append(a)
            if pos.count(acorde) == 0:
                acorde = "?"
                if len(pressionadas) >= 4:
                    pressionadas = []
            if len(pos) == 1:
                acorde = pos[0]
                return acorde
                
def identificarNota(event):
    oitava = int(event[0][1]/12)
    nota = NOTAS[event[0][1] - oitava*12]
    
    return nota, oitava-2

def detecção(nota):
    menor = 1 if nota.find("m") != -1 else 0
    segunda = 1 if nota.find("2") != -1 else 0
    quarta = 1 if nota.find("4") != -1 else 0
    qBemol = 1 if nota.find("(5b)") != -1 else 0
    sétima = 1 if nota.find("7") != -1 else 0
    sétima = 2 if nota.find("7M") != -1 else sétima
    nona = 1 if nota.find("9") != -1 else 0
    return limpar(nota), menor, segunda, quarta, qBemol, sétima, nona

o = midi.Output(3)

def tocarNotas(notasPT, oit=2, força=127, duração=1):
    maior = -1
    for n in notasPT:
        #print(notas.index(n) + 12*3)
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
def refresh(buffer=1000):
    global pressionadas
    for event in deviceIn.read(buffer):
        if event[0][0] == 144 and event[0][2] > 0:
            força = event[0][2]
            n = identificarNota(event)
            if n[0] not in pressionadas:
                pressionadas.append(n[0])
            return n, 1, força
        else:
            if event[0][0] == 144 and event[0][2] == 0:
                n = identificarNota(event)
                if n[0] in pressionadas:
                    pressionadas.remove(n[0])

def calcularAcorde(escala, grau=1):
    padrão = ["MmmMMmd","mdMmmMM"]
    escala, menor, segunda, quarta, qBemol, sétima, nona = detecção(escala)
        
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
            if i == 2 and segunda:
                n.append(NOTAS[NOTAS.index(notas[i])-2])
            if i == 4 and quarta:
                n.append(NOTAS[NOTAS.index(notas[i])-2])
            n.append(notas[i])
    if sétima != 0:
        n.append(NOTAS[(NOTAS.index(notas[6])+sétima-2+menor)%12])
    if qBemol:
        n[2] = NOTAS[(NOTAS.index(n[2])-1)%12]
    if nona:
            n.append(notas[1])
    return n

def organizar(ac):
    res = limpar(ac)
    sM = True if ac.find("7M") != -1 else False
    if sM:
        ac = ac.replace("7M", "")
    for mod in ['m', '2', '4', '(5b)', '7', '9']:
        if ac.find(mod) != -1:
            res += mod
        if mod == '(5b)' and sM:
            res += "7M"
    return res

DICACORDES = {}
for n in NOTAS:
    for mod in MODS:
        ac = n+mod
        DICACORDES[ac] = calcularAcorde(ac)
        for mod2 in [m for m in MODS if m != mod]:
            if [mod, mod2] not in [["7", "7M"], ["7M", "7"]]:
                ac = ac+mod2
                DICACORDES[organizar(ac)] = calcularAcorde(ac)
    