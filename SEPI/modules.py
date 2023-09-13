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




