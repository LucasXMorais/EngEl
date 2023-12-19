import numpy as np
import matplotlib.pyplot as plt
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

def faseTerra(impedanciaPos, impedanciaNeg, impedanciaZero, barraCurto):
    # print('--- FASE TERRA ---')
    # Impedancias da barra de falta
    barra = barraCurto - 1
    ZPos  = impedanciaPos[barra][barra]
    ZNeg  = impedanciaNeg[barra][barra]
    ZZero = impedanciaZero[barra][barra]
    # ic(ZPos)
    # ic(ZNeg)
    # ic(ZZero)

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
    tensoesBarrasZero = vetorAuxTensao + np.dot(impedanciaZero, vetorAuxCorrente)
    # ic(tensoesBarrasZero)

    vetorAuxCorrente = np.zeros((numeroBarras,1),dtype=np.complex_)
    vetorAuxCorrente[barra] = -correntePos
    vetorAuxTensao = np.ones((numeroBarras,1))
    tensoesBarrasPos = vetorAuxTensao + np.dot(impedanciaPos, vetorAuxCorrente)
    # ic(tensoesBarrasPos)

    vetorAuxCorrente = np.zeros((numeroBarras,1),dtype=np.complex_)
    vetorAuxCorrente[barra] = -correnteNeg
    vetorAuxTensao = np.zeros((numeroBarras,1))
    tensoesBarrasNeg = vetorAuxTensao + np.dot(impedanciaNeg, vetorAuxCorrente)
    # ic(tensoesBarrasNeg)

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
#Gerador 1
    # angulo = -30
    # deslocamentoTrafo = np.cos(np.deg2rad(angulo)) + (1j*np.sin(np.deg2rad(angulo)))
    deslocamentoTrafo = 1

    correnteGeradorZero = 0

    tensaoPontoPos = tensoesBarrasPos[0][0]
    # ic(tensaoPontoPos)
    admitanciaBarraPos = 1j*0.12
    correnteGeradorPos = (1-tensaoPontoPos) / admitanciaBarraPos
    # ic(correnteGeradorPos)
    correnteGeradorPos = correnteGeradorPos*deslocamentoTrafo

    tensaoPontoNeg = tensoesBarrasNeg[0][0]
    # ic(tensaoPontoNeg)
    admitanciaBarraNeg = 1j*0.12
    correnteGeradorNeg = (-tensaoPontoNeg) / admitanciaBarraNeg
    # ic(correnteGeradorNeg)
    correnteGeradorNeg = correnteGeradorNeg*deslocamentoTrafo

# Fazendo um vetor para as correntes complexas e desequilibradas
    correntesComponentesComplexasGerador = np.array( [ [correnteGeradorZero], [correnteGeradorPos], [correnteGeradorNeg] ] )
    correntesDesequilibradasGerador = np.dot( tranformacaoT, correntesComponentesComplexasGerador )
    # ic(correntesComponentesComplexasGerador)
    # ic(correntesDesequilibradasGerador)
# Passando de pu para a base na barra
# correnteBase = (100*(10**6)) / (13*(10**3))
# correntesDesequilibradasGerador = correntesDesequilibradasGerador * correnteBase
# A rotacao de fases baseada entre quais fases sao acontece o curto acontece aqui no final, ao entregar a resposta
    print(f" --- GERADOR 1 --- BARRA {barraCurto}")
    print(f'Corrente A: {np.absolute(correntesDesequilibradasGerador[0])[0]:.4f} , fase: {np.angle(correntesDesequilibradasGerador[0],deg=True)[0]:.2f}')
    print(f'Corrente B: {np.absolute(correntesDesequilibradasGerador[1])[0]:.4f} , fase: {np.angle(correntesDesequilibradasGerador[1],deg=True)[0]:.2f}')
    print(f'Corrente C: {np.absolute(correntesDesequilibradasGerador[2])[0]:.4f} , fase: {np.angle(correntesDesequilibradasGerador[2],deg=True)[0]:.2f}')
    return correntesDesequilibradasGerador

def faseFase(impedanciaPos, impedanciaNeg, impedanciaZero, barraCurto):
    # print('--- FASE FASE ---')
# Impedancias da barra de falta
    barra = barraCurto - 1
    ZPos  = impedanciaPos[barra][barra]
    ZNeg  = impedanciaNeg[barra][barra]
    ZZero = impedanciaZero[barra][barra]
    # ic(ZPos)
    # ic(ZNeg)

# Para as correntes de falta na barra de curto considerando pre-falta como 1/_0
# IaPos = ( 1/_0 ) / ( ZPos + ZNeg )
# IaNeg = - IaPos
# IaZero = 0/_0
    ZEq = ZPos + ZNeg
    correntePos = 1 / ZEq
    # ic(correntePos)
    correnteNeg = -correntePos
    correnteZero = 0+(1j*0)
# Fazendo um vetor para as correntes complexas e desequilibradas
    correntesComponentesComplexas = np.array( [ [correnteZero], [correntePos], [correnteNeg] ] )
    correntesDesequilibradasPonto = np.dot( tranformacaoT, correntesComponentesComplexas )
    # ic(correntesComponentesComplexas)
    # ic(correntesDesequilibradasPonto)

# Calculo das tensoes nas barras
    barra = barraCurto - 1
    numeroBarras = matrizYPos.shape[0]

    tensoesBarrasZero = np.zeros((numeroBarras,1),dtype=np.complex_)

    vetorAuxCorrente = np.zeros((numeroBarras,1),dtype=np.complex_)
    vetorAuxCorrente[barra] = -correntePos
    vetorAuxTensao = np.ones((numeroBarras,1))
    tensoesBarrasPos = vetorAuxTensao + np.dot(impedanciaPos, vetorAuxCorrente)
    # ic(tensoesBarrasPos)

    vetorAuxCorrente = np.zeros((numeroBarras,1),dtype=np.complex_)
    vetorAuxCorrente[barra] = -correnteNeg
    vetorAuxTensao = np.zeros((numeroBarras,1))
    tensoesBarrasNeg = vetorAuxTensao + np.dot(impedanciaNeg, vetorAuxCorrente)
    # ic(tensoesBarrasNeg)


# Calculo das tensoes em todas as barras
    tensoesDesequilibradas = []
    for barra in range(numeroBarras):
        compZero = tensoesBarrasZero[barra][0]
        compPos = tensoesBarrasPos[barra][0]
        compNeg = tensoesBarrasNeg[barra][0]
        vetorAux = np.array([ [compZero], [compPos], [compNeg] ])
        vetorTensoesFasoriais = np.dot( tranformacaoT, vetorAux )
        tensoesDesequilibradas.append(vetorTensoesFasoriais)
# ic(tensoesDesequilibradas)
# ---------- FIM ANALISE FASE-FASE-TERRA ----------
# Daqui pra baixo e feita a análise do exercicio
# No exercicio abaixo, o objeitvo era calcular as coorrentes nos
# geradores localizados nas barras 1 e 5
# A analise acima e a analise base
# Os geradores 1 e 2 estao nas barras 1 e 5 respectivamente

#Gerador 1
    angulo = -30
# deslocamentoTrafo = np.cos(np.deg2rad(angulo)) + (1j*np.sin(np.deg2rad(angulo)))
    deslocamentoTrafo = 1

    correnteGeradorZero = 0

    tensaoPontoPos = 1 - tensoesBarrasPos[1][0]
    admitanciaBarraPos = 1j*0.12
    correnteGeradorPos = (tensaoPontoPos) / admitanciaBarraPos
    # ic(correnteGeradorPos)
    correnteGeradorPos = correnteGeradorPos*deslocamentoTrafo
    # ic(correnteGeradorPos)

    tensaoPontoNeg = 0 - tensoesBarrasNeg[1][0]
    admitanciaBarraNeg = 1j*0.12
    correnteGeradorNeg = (tensaoPontoNeg) / admitanciaBarraNeg
    # ic(correnteGeradorNeg)
    correnteGeradorNeg = correnteGeradorNeg*deslocamentoTrafo
    # ic(correnteGeradorNeg)

# Fazendo um vetor para as correntes complexas e desequilibradas
    correntesComponentesComplexasGerador = np.array( [ [correnteGeradorZero], [correnteGeradorPos], [correnteGeradorNeg] ] )
    correntesDesequilibradasGerador = np.dot( tranformacaoT, correntesComponentesComplexasGerador )
    # ic(correntesComponentesComplexasGerador)
    # ic(correntesDesequilibradasGerador)
# Passando de pu para a base na barra
# correnteBase = (100*(10**6)) / (13*(10**3))
# correntesDesequilibradasGerador = correntesDesequilibradasGerador * correnteBase
# A rotacao de fases baseada entre quais fases sao acontece o curto acontece aqui no final, ao entregar a resposta
    print(f" --- GERADOR 1 --- BARRA {barraCurto}")
    print(f'Corrente A: {np.absolute(correntesDesequilibradasGerador[0])[0]:.4f} , fase: {np.angle(correntesDesequilibradasGerador[0],deg=True)[0]:.2f}')
    print(f'Corrente B: {np.absolute(correntesDesequilibradasGerador[1])[0]:.4f} , fase: {np.angle(correntesDesequilibradasGerador[1],deg=True)[0]:.2f}')
    print(f'Corrente C: {np.absolute(correntesDesequilibradasGerador[2])[0]:.4f} , fase: {np.angle(correntesDesequilibradasGerador[2],deg=True)[0]:.2f}')
    return correntesDesequilibradasGerador

def terraFaseFase(impedanciaPos, impedanciaNeg, impedanciaZero, barraCurto):
    # print('--- FASE FASE TERRA ---')
# Impedancias da barra de falta
    barra = barraCurto - 1
    ZPos  = impedanciaPos[barra][barra]
    ZNeg  = impedanciaNeg[barra][barra]
    ZZero = impedanciaZero[barra][barra]
    # ic(ZPos)
    # ic(ZNeg)
    # ic(ZZero)

# Para as correntes de falta na barra de curto considerando pre-falta como 1/_0
    ZEq = ZPos + ( (ZNeg*ZZero) / (ZNeg+ZZero) )
    correntePos = 1 / ZEq
    # ic(correntePos)
    tensaoPos = 1 - (ZPos * correntePos)
    # ic(tensaoPos)
# Tensoes de seq zer, pos e neg na barra é a pre-falta - impedancia positiva * corrente positiva
    tensaoNeg = tensaoPos
    correnteNeg = -tensaoNeg / ZNeg
    tensaoZero = tensaoPos
    correnteZero = -tensaoZero / ZZero
# Fazendo um vetor para as correntes complexas e desequilibradas
    correntesComponentesComplexas = np.array( [ [correnteZero], [correntePos], [correnteNeg] ] )
    correntesDesequilibradasPonto = np.dot( tranformacaoT, correntesComponentesComplexas )
    # ic(correntesComponentesComplexas)
    # ic(correntesDesequilibradasPonto)

# Calculo das tensoes nas barras
    numeroBarras = matrizYPos.shape[0]

    vetorAuxCorrente = np.zeros((numeroBarras,1),dtype=np.complex_)
    vetorAuxCorrente[barra] = -correnteZero
    # ic(vetorAuxCorrente)
    vetorAuxTensao = np.zeros((numeroBarras,1))
    tensoesBarrasZero = vetorAuxTensao + np.dot(impedanciaZero, vetorAuxCorrente)
    # ic(tensoesBarrasZero)

    vetorAuxCorrente = np.zeros((numeroBarras,1),dtype=np.complex_)
    vetorAuxCorrente[barra] = -correntePos
    vetorAuxTensao = np.ones((numeroBarras,1))
    tensoesBarrasPos = vetorAuxTensao + np.dot(impedanciaPos, vetorAuxCorrente)
    # ic(tensoesBarrasPos)

    vetorAuxCorrente = np.zeros((numeroBarras,1),dtype=np.complex_)
    vetorAuxCorrente[barra] = -correnteNeg
    vetorAuxTensao = np.zeros((numeroBarras,1))
    tensoesBarrasNeg = vetorAuxTensao + np.dot(impedanciaNeg, vetorAuxCorrente)
    # ic(tensoesBarrasNeg)

# Calculo das tensoes em todas as barras
    tensoesDesequilibradas = []
    for barra in range(numeroBarras):
        compZero = tensoesBarrasZero[barra][0]
        compPos = tensoesBarrasPos[barra][0]
        compNeg = tensoesBarrasNeg[barra][0]
        vetorAux = np.array([ [compZero], [compPos], [compNeg] ])
        tensoesDesequilibradas.append(np.dot( tranformacaoT, vetorAux ))

# ---------- FIM ANALISE FASE-FASE-TERRA ----------
# Daqui pra baixo e feita a análise do exercicio
# No exercicio abaixo, o objeitvo era calcular as coorrentes nos
# geradores localizados nas barras 1 e 5
# A analise acima e a analise base
# Os geradores 1 e 2 estao nas barras 1 e 5 respectivamente

#Gerador 1
    angulo = -30
# deslocamentoTrafo = np.cos(np.deg2rad(angulo)) + (1j*np.sin(np.deg2rad(angulo)))
    deslocamentoTrafo = 1

    tensaoBarraZero = 0 - tensoesBarrasZero[1][0]
    admitanciaBarraZero = 1j*0.016
    correnteGeradorZero = (tensaoBarraZero) / admitanciaBarraZero
    # ic(correnteGeradorZero)
    correnteGeradorZero = correnteGeradorZero*deslocamentoTrafo
    # ic(correnteGeradorZero)

    tensaoPontoPos = 1 - tensoesBarrasPos[1][0]
    admitanciaBarraPos = 1j*0.12
    correnteGeradorPos = (tensaoPontoPos) / admitanciaBarraPos
    # ic(correnteGeradorPos)
    correnteGeradorPos = correnteGeradorPos*deslocamentoTrafo
    # ic(correnteGeradorPos)

    tensaoPontoNeg = 0 - tensoesBarrasNeg[1][0]
    admitanciaBarraNeg = 1j*0.12
    correnteGeradorNeg = (tensaoPontoNeg) / admitanciaBarraNeg
    # ic(correnteGeradorNeg)
    correnteGeradorNeg = correnteGeradorNeg*deslocamentoTrafo
    # ic(correnteGeradorNeg)

# Fazendo um vetor para as correntes complexas e desequilibradas
    correntesComponentesComplexasGerador = np.array( [ [correnteGeradorZero], [correnteGeradorPos], [correnteGeradorNeg] ] )
    correntesDesequilibradasGerador = np.dot( tranformacaoT, correntesComponentesComplexasGerador )
    # ic(correntesComponentesComplexasGerador)
    # ic(correntesDesequilibradasGerador)
# Passando de pu para a base na barra
# correnteBase = (100*(10**6)) / (13*(10**3))
# correntesDesequilibradasGerador = correntesDesequilibradasGerador * correnteBase
# A rotacao de fases baseada entre quais fases sao acontece o curto acontece aqui no final, ao entregar a resposta
    print(f" --- GERADOR 1 --- BARRA {barraCurto}")
    print(f'Corrente A: {np.absolute(correntesDesequilibradasGerador[0])[0]:.4f} , fase: {np.angle(correntesDesequilibradasGerador[0],deg=True)[0]:.2f}')
    print(f'Corrente B: {np.absolute(correntesDesequilibradasGerador[1])[0]:.4f} , fase: {np.angle(correntesDesequilibradasGerador[1],deg=True)[0]:.2f}')
    print(f'Corrente C: {np.absolute(correntesDesequilibradasGerador[2])[0]:.4f} , fase: {np.angle(correntesDesequilibradasGerador[2],deg=True)[0]:.2f}')
    return correntesDesequilibradasGerador

# ----------------- ROTINA -----------------
# Parâmetros do exercício
# Definindo a barra do curto

# infoLinhas = [barra de, barra para, resistencia km, reatancia km, susceptancia shuntkm total, tapkm, defasagemkm]

infoLinhasPos = np.array([  [1, 1, 0.0, 0.02, 0.0, 1.0, 0.0],
                            [1, 4, 0.0, 0.37, 0.0, 1.0, 0.0],
                            [1, 6, 0.0, 0.518, 0.0, 1.0, 0.0],
                            [3, 4, 0.0, 0.133, 0.0, 1.0, 0.0],
                            [4, 6, 0.0, 0.407, 0.0, 1.0, 0.0],
                            [5, 6, 0.0, 0.3, 0.0, 1.0, 0.0],
                            [2, 5, 0.0, 0.64, 0.0, 1.0, 0.0],
                            [2, 2, 0.0, 0.06, 0.0, 1.0, 0.0],
                            [2, 3, 0.0, 1.05, 0.0, 1.0, 0.0]])

infoLinhasNeg = np.array([  [1, 1, 0.0, 0.02, 0.0, 1.0, 0.0],
                            [1, 4, 0.0, 0.37, 0.0, 1.0, 0.0],
                            [1, 6, 0.0, 0.518, 0.0, 1.0, 0.0],
                            [3, 4, 0.0, 0.133, 0.0, 1.0, 0.0],
                            [4, 6, 0.0, 0.407, 0.0, 1.0, 0.0],
                            [5, 6, 0.0, 0.3, 0.0, 1.0, 0.0],
                            [2, 5, 0.0, 0.64, 0.0, 1.0, 0.0],
                            [2, 2, 0.0, 0.06, 0.0, 1.0, 0.0],
                            [2, 3, 0.0, 1.05, 0.0, 1.0, 0.0]])

infoLinhasZero = np.array([ [1, 1, 0.0, 0.016, 0.0, 1.0, 0.0],
                            [1, 4, 0.0, 0.925, 0.0, 1.0, 0.0],
                            [1, 6, 0.0, 1.042, 0.0, 1.0, 0.0],
                            [4, 4, 0.0, 0.133, 0.0, 1.0, 0.0],
                            [4, 6, 0.0, 1.03, 0.0, 1.0, 0.0],
                            [6, 6, 0.0, 0.3, 0.0, 1.0, 0.0],
                            [2, 5, 0.0, 1.92, 0.0, 1.0, 0.0],
                            [2, 2, 0.0, 0.08, 0.0, 1.0, 0.0],
                            [2, 3, 0.0, 2.63, 0.0, 1.0, 0.0]])

#Construção das matrizes positiva
matrizYPos = np.copy(matAdm(infoLinhasPos))
impedanciaPos = np.copy(np.linalg.inv(matrizYPos))
print("Matrizes sequencia positiva")
ic(matrizYPos.imag)
ic(impedanciaPos.imag)

#Construção das matrizes negativa
matrizYNeg = np.copy(matAdm(infoLinhasNeg))
impedanciaNeg = np.copy(np.linalg.inv(matrizYNeg))
print("Matrizes sequencia negativa")
ic(matrizYNeg.imag)
ic(impedanciaNeg.imag)


#Construção das matrizes zero
matrizYZero = np.copy(matAdm(infoLinhasZero))
# matrizYZero[4][4] = 0.0 + 1j*0.0
# impedanciaZero = -1*np.copy(inversaEspecial(matrizYZero.imag))
impedanciaZero = np.copy(np.linalg.inv(matrizYZero))
print("Matrizes sequencia zero")
ic(matrizYZero.imag)
ic(impedanciaZero.imag)

bars = [x+1 for x in range(6)]

correntesGeradorFT = []
print('--------------------')
print('MEMORIAIS FASE TERRA')
for b in bars:
    correntesGeradorFT.append(faseTerra(impedanciaPos, impedanciaNeg, impedanciaZero, b))

correntesGeradorFF = []
print('-------------------')
print('MEMORIAIS FASE FASE')
for b in bars:
    correntesGeradorFF.append(faseFase(impedanciaPos, impedanciaNeg, impedanciaZero, b))

correntesGeradorFFT = []
print('-------------------------')
print('MEMORIAIS FASE FASE TERRA')
for b in bars:
    correntesGeradorFFT.append(terraFaseFase(impedanciaPos, impedanciaNeg, impedanciaZero, b))

corAFT = [np.absolute(i[0]) for i in correntesGeradorFT]
corBFF = [np.absolute(i[0]) for i in correntesGeradorFF]
corBFFT = [np.absolute(i[0]) for i in correntesGeradorFFT]

plt.plot(bars, corAFT, label='Fase Terra')
plt.plot(bars, corBFF, label='Fase Fase')
plt.plot(bars, corBFFT, label='Fase Fase Terra')
plt.legend()
plt.xlabel('Barra')
plt.ylabel('Corrente de curto')
plt.title('Gráfico corrente de curto por barra')
plt.show()
    




