# 25/03/24 - Lucas Xavier de Morais e Cássia
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
import sep , leitura 
import configparser
from icecream import ic

config = configparser.ConfigParser()
config.read('config.ini')
arquivo = config['DEFAULT']['DataFileName']
print(arquivo)

dbarras, dcircuitos = leitura.lerDados(arquivo)

matrizY = sep.matrizAdmitancia(dbarras, dcircuitos)
# ic(matrizY.real)
# ic(matrizY.imag)

angulos, tensoes = sep.calcularAngulosTensoes(matrizY, dbarras)
angDeg = [(a*180/np.pi) for a in angulos]
ic(angDeg, tensoes)

fluxoPkm, fluxoPmk, fluxoQkm, fluxoQmk = sep.calcularFluxoBarras(angulos, tensoes, dcircuitos)



