# 13/07/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
import configparser
import numpy as np
import os
from modules import *
from modules import limites

def carregarSistema() -> sistema.Sistema:
    config = configparser.ConfigParser()
    config.read('config.ini')

    files = [f for f in os.listdir() if f.split('.')[-1] == 'txt']
    files = [f for f in os.listdir() if f.split('_')[0] == 'dados']
    arquivo = config['FILE']['DATA_FILE']
    arquivo = arquivo.split(',')
    while True:
        index = 0
        for f in files:
            index += 1
            print(f'{index} - {f}')
        importar = input('Selecionar arquivo base = ')
        if importar.isnumeric():
            importar = int(importar) - 1
            if importar <= len(files): 
                arquivoDados = files[importar] 
            else:
                arquivoDados = arquivo[0] 
            break
    print(f'Iniciando Leitura de dados padrao: {arquivo}')
    dbarras, dcircuitos = leitura.lerDados(arquivoDados)
    base = float(config['PU']['BASE'])
    # Armazenando os dados do sistema na classe Sistema
    sistema = Sistema(dbarras, dcircuitos, arquivo, base)

    # Calculando as variáveis - Com o argumento TRUE para rodar em modo silencioso
    sistema.resolverFluxo(True)

    # Saidas
    output = config['FILE']['OUTPUT_FILE']
    output = 'resultados/' + output
    print(f'Exportando as respostas do sistema para {output}')
    exportacao.exportarSistema(output, sistema)

    # Exportando tabelas para Latex
    correcoes1 = []
    tabelasLatex = config['FILE']['LATEX_FILE']
    tabelasLatex = 'resultados/' + tabelasLatex
    print(f'Exportando as respostas do sistema para {tabelasLatex}')
    latex.exportarLatex(tabelasLatex, sistema, correcoes1)

    return sistema
# Fim INICIAL

def menu(sis: sistema.Sistema):
    while True:
        resposta = input('B / C / F / Q - ')
        match resposta:
            case 'b' | 'B':
                while True:
                    bar = input('Barra: ')
                    if bar.isnumeric():
                        bar = int(bar)-1
                        if bar <= len(sis.dbarras):
                            exibir.dadosBarras(sis, bar)

                            dados = modificar.valorDicionario(sis.dbarras[bar])
                            if dados[0] == 'q': break
                            sis.dbarras[bar][dados[0]] = dados[1]

                            exibir.dadosBarras(sis, bar)

                            # Salvando alterações
                            sis.calcularMatrizes()
                            exportacao.exportarSistema('dados_sistema_modificado.txt', sis)

                            break
                    # FIm Barra
                    if bar == 'q' or bar == 'Q': break
                # Fim while
            case 'c' | 'C':
                while True:
                    circ = input('Circuito: ')
                    if circ.isnumeric():
                        circ = int(circ)-1
                        if circ <= len(sis.dcircuitos):
                            exibir.dadosCircuitos(sis, circ)

                            dados = modificar.valorDicionario(sis.dcircuitos[circ])
                            if dados[0] == 'q': break
                            sis.dcircuitos[circ][dados[0]] = dados[1]

                            exibir.dadosCircuitos(sis, circ)

                            # Salvando alterações
                            sis.calcularMatrizes()
                            exportacao.exportarSistema('dados_sistema_modificado.txt', sis)

                            break
                    # Fim Circuito
                    if circ == 'q' or circ == 'Q':break
                # Fim While
            case 'f' | 'F':
                sis.resolverFluxo()
            
                # Saidas
                output = 'resultadosModificados.txt'
                output = 'resultados/' + output
                print(f'Exportando as respostas do sis para {output}')
                exportacao.exportarSistema(output, sis)
            
                # Exportando tabelas para Latex
                correcoes1 = []
                tabelasLatex = 'latexmod.txt'
                tabelasLatex = 'resultados/' + tabelasLatex
                print(f'Exportando as respostas do sis para {tabelasLatex}')
                latex.exportarLatex(tabelasLatex, sis, correcoes1)

                exibir.resumoSistema(sis)
            case 'a' | 'A':
                print('1. Controle de tensão pelas barras PV')
                print('2. Controle de tensão pelo TAP')
                print('3. Controle de potência ativa pela defasagem')
                ajuste = input('Ajuste: ')
                match ajuste:
                    case '1':
                        default = False
                        while True:
                            valoresDefault = input('Usar parâmetros padrão: ')
                            match valoresDefault:
                                case 's' | 'S':
                                    default = True
                                    break
                                case _:
                                    pass
                        # FIm While
                        while True:
                            parametrosTensao = {
                                    "MAX_ITER_TENSAO" : 100,
                                    "TOLERANCIA_TENSAO" : 0.001,
                                    "ALPHA_TENSAO" : 0.7,
                                    "BARRA_OBJETIVO_TENSAO" : 1,
                                    "OBJETIVO_TENSAO" : 1.0,
                                    "BARRAS_CONTROLE_TENSAO" : '1,2',
                                    }
                            parametrosTensao = alternados.pegarParametros(parametrosTensao, default)
                            print(parametrosTensao)
                            print('Estes valores estão corretos?') 
                            while True:
                                resposta = input('S / N')
                                if resposta in ['s','S','q','Q','n','N']: break
                            if resposta in ['s','S','q','Q']: break
                        if resposta not in ['q','Q']: 
                            correcoes = []
                            sis, correcoes = alternados.controleTensao(sis, parametrosTensao)

                            # Salvando alterações
                            sis.calcularMatrizes()
                            exportacao.exportarSistema('dados_sistema_modificado.txt', sis)
                    case '2':
                        default = False
                        while True:
                            valoresDefault = input('Usar parâmetros padrão: ')
                            match valoresDefault:
                                case 's' | 'S':
                                    default = True
                                    break
                                case _:
                                    pass
                        # FIm While
                        while True:
                            parametrosTap = {
                                    "MAX_ITER_TAP" : 100,
                                    "TOLERANCIA_TAP" : 0.001,
                                    "ALPHA_TAP" : 1.5,
                                    "BARRA_OBJETIVO_TAP" : 2,
                                    "OBJETIVO_TAP" : 1.01,
                                    "CIRCUITOS_CONTROLE_TAP" : '2',
                                    }
                            parametrosTap = alternados.pegarParametros(parametrosTap, default)
                            print(parametrosTap)
                            print('Estes valores estão corretos?') 
                            while True:
                                resposta = input('S / N')
                                if resposta in ['s','S','q','Q','n','N']: break
                            if resposta in ['s','S','q','Q']: break
                        if resposta not in ['q','Q']: 
                            correcoes = []
                            sis, correcoes = alternados.controleTap(sis, parametrosTap)

                            # Salvando alterações
                            sis.calcularMatrizes()
                            exportacao.exportarSistema('dados_sistema_modificado.txt', sis)
                    case '3':
                        default = False
                        while True:
                            valoresDefault = input('Usar parâmetros padrão: ')
                            match valoresDefault:
                                case 's' | 'S':
                                    default = True
                                    break
                                case _:
                                    pass
                        # FIm While
                        while True:
                            parametrosDefasagem = {
                                    "MAX_ITER_DEFASAGEM" : 100,
                                    "TOLERANCIA_DEFASAGEM" : 0.001,
                                    "ALPHA_DEFASAGEM" : 1.5,
                                    "BARRA_OBJETIVO_DEFASAGEM" : 4,
                                    "OBJETIVO_DEFASAGEM" : 1.01,
                                    "CIRCUITOS_CONTROLE_DEFASAGEM" : '4',
                                    }
                            parametrosDefasagem = alternados.pegarParametros(parametrosDefasagem, default)
                            print(parametrosDefasagem)
                            print('Estes valores estão corretos?') 
                            while True:
                                resposta = input('S / N')
                                if resposta in ['s','S','q','Q','n','N']: break
                            if resposta in ['s','S','q','Q']: break
                        if resposta not in ['q','Q']: 
                            correcoes = []
                            sis, correcoes = alternados.controleTensao(sis, parametrosDefasagem)

                            # Salvando alterações
                            sis.calcularMatrizes()
                            exportacao.exportarSistema('dados_sistema_modificado.txt', sis)
                    case _:
                        break
            case 'q' | 'Q': print('Encerrando'); break
            case _:
                print('Entrada inválida')
    # FIM WHILE
# Fim menu

def iniciar():
    exibir.cabecalho()
    print('Iniciando programa de analise de SEPs')
    print('Comparar sistemas ou trabalhar em um SEP')
    while True:
        menu = input('(C)omparar / (S)EP - ')
        match menu:
            case 'c' | 'C':
                while True:
                    files = [f for f in os.listdir() if f.split('.')[-1] == 'txt']
                    files = [f for f in os.listdir() if f.split('_')[0] == 'dados']
                    arquivos = []
                    c = 0
                    while True:
                        index = 0
                        for f in files:
                            index += 1
                            print(f'{index} - {f}')
                        importar = input(f'Selecionar arquivo {c+1} = ')
                        if importar.isnumeric():
                            importar = int(importar) - 1
                            if importar <= len(files): 
                                arq = files[importar]
                                arquivos.append(files[importar])
                                c += 1
                        if c >= 2: break
                    print(f'Iniciando Leitura de dados: {arquivos}')
                    dadosSistemas = []
                    dbarras, dcircuitos = leitura.lerDados(arquivos[0])
                    dadosSistemas.append((dbarras, dcircuitos))
                    dbarras, dcircuitos = leitura.lerDados(arquivos[1])
                    dadosSistemas.append((dbarras, dcircuitos))

                    compara.sistemas(dadosSistemas)
                    break
            case 's' | 'S':
                break
            case _:
                pass
    # Fim while
# FIm funcao








