# 25/03/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
import copy
from modules import *
import configparser

def main() -> None:
    exercicio1e2()
    exercicio3e4()

def exercicio1e2() -> None:
    config = configparser.ConfigParser()
    config.read('config.ini')

    print('Iniciando Leitura de dados')
    arquivo = config['FILE']['DATA_FILE_NAME_1_E_2']
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
    objetivo = float(config['ALTERNADOS']['OBJETIVO_TENSAO_12'])
    barra = int(config['ALTERNADOS']['BARRA_TENSAO_12']) - 1
    alpha = float(config['ALTERNADOS']['ALPHA_12'])
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

    outputInicial = config['FILE']['OUTPUT_FILE_1_E_2']
    output1 = config['ALTERNADOS']['OUTPUT_FILE_1']
    output2 = config['ALTERNADOS']['OUTPUT_FILE_2']
    output2banco = config['ALTERNADOS']['OUTPUT_FILE_2_BANCO']
    print(f'Montando os arquivos')

    exportacao.exportarSistema(outputInicial, sistemaInicial)
    exportacao.exportarSistema(output1, sistema1)
    exportacao.exportarSistema(output2, sistema2)
    exportacao.exportarSistema(output2banco, sistema2banco)

    return None

def exercicio3e4() -> None:
    config = configparser.ConfigParser()
    config.read('config.ini')

    print('Iniciando Leitura de dados')
    arquivo = config['FILE']['DATA_FILE_NAME_3_E_4']
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
    sistema3 = copy.deepcopy(sistemaInicial)

    maxIter = int(config['ALTERNADOS']['MAX_ITER'])
    tolerancia = float(config['ALTERNADOS']['TOLERANCIA'])
    objetivo = float(config['ALTERNADOS']['OBJETIVO_TENSAO_34'])
    barra = int(config['ALTERNADOS']['BARRA_TENSAO_34']) - 1
    alpha = float(config['ALTERNADOS']['ALPHA_34'])
    i = 1
    tapInicial = sistema3.dcircuitos[1]['TAP(PU)']
    print(f'Tap Inicial: {tapInicial:.6f}')
    while i <= maxIter:
        erro = objetivo - sistema3.tensoes[barra]  

        if np.abs(erro) <= tolerancia: print(f'Convergiu em {i-1} iteracoes'); break

        correcao = alpha * erro
        print(f'Correcao no tap: {correcao:.6f}')

        sistema3.dcircuitos[1]['TAP(PU)'] += correcao
    
        sistema3.calcularMatrizes()
        sistema3.resolverFluxo(True)

        print(f'{i} / {maxIter} || {(i/maxIter)*100:.2f}%')

        i +=1

    tapFinal = sistema3.dcircuitos[1]['TAP(PU)']
    print(f'Tap Inicial: {tapInicial:.6f}, Tap Final: {tapFinal:.6f}, para uma diferença de {tapFinal - tapInicial:.6f}')
    print('Recalculando as potências e fluxos de potência:')
    # Aqui as potências, fluxos e etc, são calculads dentro da classe para limpar o código e já gaurdar essas informações
    sistema3.calcularPotencias()

    sistema4 = copy.deepcopy(sistemaInicial)

    maxIter = int(config['ALTERNADOS']['MAX_ITER'])
    tolerancia = float(config['ALTERNADOS']['TOLERANCIA'])
    objetivo = float(config['ALTERNADOS']['OBJETIVO_POTENCIA_34'])
    circuito = int(config['ALTERNADOS']['CIRCUITO_POTENCIA']) - 1
    alpha = float(config['ALTERNADOS']['ALPHA_POT'])
    i = 1
    defInicial = sistema4.dcircuitos[1]['DEF(GRAUS)']
    print(f'Defasagem Inicial: {defInicial:.6f}')
    while i <= maxIter:
        erro = objetivo - sistema4.fluxoPkm[circuito][0]

        if np.abs(erro) <= tolerancia: print(f'Convergiu em {i-1} iteracoes'); break

        correcao = alpha * erro
        print(f'Correcao na defasagem: {correcao:.6f}')

        sistema4.dcircuitos[1]['DEF(GRAUS)'] += correcao
    
        sistema4.calcularMatrizes()
        sistema4.resolverFluxo(True)
        sistema4.calcularPotencias()

        print(f'{i} / {maxIter} || {(i/maxIter)*100:.2f}%')

        i +=1

    defFinal = sistema4.dcircuitos[1]['DEF(GRAUS)']
    print(f'Defasagem Inicial: {defInicial:.6f}, Defasagem Final: {defFinal:.6f}, para uma diferença de {defFinal - defInicial:.6f}')
    print('Recalculando as potências e fluxos de potência:')

    outputInicial = config['FILE']['OUTPUT_FILE_3_E_4']
    output3 = config['ALTERNADOS']['OUTPUT_FILE_3']
    output4 = config['ALTERNADOS']['OUTPUT_FILE_4']
    print(f'Montando os arquivos')

    exportacao.exportarSistema(outputInicial, sistemaInicial)
    exportacao.exportarSistema(output3, sistema3)
    exportacao.exportarSistema(output4, sistema4)

    return None

if __name__ == '__main__':
    main()



