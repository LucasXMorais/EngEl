# 13/07/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
import configparser
import numpy as np
import copy
import os
from modules import *
from modules import limites
import matplotlib.pyplot as plt

def iniciarSistema() -> sistema.Sistema:
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

    # Calculando as potências e fluxos de potência
    sistema.calcularPotencias()

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
        resposta = input('Mudar sistema? ( S / N / F ) ')
        match resposta:
            case 's' | 'S':
                while True:
                    print('1. Mudar dados de barra')
                    print('2. Mudar dados de circuito')
                    modo = input('')
                    match modo:
                        case '1':
                            while True:
                                numBarra = input('Alterar barra: ')
                                if numBarra == 'q' or numBarra == 'Q':break
                                if numBarra.isnumeric():
                                    numBarra = int(numBarra)-1
                                    if numBarra <= len(sis.dbarras):
                                        exibir.mostrarDadosBarras(sis, numBarra)

                                        dados = modificar.valorDicionario(sis.dbarras[numBarra])
                                        sis.dbarras[numBarra][dados[0]] = dados[1]

                                        exibir.mostrarDadosBarras(sis, numBarra)

                                        # Salvando alterações
                                        sis.calcularMatrizes()
                                        exportacao.exportarSistema('dados_sistema_modificado.txt', sis)
                                        break
                            break
                        case '2':
                            while True:
                                numCircuito = input('Alterar circuito: ')
                                if numCircuito == 'q' or numCircuito == 'Q':break
                                if numCircuito.isnumeric():
                                    numCircuito = int(numCircuito)-1
                                    if numCircuito <= len(sis.dcircuitos):

                                        exibir.mostrarDadosCircuitos(sis, numCircuito)

                                        dados = modificar.valorDicionario(sis.dcircuitos[numCircuito])
                                        sis.dcircuitos[numCircuito][dados[0]] = dados[1]

                                        exibir.mostrarDadosCircuitos(sis, numCircuito)

                                        # Salvando alterações
                                        sis.calcularMatrizes()
                                        exportacao.exportarSistema('dados_sistema_modificado.txt', sis)
                                        break
                            break
                        case 'q' | 'Q': break
                        case _:
                            print('Não encontrado')
                # FIM WHILE
            case 'n' | 'N':
                while True:
                    sair = False
                    print('1. Rodar Fluxo')
                    print('2. Sair')
                    modo = input('')
                    match modo:
                        case '1':
                            # Calculando as variáveis - Com o argumento TRUE para rodar em modo silencioso
                            sis.resolverFluxo()
                        
                            # Calculando as potências e fluxos de potência
                            sis.calcularPotencias()
                        
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
                            break
                        case '2':
                            print('Encerrando')
                            sair = True
                            break
                        case _:
                            print('Entrada inválida')
                # Fim While
                if sair: break
            case 'f' | 'F':
                sis.resolverFluxo()
            
                # Calculando as potências e fluxos de potência
                sis.calcularPotencias()
            
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
            case _:
                print('Entrada inválida')
    # FIM WHILE
# Fim menu

