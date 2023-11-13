# 13/11/23 - Lucas Xavier de Morais
# TESTE 14 
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
        if k == m :
            matrizY[k][k] = matrizY[k][k] + admitancia
            continue
        matrizY[k][k] = matrizY[k][k] + (tap**2)*admitancia + susceptancia
        matrizY[k][m] = -tap*np.exp(1j*defasagem)*admitancia
        matrizY[m][k] = -tap*np.exp(-1j*defasagem)*admitancia
        matrizY[m][m] = matrizY[m][m] + admitancia + susceptancia
    
    return matrizY

# Função criada para invereter uma matriz singular quadrada com a função lstsq do numpy
# Como nessa materia estao sendo usadas matrizes complexas, uso a parte imaginaria que 
# e o que importa pro exercicio. Mas funciona com a real. O que muda e que o resultado fica 
# mais redondo. 
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

# ----------------- TESTE 14 -----------------

# infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm total, tapkm, defasagemkm]

infoLinhasPos = np.array([  [1, 1, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [1, 2, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [2, 3, 0.0, 0.10, 0.0, 1.0, 0.0],
                            [3, 4, 0.0, 0.25, 0.0, 1.0, 0.0],
                            [4, 6, 0.0, 0.05, 0.0, 1.0, 0.0],
                            [6, 5, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [5, 5, 0.0, 0.10, 0.0, 1.0, 0.0]])

infoLinhasNeg = np.array([  [1, 1, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [1, 2, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [2, 3, 0.0, 0.10, 0.0, 1.0, 0.0],
                            [3, 4, 0.0, 0.25, 0.0, 1.0, 0.0],
                            [4, 6, 0.0, 0.05, 0.0, 1.0, 0.0],
                            [6, 5, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [5, 5, 0.0, 0.10, 0.0, 1.0, 0.0]])

infoLinhasZero = np.array([ [1, 1, 0.0, 0.05, 0.0, 1.0, 0.0],
                            [2, 2, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [2, 3, 0.0, 0.05, 0.0, 1.0, 0.0],
                            [4, 6, 0.0, 0.05, 0.0, 1.0, 0.0],
                            [6, 6, 0.0, 0.20, 0.0, 1.0, 0.0],
                            [5, 5, 0.0, 0.05, 0.0, 1.0, 0.0]])

#Construção das matrizes positiva
matrizYPos = np.copy(matAdm(infoLinhasPos))
impedanciaPos = np.copy(inversaEspecial(matrizYPos))
print("Matrizes sequencia positiva")
# print(matrizYPos)
print(impedanciaPos.imag)

#Construção das matrizes negativa
matrizYNeg = np.copy(matAdm(infoLinhasNeg))
impedanciaNeg = np.copy(inversaEspecial(matrizYNeg))
print("Matrizes sequencia negativa")
# print(matrizYNeg)
print(impedanciaNeg.imag)


#Construção das matrizes zero
matrizYZero = np.copy(matAdm(infoLinhasZero))
impedanciaZero = np.copy(inversaEspecial(matrizYZero))
print("Matrizes sequencia zero")
# print(matrizYZero.imag)
print(impedanciaZero.imag)

#para uma falta na barra 5, utiliza-se os valores da impedacnia em 5,5
ZPos  = impedanciaPos[4][4]
ZNeg  = impedanciaNeg[4][4]
ZZero = impedanciaZero[4][4]

#Para as correntes de falta na barra 5 considerando pre-falta como 1/_0
ZEq = ZPos + ( (ZNeg*ZZero) / (ZNeg+ZZero) )
correntePos = 1 / ZEq
correnteNeg = -1 / ZNeg
correnteZero = -1 / ZZero
# Fazendo um vetor para as correntes complexas e desequilibradas
correntesComponentesComplexas = np.array( [ [correnteZero], [correntePos], [correnteNeg] ] )
correntesDesequilibradasPonto = np.dot( tranformacaoT, correntesComponentesComplexas )

# Tensoes de seq zer, pos e neg na barra é a pre-falta - impedancia positiva * corrente positiva
tensaoPos = 1 - (ZPos * correntePos)
tensaoNeg = tensaoPos
tensaoZero = tensaoPos

vetorAuxCorrente = np.array([ [0.0], [0.0], [0.0], [0.0], [-correnteZero], [0.0] ])
vetorAuxTensao = np.array([ [0.0], [0.0], [0.0], [0.0], [0.0], [0.0] ])
tensoesBarrasZero = vetorAuxTensao + np.dot(impedanciaZero, vetorAuxCorrente)

vetorAuxCorrente = np.array([ [0.0], [0.0], [0.0], [0.0], [-correnteZero], [0.0] ])
vetorAuxTensao = np.array([ [0.0], [0.0], [0.0], [0.0], [0.0], [0.0] ])
tensoesBarrasPos = vetorAuxTensao + np.dot(impedanciaPos, vetorAuxCorrente)

vetorAuxCorrente = np.array([ [0.0], [0.0], [0.0], [0.0], [-correnteZero], [0.0] ])
vetorAuxTensao = np.array([ [1.0], [1.0], [1.0], [1.0], [1.0], [1.0] ])
tensoesBarrasNeg = vetorAuxTensao + np.dot(impedanciaNeg, vetorAuxCorrente)

tensoesDesequilibradas = []
for barra in range(6):
    compZero = tensoesBarrasZero.real[0][0]
    compPos = tensoesBarrasPos.real[0][0]
    compNeg = tensoesBarrasNeg.real[0][0]
    vetorAux = np.array([ [compZero], [compPos], [compNeg] ])
    tensoesDesequilibradas.append(np.dot( tranformacaoT, vetorAux ))

# Os geradores 1 e 2 estao nas barras 1 e 5 respectivamente

#Gerador 1
tensaoBarraZero = tensoesDesequilibradas[0][0][0]
admitanciaBarraZero = 1j*0.05
correnteGeradorZero = (-tensaoBarraZero) / admitanciaBarraZero 

tensaoBarraPos = tensoesDesequilibradas[0][1][0]
admitanciaBarraPos = 1j*0.2
correnteGeradorPos = (1-tensaoBarraPos) / admitanciaBarraPos 

tensaoBarraNeg = tensoesDesequilibradas[0][2][0]
admitanciaBarraNeg = 1j*0.2
correnteGeradorNeg = (-tensaoBarraNeg) / admitanciaBarraNeg 

# Fazendo um vetor para as correntes complexas e desequilibradas
correntesComponentesComplexasGerador = np.array( [ [correnteGeradorZero], [correnteGeradorPos], [correnteGeradorNeg] ] )
correntesDesequilibradasGerador = np.dot( tranformacaoT, correntesComponentesComplexasGerador )
# Passando de pu para a base na barra
correnteBase = (100*(10**6)) / (13*(10**3))
correntesDesequilibradasGerador = correntesDesequilibradasGerador * correnteBase
print(" --- GERADOR 1 --- ")
print(f'Corrente A: {np.absolute(correntesDesequilibradasGerador[0])[0]} , fase: {np.angle(correntesDesequilibradasGerador[0],deg=True)[0]}')
print(f'Corrente B: {np.absolute(correntesDesequilibradasGerador[1])[0]} , fase: {np.angle(correntesDesequilibradasGerador[1],deg=True)[0]}')
print(f'Corrente C: {np.absolute(correntesDesequilibradasGerador[2])[0]} , fase: {np.angle(correntesDesequilibradasGerador[2],deg=True)[0]}')

#Gerador 2
tensaoBarraZero = tensoesDesequilibradas[4][0][0]
admitanciaBarraZero = 1j*0.05
correnteGeradorZero = (-tensaoBarraZero) / admitanciaBarraZero 

tensaoBarraPos = tensoesDesequilibradas[4][1][0]
admitanciaBarraPos = 1j*0.1
correnteGeradorPos = (1-tensaoBarraPos) / admitanciaBarraPos 

tensaoBarraNeg = tensoesDesequilibradas[4][2][0]
admitanciaBarraNeg = 1j*0.1
correnteGeradorNeg = (-tensaoBarraNeg) / admitanciaBarraNeg 

# Fazendo um vetor para as correntes complexas e desequilibradas
correntesComponentesComplexasGerador = np.array( [ [correnteGeradorZero], [correnteGeradorPos], [correnteGeradorNeg] ] )
correntesDesequilibradasGerador = np.dot( tranformacaoT, correntesComponentesComplexasGerador )
# Passando de pu para a base na barra
correnteBase = (100*(10**6)) / (13*(10**3))
correntesDesequilibradasGerador = correntesDesequilibradasGerador * correnteBase
print(" --- GERADOR 2 --- ")
print(f'Corrente A: {np.absolute(correntesDesequilibradasGerador[0])[0]} , fase: {np.angle(correntesDesequilibradasGerador[0],deg=True)[0]}')
print(f'Corrente B: {np.absolute(correntesDesequilibradasGerador[1])[0]} , fase: {np.angle(correntesDesequilibradasGerador[1],deg=True)[0]}')
print(f'Corrente C: {np.absolute(correntesDesequilibradasGerador[2])[0]} , fase: {np.angle(correntesDesequilibradasGerador[2],deg=True)[0]}')






