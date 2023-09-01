# 28/08/23 - Lucas Xavier de Morais
# Scripts e módulos rápidos para a matéria de Análise de Sistema de Potências I - Engenharia Elétrica (UFSJ)
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

def montarVetorP(tabelaPotencias, barraReferencia):
    matrizP = np.delete(tabelaPotencias, barraReferencia-1, 0) 
    vetorP = np.zeros((np.shape(matrizP)[0],))
    count = 0
    for barra in matrizP:
        vetorP[count] = barra[1] - barra[2] - barra[3]
        count += 1
    return vetorP

def montarMatrizPotencia(tabelaPotencias):
    return

def montarVetorB(matrizY, barraReferencia):
    vetorB = np.delete(np.delete(matrizY, barraReferencia-1, 1), barraReferencia-1, 0)
    vetorB = vetorB.imag
    return vetorB

def calcularAngulos(vetorB, vetorP, barraReferencia):
    vetorThetaAux = np.zeros(np.shape(vetorP))
    vetorTheta = np.zeros(len(vetorP)+1)

    vetorThetaAux = np.dot(-1*np.linalg.inv(vetorB),vetorP)
    for i in range(len(vetorTheta)):
        if i+1 < barraReferencia: vetorTheta[i] = vetorThetaAux[i];  
        if i+1 == barraReferencia: vetorTheta[i] = 0;  
        if i+1 > barraReferencia: vetorTheta[i] = vetorThetaAux[i-1];  

    return vetorTheta 

def calcularMatrizFluxo(matrizY, vetorTheta):
    matrizB = np.copy(matrizY.imag)
    matrizFluxo = np.zeros(np.shape(matrizY))

    for i in range(len(matrizY)):
        for j in range(len(matrizY)):
            if i == j: continue
            matrizFluxo[i][j] = matrizB[i][j]*(vetorTheta[i] - vetorTheta[j])

    return matrizFluxo 

def calcularFluxo(matrizFluxo, barra):
    fluxo = 0
    for fluxokm in matrizFluxo[barra-1]:
        fluxo += fluxokm
    return fluxo

def calcularPerdas(infoLinhas, tabelaPotencias, vetorTheta):
    potencias = np.copy(tabelaPotencias)
    Max = int(infoLinhas[np.argmax(infoLinhas,axis=0)[0]][np.argmax(infoLinhas,axis=1)[0]])
    admitancia = np.zeros((Max,Max),dtype=np.complex_)

    for linha in infoLinhas: 
        k = int(linha[0]) - 1
        m = int(linha[1]) - 1
        admitancia = linha[2]/((linha[2]**2) + (linha[3])**2)

        perda = admitancia*((vetorTheta[k] - vetorTheta[m])**2) 
        potencias[k][3] = potencias[k][3] + (perda/2) 
        potencias[m][3] = potencias[m][3] + (perda/2) 
    return potencias

# infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm/2, tapkm, defasagemkm]

infoLinhas = np.array([ [1, 2, 0.03, 0.25, 0.0, 1.0, 0.0],
                        [1, 3, 0.03, 0.30, 0.0, 1.0, 0.0],
                        [2, 3, 0.04, 0.40, 0.0, 1.0, 0.0],
                        [2, 4, 0.04, 0.35, 0.0, 1.0, 0.0],
                        [3, 4, 0.05, 0.50, 0.0, 1.0, 0.0]])

# tabelaPotencias = [barra, potência geração, potência carga, perdas na barra]

tabelaPotencias = np.array([[1, 2.0, 0.0, 0.0],
                            [2, 0.0, 2.0, 0.0],
                            [3, 0.0, 2.5, 0.0],
                            [4, 0.0, 0.0, 0.0]])

barraReferencia = 4
barraFluxo = 4 
erro = 1
tolerancia = 0.001
maxIter = 10

matrizY = np.copy(matAdm(infoLinhas))
vetorB = np.copy(montarVetorB(matrizY, barraReferencia))

vetorP = np.copy(montarVetorP(tabelaPotencias, barraReferencia))

vetorTheta = np.copy(calcularAngulos(vetorB, vetorP, barraReferencia))
perdasAntigas = np.zeros(np.shape(tabelaPotencias))
iter = 0
while ((erro > tolerancia) and (iter <= maxIter)):
    tabelaPerdas = np.copy(calcularPerdas(infoLinhas, tabelaPotencias, vetorTheta))
    vetorP = np.copy(montarVetorP(tabelaPerdas, barraReferencia))

    desvioDasPerdas = np.zeros(len(tabelaPerdas))
    for i in range(len(desvioDasPerdas)):
        delta = abs(tabelaPerdas[i][3] - perdasAntigas[i][3])
        desvioDasPerdas[i] = delta 
    erro = desvioDasPerdas[np.argmax(desvioDasPerdas)]
    print('Erro: ',erro,' - Iteração: ',iter+1)

    vetorTheta = np.copy(calcularAngulos(vetorB, vetorP, barraReferencia))
    perdasAntigas = np.copy(tabelaPerdas)
    iter += 1

matrizFluxo = calcularMatrizFluxo(matrizY, vetorTheta)
fluxo = calcularFluxo(matrizFluxo, barraFluxo)
print('O fluxo na barra ', barraFluxo, ' = ',fluxo , ' pu')





