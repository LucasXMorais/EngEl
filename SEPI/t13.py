# 07/11/23 - Lucas Xavier de Morais
# TESTE 13 
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

# ----------------- TESTE 13 -----------------

# infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm total, tapkm, defasagemkm]

infoLinhasPos = np.array([  [1, 2, 0.000, 0.080, 0.0, 1.00, 0.0],
                            [1, 1, 0.000, 0.250, 0.0, 1.00, 0.0],
                            [3, 3, 0.000, 0.200, 0.0, 1.00, 0.0],
                            [1, 3, 0.000, 0.130, 0.0, 1.00, 0.0],
                            [2, 3, 0.000, 0.060, 0.0, 1.00, 0.0],
                            [2, 3, 0.000, 0.060, 0.0, 1.00, 0.0]])

infoLinhasNeg = np.array([  [1, 2, 0.000, 0.080, 0.0, 1.00, 0.0],
                            [1, 1, 0.000, 0.150, 0.0, 1.00, 0.0],
                            [3, 3, 0.000, 0.120, 0.0, 1.00, 0.0],
                            [1, 3, 0.000, 0.130, 0.0, 1.00, 0.0],
                            [2, 3, 0.000, 0.060, 0.0, 1.00, 0.0],
                            [2, 3, 0.000, 0.060, 0.0, 1.00, 0.0]])

infoLinhasZero = np.array([ [1, 2, 0.000, 0.140, 0.0, 1.00, 0.0],
                            [1, 1, 0.000, 0.030, 0.0, 1.00, 0.0],
                            [3, 3, 0.000, 0.020, 0.0, 1.00, 0.0],
                            [1, 3, 0.000, 0.170, 0.0, 1.00, 0.0],
                            [2, 3, 0.000, 0.100, 0.0, 1.00, 0.0],
                            [2, 3, 0.000, 0.100, 0.0, 1.00, 0.0]])

# # infoBarras = [barra , tipo, tensao, angulo, P.Ativa Geracao (PG), P.Reativa Geracao (QG), P.Ativa Carga (PL), P.Reativa Carga (QL) ]

# infoBarrasPos = np.array([ [1, 'V0', 1.0, 0.0, 0.6, 0.0, 0.0, 0.0],
#                         [2, 'PQ', '-', '-', 0.0, 0.0, 0.0, 0.0],
#                         [3, 'PQ', '-', '-', 0.0, 0.0, 0.0, 0.0],
#                         [4, 'PV', 1.0, '-', 0.0, 0.0, 0.468, 0.306],
#                         [5, 'PQ', '-', '-', 0.0, 0.0, 0.0, 0.0] ])

# infoBarrasNeg = np.array([ [1, 'V0', 1.0, 0.0, 0.6, 0.0, 0.0, 0.0],
#                         [2, 'PQ', '-', '-', 0.0, 0.0, 0.0, 0.0],
#                         [3, 'PQ', '-', '-', 0.0, 0.0, 0.0, 0.0],
#                         [4, 'PV', 1.0, '-', 0.0, 0.0, 0.468, 0.306],
#                         [5, 'PQ', '-', '-', 0.0, 0.0, 0.0, 0.0] ])

# infoBarrasZero = np.array([ [1, 'V0', 1.0, 0.0, 0.6, 0.0, 0.0, 0.0],
#                         [2, 'PQ', '-', '-', 0.0, 0.0, 0.0, 0.0],
#                         [3, 'PQ', '-', '-', 0.0, 0.0, 0.0, 0.0],
#                         [4, 'PV', 1.0, '-', 0.0, 0.0, 0.468, 0.306],
#                         [5, 'PQ', '-', '-', 0.0, 0.0, 0.0, 0.0] ])

#Construção das matrizes positiva
matrizYPos = np.copy(matAdm(infoLinhasPos))
impedanciaPos = np.linalg.inv(matrizYPos)

#Construção das matrizes negativa
matrizYNeg = np.copy(matAdm(infoLinhasNeg))
impedanciaNeg = np.copy(np.linalg.inv(matrizYNeg))

#Construção das matrizes zero
matrizYZero = np.copy(matAdm(infoLinhasZero))
impedanciaZero = np.copy(np.linalg.inv(matrizYZero))

correntePos =  1 / ( impedanciaPos[2][2] + ((impedanciaNeg[2][2]*impedanciaZero[2][2]) / (impedanciaNeg[2][2]+impedanciaPos[2][2]))) 
correnteNeg = - correntePos
correntesComponentesComplexas = np.array( [ [0.0], [correntePos], [correnteNeg] ] )
# correntePreFaltaPos =  1 / ( impedanciaPos[2][2] ((impedanciaNeg[2][2]*impedanciaZero[2][2]) / (impedanciaNeg[2][2]+impedanciaPos[2][2])) 

alpha = np.cos(120*np.pi/180) + 1j*np.sin(120*np.pi/180)
alpha2 = np.cos(240*np.pi/180) + 1j*np.sin(240*np.pi/180)

tranformacaoT = np.array( [ [1,      1,      1],
                            [1, alpha2,  alpha],
                            [1,  alpha, alpha2 ]])

correntesFases = np.dot(tranformacaoT, correntesComponentesComplexas)

tensoesNodaisPos = np.array([[1.0],[1.0],[1.0]]) + np.dot(impedanciaPos, np.array([ [0.0], [-correntePos], [0.0] ]))
tensoesNodaisNeg = np.array([[0.0],[0.0],[0.0]]) + np.dot(impedanciaNeg, np.array([ [0.0], [-correnteNeg], [0.0] ]))

tensoesDeslocadaFaseBarra1 = np.dot(tranformacaoT, np.array( [ [0.0], [tensoesNodaisPos[0][0]], [tensoesNodaisPos[0][0]] ] ))                                                        

tensoesDeslocadaFaseBarra2 = np.dot(tranformacaoT, np.array( [ [0.0], [tensoesNodaisPos[1][0]], [tensoesNodaisPos[1][0]] ] ))                                                        

tensoesDeslocadaFaseBarra3 = np.dot(tranformacaoT, np.array( [ [0.0], [tensoesNodaisPos[2][0]], [tensoesNodaisPos[2][0]] ] ))                                                        

correnteZeroGerador1 = 0.0
correntePosGerador1 = (1 - (tensoesNodaisPos[0][0]) ) / (0.25)
correnteNegGerador1 = (0 - (tensoesNodaisNeg[0][0]) ) / (0.25)
correnteDeslocadaGerador1 = np.dot(tranformacaoT, np.array( [ [correnteZeroGerador1], [correntePosGerador1], [correnteNegGerador1] ] ))

correnteZeroGerador2 = 0.0
correntePosGerador2 = (1 - (tensoesNodaisPos[2][0]) ) / (0.2)
correnteNegGerador2 = (0 - (tensoesNodaisNeg[2][0]) ) / (0.2)
correnteDeslocadaGerador2 = np.dot(tranformacaoT, np.array( [ [correnteZeroGerador2], [correntePosGerador2], [correnteNegGerador2] ] ))

correnteZeroLinha12 = 0.0
correntePosLinha12 = ((tensoesNodaisPos[0][0]) - (tensoesNodaisPos[1][0]) ) / (0.08)
correnteNegLinha12 = ((tensoesNodaisNeg[0][0]) - (tensoesNodaisNeg[1][0]) ) / (0.08)
correnteDeslocadaLinha12 = np.dot(tranformacaoT, np.array( [ [correnteZeroLinha12], [correntePosLinha12], [correnteNegLinha12] ] ))

correnteZeroLinha23 = 0.0
correntePosLinha23 = ((tensoesNodaisPos[1][0]) - (tensoesNodaisPos[2][0]) ) / (0.06)
correnteNegLinha23 = ((tensoesNodaisNeg[1][0]) - (tensoesNodaisNeg[2][0]) ) / (0.06)
correnteDeslocadaLinha23 = np.dot(tranformacaoT, np.array( [ [correnteZeroLinha23], [correntePosLinha23], [correnteNegLinha23] ] ))

correnteZeroLinha13 = 0.0
correntePosLinha13 = ((tensoesNodaisPos[0][0]) - (tensoesNodaisPos[2][0]) ) / (0.13)
correnteNegLinha13 = ((tensoesNodaisNeg[0][0]) - (tensoesNodaisNeg[2][0]) ) / (0.13)
correnteDeslocadaLinha13 = np.dot(tranformacaoT, np.array( [ [correnteZeroLinha13], [correntePosLinha13], [correnteNegLinha13] ] ))

print("a) As correntes desequilibradas no ponto de falta;")
print(correntesFases)

print("b) As tensões desequilibradas em todas as barras;")
print("Barra 1")
print(tensoesDeslocadaFaseBarra1)

print("Barra 2")
print(tensoesDeslocadaFaseBarra2)

print("Barra 3")
print(tensoesDeslocadaFaseBarra3)

print("c) As correntes desequilibradas nas linhas de transmissão;")
print("Linha 12")
print(correnteDeslocadaLinha12)

print("Linha 23")
print(correnteDeslocadaLinha23)

print("Linha 13")
print(correnteDeslocadaLinha13)

print("d) As correntes desequilibradas no gerador e no motor. ")
print("Gerador 1")
print(correnteDeslocadaGerador1)

print("Gerador 2 / Motor 1")
print(correnteDeslocadaGerador2)


# tensaoPos = 1 - (impedanciaPos[2][2]*correntePreFaltaPos)
# tensaoNeg = tensaoPos
# tensaoZero = tensaoPos

# correntePreFaltaNeg =  ((-1)*tensaoNeg) / impedanciaNeg[2][2]
# correntePreFaltaZero =  ((-1)*tensaoZero) / impedanciaZero[2][2]

# correnteA = correntePreFaltaPos + correntePreFaltaNeg + correntePreFaltaZero
# correnteB = correntePreFaltaPos + (alpha2*correntePreFaltaNeg) + (alpha*correntePreFaltaZero)
# correnteC = correntePreFaltaPos + (alpha*correntePreFaltaNeg) + (alpha2*correntePreFaltaZero)

# correnteNeutro = correnteA + correnteC

# tensaoA = tensaoPos + tensaoNeg + tensaoZero
# tensaoB = tensaoPos + (alpha2*tensaoNeg) + (alpha*tensaoZero)
# tensaoC = tensaoPos + (alpha*tensaoNeg) + (alpha2*tensaoZero)

# tensaoAB = tensaoA - tensaoB
# tensaoBC = tensaoB - tensaoC
# tensaoCA = tensaoC - tensaoA








