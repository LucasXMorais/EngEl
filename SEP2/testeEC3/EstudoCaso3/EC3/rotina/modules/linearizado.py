# 04/08/24 - Lucas Xavier de Morais 
# FLuxo de potência linearizado com perdasd
# SEP II - Engenharia Elétrica (UFSJ)
import os
import configparser
import numpy as np
from modules import *

def fluxoLinear(sis):
    config = configparser.ConfigParser()
    config.read('config.ini')

    def calcularPerdas():

        perdas = np.zeros((sis.ncircuitos,1))
        for circ in sis.dcircuitos:
            k = int(circ["BDE"]) - 1
            m = int(circ["BPARA"]) - 1
            nCir = int(circ["NCIR"]) - 1
            Gkm = sis.matGkmLinear[k][m]
            angulokm = angs[k] - angs[m]
            perdas[nCir] += ( Gkm * (angulokm**2) ) / 2

        perdaBarra = np.zeros((sis.nbarras-1,1))

        c = 0
        for barra  in sis.dbarras:
            if barra["TIPO"] == "SW": continue

            for circ, p in zip(sis.dcircuitos, perdas):
                k = int(circ["BDE"]) - 1
                m = int(circ["BPARA"]) - 1
                if int(barra['BARRA'])-1 not in [k,m]: continue
                perdaBarra[c] += p[0]
            c+=1
        return perdaBarra
        
    # Calculando as perdas no sistema
    def potencias():
        PLinear = np.zeros((sis.nbarras-1,1))
        perdaBarra = calcularPerdas()

        c = 0
        for barra  in sis.dbarras:
            if barra["TIPO"] == "SW": continue
            PLinear[c] = barra['PGesp(PU)'] - barra['PD(PU)'] + perdaBarra[c]
            c+=1

        return PLinear
        # Fim potencias

    def matrizes():
        BLinear = np.zeros((sis.nbarras-1,sis.nbarras-1))
        GLinear = np.zeros((sis.nbarras-1,sis.nbarras-1))
        barraSW = 0
        for bar in sis.dbarras:
            if bar["TIPO"] == 'SW': 
                barraSW = bar["BARRA"]
                break
        barraSW = int(barraSW)-1

        x = 0
        for i in range(sis.nbarras):
            y = 0
            for j in range(sis.nbarras):
                if j == barraSW: continue
                bkm = sis.matBkmLinear[i][j]
                BLinear[x][y] = bkm
                gkm = sis.matGkmLinear[i][j]
                GLinear[x][y] = gkm
                y+=1
            if i == barraSW : continue
            x+=1

        # print(BLinear, GLinear)
        return BLinear, GLinear

    angLinear = np.zeros((sis.nbarras-1,1))
    angs = np.zeros((sis.nbarras,1))
    angsAntigo = np.zeros((sis.nbarras-1,1))
    sis.angulos = np.zeros((sis.nbarras,1))
    perdas = np.zeros((sis.ncircuitos,1))
    perdaBarra = np.zeros((sis.nbarras-1,1))

    # Definindo parâmetros iniciais do método de newton
    maxIter = int(config['LINEARIZADO']['MAX_ITER'])
    tol = float(config['LINEARIZADO']['TOLERANCIA'])
    i = 1
    fim = 0

    BLinear, GLinear = matrizes()
    try:
        sis.convergiu = True
        BLinear = np.linalg.inv(BLinear)
    except:
        sis.convergiu = False
        BLinear = np.linalg.pinv(BLinear)
    dPk = 1000000

    while i <= maxIter:

        if dPk < tol: 
            sis.iteracoes = i
            # print('fim calc')
            break

        PLinear = potencias()
        angLinear = np.dot(-BLinear,PLinear)
        c = 0
        angs = []
        for b in sis.dbarras:
            if b["TIPO"] == 'SW':
                angs.append(0)
            else:
                angs.append(angLinear[c][0])
                c+=1 


        deltaAngulos = angLinear - angsAntigo
        dPk = np.max(np.abs(deltaAngulos))

        angsAntigo = np.copy(angLinear)

        # print(i, dPk)

        i+=1
    # Fim while

    k = 0
    for a in angs:
        sis.angulos[k] = a
        k+=1
    
    sis.angulos = [a for a in sis.angulos]
    sis.angulosGrau = [(a[0]*180/np.pi) for a in sis.angulos]

    sis.fluxoPkm = np.zeros((sis.ncircuitos,1))
    sis.fluxoPmk = np.zeros((sis.ncircuitos,1))
    for circ in sis.dcircuitos:
        k = int(circ["BDE"]) - 1
        m = int(circ["BPARA"]) - 1
        nCir = int(circ["NCIR"]) - 1
        Bkm = sis.matBkmLinear[k][m]
        angulokm = angs[k] - angs[m]
        angulomk = angs[m] - angs[k]
        sis.fluxoPkm[nCir] += angulokm * Bkm
        sis.fluxoPmk[nCir] += angulomk * Bkm
        
    # Fim calcular fluxo por linearizado












    

    


