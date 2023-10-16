# 06/10/23 - Lucas Xavier de Morais
# PROVA
# SEP I - Engenharia Elétrica (UFSJ)
import numpy as np

# Construção da matriz admitancia Y completa
def matAdm(infoLinhas):
    Max = 0
    for linha in infoLinhas:
        if linha[0] > Max: Max = int(linha[0])
        if linha[1] > Max: Max = int(linha[1])
    matrizY = np.zeros((Max,Max),dtype=np.complex_)

    for linha in infoLinhas: 
        k = int(linha[0]) - 1
        m = int(linha[1]) - 1
        admitancia = 1/(linha[2] + (1j*linha[3]))
        susceptancia = 1j*linha[4]/2
        tap = linha[5]
        defasagem = linha[6]*np.pi/180
        matrizY[k][k] = matrizY[k][k] + (tap**2)*admitancia + susceptancia
        matrizY[k][m] = -tap*np.exp(1j*defasagem)*admitancia
        matrizY[m][k] = -tap*np.exp(-1j*defasagem)*admitancia
        matrizY[m][m] = matrizY[m][m] + admitancia + susceptancia
    
    return matrizY

# Funcão para montar os vetores com todos os ângulos e tensões do sistema
# para os angulos incógnitas o valor inicial é definido como 0 e para as tensões é 1
def vetoresAngulosTensoes(infoBarras):
    angulos = np.zeros((np.shape(infoBarras)[0],1))
    tensoes = np.zeros((np.shape(infoBarras)[0],1))
    c = 0
    for barra in infoBarras:
        if (barra[1] != 'V0'): 
            angulos[c] = 0.0 
        else :
            angulos[c] = float(barra[3])
        if (barra[1] == 'PQ') : 
            tensoes[c] = 1.0 
        else :
            tensoes[c] = float(barra[2])
        c += 1

    return angulos, tensoes

# Definindo vetores dos indices das incognitas para auxiliar o código
def vetoresIndices(infoBarras, nPV, nPQ):
    size = nPV + 2*nPQ
    indices = np.zeros((size,1))
    a = 0
    t = nPV+nPQ 
    for barra in infoBarras:
        if barra[1] == 'PV': 
            indices[a] = int(barra[0])
            a += 1
        if barra[1] == 'PQ': 
            indices[a] = int(barra[0]) 
            indices[t] = int(barra[0])
            a += 1
            t += 1
    # Para facilitar o código, separando os vetores em 2, um para os indices dos angulos e outro para os indices das tensoes
    indicesAngulos = [] 
    indicesTensoes = []
    c = 0
    for i in indices:
        if (c < (nPV+nPQ)): indicesAngulos.append(int(i[0]))
        if (c >= (nPV+nPQ)): indicesTensoes.append(int(i[0]))
        c += 1

    return indices, indicesAngulos, indicesTensoes

# Calcular as potenicas esperadas e agrupá-las em dois vetores, um para 
# potencias ativas e outro para potencias reativas
def calcularPotenciasEsp(infoBarras):
    ativaEsp = np.zeros((np.shape(infoBarras)[0],1))
    reativaEsp = np.zeros((np.shape(infoBarras)[0],1))
    c = 0
    for barra in infoBarras:
        ativaEsp[c] = float(barra[4]) - float(barra[6])
        reativaEsp[c] = float(barra[5]) - float(barra[7])
        c += 1
    return ativaEsp, reativaEsp 

# Funcao para o calculo de potencias (Pcalc) a cada iteração
def calcularPotenciasCalc(matrizY, angulos, tensoes):
    G = np.copy(matrizY.real)
    B = np.copy(matrizY.imag)
    ativasKCalculada = np.zeros(np.shape(angulos))
    reativasKCalculada = np.zeros(np.shape(angulos))

    for k in range(len(tensoes)):
        for m in range(len(tensoes)):
            Gkm = G[k][m]
            Bkm = B[k][m]
            angulokm = angulos[k] - angulos[m]
            tensaokm = tensoes[k]*tensoes[m]
            cosThetakm = np.cos(angulokm)
            sinThetakm = np.sin(angulokm)

            ativasKCalculada[k] += tensaokm * ( (Gkm * cosThetakm) + (Bkm * sinThetakm) )
            reativasKCalculada[k] += tensaokm * ( (Gkm * sinThetakm) - (Bkm * cosThetakm) )

    return ativasKCalculada, reativasKCalculada

# Calculo do vetor H (dP/dTheta)
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
            angulokm = angulos[k][0] - angulos[m][0]
            tensaokm = tensoes[k][0]*tensoes[m][0]
            cosThetakm = np.cos(angulokm)
            sinThetakm = np.sin(angulokm)

            # Verificando se está iterando sobre a diagonal onde o calculo é diferente
            if (k != m):
                jacobianoH[linha][coluna] = tensaokm * ( (Gkm * sinThetakm) - (Bkm * cosThetakm) )
                continue
            jacobianoH[linha][coluna] = -1*(tensaokm**2)*Bkm            
            for mAux in range(len(angulos)):
                GkmAux = G[k][mAux]
                BkmAux = B[k][mAux]
                angulokmAux = angulos[k][0] - angulos[mAux][0]
                tensaokmAux = tensoes[k][0]*tensoes[mAux][0]
                cosThetakmAux = np.cos(angulokmAux)
                sinThetakmAux = np.sin(angulokmAux)

                jacobianoH[linha][coluna] -= tensaokmAux * ( (GkmAux * sinThetakmAux) - (BkmAux * cosThetakmAux) )

    return jacobianoH

# Calculo do vetor N (dP/dV)
def dPdV(matrizY, angulos, tensoes, nPV, nPQ, indicesAngulos, indicesTensoes):
    G = np.copy(matrizY.real)
    B = np.copy(matrizY.imag)

    jacobianoN = np.zeros((nPV+nPQ, nPQ    ))
    
    for linha in range(nPV+nPQ):
        # Indice atual é o indice do angulo - 1 para poder iterar sorbe a array
        k = indicesAngulos[linha] - 1
        for coluna in range(nPQ):
            m = indicesTensoes[coluna] - 1
            Gkm = G[k][m]
            Bkm = B[k][m]
            angulokm = angulos[k][0] - angulos[m][0]
            cosThetakm = np.cos(angulokm)
            sinThetakm = np.sin(angulokm)

            # Verificando se está iterando sobre a diagonal onde o calculo é diferente
            if (k != m):
                jacobianoN[linha][coluna] = tensoes[k][0] * ( (Gkm * cosThetakm) + (Bkm * sinThetakm) )
                continue
            jacobianoN[linha][coluna] = tensoes[k][0]*Gkm            
            for mAux in range(len(angulos)):
                GkmAux = G[k][mAux]
                BkmAux = B[k][mAux]
                angulokmAux = angulos[k][0] - angulos[mAux][0]
                cosThetakmAux = np.cos(angulokmAux)
                sinThetakmAux = np.sin(angulokmAux)

                jacobianoN[linha][coluna] += tensoes[mAux][0] * ( (GkmAux * cosThetakmAux) + (BkmAux * sinThetakmAux) )

    return jacobianoN

# Calculo do vetor M (dQ/dTheta)
def dQdTheta(matrizY, angulos, tensoes, nPV, nPQ, indicesAngulos, indicesTensoes):
    G = np.copy(matrizY.real)
    B = np.copy(matrizY.imag)

    jacobianoM = np.zeros((    nPQ, nPV+nPQ))
    
    for linha in range(nPQ):
        # Indice atual é o indice do angulo - 1 para poder iterar sorbe a array
        k = indicesTensoes[linha] - 1
        for coluna in range(nPV+nPQ):
            m = indicesAngulos[coluna] - 1
            Gkm = G[k][m]
            Bkm = B[k][m]
            angulokm = angulos[k][0] - angulos[m][0]
            tensaokm = tensoes[k][0]*tensoes[m][0]
            cosThetakm = np.cos(angulokm)
            sinThetakm = np.sin(angulokm)

            # Verificando se está iterando sobre a diagonal onde o calculo é diferente
            if (k != m):
                jacobianoM[linha][coluna] = (-1*tensaokm) * ( (Gkm * cosThetakm) + (Bkm * sinThetakm) )
                continue
            jacobianoM[linha][coluna] = -1*(tensaokm**2)*Gkm            
            for mAux in range(len(angulos)):
                GkmAux = G[k][mAux]
                BkmAux = B[k][mAux]
                angulokmAux = angulos[k][0] - angulos[mAux][0]
                tensaokmAux = tensoes[k][0]*tensoes[mAux][0]
                cosThetakmAux = np.cos(angulokmAux)
                sinThetakmAux = np.sin(angulokmAux)

                jacobianoM[linha][coluna] += (-1*tensaokmAux) * ( (GkmAux * cosThetakmAux) + (BkmAux * sinThetakmAux) )

    return jacobianoM

# Calculo do vetor L (dQ/dV)
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
            angulokm = angulos[k][0] - angulos[m][0]
            cosThetakm = np.cos(angulokm)
            sinThetakm = np.sin(angulokm)

            # Verificando se está iterando sobre a diagonal onde o calculo é diferente
            if (k != m):
                jacobianoL[linha][coluna] = tensoes[k][0] * ( (Gkm * sinThetakm) - (Bkm * cosThetakm) )
                continue
            jacobianoL[linha][coluna] = -1*tensoes[k][0]*Bkm            
            for mAux in range(len(angulos)):
                GkmAux = G[k][mAux]
                BkmAux = B[k][mAux]
                angulokmAux = angulos[k][0] - angulos[mAux][0]
                cosThetakmAux = np.cos(angulokmAux)
                sinThetakmAux = np.sin(angulokmAux)

                jacobianoL[linha][coluna] += tensoes[mAux][0] * ( (GkmAux * sinThetakmAux) - (BkmAux * cosThetakmAux) )

    return jacobianoL 

# Função simples para montar a matriz jacobiano montando primeiro as componentes H, N, M e L
def montarJacobiano(matrizY, angulos, tensoes, indicesAngulos, indicesTensoes, nPV, nPQ):
    #Primeiro são feitas as componentes H, N, M e L
    jacobianoH = np.copy(dPdTheta(matrizY, angulos, tensoes, nPV, nPQ, indicesAngulos))
    jacobianoN = np.copy(dPdV(matrizY, angulos, tensoes, nPV, nPQ, indicesAngulos, indicesTensoes))
    jacobianoM = np.copy(dQdTheta(matrizY, angulos, tensoes, nPV, nPQ, indicesAngulos, indicesTensoes))
    jacobianoL = np.copy(dQdV(matrizY, angulos, tensoes, nPV, nPQ, indicesTensoes))

    #Essas 2 linhas são para juntar as matrizes H, N e M, L, respectivamente
    jacobianoAuxP = np.concatenate((jacobianoH, jacobianoN), axis=1)
    jacobianoAuxQ = np.concatenate((jacobianoM, jacobianoL), axis=1)

    #Finalmente, juntar todas as matrizes para finalizar o jacobiano
    jacobiano = np.concatenate((jacobianoAuxP, jacobianoAuxQ), axis=0)

    return jacobiano

def fluxoPotencia(matrizY, angulos, tensoes, infoLinhas):
    #fluxos = [barra de, barra para, fluxo de potencia ativa, fluxo de potencia reativa]
    fluxos = np.zeros((len(angulos), 4))

    c = 0
    for linha in infoLinhas: 
        k = int(linha[0]) - 1
        m = int(linha[1]) - 1
        gkm = (linha[2]) / (linha[2]**2 + linha[3]**2) 
        bkm = (linha[3]) / (linha[2]**2 + linha[3]**2) 
        bshunt = linha[4]/2 
        tap = linha[5]
        defasagem = linha[6]*np.pi/180
        Vk = tensoes[k][0]
        Vm = tensoes[m][0]
        tapkmVk = tap * Vk 
        thetakm = angulos[k][0] - angulos[m][0]
        fluxos[c][0] = k + 1
        fluxos[c][1] = m + 1
        fluxos[c][2] = (((tapkmVk)**2)*gkm) - (tapkmVk*Vm*gkm*np.cos(thetakm + defasagem)) - (tapkmVk*Vm*bkm*np.sin(thetakm + defasagem))
        fluxos[c][3] = (-((tapkmVk)**2)*(bkm + bshunt)) + (tapkmVk*Vm*bkm*np.cos(thetakm + defasagem)) - (tapkmVk*Vm*gkm*np.sin(thetakm + defasagem))
        c += 1

    return fluxos

## ----------------- PROVA - ORIGINAL -----------------
#print('Antes do corte')

## infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm total, tapkm, defasagemkm]

#infoLinhas = np.array([ [1, 2, 0.000, 0.020, 0.0, 1.00, 0.0],
#                        [1, 3, 0.000, 0.045, 0.0, 1.00, 0.0],
#                        [2, 3, 0.000, 0.020, 0.0, 1.00, 0.0]])

## infoBarras = [barra , tipo, tensao, angulo, P.Ativa Geracao (PG), P.Reativa Geracao (QG), P.Ativa Carga (PL), P.Reativa Carga (QL) ]
## SBase = 100 MVA , VBase = 345kV
#infoBarras = np.array([ [1, 'V0', 1.00, 0.00, 1.0, 1.0380, 0.00, 0.00],
#                        [2, 'PQ', 0.9799, -1.7 , 0.0, 0.0000, 3.9, 1.9],
#                        [3, 'PQ', 1.00, 1.17, 2.9, 1.0776, 0.00, 0.00] ])

##Construcao da matriz admitania do sistema
#matrizY = np.copy(matAdm(infoLinhas))

##Construcao dos vetores de angulos e tensoes do sistema
#angulos, tensoes = vetoresAngulosTensoes(infoBarras)

## Definindo o número de barras PV e PQ
#nPV = 0
#nPQ = 0
#for barra in infoBarras:
#    if barra[1] == 'PV': nPV += 1
#    if barra[1] == 'PQ': nPQ += 1

## Montando vetores para armazenar os indices das incognitas do problema
#indices, indicesAngulos, indicesTensoes = vetoresIndices(infoBarras, nPV, nPQ)

##Calcular as potencias esperadas
#ativaEsp, reativaEsp = calcularPotenciasEsp(infoBarras)

#print('Jacobiano')
## Definindo parâmetros iniciais do método de newton
#maxIter = 100
#iter = 0
#tol = 0.001
#fimP = 0
#fimQ = 0

#while iter < maxIter :
#    # Calculando pcalc para valores iniciais
#    ativasKCalculada, reativasKCalculada = calcularPotenciasCalc(matrizY, angulos, tensoes)

#    #Calculando deltaP e deltaQ
#    deltaPks = np.zeros((nPV+nPQ,1))
#    deltaQks = np.zeros((nPQ,1))
#    c = 0
#    for i in indicesAngulos:
#        deltaPks[c] = ativaEsp[i-1] + ativasKCalculada[i-1]
#        c += 1
#    c = 0
#    for i in indicesTensoes:
#        deltaQks[c] = reativaEsp[i-1] + reativasKCalculada[i-1]
#        c += 1

#    # Testando convergência
#    if np.max(np.abs(deltaPks)) < tol: fimP = 1
#    if np.max(np.abs(deltaQks)) < tol: fimQ = 1
#    if fimP and fimQ: print('Convergiu em ', iter, ' iterações'); break

#    # Montando um vetor com as variações de potência 
#    deltaPotencias = np.concatenate((deltaPks, deltaQks), axis=0)

#    #Montando o jacobiano da iteração
#    jacobiano = np.copy(montarJacobiano(matrizY, angulos, tensoes, indicesAngulos, indicesTensoes, nPV, nPQ))

#    # Fazendo dx = -J^(-1) * g
#    deltaX = np.zeros(( len(indicesAngulos) + len(indicesTensoes) ,1))
#    deltaX = (-1)*np.dot(np.linalg.inv(jacobiano) , deltaPotencias) 

#    # Atualizando os ângulos
#    c = 0
#    for a in indicesAngulos:
#        angulos[a-1] += deltaX[c]
#        c += 1
#    for t in indicesTensoes:
#        tensoes[t-1] += deltaX[c]
#        c += 1

#    iter += 1

#print('Angulos')
#print(angulos)
#print('Tensoes')
#print(tensoes)

#potenciaAtivaFinal, potenciaReativaFinal = calcularPotenciasCalc(matrizY, angulos, tensoes)
#print('Potencias Finais')
#print('Potencia Ativa')
#print(potenciaAtivaFinal)
#print('Potencia Reativa')
#print(potenciaReativaFinal)

#print('Fluxos de Potências Ativa e Reativa')
#fluxos = np.copy(fluxoPotencia(matrizY, angulos, tensoes, infoLinhas))
#print(fluxos)


## ----------------- PROVA - ENGENHEIRO A -----------------
#print('Engenheiro A')

## infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm total, tapkm, defasagemkm]

#infoLinhas = np.array([ [1, 2, 0.000, 0.020, 0.0, 1.00, 0.0],
#                        [1, 3, 0.000, 0.045, 0.0, 1.00, 0.0],
#                        [2, 3, 0.000, 0.020, 0.0, 1.00, 0.0]])

## ENGENHEIRO A
## infoBarras = [barra , tipo, tensao, angulo, P.Ativa Geracao (PG), P.Reativa Geracao (QG), P.Ativa Carga (PL), P.Reativa Carga (QL) ]
## SBase = 100 MVA , VBase = 345kV
#infoBarras = np.array([ [1, 'V0', 1.00, 0.00, 1.0, 1.0380, 0.00, 0.00],
#                        [2, 'PQ',  '-',  '-', 0.0, 0.0000, 3.62, 1.77],
#                        [3, 'PV', 0.90, 1.17, 2.9, 1.0776, 0.00, 0.00] ])

##Construcao da matriz admitania do sistema
#matrizY = np.copy(matAdm(infoLinhas))

##Construcao dos vetores de angulos e tensoes do sistema
#angulos, tensoes = vetoresAngulosTensoes(infoBarras)

## Definindo o número de barras PV e PQ
#nPV = 0
#nPQ = 0
#for barra in infoBarras:
#    if barra[1] == 'PV': nPV += 1
#    if barra[1] == 'PQ': nPQ += 1

## Montando vetores para armazenar os indices das incognitas do problema
#indices, indicesAngulos, indicesTensoes = vetoresIndices(infoBarras, nPV, nPQ)

##Calcular as potencias esperadas
#ativaEsp, reativaEsp = calcularPotenciasEsp(infoBarras)

#print('Jacobiano')
## Definindo parâmetros iniciais do método de newton
#maxIter = 100
#iter = 0
#tol = 0.001
#fimP = 0
#fimQ = 0

#while iter < maxIter :
#    # Calculando pcalc para valores iniciais
#    ativasKCalculada, reativasKCalculada = calcularPotenciasCalc(matrizY, angulos, tensoes)

#    #Calculando deltaP e deltaQ
#    deltaPks = np.zeros((nPV+nPQ,1))
#    deltaQks = np.zeros((nPQ,1))
#    c = 0
#    for i in indicesAngulos:
#        deltaPks[c] = ativaEsp[i-1] + ativasKCalculada[i-1]
#        c += 1
#    c = 0
#    for i in indicesTensoes:
#        deltaQks[c] = reativaEsp[i-1] + reativasKCalculada[i-1]
#        c += 1

#    # Testando convergência
#    if np.max(np.abs(deltaPks)) < tol: fimP = 1
#    if np.max(np.abs(deltaQks)) < tol: fimQ = 1
#    if fimP and fimQ: print('Convergiu em ', iter, ' iterações'); break

#    # Montando um vetor com as variações de potência 
#    deltaPotencias = np.concatenate((deltaPks, deltaQks), axis=0)

#    #Montando o jacobiano da iteração
#    jacobiano = np.copy(montarJacobiano(matrizY, angulos, tensoes, indicesAngulos, indicesTensoes, nPV, nPQ))

#    # Fazendo dx = -J^(-1) * g
#    deltaX = np.zeros(( len(indicesAngulos) + len(indicesTensoes) ,1))
#    deltaX = (-1)*np.dot(np.linalg.inv(jacobiano) , deltaPotencias) 

#    # Atualizando os ângulos
#    c = 0
#    for a in indicesAngulos:
#        angulos[a-1] += deltaX[c]
#        c += 1
#    for t in indicesTensoes:
#        tensoes[t-1] += deltaX[c]
#        c += 1

#    iter += 1

#print('Angulos')
#print(angulos)
#print('Tensoes')
#print(tensoes)

#potenciaAtivaFinal, potenciaReativaFinal = calcularPotenciasCalc(matrizY, angulos, tensoes)
#print('Potencias Finais')
#print('Potencia Ativa')
#print(potenciaAtivaFinal)
#print('Potencia Reativa')
#print(potenciaReativaFinal)

#print('Fluxos de Potências Ativa e Reativa')
#fluxos = np.copy(fluxoPotencia(matrizY, angulos, tensoes, infoLinhas))
#print(fluxos)

## ----------------- PROVA - ENGENHEIRO B -----------------
#print('Engenheiro B - sem corte')

## infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm total, tapkm, defasagemkm]

#infoLinhas = np.array([ [1, 2, 0.000, 0.020, 0.0, 1.00, 0.0],
#                        [1, 3, 0.000, 0.045, 0.0, 1.00, 0.0],
#                        [2, 3, 0.000, 0.020, 0.0, 1.00, 0.0]])

## ENGENHEIRO B
## infoBarras = [barra , tipo, tensao, angulo, P.Ativa Geracao (PG), P.Reativa Geracao (QG), P.Ativa Carga (PL), P.Reativa Carga (QL) ]
## SBase = 100 MVA , VBase = 345kV
#infoBarras = np.array([ [1, 'V0', 1.00, 0.00, 1.0, 1.0380, 0.00, 0.00],
#                        [2, 'PQ',  '-',  '-', 0.0, 0.0000, 3.90, 1.90],
#                        [3, 'PQ',  '-',  '-', 2.9, 1.0776, 0.00, 0.00] ])

##Construcao da matriz admitania do sistema
#matrizY = np.copy(matAdm(infoLinhas))

##Construcao dos vetores de angulos e tensoes do sistema
#angulos, tensoes = vetoresAngulosTensoes(infoBarras)

## Definindo o número de barras PV e PQ
#nPV = 0
#nPQ = 0
#for barra in infoBarras:
#    if barra[1] == 'PV': nPV += 1
#    if barra[1] == 'PQ': nPQ += 1

## Montando vetores para armazenar os indices das incognitas do problema
#indices, indicesAngulos, indicesTensoes = vetoresIndices(infoBarras, nPV, nPQ)

##Calcular as potencias esperadas
#ativaEsp, reativaEsp = calcularPotenciasEsp(infoBarras)

#print('Jacobiano')
## Definindo parâmetros iniciais do método de newton
#maxIter = 100
#iter = 0
#tol = 0.001
#fimP = 0
#fimQ = 0

#while iter < maxIter :
#    # Calculando pcalc para valores iniciais
#    ativasKCalculada, reativasKCalculada = calcularPotenciasCalc(matrizY, angulos, tensoes)

#    #Calculando deltaP e deltaQ
#    deltaPks = np.zeros((nPV+nPQ,1))
#    deltaQks = np.zeros((nPQ,1))
#    c = 0
#    for i in indicesAngulos:
#        deltaPks[c] = ativaEsp[i-1] + ativasKCalculada[i-1]
#        c += 1
#    c = 0
#    for i in indicesTensoes:
#        deltaQks[c] = reativaEsp[i-1] + reativasKCalculada[i-1]
#        c += 1

#    # Testando convergência
#    if np.max(np.abs(deltaPks)) < tol: fimP = 1
#    if np.max(np.abs(deltaQks)) < tol: fimQ = 1
#    if fimP and fimQ: print('Convergiu em ', iter, ' iterações'); break

#    # Montando um vetor com as variações de potência 
#    deltaPotencias = np.concatenate((deltaPks, deltaQks), axis=0)

#    #Montando o jacobiano da iteração
#    jacobiano = np.copy(montarJacobiano(matrizY, angulos, tensoes, indicesAngulos, indicesTensoes, nPV, nPQ))

#    # Fazendo dx = -J^(-1) * g
#    deltaX = np.zeros(( len(indicesAngulos) + len(indicesTensoes) ,1))
#    deltaX = (-1)*np.dot(np.linalg.inv(jacobiano) , deltaPotencias) 

#    # Atualizando os ângulos
#    c = 0
#    for a in indicesAngulos:
#        angulos[a-1] += deltaX[c]
#        c += 1
#    for t in indicesTensoes:
#        tensoes[t-1] += deltaX[c]
#        c += 1

#    iter += 1

#print('Angulos')
#print(angulos)
#print('Tensoes')
#print(tensoes)

#potenciaAtivaFinal, potenciaReativaFinal = calcularPotenciasCalc(matrizY, angulos, tensoes)
#print('Potencias Finais')
#print('Potencia Ativa')
#print(potenciaAtivaFinal)
#print('Potencia Reativa')
#print(potenciaReativaFinal)

#print('Fluxos de Potências Ativa e Reativa')
#fluxos = np.copy(fluxoPotencia(matrizY, angulos, tensoes, infoLinhas))
#print(fluxos)

## ----------------- PROVA - ENGENHEIRO B -----------------
#print('Engenheiro B')

## infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm total, tapkm, defasagemkm]

#infoLinhas = np.array([ [1, 2, 0.000, 0.020, 0.0, 1.00, 0.0],
#                        [1, 3, 0.000, 0.045, 0.0, 1.00, 0.0],
#                        [2, 3, 0.000, 0.020, 0.0, 1.00, 0.0]])

## ENGENHEIRO B
## infoBarras = [barra , tipo, tensao, angulo, P.Ativa Geracao (PG), P.Reativa Geracao (QG), P.Ativa Carga (PL), P.Reativa Carga (QL) ]
## SBase = 100 MVA , VBase = 345kV
#infoBarras = np.array([ [1, 'V0', 1.00, 0.00, 1.0, 1.0380, 0.00, 0.00],
#                        [2, 'PQ',  '-',  '-', 0.0, 0.0000, 3.62, 1.77],
#                        [3, 'PQ',  '-',  '-', 2.9, 1.0776, 0.00, 0.00] ])

##Construcao da matriz admitania do sistema
#matrizY = np.copy(matAdm(infoLinhas))

##Construcao dos vetores de angulos e tensoes do sistema
#angulos, tensoes = vetoresAngulosTensoes(infoBarras)

## Definindo o número de barras PV e PQ
#nPV = 0
#nPQ = 0
#for barra in infoBarras:
#    if barra[1] == 'PV': nPV += 1
#    if barra[1] == 'PQ': nPQ += 1

## Montando vetores para armazenar os indices das incognitas do problema
#indices, indicesAngulos, indicesTensoes = vetoresIndices(infoBarras, nPV, nPQ)

##Calcular as potencias esperadas
#ativaEsp, reativaEsp = calcularPotenciasEsp(infoBarras)

#print('Jacobiano')
## Definindo parâmetros iniciais do método de newton
#maxIter = 100
#iter = 0
#tol = 0.001
#fimP = 0
#fimQ = 0

#while iter < maxIter :
#    # Calculando pcalc para valores iniciais
#    ativasKCalculada, reativasKCalculada = calcularPotenciasCalc(matrizY, angulos, tensoes)

#    #Calculando deltaP e deltaQ
#    deltaPks = np.zeros((nPV+nPQ,1))
#    deltaQks = np.zeros((nPQ,1))
#    c = 0
#    for i in indicesAngulos:
#        deltaPks[c] = ativaEsp[i-1] + ativasKCalculada[i-1]
#        c += 1
#    c = 0
#    for i in indicesTensoes:
#        deltaQks[c] = reativaEsp[i-1] + reativasKCalculada[i-1]
#        c += 1

#    # Testando convergência
#    if np.max(np.abs(deltaPks)) < tol: fimP = 1
#    if np.max(np.abs(deltaQks)) < tol: fimQ = 1
#    if fimP and fimQ: print('Convergiu em ', iter, ' iterações'); break

#    # Montando um vetor com as variações de potência 
#    deltaPotencias = np.concatenate((deltaPks, deltaQks), axis=0)

#    #Montando o jacobiano da iteração
#    jacobiano = np.copy(montarJacobiano(matrizY, angulos, tensoes, indicesAngulos, indicesTensoes, nPV, nPQ))

#    # Fazendo dx = -J^(-1) * g
#    deltaX = np.zeros(( len(indicesAngulos) + len(indicesTensoes) ,1))
#    deltaX = (-1)*np.dot(np.linalg.inv(jacobiano) , deltaPotencias) 

#    # Atualizando os ângulos
#    c = 0
#    for a in indicesAngulos:
#        angulos[a-1] += deltaX[c]
#        c += 1
#    for t in indicesTensoes:
#        tensoes[t-1] += deltaX[c]
#        c += 1

#    iter += 1

#print('Angulos')
#print(angulos)
#print('Tensoes')
#print(tensoes)

#potenciaAtivaFinal, potenciaReativaFinal = calcularPotenciasCalc(matrizY, angulos, tensoes)
#print('Potencias Finais')
#print('Potencia Ativa')
#print(potenciaAtivaFinal)
#print('Potencia Reativa')
#print(potenciaReativaFinal)

#print('Fluxos de Potências Ativa e Reativa')
#fluxos = np.copy(fluxoPotencia(matrizY, angulos, tensoes, infoLinhas))
#print(fluxos)



# ----------------- PROVA - ENGENHEIRO B -----------------
print('questao2')

# infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm total, tapkm, defasagemkm]

infoLinhas = np.array([ [1, 2, 0.000, 0.020, 0.0, 1.00, 0.0],
                        [2, 3, 0.000, 0.045, 0.0, 1.00, 0.0],
                        [3, 4, 0.000, 0.045, 0.0, 1.00, 0.0],
                        [4, 5, 0.000, 0.020, 0.0, 1.00, 0.0]])

# ENGENHEIRO B
# infoBarras = [barra , tipo, tensao, angulo, P.Ativa Geracao (PG), P.Reativa Geracao (QG), P.Ativa Carga (PL), P.Reativa Carga (QL) ]
# SBase = 100 MVA , VBase = 345kV
infoBarras = np.array([ [1, 'V0', 1.00, 0.00, 1.0, 1.0380, 0.00, 0.00],
                        [2, 'PQ',  '-',  '-', 0.0, 0.0000, 0.90, 0.90],
                        [3, 'PQ',  '-',  '-', 0.0, 0.0000, 1.90, 1.00],
                        [4, 'PQ',  '-',  '-', 0.0, 0.0000, 0.00, 0.00] ])

#Construcao da matriz admitania do sistema
matrizY = np.copy(matAdm(infoLinhas))

#Construcao dos vetores de angulos e tensoes do sistema
angulos, tensoes = vetoresAngulosTensoes(infoBarras)

# Definindo o número de barras PV e PQ
nPV = 0
nPQ = 0
for barra in infoBarras:
    if barra[1] == 'PV': nPV += 1
    if barra[1] == 'PQ': nPQ += 1

# Montando vetores para armazenar os indices das incognitas do problema
indices, indicesAngulos, indicesTensoes = vetoresIndices(infoBarras, nPV, nPQ)

#Calcular as potencias esperadas
ativaEsp, reativaEsp = calcularPotenciasEsp(infoBarras)

print('Jacobiano')
# Definindo parâmetros iniciais do método de newton
maxIter = 100
iter = 0
tol = 0.001
fimP = 0
fimQ = 0

while iter < maxIter :
    # Calculando pcalc para valores iniciais
    ativasKCalculada, reativasKCalculada = calcularPotenciasCalc(matrizY, angulos, tensoes)

    #Calculando deltaP e deltaQ
    deltaPks = np.zeros((nPV+nPQ,1))
    deltaQks = np.zeros((nPQ,1))
    c = 0
    for i in indicesAngulos:
        deltaPks[c] = ativaEsp[i-1] + ativasKCalculada[i-1]
        c += 1
    c = 0
    for i in indicesTensoes:
        deltaQks[c] = reativaEsp[i-1] + reativasKCalculada[i-1]
        c += 1

    # Testando convergência
    if np.max(np.abs(deltaPks)) < tol: fimP = 1
    if np.max(np.abs(deltaQks)) < tol: fimQ = 1
    if fimP and fimQ: print('Convergiu em ', iter, ' iterações'); break

    # Montando um vetor com as variações de potência 
    deltaPotencias = np.concatenate((deltaPks, deltaQks), axis=0)

    #Montando o jacobiano da iteração
    jacobiano = np.copy(montarJacobiano(matrizY, angulos, tensoes, indicesAngulos, indicesTensoes, nPV, nPQ))

    # Fazendo dx = -J^(-1) * g
    deltaX = np.zeros(( len(indicesAngulos) + len(indicesTensoes) ,1))
    deltaX = (-1)*np.dot(np.linalg.inv(jacobiano) , deltaPotencias) 

    # Atualizando os ângulos
    c = 0
    for a in indicesAngulos:
        angulos[a-1] += deltaX[c]
        c += 1
    for t in indicesTensoes:
        tensoes[t-1] += deltaX[c]
        c += 1

    iter += 1

print(jacobiano)
print('Angulos')
print(angulos)
print('Tensoes')
print(tensoes)

