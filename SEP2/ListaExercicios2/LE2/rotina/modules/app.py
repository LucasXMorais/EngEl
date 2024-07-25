# 13/07/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
import os
import configparser
import numpy as np
from modules import *

def carregarSistema() -> sistema.Sistema:
    config = configparser.ConfigParser()
    config.read('config.ini')

    files = [f for f in os.listdir('dados/') if f.split('.')[-1] == 'txt']
    files = [f for f in files if f.split('_')[0] == 'dados']
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
                arquivo[0] = files[importar] 
            else:
                arquivo[0] = arquivo[0] 
            break
    arquivo = ['dados/' + a for a in arquivo]
    print(f'Iniciando Leitura de dados: {arquivo}')
    dbarras, dcircuitos = leitura.lerDados(arquivo[0])
    base = float(config['PU']['BASE'])
    # Armazenando os dados do sistema na classe Sistema
    sis = Sistema(dbarras, dcircuitos, arquivo, base)

    # Calculando as variáveis - Com o argumento TRUE para rodar em modo silencioso
    sis.resolverFluxo(True)

    # Saidas
    output = config['FILE']['OUTPUT_FILE']
    output = 'resultados/' + output
    print(f'Exportando as respostas do sis para {output}')
    exportacao.relatorio(output, sis)

    # Exportando tabelas para Latex
    correcoes1 = []
    tabelasLatex = config['FILE']['LATEX_FILE']
    tabelasLatex = 'resultados/' + tabelasLatex
    print(f'Exportando as respostas do sis para {tabelasLatex}')
    latex.exportarLatex(tabelasLatex, sis, correcoes1)

    return sis
# Fim INICIAL

def menu(sis: sistema.Sistema):
    config = configparser.ConfigParser()
    config.read('config.ini')
    logNumber = logs.getLogNumber()
    logs.createNewFile(logNumber)
    while True:
        resposta = input('B / C / F / A / Q / comp / G - ')
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
                            valorAntigo = sis.dbarras[bar][dados[0]]
                            sis.dbarras[bar][dados[0]] = dados[1]
                            message = f'Barra {bar+1} mudou {dados[0]} de {valorAntigo} para {dados[1]}'
                            logs.log(logNumber, message, 'ALT')

                            exibir.dadosBarras(sis, bar)

                            # Salvando alterações
                            sis.calcularMatrizes()
                            exportacao.exportarSistema('dados/dados_sistema_modificado.txt', sis)

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
                            valorAntigo = sis.dcircuitos[circ][dados[0]]
                            sis.dcircuitos[circ][dados[0]] = dados[1]
                            message = f'Circuito {circ+1} mudou {dados[0]} de {valorAntigo} para {dados[1]}'
                            logs.log(logNumber, message, 'ALT')

                            exibir.dadosCircuitos(sis, circ)

                            # Salvando alterações
                            sis.calcularMatrizes()
                            exportacao.exportarSistema('dados/dados_sistema_modificado.txt', sis)

                            break
                    # Fim Circuito
                    if circ == 'q' or circ == 'Q':break
                # Fim While
            case 'f' | 'F':
                sis.resolverFluxo()
            
                # Saidas
                output = config['FILE']['OUTPUT_FILE']
                output = 'resultados/' + output
                print(f'Exportando as respostas do sistema para {output}')
                exportacao.exportarSistema('dados/dados_sistema_modificado.txt', sis)
                exportacao.relatorio(output, sis)

                # Exportando tabelas para Latex
                correcoes = []
                tabelasLatex = config['FILE']['LATEX_FILE']
                tabelasLatex = 'resultados/' + tabelasLatex
                print(f'Exportando as respostas do sistema para {tabelasLatex}')
                latex.exportarLatex(tabelasLatex, sis, correcoes)

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
                            barrasControle = parametrosTensao["BARRAS_CONTROLE_TENSAO"]
                            barrasControle = barrasControle.split(',')
                            barrasControle = [ int(b)-1 for b in barrasControle ]
                            valoresAntigos = []
                            for b in barrasControle:
                                valoresAntigos.append(sis.dbarras[b]['Vesp(PU)'])
                            sis, correcoes = alternados.controleTensao(sis, parametrosTensao)
                            for b, va in zip(barrasControle, valoresAntigos):
                                message = f'Barra {b} mudou tensão PV de {va} para {sis.dbarras[b]["Vesp(PU)"]}'
                                logs.log(logNumber, message, 'ALT')

                            # Salvando alterações
                            sis.calcularMatrizes()
                            exportacao.exportarSistema('dados/dados_sistema_modificado.txt', sis)
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
                            circuitosControle = parametrosTap["CIRCUITOS_CONTROLE_TAP"]
                            circuitosControle = circuitosControle.split(',')
                            circuitosControle = [ int(b)-1 for b in circuitosControle ]
                            valoresAntigos = []
                            for b in circuitosControle:
                                valoresAntigos.append(sis.dcircuitos[b]['TAP(PU)'])
                            sis, correcoes = alternados.controleTap(sis, parametrosTap)
                            for b, va in zip(circuitosControle, valoresAntigos):
                                message = f'Circuito {b} mudou tap de {va} para {sis.dcircuitos[b]["TAP(PU)"]}'
                                logs.log(logNumber, message, 'ALT')

                            # Salvando alterações
                            sis.calcularMatrizes()
                            exportacao.exportarSistema('dados/dados_sistema_modificado.txt', sis)
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
                                    "CIRCUITO_OBJETIVO_DEFASAGEM" : 4,
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
                            circuitosControle = parametrosTap["CIRCUITOS_CONTROLE_DEFASAGEM"]
                            circuitosControle = circuitosControle.split(',')
                            circuitosControle = [ int(b)-1 for b in circuitosControle ]
                            valoresAntigos = []
                            for b in circuitosControle:
                                valoresAntigos.append(sis.dcircuitos[b]['TAP(PU)'])
                            sis, correcoes = alternados.controleDefasagem(sis, parametrosDefasagem)
                            for b, va in zip(circuitosControle, valoresAntigos):
                                message = f'Circuito {b} mudou defasagem de {va} para {sis.dcircuitos[b]["TAP(PU)"]}'
                                logs.log(logNumber, message, 'ALT')

                            # Salvando alterações
                            sis.calcularMatrizes()
                            exportacao.exportarSistema('dados/dados_sistema_modificado.txt', sis)
                    case _:
                        break
            case 'comp' | 'COMP': 
                dadosSistemas = []
                arquivos = []
                while True:
                    files = [f for f in os.listdir('dados/') if f.split('.')[-1] == 'txt']
                    files = [f for f in files if f.split('_')[0] == 'dados']
                    c = 0
                    while True:
                        index = 0
                        for f in files:
                            index += 1
                            print(f'{index} - {f}')
                        importar = input(f'Selecionar arquivo = ')
                        if importar.isnumeric():
                            importar = int(importar) - 1
                            if importar <= len(files): 
                                arq = 'dados/' + files[importar]
                                break
                    print(f'Iniciando Leitura de dados: {arquivos}')
                    dbarras, dcircuitos = leitura.lerDados(arq)
                    dadosSistemas.append((dbarras, dcircuitos))
                    dbarras, dcircuitos = np.copy(sis.dbarras), np.copy(sis.dcircuitos)
                    dadosSistemas.append((dbarras, dcircuitos))

                    if len(dadosSistemas[0][0]) != len(dadosSistemas[1][0]) or len(dadosSistemas[0][1]) != len(dadosSistemas[1][1]):
                        print('Sistemas com diferentes números de barras ou circuitos | Não comparou')
                        break
                    
                    compara.sistemas(dadosSistemas)
                    break
            case 'g' | 'G':
                indices = analise(sis, 3)
                # print(indices)
            case 'i' | 'I':
                print('Comentário: ')
                message = input('')
                logs.log(logNumber, message, 'CMT')
            case 'q' | 'Q': print('Encerrando'); break
            case _:
                pass
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
                    files = [f for f in os.listdir('dados/') if f.split('.')[-1] == 'txt']
                    files = [f for f in files if f.split('_')[0] == 'dados']
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








