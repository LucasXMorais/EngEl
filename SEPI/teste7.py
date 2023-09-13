# 13/09/23 - Lucas Xavier de Morais
# TESTE 7 
# SEP I - Engenharia Elétrica (UFSJ)
import numpy as np


def matAdm(infoLinhas):
    Max = int(infoLinhas[np.argmax(infoLinhas,axis=0)[0]][np.argmax(infoLinhas,axis=1)[0]])
    matrizY = np.zeros((Max,Max),dtype=np.complex_)

    for linha in infoLinhas: 
        k = int(linha[0]) - 1
        m = int(linha[1]) - 1
        admitancia = 1/(linha[2] + (1j*linha[3]))
        susceptacancia = 1j*linha[4]
        tap = linha[5]
        defasagem = linha[6]*np.pi/180
        matrizY[k][k] = matrizY[k][k] + (tap**2)*admitancia + susceptacancia
        matrizY[k][m] = -tap*np.exp(1j*defasagem)*admitancia
        matrizY[m][k] = -tap*np.exp(-1j*defasagem)*admitancia
        matrizY[m][m] = matrizY[m][m] + admitancia + susceptacancia
    
    return matrizY

def calcularPotenciasEsp(infoBarras):
    ativaEsp = np.zeros((np.shape(infoBarras)[0],1))
    reativaEsp = np.zeros((np.shape(infoBarras)[0],1))
    c = 0
    for barra in infoBarras:
        ativaEsp[c] = float(barra[4]) - float(barra[6])
        reativaEsp[c] = float(barra[5]) - float(barra[7])
        c += 1
    return ativaEsp, reativaEsp 

def calcularPotenciasCalc(matrizY, angulos, tensoes):
    G = np.copy(matrizY.real)
    B = np.copy(matrizY.imag)
    ativasKCalculada = np.zeros(np.shape(angulos))
    reativasKCalculada = np.zeros(np.shape(angulos))

    k = 0
    for potencia in ativasKCalculada:
        for m in range(len(tensoes)):
            Gkm = G[k][m]
            Bkm = B[k][m]
            angulokm = angulos[k] - angulos[m]
            tensaokm = tensoes[k]*tensoes[m]
            cosThetakm = np.cos(angulokm)
            sinThetakm = np.sin(angulokm)

            potencia += tensaokm * ( (Gkm * cosThetakm) + (Bkm * sinThetakm) )
            reativasKCalculada[k] += tensaokm * ( (Gkm * sinThetakm) - (Bkm * cosThetakm) )
        k += 1

    return ativasKCalculada, reativasKCalculada

def dPdTheta(matrizY, angulos, tensoes, nPV, nPQ, indicesAngulos):
    G = np.copy(matrizY.real)
    B = np.copy(matrizY.imag)

    jacobianoH = np.zeros((nPV+nPQ, nPV+nPQ))
    
    for linha in range(nPV+nPQ):
        # Indice atual é o indice do angulo - 1 para poder iterar sorbe a array
        k = indicesAngulos[linha] - 1
        for coluna in range(nPV+nPQ):
            m = indicesAngulos[coluna] - 1
            Gkm = G[k][m]
            Bkm = B[k][m]
            angulokm = angulos[k] - angulos[m]
            tensaokm = tensoes[k]*tensoes[m]
            cosThetakm = np.cos(angulokm)
            sinThetakm = np.sin(angulokm)

            if (k != m):
                jacobianoH[linha][coluna] = tensaokm * ( (Gkm * sinThetakm) - (Bkm * cosThetakm) )
                continue
            jacobianoH[linha][coluna] = -1*(tensaokm**2)*Bkm            
            for mAux in range(len(angulos)):
                GkmAux = G[k][mAux]
                BkmAux = B[k][mAux]
                angulokmAux = angulos[k] - angulos[mAux]
                tensaokmAux = tensoes[k]*tensoes[mAux]
                cosThetakmAux = np.cos(angulokmAux)
                sinThetakmAux = np.sin(angulokmAux)

                jacobianoH[linha][coluna] -= tensaokmAux * ( (GkmAux * sinThetakmAux) - (BkmAux * cosThetakmAux) )

    return jacobianoH

def dPdV(matrizY, angulos, tensoes, nPV, nPQ, indicesTensoes):
    G = np.copy(matrizY.real)
    B = np.copy(matrizY.imag)

    jacobianoN = np.zeros((nPV+nPQ, nPQ    ))
    
    for linha in range(nPV+nPQ):
        # Indice atual é o indice do angulo - 1 para poder iterar sorbe a array
        k = indicesTensoes[linha] - 1
        for coluna in range(nPQ):
            m = indicesTensoes[coluna] - 1
            Gkm = G[k][m]
            Bkm = B[k][m]
            angulokm = angulos[k] - angulos[m]
            cosThetakm = np.cos(angulokm)
            sinThetakm = np.sin(angulokm)

            if (k != m):
                jacobianoN[linha][coluna] = tensoes[k] * ( (Gkm * cosThetakm) + (Bkm * sinThetakm) )
                continue
            jacobianoN[linha][coluna] = tensoes[k]*Gkm            
            for mAux in range(len(angulos)):
                GkmAux = G[k][mAux]
                BkmAux = B[k][mAux]
                angulokmAux = angulos[k] - angulos[mAux]
                cosThetakmAux = np.cos(angulokmAux)
                sinThetakmAux = np.sin(angulokmAux)

                jacobianoN[linha][coluna] += tensoes[mAux] * ( (GkmAux * cosThetakmAux) + (BkmAux * sinThetakmAux) )

    return jacobianoN

def dQdTheta(matrizY, angulos, tensoes, nPV, nPQ, indicesAngulos):
    G = np.copy(matrizY.real)
    B = np.copy(matrizY.imag)

    jacobianoM = np.zeros((    nPQ, nPV+nPQ))
    
    for linha in range(nPQ):
        # Indice atual é o indice do angulo - 1 para poder iterar sorbe a array
        k = indicesAngulos[linha] - 1
        for coluna in range(nPV+nPQ):
            m = indicesAngulos[coluna] - 1
            Gkm = G[k][m]
            Bkm = B[k][m]
            angulokm = angulos[k] - angulos[m]
            tensaokm = tensoes[k]*tensoes[m]
            cosThetakm = np.cos(angulokm)
            sinThetakm = np.sin(angulokm)

            if (k != m):
                jacobianoM[linha][coluna] = (-1*tensaokm) * ( (Gkm * cosThetakm) + (Bkm * sinThetakm) )
                continue
            jacobianoM[linha][coluna] = -1*(tensaokm**2)*Gkm            
            for mAux in range(len(angulos)):
                GkmAux = G[k][mAux]
                BkmAux = B[k][mAux]
                angulokmAux = angulos[k] - angulos[mAux]
                tensaokmAux = tensoes[k]*tensoes[mAux]
                cosThetakmAux = np.cos(angulokmAux)
                sinThetakmAux = np.sin(angulokmAux)

                jacobianoM[linha][coluna] += (-1*tensaokmAux) * ( (GkmAux * cosThetakmAux) + (BkmAux * sinThetakmAux) )

    return jacobianoM

def dQdV(matrizY, angulos, tensoes, nPV, nPQ, indicesTensoes):
    G = np.copy(matrizY.real)
    B = np.copy(matrizY.imag)

    jacobianoL = np.zeros((    nPQ,     nPQ))
    
    for linha in range(nPQ):
        # Indice atual é o indice do angulo - 1 para poder iterar sorbe a array
        k = indicesTensoes[linha] - 1
        for coluna in range(nPQ):
            m = indicesTensoes[coluna] - 1
            Gkm = G[k][m]
            Bkm = B[k][m]
            angulokm = angulos[k] - angulos[m]
            tensaokm = tensoes[k]*tensoes[m]
            cosThetakm = np.cos(angulokm)
            sinThetakm = np.sin(angulokm)

            if (k != m):
                jacobianoL[linha][coluna] = tensoes[k] * ( (Gkm * sinThetakm) - (Bkm * cosThetakm) )
                continue
            jacobianoL[linha][coluna] = -1*tensoes[k]*Bkm            
            for mAux in range(len(angulos)):
                GkmAux = G[k][mAux]
                BkmAux = B[k][mAux]
                angulokmAux = angulos[k] - angulos[mAux]
                tensaokmAux = tensoes[k]*tensoes[mAux]
                cosThetakmAux = np.cos(angulokmAux)
                sinThetakmAux = np.sin(angulokmAux)

                jacobianoL[linha][coluna] += tensoes[mAux] * ( (GkmAux * sinThetakmAux) - (BkmAux * cosThetakmAux) )

    return jacobianoL 

def calcularJacobiano(matrizY, angulos, tensoes, indices, nPV, nPQ):

    size = nPV + 2*nPQ
    jacobiano = np.zeros((size,size))

    indicesAngulos = np.zeros((nPV+nPQ,1))
    indicesTensoes = np.zeros((nPQ,1))
    c = 0
    for i in indices:
        if (c < (nPV+nPQ)): indicesAngulos[c] = i
        if (c >= (nPV+nPQ)): indicesTensoes[c-nPV-nPQ] = i
        c += 1

    jacobianoH = np.copy(dPdTheta(matrizY, angulos, tensoes, nPV, nPQ, indicesAngulos))
    jacobianoN = np.copy(dPdV(matrizY, angulos, tensoes, nPV, nPQ, indicesTensoes))
    jacobianoM = np.copy(dQdTheta(matrizY, angulos, tensoes, nPV, nPQ, indicesAngulos))
    jacobianoL = np.copy(dQdV(matrizY, angulos, tensoes, nPV, nPQ, indicesTensoes))

    return 1

def metodoNewton(infoBarras, matrizY, angulos, tensoes):
    #Determinando as matrizes do problema g = -J . dx 
    nPV = 0
    nPQ = 0
    for barra in infoBarras:
        if barra[1] == 'PV':
            nPV += 1
        if barra[1] == 'PQ':
            nPQ += 1
    size = nPV + 2*nPQ
    variacoesPotencia = np.zeros((size,1))
    jacobiano = np.zeros((size,size))
    deltax = np.zeros((size,1))
    indices = np.zeros((size,1))

    #Calcular as potencias esperadas
    ativaEsp, reativaEsp = calcularPotenciasEsp(infoBarras)

    #Calcular as potencias para valores iniciais
    ativasKCalculada, reativasKCalculada = calcularPotenciasCalc(matrizY, angulos, tensoes)

    return 1

# infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm/2, tapkm, defasagemkm]

infoLinhas = np.array([ [1, 2, 0.006, 0.032, 0.010, 1.0, 0.0],
                        [1, 3, 0.012, 0.064, 0.020, 1.0, 0.0],
                        [2, 3, 0.036, 0.192, 0.060, 1.0, 0.0]])

# infoBarras = [barra , tipo, tensao, angulo, P.Ativa Geracao (PG), P.Reativa Geracao (QG), P.Ativa Carga (PL), P.Reativa Carga (QL) ]

infoBarras = np.array([ [1, 'PV', 1.05, '-', 0.5, 0.0, 0.0, 0.0],
                        [2, 'V0', 1.00, 0.0, 0.0, 0.0, 1.0, 0.3],
                        [3, 'PQ', '-' , '-', 0.0, 0.0, 0.5, 0.2] ])

#Construcao da matriz admitania do sistema
matrizY = np.copy(matAdm(infoLinhas))

#Construcao dos vetores de angulos e tensoes do sistema
#e definindo os valores iniciais dos angulos desconhecidos como 0 e tensoes como 1
angulos = np.zeros((np.shape(infoBarras)[0],1))
tensoes = np.zeros((np.shape(infoBarras)[0],1))
c = 0
for barra in infoBarras:
    if (barra[3] == '-') : 
        angulos[c] = 0.0 
    else :
        angulos[c] = float(barra[3])

    if (barra[2] == '-') : 
        tensoes[c] = 1.0 
    else :
        tensoes[c] = float(barra[2])
    c += 1



















