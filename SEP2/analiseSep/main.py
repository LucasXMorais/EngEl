# 25/03/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
import sep , leitura, exportacao
import configparser
from icecream import ic

def main() -> None:
    config = configparser.ConfigParser()
    config.read('config.ini')

    print('Iniciando Leitura de dados')
    arquivo = config['FILE']['DATA_FILE_NAME']
    dbarras, dcircuitos = leitura.lerDados(arquivo)

    print('Montando a matrizY')
    matrizY = sep.matrizAdmitancia(dbarras, dcircuitos)

    print('Calculando as variáveis')
    angulos, tensoes = sep.calcularAngulosTensoes(matrizY, dbarras)
    angDeg = [(a*180/np.pi) for a in angulos]

    print('Calculando as potências e fluxos de potência:')
    fluxoPkm, fluxoPmk, fluxoQkm, fluxoQmk, fluxoSkm, fluxoSmk = sep.calcularFluxoBarras(angulos, tensoes, dcircuitos)
    perdasP, perdasQ, perdasAtivasTotais, perdasReativasTotais = sep.calcularPerdas(fluxoPkm, fluxoPmk, fluxoQkm, fluxoQmk)
    pG, qG, sG = sep.potencias(matrizY, angulos, tensoes, dbarras)
    nbarras = len(dbarras)
    pCalc = np.zeros((nbarras,1))
    qCalc = np.zeros((nbarras,1))
    pCalc, qCalc = sep.calcularFluxoKM(matrizY, angulos, tensoes)

    output = config['FILE']['OUTPUT_FILE']
    print(f'Montando o arquivo {output}')
    sistema = {
        'BARRAS' : dbarras,
        'CIRCUITOS' : dcircuitos,
        'PG' : pG,
        'QG' : qG,
        'SG' : sG,
        'perdasP' : perdasP,
        'perdasQ' : perdasQ,
        'PerdasPTotais' : perdasAtivasTotais,
        'PerdasQTotais' : perdasReativasTotais,
        'angulos' : angulos,
        'tensoes' : tensoes,
        'BASE' : float(config['PU']['BASE']),
        'pCalc' : pCalc,
        'qCalc' : qCalc,
        'fluxoPkm' : fluxoPkm,
        'fluxoPmk' : fluxoPmk,
        'fluxoQkm' : fluxoQkm,
        'fluxoQmk' : fluxoQmk,
        'fluxoSkm' : fluxoSkm,
        'fluxoSmk' : fluxoSmk
    }

    exportacao.exportarSistema(output, sistema)

    return None

if __name__ == '__main__':
    main()



