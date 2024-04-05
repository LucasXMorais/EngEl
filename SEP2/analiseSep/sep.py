# 25/03/24 - Lucas Xavier de Morais e Cássia
# Funções base para SEP
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
from icecream import ic
import configparser

# Construção da matriz admitancia Y completa
def matrizAdmitancia(dbarras, dcircuitos):
    nbar = len(dbarras)
    matrizY = np.zeros((nbar,nbar),dtype=np.complex_)

    for c in dcircuitos:
        if c['LIG(L)DESL(D)'] != 'L' : continue
        k = c['BDE'] - 1
        m = c['BPARA'] - 1
        resistencia = c['RES(PU)']
        reatancia = c['REAT(PU)']
        admitancia = 1/(resistencia + (1j*reatancia))
        susceptancia = 1j*c['SUCsh(PU)']/2
        tap = c['TAP(PU)']
        defasagem = c['DEF(GRAUS)']*np.pi/180
        if k == m :
            matrizY[k][k] = matrizY[k][k] + admitancia
            continue
        matrizY[k][k] = matrizY[k][k] + (tap**2)*admitancia + susceptancia
        matrizY[k][m] = matrizY[k][m] - tap*np.exp(-1j*defasagem)*admitancia
        matrizY[m][k] = matrizY[m][k] - tap*np.exp(1j*defasagem)*admitancia
        matrizY[m][m] = matrizY[m][m] + admitancia + susceptancia

    for b in dbarras:
        k = b['BARRA'] - 1
        if (b['Bsh(PU)'] != 0) : matrizY[k][k] += 1j*b['Bsh(PU)']

    return matrizY

# Funcao para o calculo de potencias (Pcalc) a cada iteração
def calcularFluxoKM(matrizY, angulos, tensoes):
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

# Montando a matriz Jacobiana
def jacobian(matrizY, angulos, tensoes, dbarras):

    nbarras = len(angulos)
    G = np.copy(matrizY.real)
    B = np.copy(matrizY.imag)

    # Montando as matrizes H , N, M e L da Jacobiana
    H = np.zeros((nbarras,nbarras))
    N = np.zeros((nbarras,nbarras))
    M = np.zeros((nbarras,nbarras))
    L = np.zeros((nbarras,nbarras))
    for k in range(nbarras):
        totalH = 0
        totalN = 0
        totalM = 0
        totalL = 0
        vk = tensoes[k]
        Gkk = G[k][k]
        Bkk = B[k][k]
        for m in range(nbarras):
            Gkm = G[k][m]
            Bkm = B[k][m]
            thetakm = angulos[k] - angulos[m]
            vkm = tensoes[k]*tensoes[m]
            vm = tensoes[m]
            cosThetakm = np.cos(thetakm)
            sinThetakm = np.sin(thetakm)

            H[k][m] = vkm * ( (Gkm*sinThetakm) - (Bkm*cosThetakm) ) 
            somaH = vm * ( (Gkm*sinThetakm) - (Bkm*cosThetakm) )
            totalH += somaH

            N[k][m] = vk * ( (Gkm*cosThetakm) + (Bkm*sinThetakm) ) 
            somaN = vm * ( (Gkm*cosThetakm) + (Bkm*sinThetakm) )
            totalN += somaN

            M[k][m] = -1 * vkm * ( (Gkm*cosThetakm) + (Bkm*sinThetakm) ) 
            somaM = vm * ( (Gkm*cosThetakm) + (Bkm*sinThetakm) )
            totalM += somaM

            L[k][m] = vk * ( (Gkm*sinThetakm) - (Bkm*cosThetakm) ) 
            somaL = vm * ( (Gkm*sinThetakm) - (Bkm*cosThetakm) )
            totalL += somaL

        H[k][k] = (-1 * (vk*vk) * Bkk ) - (totalH * vk)
        N[k][k] = (vk*Gkk) + totalN
        M[k][k] = (-1 * (vk*vk) * Gkk ) + (totalM * vk)
        L[k][k] = (-1*vk*Bkk) + totalL
    
    for k in range(nbarras):
        for m in range(nbarras):
            if dbarras[k]['TIPO'] != 'PQ':
                L[k][m] = 0
                L[m][k] = 0
                N[m][k] = 0
                M[k][m] = 0

            if dbarras[k]['TIPO'] == 'SW':
                H[k][m] = 0
                H[m][k] = 0
                M[m][k] = 0
                N[k][m] = 0

        if dbarras[k]['TIPO'] != 'PQ':
            L[k][k] = 10**20

        if dbarras[k]['TIPO'] == 'SW':
            H[k][k] = 10**20

    #Essas 2 linhas são para juntar as matrizes H, N e M, L, respectivamente
    jacobianoAuxP = np.concatenate((H, N), axis=1)
    jacobianoAuxQ = np.concatenate((M, L), axis=1)

    #Finalmente, juntar todas as matrizes para finalizar o jacobiano
    jacobiano = np.concatenate((jacobianoAuxP, jacobianoAuxQ), axis=0)

    return jacobiano 

# Funcao para imprimir matrizes para debugar com o octave
def printToOcatve(mat, name='mat'):
    print(f'{name} = [')
    for i in mat:
        st = ''
        for j in i:
            if j == 0 :
                s = str(int(j)) 
            else: 
                s = f'{j:.6f}'
            st += s + ' '

        st += ';'
        print(st)
    print('];')

    return 1

# Calculando os angulos e tensoes do problema de fluxo
def calcularAngulosTensoes(matrizY, dbarras):

    # Obtendo parâmetros 
    config = configparser.ConfigParser()
    config.read('config.ini')

    #Construcao dos vetores de angulos e tensoes do sistema
    nbarras = len(dbarras)
    angulos = np.zeros((nbarras,1))
    tensoes = np.ones((nbarras,1))
    for barra, v in zip(dbarras, tensoes):
        if (barra['TIPO'] == 'PV' or barra['TIPO'] == 'SW') : v[0] = barra['Vesp(PU)']

    # Calcular as potencias esperadas e agrupá-las em dois vetores, um para
    # potencias ativas e outro para potencias reativas
    ativaEsp = np.zeros((nbarras,1))
    reativaEsp = np.zeros((nbarras,1))
    for barra in dbarras:
        k = barra['BARRA'] - 1
        ativaEsp[k] = barra['PGesp(PU)'] - barra['PD(PU)']
        reativaEsp[k] = - barra['QD(PU)']
    # ativaEsp, reativaEsp = calcularFluxoKM(matrizY, angulos, tensoes)

    # Definindo parâmetros iniciais do método de newton
    maxIter = int(config['NEWTON']['MAX_ITER'])
    tol = float(config['NEWTON']['TOLERANCIA'])
    iter = 1
    fimP = 0
    fimQ = 0

    # Calculando pcalc para valores iniciais
    ativasKCalculada, reativasKCalculada = calcularFluxoKM(matrizY, angulos, tensoes)

    #Calculando deltaP e deltaQ
    deltaPks = np.zeros((nbarras,1))
    deltaQks = np.zeros((nbarras,1))
    for esp, calc, dp in zip(ativaEsp, ativasKCalculada, deltaPks):
        dp[0] = esp - calc
    for esp, calc, dq in zip(reativaEsp, reativasKCalculada, deltaQks):
        dq[0] = esp - calc

    # Montando um vetor com as variações de potência
    deltaPotencias = np.concatenate((deltaPks, deltaQks), axis=0)

    # Calculando a maior diferenca
    dPk = np.max(np.abs(deltaPks))
    dQk = np.max(np.abs(deltaQks))

    while iter <= maxIter :

        # Testando convergência
        if dPk < tol: fimP = 1
        if dQk < tol: fimQ = 1
        if fimP and fimQ: print(f'Convergiu em {iter-1} iterações'); break

        # Matriz Jacobiana
        jacobiano = jacobian(matrizY, angulos, tensoes, dbarras)

        # Fazendo dx = -J^(-1) * g
        invJac = np.linalg.inv(jacobiano)
        deltaX = np.dot(invJac, deltaPotencias)

        # Atualizando os angulos e tensoes
        c = 0
        for a, t in zip(angulos, tensoes):
            a += deltaX[c]
            t += deltaX[c+len(angulos)]
            c+=1

        # Calculando pcalc para a próxima iteração
        ativasKCalculada, reativasKCalculada = calcularFluxoKM(matrizY, angulos, tensoes)

        #Calculando deltaP e deltaQ
        deltaPks = np.zeros((nbarras,1))
        deltaQks = np.zeros((nbarras,1))
        for esp, calc, dp in zip(ativaEsp, ativasKCalculada, deltaPks):
            dp[0] = esp - calc
        for esp, calc, dq in zip(reativaEsp, reativasKCalculada, deltaQks):
            dq[0] = esp - calc


        # Resetando as potencias nas barras SW e PV
        for barra, dp, dq in zip(dbarras, deltaPks, deltaQks):
            if barra['TIPO'] != 'PQ':
                dq[0] = 0
            if barra['TIPO'] == 'SW':
                dp[0] = 0

        # Calculando a maior diferenca
        dPk = np.max(np.abs(deltaPks))
        dQk = np.max(np.abs(deltaQks))

        # Montando um vetor com as variações de potência
        deltaPotencias = np.concatenate((deltaPks, deltaQks), axis=0)

        # Imprimindo progresso
        print(f'{iter} / {maxIter} || {(iter/maxIter)*100:.2f}% || diff P = {dPk - tol:.6f} ; diff Q = {dQk - tol:.6f} ; ')

        iter += 1

    if iter >= maxIter: print("Nao convergiu")

    angulos = [a[0] for a in angulos]
    tensoes = [t[0] for t in tensoes]

    return angulos, tensoes

# Calculando os fluxos nos circuitos do sistema
def calcularFluxoBarras(angulos, tensoes, dcircuitos):

    ncirc = len(dcircuitos)
    fluxoPkm = np.zeros((ncirc,1))
    fluxoPmk = np.zeros((ncirc,1))
    fluxoQkm = np.zeros((ncirc,1))
    fluxoQmk = np.zeros((ncirc,1))
    fluxoSkm = np.zeros((ncirc,1))
    fluxoSmk = np.zeros((ncirc,1))

    for c, pkm, pmk, qkm, qmk in zip(dcircuitos, fluxoPkm, fluxoPmk, fluxoQkm, fluxoQmk):
        if c['LIG(L)DESL(D)'] != 'L' : continue
        k = c['BDE'] - 1
        m = c['BPARA'] - 1
        resistencia = c['RES(PU)']
        reatancia = c['REAT(PU)']
        admitancia = 1/(resistencia + (1j*reatancia))
        gkm = admitancia.real
        bkm = admitancia.imag
        bshunt = 1j*c['SUCsh(PU)']/2
        bshunt = bshunt.imag
        tap = c['TAP(PU)']
        defasagem = c['DEF(GRAUS)']*np.pi/180
        vk = tensoes[k]
        vm = tensoes[m]
        vkm = tensoes[k]*tensoes[m]
        thetakm = angulos[k] - angulos[m]
        thetamk = angulos[m] - angulos[k]
        cosThetakmPos = np.cos(thetakm + defasagem)
        cosThetakmNeg = np.cos(thetakm - defasagem)
        sinThetakmPos = np.sin(thetakm + defasagem)
        sinThetakmNeg = np.sin(thetakm - defasagem)

        pkm[0] = (((tap*vk)**2)*gkm) - (tap*vkm*gkm*np.cos(thetakm+defasagem)) - (tap*vkm*bkm*np.sin(thetakm+defasagem)) 
        pmk[0] = ((vm**2)*gkm) - (tap*vkm*gkm*np.cos(thetamk-defasagem)) - (tap*vkm*bkm*np.sin(thetamk-defasagem)) 
        qkm[0] = (-1*((tap*vk)**2)*(bkm + bshunt)) + (tap*vkm*bkm*np.cos(thetakm+defasagem)) - (tap*vkm*gkm*np.sin(thetakm+defasagem)) 
        qmk[0] = (-1*(vm**2)*(bkm+ bshunt)) + (tap*vkm*bkm*np.cos(thetamk-defasagem)) - (tap*vkm*gkm*np.sin(thetamk-defasagem)) 

    for pkm, qkm, skm in zip(fluxoPkm, fluxoQkm, fluxoSkm):
        skm[0] = np.sqrt( (pkm**2) + (qkm**2) )
    for pmk, qmk, smk in zip(fluxoPmk, fluxoQmk, fluxoSmk):
        smk[0] = np.sqrt( (pmk**2) + (qmk**2) )

    return fluxoPkm, fluxoPmk, fluxoQkm, fluxoQmk, fluxoSkm, fluxoSmk

# Calculando as perdas no sistema
def calcularPerdas(fluxoPkm, fluxoPmk, fluxoQkm, fluxoQmk):
    nbarras = len(fluxoPkm)
    perdasP = np.zeros((nbarras,1))
    perdasQ = np.zeros((nbarras,1))
    perdasAtivasTotais = 0
    perdasReativasTotais = 0

    for pkm, pmk, perP in zip(fluxoPkm, fluxoPmk, perdasP):
        perP[0] = pkm + pmk
        perdasAtivasTotais += perP[0]
    for qkm, qmk, qerQ in zip(fluxoQkm, fluxoQmk, perdasQ):
        qerQ[0] = qkm + qmk
        perdasReativasTotais += qerQ[0]

    return perdasP, perdasQ, perdasAtivasTotais, perdasReativasTotais

# Calculando as perdas no sistema
def potencias(matrizY, angulos, tensoes, dbarras):
    nbarras = len(angulos)
    pG = np.zeros((nbarras,1))
    qG = np.zeros((nbarras,1))
    sG = np.zeros((nbarras,1))
    pCalc = np.zeros((nbarras,1))
    qCalc = np.zeros((nbarras,1))

    # Calculando pcalc para a próxima iteração
    pCalc, qCalc = calcularFluxoKM(matrizY, angulos, tensoes)

    for barra, pg, pc in zip(dbarras, pG, pCalc):
        pg[0] = barra['PD(PU)'] + pc
    for barra, qg, qc in zip(dbarras, qG, qCalc):
        qg[0] = barra['QD(PU)'] + qc
    for pg, qg, sg in zip(pG, qG, sG):
        sg[0] = np.abs(pg[0] + (1j*qg[0]))

    return pG, qG, sG










