# 25/03/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
import copy
from modules import *
import configparser

def main() -> None:
    config = configparser.ConfigParser()
    config.read('config.ini')

    print('Iniciando Leitura de dados')
    arquivo = config['FILE']['DATA_FILE_NAME']
    dbarras, dcircuitos = leitura.lerDados(arquivo)
    base = float(config['PU']['BASE'])
    # Armazenando os dados do sistema na classe Sistema
    sistemaInicial = Sistema(dbarras, dcircuitos, arquivo, base)

    print('Calculando as variáveis')
    sistemaInicial.resolverFluxo()

    print('Calculando as potências e fluxos de potência:')
    # Aqui as potências, fluxos e etc, são calculads dentro da classe para limpar o código e já gaurdar essas informações
    sistemaInicial.calcularPotencias()

    # Copiando o sistema original para preservar os valores 
    sistema1 = copy.deepcopy(sistemaInicial)

    maxIter = int(config['ALTERNADOS']['MAX_ITER'])
    toleranciaDe1 = float(config['ALTERNADOS']['TOLERANCIA'])
    objetivo = float(config['ALTERNADOS']['OBJETIVO_TENSAO'])
    barra = int(config['ALTERNADOS']['BARRA_TENSAO']) - 1
    alpha = float(config['ALTERNADOS']['ALPHA'])
    i = 1
    while i <= maxIter:
        erro = objetivo - sistema1.tensoes[barra]  

        if np.abs(erro) <= toleranciaDe1: print(f'Convergiu em {i-1} iteracoes'); break

        correcao = alpha * erro
        correcao = correcao / 2
        print(f'Correcao por barra: {correcao:.6f}')

        sistema1.dbarras[0]['Vesp(PU)'] += correcao
        sistema1.dbarras[1]['Vesp(PU)'] += correcao
    
        sistema1.calcularMatrizes()
        sistema1.resolverFluxo(True)

        print(f'{i} / {maxIter} || {(i/maxIter)*100:.2f}%')

        i +=1

    print('Recalculando as potências e fluxos de potência:')
    # Aqui as potências, fluxos e etc, são calculads dentro da classe para limpar o código e já gaurdar essas informações
    sistema1.calcularPotencias()

    # Copiando o sistema 1
    arquivo2 = config['ALTERNADOS']['DATA_FILE_NAME']
    sistema2 = copy.deepcopy(sistema1)
    sistema2.dbarras[1]['PD(PU)'] *= 1.2
    sistema2.dbarras[1]['QD(PU)'] *= 1.2
    sistema2.dbarras[2]['PD(PU)'] *= 1.2
    sistema2.dbarras[2]['QD(PU)'] *= 1.2

    # Calculando as novas potências
    sistema2.resolverFluxo(True)
    sistema2.calcularPotencias()

    # Inserindo banco no sistema 2 e calculando o fluxo
    sistema2banco = copy.deepcopy(sistema2)
    sistema2banco.dbarras[1]['Bsh(PU)'] = 0.14
    sistema2banco.calcularMatrizes()
    sistema2banco.resolverFluxo(True)
    sistema2banco.calcularPotencias()

    outputInicial = config['FILE']['OUTPUT_FILE']
    output1 = config['ALTERNADOS']['OUTPUT_FILE_1']
    output2 = config['ALTERNADOS']['OUTPUT_FILE_2']
    output2banco = config['ALTERNADOS']['OUTPUT_FILE_2_BANCO']
    print(f'Montando os arquivos')

    exportacao.exportarSistema(outputInicial, sistemaInicial)
    exportacao.exportarSistema(output1, sistema1)
    exportacao.exportarSistema(output2, sistema2)
    exportacao.exportarSistema(output2banco, sistema2banco)

    return None

if __name__ == '__main__':
    main()



