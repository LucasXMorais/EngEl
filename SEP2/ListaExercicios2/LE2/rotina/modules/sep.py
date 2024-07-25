# 25/03/24 - Lucas Xavier de Morais 
# Funções base para SEP
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
import configparser

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


# Construção da matriz admitancia Y completa
def matrizAdmitancia(sis) -> np.ndarray:
    dbarras = sis.dbarras
    dcircuitos = sis.dcircuitos
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
    # Fim matrizAdmitancia

def matrizLinearizados(sis) -> np.ndarray:
    dbarras = sis.dbarras
    dcircuitos = sis.dcircuitos
    nbar = len(dbarras)
    matYLinearizado = np.zeros((nbar,nbar),dtype=np.complex_)

    for c in dcircuitos:
        if c['LIG(L)DESL(D)'] != 'L' : continue
        k = c['BDE'] - 1
        m = c['BPARA'] - 1
        resistencia = c['RES(PU)']
        reatancia = c['REAT(PU)']
        # moduloAdmitancia = np.sqrt(resistencia**2 + reatancia**2)
        condutancia = 1/(resistencia + (1j*reatancia))
        admitancia = 1/(1j*reatancia)
        aux = condutancia.real + admitancia
        # susceptancia = 1j*c['SUCsh(PU)']/2
        if k == m :
            matYLinearizado[k][k] = matYLinearizado[k][k] + aux
            continue
        matYLinearizado[k][k] = matYLinearizado[k][k] + aux 
        matYLinearizado[k][m] = matYLinearizado[k][m] - aux
        matYLinearizado[m][k] = matYLinearizado[m][k] - aux
        matYLinearizado[m][m] = matYLinearizado[m][m] + aux 

    return matYLinearizado
# Fim matrizLinearizados

