# 03/07/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência - Módulo para fazer ajustes alternados
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
import configparser
from modules import sistema

# ---- CONTROLE POR TENSAO ----
def controleTensao(sistema: sistema.Sistema, parametros: dict = None):
#     parametrosTensao = {
#             "MAX_ITER_TENSAO" : 100,
#             "TOLERANCIA_TENSAO" : 0.001,
#             "ALPHA_TENSAO" : 0.7,
#             "OBJETIVO_TENSAO" : 1.0,
#             "BARRA_OBJETIVO_TENSAO" : 3,
#             "BARRAS_CONTROLE_TENSAO" : '1,2',
#             }
    config = configparser.ConfigParser()
    config.read('config.ini')

    if parametros:
        maxAlternadosIter = parametros["MAX_ITER_TENSAO"]
        tolerancia = parametros["TOLERANCIA_TENSAO"]
        obetivoTensao = parametros["OBJETIVO_TENSAO"]
        barraObjetivo = parametros["BARRA_OBJETIVO_TENSAO"] - 1
        barrasControle = parametros["BARRAS_CONTROLE_TENSAO"]
        barrasControle = barrasControle.split(',')
        barrasControle = [ int(b)-1 for b in barrasControle ]
        numeroBarrasControle = len(barrasControle)
        alpha = parametros["ALPHA_TENSAO"]
    else:
        maxAlternadosIter = int(config['ALTERNADOS']['MAX_ITER_TENSAO'])
        tolerancia = float(config['ALTERNADOS']['TOLERANCIA_TENSAO'])
        obetivoTensao = float(config['ALTERNADOS']['OBJETIVO_TENSAO'])
        barraObjetivo = int(config['ALTERNADOS']['BARRA_OBJETIVO_TENSAO']) - 1
        barrasControle = str(config['ALTERNADOS']['BARRAS_CONTROLE_TENSAO']) 
        barrasControle = barrasControle.split(',')
        barrasControle = [ int(b)-1 for b in barrasControle ]
        numeroBarrasControle = len(barrasControle)
        alpha = float(config['ALTERNADOS']['ALPHA_TENSAO'])

    i = 1
    correcoes = []
    while i <= maxAlternadosIter:
        erro = obetivoTensao - sistema.tensoes[barraObjetivo]  

        if np.abs(erro) <= tolerancia: print(f'Convergiu em {i-1} iteracoes'); break

        correcao = alpha * erro
        correcao = correcao / numeroBarrasControle
        print(f'Correcao por barra: {correcao:.6f}')

        for b in barrasControle:
            sistema.dbarras[b]['Vesp(PU)'] += correcao
            correcoes.append([correcao, sistema.dbarras[0]['Vesp(PU)']])
    
        sistema.calcularMatrizes()
        sistema.resolverFluxo(True)

        print(f'{i} / {maxAlternadosIter} || {(i/maxAlternadosIter)*100:.2f}%')

        i +=1

    return sistema, correcoes

# ---- CONTROLE POR TAP ----
def controleTap(sistema: sistema.Sistema, parametros: dict = None):
#     parametrosTap = {
#             "MAX_ITER_TAP" : 100,
#             "TOLERANCIA_TAP" : 0.001,
#             "ALPHA_TAP" : 1.5,
#             "OBJETIVO_TAP" : 1.01,
#             "BARRA_OBJETIVO_TAP" : 2,
#             "CIRCUITOS_CONTROLE_TAP" : '2',
#             }
    config = configparser.ConfigParser()
    config.read('config.ini')

    if parametros:
        maxAlternadosIter = parametros["MAX_ITER_TAP"]
        tolerancia = parametros["TOLERANCIA_TAP"]
        objetivoTap = parametros["OBJETIVO_TAP"]
        barraObjetivo = parametros["BARRA_OBJETIVO_TAP"] - 1
        circuitosControle = parametros["CIRCUITOS_CONTROLE_TAP"]
        circuitosControle = circuitosControle.split(',')
        circuitosControle = [ int(c)-1 for c in circuitosControle ]
        numeroCircuitosControle = len(circuitosControle)
        alpha = parametros["ALPHA_TAP"]
    else:
        maxAlternadosIter = int(config['ALTERNADOS']['MAX_ITER_TAP'])
        tolerancia = float(config['ALTERNADOS']['TOLERANCIA_TAP'])
        objetivoTap = float(config['ALTERNADOS']['OBJETIVO_TAP'])
        barraObjetivo = int(config['ALTERNADOS']['BARRA_OBJETIVO_TAP']) - 1
        circuitosControle = str(config['ALTERNADOS']['CIRCUITOS_CONTROLE_TAP']) 
        circuitosControle = circuitosControle.split(',')
        circuitosControle = [ int(c)-1 for c in circuitosControle ]
        numeroCircuitosControle = len(circuitosControle)
        alpha = float(config['ALTERNADOS']['ALPHA_TAP'])

    i = 1
    tapInicial = []
    for c in circuitosControle:
        tapInicial.append(sistema.dcircuitos[c]['TAP(PU)'])
        print(f'Tap Inicial: {tapInicial[-1]:.6f} | Circuito: {c+1}')
    correcoes = []
    while i <= maxAlternadosIter:
        erro = objetivoTap - sistema.tensoes[barraObjetivo]  

        if np.abs(erro) <= tolerancia: print(f'Convergiu em {i-1} iteracoes'); break

        correcao = alpha * erro
        correcao = correcao / numeroCircuitosControle
        print(f'Correcao no tap: {correcao:.6f}')

        for c in circuitosControle:
            sistema.dcircuitos[c]['TAP(PU)'] += correcao
            correcoes.append([correcao, sistema.dcircuitos[c]['TAP(PU)']])
    
        sistema.calcularMatrizes()
        sistema.resolverFluxo(True)

        print(f'{i} / {maxAlternadosIter} || {(i/maxAlternadosIter)*100:.2f}%')

        i +=1

    tapFinal = []
    for c,a in zip(circuitosControle,range(numeroCircuitosControle)):
        tapFinal.append(sistema.dcircuitos[c]['TAP(PU)'])

    return sistema, correcoes

# ---- CONTROLE POR DEFASAGEM ----
def controleDefasagem(sistema: sistema.Sistema, parametros: dict = None):
#     parametrosDefasagem = {
#             "MAX_ITER_DEFASAGEM" : 100,
#             "TOLERANCIA_DEFASAGEM" : 0.001,
#             "ALPHA_DEFASAGEM" : 1.5,
#             "OBJETIVO_DEFASAGEM" : 1.01,
#             "BARRA_OBJETIVO_DEFASAGEM" : 4,
#             "CIRCUITOS_CONTROLE_DEFASAGEM" : '4',
#             }
    config = configparser.ConfigParser()
    config.read('config.ini')

    if parametros:
        maxAlternadosIter = parametros["MAX_ITER_DEFASAGEM"]
        tolerancia = parametros["TOLERANCIA_DEFASAGEM"]
        objetivoDefasagem = parametros["OBJETIVO_DEFASAGEM"]
        barraObjetivo = parametros["CIRCUITO_OBJETIVO_DEFASAGEM"] - 1
        circuitosControle = parametros["CIRCUITOS_CONTROLE_DEFASAGEM"]
        circuitosControle = circuitosControle.split(',')
        circuitosControle = [ int(c)-1 for c in circuitosControle ]
        numeroCircuitosControle = len(circuitosControle)
        alpha = parametros["ALPHA_DEFASAGEM"]
    else:
        maxAlternadosIter = int(config['ALTERNADOS']['MAX_ITER_DEFASAGEM'])
        tolerancia = float(config['ALTERNADOS']['TOLERANCIA_DEFASAGEM'])
        objetivoDefasagem = float(config['ALTERNADOS']['OBJETIVO_DEFASAGEM'])
        circuitoObjetivo = int(config['ALTERNADOS']['CIRCUITO_OBJETIVO_DEFASAGEM']) - 1
        circuitosControle = str(config['ALTERNADOS']['CIRCUITOS_CONTROLE_DEFASAGEM']) 
        circuitosControle = circuitosControle.split(',')
        circuitosControle = [ int(c)-1 for c in circuitosControle ]
        numeroCircuitosControle = len(circuitosControle)
        alpha = float(config['ALTERNADOS']['ALPHA_DEFASAGEM'])

    i = 1
    defInicial = []
    for c in circuitosControle:
        defInicial.append(sistema.dcircuitos[c]['TAP(PU)'])
        print(f'Tap Inicial: {defInicial[-1]:.6f} | Circuito: {c+1}')
    correcoes = []
    while i <= maxAlternadosIter:
        erro = objetivoDefasagem - sistema.fluxoPkm[circuitoObjetivo][0]

        if np.abs(erro) <= tolerancia: print(f'Convergiu em {i-1} iteracoes'); break

        correcao = alpha * erro
        correcao = correcao / numeroCircuitosControle
        print(f'Correcao na defasagem: {correcao:.6f}')

        for c in circuitosControle:
            sistema.dcircuitos[c]['DEF(GRAUS)'] += correcao
            correcoes.append([correcao, sistema.dcircuitos[c]['DEF(GRAUS)']])
    
        sistema.calcularMatrizes()
        sistema.resolverFluxo(True)

        print(f'{i} / {maxAlternadosIter} || {(i/maxAlternadosIter)*100:.2f}%')

        i +=1

    defFinal = []
    for c,a in zip(circuitosControle,range(numeroCircuitosControle)):
        defFinal.append(sistema.dcircuitos[c]['TAP(PU)'])

    return sistema, correcoes

def pegarParametros(dicionario: dict, default: bool = None) -> dict:
    saida = dicionario
    for key in dicionario:
        valor = False
        while True:
            if not default:
                valor = input(f'Novo valor do campo {key}: ')
            elif key.split('_')[0] not in ['MAX','TOLERANCIA']:
                valor = input(f'Novo valor do campo {key}: ')
            if not valor: break
            tipo = dicionario[key]
            if isinstance(tipo, int):
                valor = int(valor)
                saida[key] = valor
                break
            if isinstance(tipo, float):
                valor = float(valor)
                saida[key] = valor
                break
            if isinstance(tipo, str):
                valor = str(valor)
                saida[key] = valor
                break
            print('Valor Inválido')
        # Fim while
    # Fim for
    return saida


