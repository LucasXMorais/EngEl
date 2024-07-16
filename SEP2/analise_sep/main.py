# 24/06/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
import configparser
import numpy as np
import copy
from modules import *
import matplotlib.pyplot as plt


def estudoCaso2():
    config = configparser.ConfigParser()
    config.read('config.ini')

    print('Iniciando Leitura de dados')
    arquivo = config['FILE']['DATA_FILE']
    dbarras, dcircuitos = leitura.lerDados(arquivo)
    base = float(config['PU']['BASE'])
    # Armazenando os dados do sistema na classe Sistema
    sistemaInicial = Sistema(dbarras, dcircuitos, arquivo, base)

    print('Calculando as variáveis')
    sistemaInicial.resolverFluxo()

    print('Calculando as potências e fluxos de potência:')
    # Aqui as potências, fluxos e etc, são calculads dentro da classe 
    sistemaInicial.calcularPotencias()

    # Saidas
    outputInicial = config['FILE']['OUTPUT_FILE']
    print('Montando os arquivos')
    exportacao.exportarSistema(outputInicial, sistemaInicial)

    # Exportando tabelas para Latex
    correcoes1 = []
    latex.exportarLatex('latexFileInicial.txt', sistemaInicial, correcoes1)

def estudo2Teste():
    config = configparser.ConfigParser()
    config.read('config.ini')

    print('Iniciando Leitura de dados')
    arquivo = config['FILE']['DATA_FILE']
    dbarras, dcircuitos = leitura.lerDados(arquivo)
    base = float(config['PU']['BASE'])
    # Armazenando os dados do sistema na classe Sistema
    sistemaInicial = Sistema(dbarras, dcircuitos, arquivo, base)

    print('Calculando as variáveis')
    sistemaInicial.resolverFluxo()

    print('Calculando as potências e fluxos de potência:')
    # Aqui as potências, fluxos e etc, são calculads dentro da classe 
    sistemaInicial.calcularPotencias()

    # ---- CONTROLE POR TENSAO ----
    # Copiando o sistema original para preservar os valores 
    sistema1 = copy.deepcopy(sistemaInicial)

    # Aplicando Ajustes alternados com controle por tensão 
    parametrosTensao = {
            "MAX_ITER_TENSAO" : 100,
            "TOLERANCIA_TENSAO" : 0.001,
            "ALPHA_TENSAO" : 0.7,
            "OBJETIVO_TENSAO" : 1.0,
            "BARRA_OBJETIVO_TENSAO" : 3,
            "BARRAS_CONTROLE_TENSAO" : '1,2',
            }
    correcoes1 = []
    sistema1, correcoes1 = alternados.controleTensao(sistema1, parametrosTensao)
    # correcoes1 = []
    # sistema1, correcoes1 = alternados.controleTensao(sistema1)

    print('Recalculando as potências e fluxos de potência:')
    # Cálculo das potências, fluxos e etc
    sistema1.calcularPotencias()
    
    # ---- CONTROLE POR TAP ----
    # Copiando o sistema original para preservar os valores 
    sistema3 = copy.deepcopy(sistemaInicial)

    # Aplicando Ajustes alternados com controle por tap 
    parametrosTap = {
            "MAX_ITER_TAP" : 100,
            "TOLERANCIA_TAP" : 0.001,
            "ALPHA_TAP" : 1.5,
            "OBJETIVO_TAP" : 1.01,
            "BARRA_OBJETIVO_TAP" : 2,
            "CIRCUITOS_CONTROLE_TAP" : '2',
            }
    correcoes3 = []
    sistema3, correcoes3 = alternados.controleTap(sistema3, parametrosTap)
    # correcoes3 = []
    # sistema3, correcoes3 = alternados.controleTap(sistema3)

    print('Recalculando as potências e fluxos de potência:')
    # Aqui as potências, fluxos e etc
    sistema3.calcularPotencias()

    # ---- CONTROLE POR DEFASAGEM ----
    # Copiando o sistema original para preservar os valores 
    sistema4 = copy.deepcopy(sistemaInicial)

    # Aplicando Ajustes alternados com controle por tap 
    parametrosDefasagem = {
            "MAX_ITER_DEFASAGEM" : 100,
            "TOLERANCIA_DEFASAGEM" : 0.001,
            "ALPHA_DEFASAGEM" : 1.5,
            "OBJETIVO_DEFASAGEM" : 1.01,
            "BARRA_OBJETIVO_DEFASAGEM" : 4,
            "CIRCUITOS_CONTROLE_DEFASAGEM" : '4',
            }
    correcoes4 = []
    sistema4, correcoes4 = alternados.controleDefasagem(sistema4, parametrosDefasagem)
    # correcoes4 = []
    # sistema4, correcoes4 = alternados.controleDefasagem(sistema4)

    print('Recalculando as potências e fluxos de potência:')
    # Aqui as potências, fluxos e etc
    sistema4.calcularPotencias()

    # Saidas
    outputInicial = config['FILE']['OUTPUT_FILE_1_E_2']
    output1 = config['ALTERNADOS']['OUTPUT_FILE_1']
    output2 = config['ALTERNADOS']['OUTPUT_FILE_2']
    output2banco = config['ALTERNADOS']['OUTPUT_FILE_2_BANCO']
    print('Montando os arquivos')
    exportacao.exportarSistema(outputInicial, sistemaInicial)
    exportacao.exportarSistema(output1, sistema1)
    exportacao.exportarSistema(output2, sistema2)
    exportacao.exportarSistema(output2banco, sistema2banco)

    # Exportando tabelas para Latex
    latex.exportarLatex('latexFileInicial1.txt', sistemaInicial, correcoes1)
    latex.exportarLatex('latexFile1.txt', sistema1, correcoes1)
    latex.exportarLatex('latexFile2.txt', sistema2, correcoes1)
    latex.exportarLatex('latexFile2banco.txt', sistema2banco, correcoes1)


def main() -> None:
    estudoCaso2()

if __name__ == '__main__':
    main()



