# 13/07/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
import configparser
import numpy as np
import copy
from modules import *


def printarCabecalho():
    print(f'{100*"="}')
    now: datetime = datetime.now()
    now = f'{now:%c}'
    print(f'{now:^100}')
    print(f'{100*"="}')
    print(f'{"Universidade Federal de São João Del Rei":^100}')
    print(f'{"Análise de Sistemas Elétricos de Potência II":^100}')
    print(f'{100*"-"}')
    print(f'{"Relatório do Sistema do Estudo de Caso 2":^100}')
    print(f'{100*"="}')
    print(f'{"Autores:":^25} {"Cássia R. A. Freitas":^25} {"Gabriel L. de Sousa":^25} {"Lucas X. Morais":^25}')
    print(f'{"Matrícula:":^25} {"190900048":^25} {"180950030":^25} {"190950011":^25}')
    # print(f'{"Autor: Lucas X. Morais":^100}')
    # print(f'{"Matrícula: 190950011":^100}')
    print(f'{100*"="}')
# Fim cabecalho

def resumoSistema(sep: sistema.Sistema):
    print(f' {63*"-"}')
    print(f'|{"BARRA":^10} | {"TENSAO":^10} | {"ANGULO":^10} | {"V (kV)":^10} | {"DENTRO LIM":^10}|')
    print(f' {63*"-"}')

    for b, t, a in zip(sep.dbarras, sep.tensoes, sep.angulosGrau):
        string = '|'
        string += (f'{b["BARRA"]:^10}')
        string += ' | '
        ten = f"{t:.4f}"
        string += (f"{ten:^10}")
        string += ' | '
        ang = f"{a:.4f}"
        string += (f"{ang:^10}")
        string += ' | '
        kv = b["VBase"]
        string += (f"{kv:^10}")
        string += ' | '
        aceitavel = limites.limiteTensao(kv, ten)
        string += (f"{aceitavel:^10}")
        string += '|'
        print(string)
    # Fim for
    print(f' {63*"-"}')
    # FIM TENSOES
    
    # GERACAO
    print(f' {100*"-"}')
    print(f'|{"BARRA":^10}{"PG":^18}{"Carga Máxima":^18}{"Carga Mínima":^18}{"Prop. de uso":^18}{"Respeita lim.?":^18}|')
    print(f' {100*"-"}')
    barrasAlerta = []
    for b, pGeracao in zip(sep.dbarras, sep.pG):
        if b["TIPO"] == "PQ": continue
        string = '|'
        string += f'{b["BARRA"]:^10}'
        pg = f"{pGeracao[0]:.4f}"
        string += f"{pg:^18}"
        limiteMaximoPercentual = 1
        limiteMinimoPercentual = 0
        cgmax = f'{b["CGmax(PU)"]:.2f}'
        string += f"{cgmax:^18}"
        cgmin = f'{b["CGmin(PU)"]:.2f}'
        string += f"{cgmin:^18}"
        if b["CGmax(PU)"] > 0:
            limiteMinimoPercentual = b["CGmin(PU)"] / b["CGmax(PU)"]
        potenciaGeracaoPercentual = (pGeracao[0] / b["CGmax(PU)"]) 
        stringPGerPerc = f'{(potenciaGeracaoPercentual*100):.2f}' 
        string += f"{stringPGerPerc:^18}"
        aceitavel = "SIM"
        if b["CGmax(PU)"] != 0:
            if potenciaGeracaoPercentual < limiteMinimoPercentual * 1.05 or potenciaGeracaoPercentual > limiteMaximoPercentual * 0.95:
                aceitavel = "ALE"
            if potenciaGeracaoPercentual < limiteMinimoPercentual or potenciaGeracaoPercentual > limiteMaximoPercentual:
                aceitavel = "NÃO"
        if aceitavel in ["NÃO", "ALE"] : barrasAlerta.append(b["BARRA"])
        string += f"{aceitavel:^18}"
        string += '|'
        print(string)

    if barrasAlerta : 
        print(f"Atenção para a(s) barra(s) {barrasAlerta}")
    else:
        print(f"Geração respeitando os limites")
    print(f' {100*"-"}')
    # FIM GERACAO
    
    # CIRCUITOS
    print(f' {105*"-"}')
    print(f'|{"NCIR":^5}{"BARRA DE/PARA":^10}{"SKM":^15}{"% de uso":^15}{"SMK":^15}{"% de uso":^15}{"Capacidade":^15}{"Respeita lim.?":^15}|')
    print(f' {105*"-"}')

    linhasAlerta = []
    for c, skm, smk in zip(sep.dcircuitos, sep.fluxoSkm, sep.fluxoSmk):
        string = '|'
        string += f'{c["NCIR"]:^5}'
        string += f'{c["BDE"]:^5}'
        string += f'{c["BPARA"]:^5}'

        capacidade = c["CAP(PU)"]

        stringSkm = f"{skm[0]:.4f}"
        string += f"{stringSkm:^15}"

        pskm = skm[0] / capacidade
        stringpskm = f'{(pskm*100):.2f}'
        string += f"{stringpskm:^15}"

        stringSmk = f"{smk[0]:.4f}"
        string += f"{stringSmk:^15}"
        
        psmk = smk[0] / capacidade
        stringpsmk = f'{(psmk*100):.2f}'
        string += f"{stringpsmk:^15}"

        string += f'{c["CAP(PU)"]:^15}'
        aceitavel = "SIM" 
        if ( pskm > 0.95 ) or ( psmk > 0.95 ) :
            aceitavel = "ALE"
        if ( pskm > 1 ) or ( psmk > 1 ) :
            aceitavel = "NÃO"
        if aceitavel in ["NÃO", "ALE"] : linhasAlerta.append((c["BDE"], c["BPARA"]))
        string += f"{aceitavel:^15}"
        string += '|'
        print(string)

    print(f' {105*"-"}')

    if linhasAlerta : 
        print(f"Atenção para a(s) linhas(s) {linhasAlerta}") 
    else:
        print(f"Linhas operando dentro dos limites de potência") 

    print(f' {105*"-"}')
    # FIM CIRCUITOS
# Fim sep

def mostrarDadosBarras(sep: sistema.Sistema, numBarra: int):
    print(f'{4*"|-+-|"}')
    barra = sep.dbarras[numBarra]
    for b in barra:
        print(f' {b:^10} : {barra[b]:^7}')
    print(f'{4*"|-+-|"}')
# FIM BARRA

def mostrarDadosCircuitos(sep: sistema.Sistema, numCircuito: int):
    print(f'{4*"|-+-|"}')
    circuito = sep.dcircuitos[numCircuito]
    for c in circuito:
        print(f' {c:^10} : {circuito[c]:^7}')
    print(f'{4*"|-+-|"}')
# FIM CIRCUITO


