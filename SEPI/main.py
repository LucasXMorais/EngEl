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
        vetorP[count] = barra[1] - barra[3] - barra[5]
        count += 1
    return vetorP

def montarVetorB(matrizY, barraReferencia):
    vetorB = np.delete(np.delete(matrizY, barraReferencia-1, 1), barraReferencia-1, 0)
    vetorB = vetorB.imag
    return vetorB

def calcularAngulos(vetorB, vetorP, barraReferencia):
    vetorThetaAux = np.zeros(np.shape(vetorP))
    vetorTheta = np.zeros(len(vetorP)+1)

    vetorThetaAux = np.dot(-1*np.linalg.inv(vetorB),vetorP)

    for i in range(len(vetorTheta)):
        if i+1 < barraReferencia: vetorTheta[i] = vetorThetaAux[i]
        if i+1 == barraReferencia: vetorTheta[i] = 0
        if i+1 > barraReferencia: vetorTheta[i] = vetorThetaAux[i-1]

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
        potencias[k][5] = potencias[k][5] + (perda/2) 
        potencias[m][5] = potencias[m][5] + (perda/2) 
    return potencias

def calcularFluxoPorBarra(matrizY, vetorTensaoAngulos):
    n = np.shape(vetorTensaoAngulos)[0]

    matrizYReal = np.copy(matrizY.real)
    matrizYImag = np.copy(matrizY.imag)

    fluxoReal = np.zeros(np.shape(matrizY))
    fluxoImag = np.zeros(np.shape(matrizY))

    for k in range(n):
        for m in range(n):
            fluxoReal[k][m] += vetorTensaoAngulos[m][1]*( (matrizYReal[k][m]*np.cos(vetorTensaoAngulos[k][2]-vetorTensaoAngulos[m][2])) + (matrizYReal[k][m]*np.sin(vetorTensaoAngulos[k][2]-vetorTensaoAngulos[m][2])) ) 
            fluxoImag[k][m] += vetorTensaoAngulos[m][1]*( (matrizYImag[k][m]*np.sin(vetorTensaoAngulos[k][2]-vetorTensaoAngulos[m][2])) - (matrizYImag[k][m]*np.cos(vetorTensaoAngulos[k][2]-vetorTensaoAngulos[m][2])) ) 

    print(fluxoReal)
    print(fluxoImag)

    fluxoAtivo = np.zeros((n,1)) 
    fluxoReativo = np.zeros((n,1)) 

    for i in range(n):
        for j in range(n):
            fluxoAtivo[i] += fluxoReal[i][j]
            fluxoReativo[i] += fluxoImag[i][j]

    for i in range(n):
        fluxoAtivo[i] = fluxoAtivo[i]*vetorTensaoAngulos[i][1]
        fluxoReativo[i] = fluxoReativo[i]*vetorTensaoAngulos[i][1]

    print(fluxoAtivo)
    print(fluxoReativo)

    return  

## ----- TESTE RÁPIDO 5 ----- ##

# infoLinhas = np.array([ [1, 2, 0.03, 0.25, 0.0, 1.0, 0.0],
#                         [1, 3, 0.03, 0.30, 0.0, 1.0, 0.0],
#                         [2, 3, 0.04, 0.40, 0.0, 1.0, 0.0],
#                         [2, 4, 0.04, 0.35, 0.0, 1.0, 0.0],
#                         [3, 4, 0.05, 0.50, 0.0, 1.0, 0.0]])

# tabelaPotencias = np.array([[1, 2.0, 0.0, 0.0],
#                             [2, 0.0, 2.0, 0.0],
#                             [3, 0.0, 2.5, 0.0],
#                             [4, 0.0, 0.0, 0.0]])

# barraReferencia = 4
# barraFluxo = 4 
# erro = 1
# tolerancia = 0.001
# maxIter = 10

# matrizY = np.copy(matAdm(infoLinhas))
# vetorB = np.copy(montarVetorB(matrizY, barraReferencia))

# vetorP = np.copy(montarVetorP(tabelaPotencias, barraReferencia))

# vetorTheta = np.copy(calcularAngulos(vetorB, vetorP, barraReferencia))
# perdasAntigas = np.zeros(np.shape(tabelaPotencias))
# iter = 0
# while ((erro > tolerancia) and (iter <= maxIter)):
#     tabelaPerdas = np.copy(calcularPerdas(infoLinhas, tabelaPotencias, vetorTheta))
#     vetorP = np.copy(montarVetorP(tabelaPerdas, barraReferencia))

#     desvioDasPerdas = np.zeros(len(tabelaPerdas))
#     for i in range(len(desvioDasPerdas)):
#         delta = abs(tabelaPerdas[i][3] - perdasAntigas[i][3])
#         desvioDasPerdas[i] = delta 
#     erro = desvioDasPerdas[np.argmax(desvioDasPerdas)]
#     print('Erro: ',erro,' - Iteração: ',iter+1)

#     vetorTheta = np.copy(calcularAngulos(vetorB, vetorP, barraReferencia))
#     perdasAntigas = np.copy(tabelaPerdas)
#     iter += 1

# matrizFluxo = calcularMatrizFluxo(matrizY, vetorTheta)
# fluxo = calcularFluxo(matrizFluxo, barraFluxo)
# print('O fluxo na barra ', barraFluxo, ' = ',fluxo , ' pu')

## ----- TESTE RÁPIDO 6 ----- ##

# Incognitas: theta 1, theta 3 e v3

# infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm/2, tapkm, defasagemkm]

# infoLinhas = np.array([ [1, 2, 0.01, 0.1, 0.0, 0.98, 0.0],
#                         [1, 3, 0.02, 0.2, 0.0, 1.0, 30.0],
#                         [2, 3, 0.03, 0.6, 0.05, 1.0, 0.0]])

infoLinhas = np.array([ [1, 2, 0.006, 0.032, 0.005, 1.0, 0.0],
                        [1, 3, 0.012, 0.064, 0.010, 1.0, 0.0],
                        [2, 3, 0.036, 0.192, 0.030, 1.0, 0.0]])

# tabelaPotencias = [barra, potência geração ativa, potência geração reativa, potência carga ativa, potência carga ativa, perdas na barra]

tabelaPotencias = np.array([[1, 0.5, 0.0, 0.0, 0.0, 0.0],
                            [2, 0.0, 0.0, 1.0, 0.3, 0.0],
                            [3, 0.0, 0.0, 0.5, 0.2, 0.0]])

# tensoesBarras = [barra, tensao, angulo]

tensoesAngulosBarras = np.array([[1, 1.05, -0.01733025],
                                 [2, 1.00, 0.07425951],
                                 [3, -0.00230929, 0.0]])


# barraReferencia = 3
# barraFluxo = 4 
# erro = 1
# tolerancia = 0.001
# maxIter = 10

# infoLinhas = np.array([[1, 2, 0.2, 1.0, 0.02, 1.0, 0.0]])


matrizY = np.copy(matAdm(infoLinhas))

print(matrizY)
print(matrizY.real)
print(matrizY.imag)





