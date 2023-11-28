# 14/11/23 - Lucas Xavier de Morais
# Análise de falta fase-fase
# SEP I - Engenharia Elétrica (UFSJ)
import numpy as np
from icecream import ic

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
        if k == m :
            matrizY[k][k] = matrizY[k][k] + admitancia
            continue
        matrizY[k][k] = matrizY[k][k] + (tap**2)*admitancia + susceptancia
        matrizY[k][m] = -tap*np.exp(1j*defasagem)*admitancia
        matrizY[m][k] = -tap*np.exp(-1j*defasagem)*admitancia
        matrizY[m][m] = matrizY[m][m] + admitancia + susceptancia
    
    return matrizY

def inversaEspecial(m):
    a, b = m.shape
    if a != b: raise ValueError("A funcao inversa especial funciona apenas com matrizes quadradas")
    i = np.eye(a,a)
    retM = np.linalg.lstsq(m.imag, i, rcond=-1)[0]
    return 1j*retM

#Definindo a mtriz T
alpha = np.cos(120*np.pi/180) + 1j*np.sin(120*np.pi/180)
alpha2 = np.cos(240*np.pi/180) + 1j*np.sin(240*np.pi/180)
tranformacaoT = np.array( [ [1,      1,      1],
                            [1, alpha2,  alpha],
                            [1,  alpha, alpha2 ]])

# ----------------- ROTINA -----------------

# Parâmetros do exercício

# Definindo a barra do curto 
barraCurto = 3

# Definicao da fases do curto fase-fase
# 1 : falta BC; 2 : falta CA; 3 : falta AB
# 1 : Ia      ; 2 : Ib      ; 3 : Ic
# O padrão é uma falta BC, e os cálculos são feitos com base na corrente da fase A 
# Se for feito em outra fase, basta fazer como se fosse pra A, e depois rotacionar a partir 
# da corrente em questão como de esta fosse a A. 
# Por exemplo, neste exercicio o curto e entre as fases AB. Logo, ao final das contas,  
# a corrente calculada como A, é a corrente em C, a corrente como B seria a proxima da rotacao
# que seria a A, e por fim a corrente C seria a B.
# Ia -> Ic 
# Ib -> Ia 
# Ic -> Ib 
falta = 3

# Construir aqui as tabelas para as linhas para cada sequencia
# infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm total, tapkm, defasagemkm]

infoLinhasPos = np.array([  [1, 1, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [1, 3, 0.0, 0.10, 0.0, 1.0, 0.0],
                            [3, 4, 0.0, 0.10, 0.0, 1.0, 0.0],
                            [3, 4, 0.0, 0.10, 0.0, 1.0, 0.0],
                            [4, 5, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [2, 2, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [2, 3, 0.0, 0.10, 0.0, 1.0, 0.0]])

infoLinhasNeg = np.array([  [1, 1, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [1, 3, 0.0, 0.10, 0.0, 1.0, 0.0],
                            [3, 4, 0.0, 0.10, 0.0, 1.0, 0.0],
                            [3, 4, 0.0, 0.10, 0.0, 1.0, 0.0],
                            [4, 5, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [2, 2, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [2, 3, 0.0, 0.10, 0.0, 1.0, 0.0]])

infoLinhasZero = np.array([ [1, 1, 0.0, 0.50, 0.0, 1.0, 0.0],
                            [3, 3, 0.0, 0.10, 0.0, 1.0, 0.0],
                            [3, 4, 0.0, 0.10, 0.0, 1.0, 0.0],
                            [3, 4, 0.0, 0.10, 0.0, 1.0, 0.0],
                            [4, 4, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [5, 5, 0.0, 0.01, 0.0, 1.0, 0.0],
                            [2, 2, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [2, 3, 0.0, 0.10, 0.0, 1.0, 0.0]])


# #DETALHE IMPORTANTE:SE A IMPEDANCIA NAO ESTA CONECTADA NAO COLOCAR ELA NA MATRIZ
# COLOCAR APENAS AS QUE ESTAO CONECTADAS A TERRA

# infoLinhasPos = np.array([  [1, 1, 0.0, 0.20, 0.0, 1.0, 0.0],
#                             [1, 2, 0.0, 0.20, 0.0, 1.0, 0.0],
#                             [2, 3, 0.0, 0.10, 0.0, 1.0, 0.0],
#                             [3, 4, 0.0, 0.25, 0.0, 1.0, 0.0],
#                             [4, 6, 0.0, 0.05, 0.0, 1.0, 0.0],
#                             [6, 5, 0.0, 0.20, 0.0, 1.0, 0.0],
#                             [5, 5, 0.0, 0.10, 0.0, 1.0, 0.0]])
#
# infoLinhasNeg = np.array([  [1, 1, 0.0, 0.20, 0.0, 1.0, 0.0],
#                             [1, 2, 0.0, 0.20, 0.0, 1.0, 0.0],
#                             [2, 3, 0.0, 0.10, 0.0, 1.0, 0.0],
#                             [3, 4, 0.0, 0.25, 0.0, 1.0, 0.0],
#                             [4, 6, 0.0, 0.05, 0.0, 1.0, 0.0],
#                             [6, 5, 0.0, 0.20, 0.0, 1.0, 0.0],
#                             [5, 5, 0.0, 0.10, 0.0, 1.0, 0.0]])
#
# infoLinhasZero = np.array([ [1, 1, 0.0, 0.05, 0.0, 1.0, 0.0],
#                             [2, 2, 0.0, 0.20, 0.0, 1.0, 0.0],
#                             [2, 3, 0.0, 0.05, 0.0, 1.0, 0.0],
#                             [4, 6, 0.0, 0.05, 0.0, 1.0, 0.0],
#                             [6, 6, 0.0, 0.20, 0.0, 1.0, 0.0],
#                             [5, 5, 0.0, 0.05, 0.0, 1.0, 0.0]])


#Construção das matrizes positiva
matrizYPos = np.copy(matAdm(infoLinhasPos))
impedanciaPos = np.copy(np.linalg.inv(matrizYPos))
print("Matrizes sequencia positiva")
print(matrizYPos.imag)
print(impedanciaPos.imag)

#Construção das matrizes negativa
matrizYNeg = np.copy(matAdm(infoLinhasNeg))
impedanciaNeg = np.copy(np.linalg.inv(matrizYNeg))
print("Matrizes sequencia negativa")
print(matrizYNeg.imag)
print(impedanciaNeg.imag)


#Construção das matrizes zero
matrizYZero = np.copy(matAdm(infoLinhasZero))
matrizYZero[4][4] = 0.0 + 1j*0.0
impedanciaZero = -1*np.copy(inversaEspecial(matrizYZero))
# impedanciaZero = np.copy(np.linalg.inv(matrizYZero))
print("Matrizes sequencia zero")
print(matrizYZero.imag)
print(impedanciaZero.imag)

# Impedancias da barra de falta
barra = barraCurto - 1
ZPos  = impedanciaPos[barra][barra]
ZNeg  = impedanciaNeg[barra][barra]
ZZero = impedanciaZero[barra][barra]
ic(ZPos)
ic(ZNeg)
ic(ZZero)

# Para as correntes de falta na barra de curto considerando pre-falta como 1/_0
# IaPos = ( 1/_0 ) / ( ZPos + ZNeg + ZZero )
ZEq = ZPos + ZNeg + ZZero
correntePos = 1 / ZEq
# Ia = IaPos + IaNeg + IaZero
# MAS IaPos = IaNeg = IaZero
correnteNeg = correntePos
correnteZero = correntePos
# Fazendo um vetor para as correntes complexas e desequilibradas
correntesComponentesComplexas = np.array( [ [correnteZero], [correntePos], [correnteNeg] ] )
correntesDesequilibradasPonto = np.dot( tranformacaoT, correntesComponentesComplexas )
# ic(correntesComponentesComplexas)
# ic(correntesDesequilibradasPonto)

# Calculo das tensoes nas barras
barra = barraCurto - 1
numeroBarras = matrizYPos.shape[0]

vetorAuxCorrente = np.zeros((numeroBarras,1),dtype=np.complex_)
vetorAuxCorrente[barra] = -correnteZero
vetorAuxTensao = np.zeros((numeroBarras,1))
tensoesBarrasZero = vetorAuxTensao + ic(np.dot(impedanciaZero, vetorAuxCorrente))
ic(tensoesBarrasZero)

vetorAuxCorrente = np.zeros((numeroBarras,1),dtype=np.complex_)
vetorAuxCorrente[barra] = -correntePos
vetorAuxTensao = np.ones((numeroBarras,1))
tensoesBarrasPos = vetorAuxTensao + np.dot(impedanciaPos, vetorAuxCorrente)
ic(tensoesBarrasPos)

vetorAuxCorrente = np.zeros((numeroBarras,1),dtype=np.complex_)
vetorAuxCorrente[barra] = -correnteNeg
vetorAuxTensao = np.zeros((numeroBarras,1))
tensoesBarrasNeg = vetorAuxTensao + np.dot(impedanciaNeg, vetorAuxCorrente)
ic(tensoesBarrasNeg)

# Calculo das tensoes em todas as barras
tensoesDesequilibradas = []
for barra in range(numeroBarras):
    compZero = tensoesBarrasZero[barra][0]
    compPos = tensoesBarrasPos[barra][0]
    compNeg = tensoesBarrasNeg[barra][0]
    vetorAux = np.array([ [compZero], [compPos], [compNeg] ])
    vetorTensoesFasoriais = np.dot( tranformacaoT, vetorAux )
    tensoesDesequilibradas.append(vetorTensoesFasoriais)

# c = 1
# for bar in tensoesDesequilibradas:
#     print(f'BARRA {c}')
#     for fase in bar:
#         print(f'TENSAO : {np.absolute(fase[0])} , fase: {np.angle(fase[0],deg=True)}')
#     c+=1

# ---------- FIM ANALISE FASE-TERRA ----------
# Daqui pra baixo e feita a análise do exercicio

#Tensoes no ponto de falha
# tensaoAB = tensoesDesequilibradas[0][0][0] - tensoesDesequilibradas[0][1][0]
# tensaoBC = tensoesDesequilibradas[0][1][0] - tensoesDesequilibradas[0][2][0]
# tensaoCA = tensoesDesequilibradas[0][2][0] - tensoesDesequilibradas[0][0][0]
# print(" --- TENSOES --- ")
# print(f'TENSAO AB: {np.absolute(tensaoAB)} , fase: {np.angle(tensaoAB,deg=True)}')
# print(f'TENSAO BC: {np.absolute(tensaoBC)} , fase: {np.angle(tensaoBC,deg=True)}')
# print(f'TENSAO CA: {np.absolute(tensaoCA)} , fase: {np.angle(tensaoCA,deg=True)}')

#Gerador 1
angulo = -30
deslocamentoTrafo = np.cos(np.deg2rad(angulo)) + (1j*np.sin(np.deg2rad(angulo)))
# deslocamentoTrafo = 1

correnteGeradorZero = 0

tensaoPontoPos = tensoesBarrasPos[0][0]
ic(tensaoPontoPos)
admitanciaBarraPos = 1j*0.2
correnteGeradorPos = (1-tensaoPontoPos) / admitanciaBarraPos
ic(correnteGeradorPos)
correnteGeradorPos = correnteGeradorPos*deslocamentoTrafo

tensaoPontoNeg = tensoesBarrasNeg[0][0]
ic(tensaoPontoNeg)
admitanciaBarraNeg = 1j*0.2
correnteGeradorNeg = (-tensaoPontoNeg) / admitanciaBarraNeg 
ic(correnteGeradorNeg)
correnteGeradorNeg = correnteGeradorNeg*deslocamentoTrafo

# Fazendo um vetor para as correntes complexas e desequilibradas
correntesComponentesComplexasGerador = np.array( [ [correnteGeradorZero], [correnteGeradorPos], [correnteGeradorNeg] ] )
correntesDesequilibradasGerador = np.dot( tranformacaoT, correntesComponentesComplexasGerador )
ic(correntesComponentesComplexasGerador)
ic(correntesDesequilibradasGerador)
# Passando de pu para a base na barra
# correnteBase = (100*(10**6)) / (13*(10**3))
# correntesDesequilibradasGerador = correntesDesequilibradasGerador * correnteBase
# A rotacao de fases baseada entre quais fases sao acontece o curto acontece aqui no final, ao entregar a resposta
print(" --- GERADOR 1 --- ")
print(f'Corrente A: {np.absolute(correntesDesequilibradasGerador[0])[0]} , fase: {np.angle(correntesDesequilibradasGerador[0],deg=True)[0]}')
print(f'Corrente B: {np.absolute(correntesDesequilibradasGerador[1])[0]} , fase: {np.angle(correntesDesequilibradasGerador[1],deg=True)[0]}')
print(f'Corrente C: {np.absolute(correntesDesequilibradasGerador[2])[0]} , fase: {np.angle(correntesDesequilibradasGerador[2],deg=True)[0]}')




