# 24/07/24 - Lucas Xavier de Morais 
# Funções para o cálculo de fluxo pelo método Newton
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
import configparser

# Montando a matriz Jacobiana
def jacobian(sis) -> np.ndarray :

    nbarras = len(sis.angulos)
    G = np.copy(sis.matrizY.real)
    B = np.copy(sis.matrizY.imag)
    angulos = np.copy(sis.angulos)
    tensoes = np.copy(sis.tensoes)
    dbarras = sis.dbarras

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
    # Fim jacobian

# Calculando os fluxos nos circuitos do sistema
def calcularFluxoBarras(sis):

    angulos = np.copy(sis.angulos)
    tensoes = np.copy(sis.tensoes)
    ncirc = len(sis.dcircuitos)
    fluxoPkm = np.zeros((ncirc,1))
    fluxoPmk = np.zeros((ncirc,1))
    fluxoQkm = np.zeros((ncirc,1))
    fluxoQmk = np.zeros((ncirc,1))
    fluxoSkm = np.zeros((ncirc,1))
    fluxoSmk = np.zeros((ncirc,1))
    dcircuitos = np.copy(sis.dcircuitos)

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

        pkm[0] = (((tap*vk)**2)*gkm) - (tap*vkm*gkm*np.cos(thetakm+defasagem)) - (tap*vkm*bkm*np.sin(thetakm+defasagem)) 
        pmk[0] = ((vm**2)*gkm) - (tap*vkm*gkm*np.cos(thetamk-defasagem)) - (tap*vkm*bkm*np.sin(thetamk-defasagem)) 
        qkm[0] = (-1*((tap*vk)**2)*(bkm + bshunt)) + (tap*vkm*bkm*np.cos(thetakm+defasagem)) - (tap*vkm*gkm*np.sin(thetakm+defasagem)) 
        qmk[0] = (-1*(vm**2)*(bkm+ bshunt)) + (tap*vkm*bkm*np.cos(thetamk-defasagem)) - (tap*vkm*gkm*np.sin(thetamk-defasagem)) 

    for pkm, qkm, skm in zip(fluxoPkm, fluxoQkm, fluxoSkm):
        skm[0] = np.sqrt( (pkm**2) + (qkm**2) )
    for pmk, qmk, smk in zip(fluxoPmk, fluxoQmk, fluxoSmk):
        smk[0] = np.sqrt( (pmk**2) + (qmk**2) )

    sis.fluxoPkm = fluxoPkm
    sis.fluxoPmk = fluxoPmk
    sis.fluxoQkm = fluxoQkm
    sis.fluxoQmk = fluxoQmk
    sis.fluxoSkm = fluxoSkm
    sis.fluxoSmk = fluxoSmk
    # Fim calcularFluxoBarras

# Calculando as perdas no sistema
def calcularPerdas(sis):
    fluxoPkm = np.copy(sis.fluxoPkm)
    fluxoPmk = np.copy(sis.fluxoPmk)
    fluxoQkm = np.copy(sis.fluxoQkm)
    fluxoQmk = np.copy(sis.fluxoQmk)
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

    sis.perdasP = perdasP
    sis.perdasQ = perdasQ
    sis.perdasAtivasTotais = perdasAtivasTotais
    sis.perdasReativasTotais = perdasReativasTotais
    # Fim calcularPerdas

# Calculando as perdas no sistema
def potencias(sis):

    nbarras = len(sis.angulos)
    pCalc = np.copy(sis.pCalc)
    qCalc = np.copy(sis.qCalc)
    pG = np.zeros((nbarras,1))
    qG = np.zeros((nbarras,1))
    sG = np.zeros((nbarras,1))
    dbarras = np.copy(sis.dbarras)

    for barra, pg, pc in zip(dbarras, pG, pCalc):
        pg[0] = barra['PD(PU)'] + pc
    for barra, qg, qc in zip(dbarras, qG, qCalc):
        qg[0] = barra['QD(PU)'] + qc
    for pg, qg, sg in zip(pG, qG, sG):
        sg[0] = np.abs(pg[0] + (1j*qg[0]))

    sis.pG = pG
    sis.qG = qG
    sis.sG = sG
    # Fim potencias

# Funcao para o calculo de potencias (Pcalc) a cada iteração
def calcularFluxoKM(sis):
    G = np.copy(sis.matrizY.real)
    B = np.copy(sis.matrizY.imag)
    ativasKCalculada = np.zeros(np.shape(sis.angulos))
    reativasKCalculada = np.zeros(np.shape(sis.angulos))
    lenTensoes = len(sis.tensoes)

    for k in range(lenTensoes):
        for m in range(lenTensoes):
            Gkm = G[k][m]
            Bkm = B[k][m]
            angulokm = sis.angulos[k] - sis.angulos[m]
            tensaokm = sis.tensoes[k] * sis.tensoes[m]
            cosThetakm = np.cos(angulokm)
            sinThetakm = np.sin(angulokm)

            ativasKCalculada[k] += tensaokm * ( (Gkm * cosThetakm) + (Bkm * sinThetakm) )
            reativasKCalculada[k] += tensaokm * ( (Gkm * sinThetakm) - (Bkm * cosThetakm) )

    sis.pCalc = ativasKCalculada
    sis.qCalc = reativasKCalculada
    # Fim calcularFluxoKM

# Calculando os angulos e tensoes do problema de fluxo
def calcularFluxoNewton(sis, silent: bool=False):

    # Obtendo parâmetros 
    config = configparser.ConfigParser()
    config.read('config.ini')

    #Construcao dos vetores de sistema.angulos e tensoes do sistema
    nbarras = len(sis.dbarras)
    sis.angulos = np.zeros((nbarras,1))
    sis.tensoes = np.ones((nbarras,1))
    for barra, v in zip(sis.dbarras, sis.tensoes):
        if (barra['TIPO'] == 'PV' or barra['TIPO'] == 'SW') : v[0] = barra['Vesp(PU)']

    # Calcular as potencias esperadas e agrupá-las em dois vetores, um para
    # potencias ativas e outro para potencias reativas
    ativaEsp = np.zeros((nbarras,1))
    reativaEsp = np.zeros((nbarras,1))
    for barra in sis.dbarras:
        k = barra['BARRA'] - 1
        ativaEsp[k] = barra['PGesp(PU)'] - barra['PD(PU)']
        reativaEsp[k] = - barra['QD(PU)']

    # Definindo parâmetros iniciais do método de newton
    maxIter = int(config['NEWTON']['MAX_ITER'])
    tol = float(config['NEWTON']['TOLERANCIA'])
    iter = 1
    fimP = 0
    fimQ = 0

    # Calculando pcalc para valores iniciais
    calcularFluxoKM(sis)
    ativasKCalculada = np.copy(sis.pCalc)
    reativasKCalculada = np.copy(sis.qCalc)

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
        if fimP and fimQ:
            if not silent: print(f'Convergiu em {iter-1} iterações')
            break

        # Matriz Jacobiana
        jacobiano = jacobian(sis)

        # Fazendo dx = -J^(-1) * g
        try:
            invJac = np.linalg.inv(jacobiano)
        except:
            # print('nao inverteu')
            invJac = np.linalg.pinv(jacobiano)
        deltaX = np.dot(invJac, deltaPotencias)

        # Atualizando os angulos e tensoes
        c = 0
        for a, t in zip(sis.angulos, sis.tensoes):
            a += deltaX[c]
            t += deltaX[c+len(sis.angulos)]
            c+=1

        # Calculando pcalc para a próxima iteração
        calcularFluxoKM(sis)
        ativasKCalculada = np.copy(sis.pCalc)
        reativasKCalculada = np.copy(sis.qCalc)

        #Calculando deltaP e deltaQ
        deltaPks = np.zeros((nbarras,1))
        deltaQks = np.zeros((nbarras,1))
        for esp, calc, dp in zip(ativaEsp, ativasKCalculada, deltaPks):
            dp[0] = esp - calc
        for esp, calc, dq in zip(reativaEsp, reativasKCalculada, deltaQks):
            dq[0] = esp - calc


        # Resetando as potencias nas barras SW e PV
        for barra, dp, dq in zip(sis.dbarras, deltaPks, deltaQks):
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
        if not silent : print(f'{iter} / {maxIter} || {(iter/maxIter)*100:.2f}% || diff P = {dPk - tol:.6f} ; diff Q = {dQk - tol:.6f} ; ')

        iter += 1
    # Fim While

    sis.convergiu = True
    if iter >= maxIter: 
        if not silent: print("Nao convergiu")
        sis.convergiu = False


    sis.angulos = [a[0] for a in sis.angulos]
    sis.angulosGrau = [(a*180/np.pi) for a in sis.angulos]
    sis.tensoes = [t[0] for t in sis.tensoes]
    # Fim calcular fluxo por newthon








