# Lucas Xavier de Morais
# 24/07/24 - Análise de contingêcnias
# SEP II - Engenharia Elétrica (UFSJ)
import copy
import itertools
import numpy as np

# Gera combincaoes de k itens de 1 a n
def combinacoes(lista, k) -> list:
    combos = []

    i = 0
    def recursao(corpo, combinacao):
        if len(combinacao) == k:
            combos.append(combinacao.copy())
            return

        c = 1
        for item in corpo:
            combinacao.append(item)
            recursao(corpo[c:], combinacao)
            combinacao.pop()
            c+=1

    recursao(lista[i:], [])
    i+=1
    return combos

# Registra todas as combinações de 1 a k
def listarCombinacoesNMenosk(circuitos, nmenos) -> list:
    lista = []
    for i in range(nmenos):
        lista += combinacoes(circuitos, i+1)
    return lista

def indiceContingencias(sis):
    indice = 0
    sobrecargas = []
    # Para o EC3 vou apenas mudar para fluxo linear e analise de ativa
    # for circ, km, mk in zip(sis.dcircuitos, sis.fluxoSkm, sis.fluxoSmk):
        # skm = km[0]
        # smk = mk[0]
    for circ, km, mk in zip(sis.dcircuitos, sis.fluxoPkm, sis.fluxoPmk):
        pkm = km[0]
        pmk = mk[0]
        sobrecarga = 0
        capacidade = circ["CAP(PU)"]
        maiorFluxo = pkm.copy()
        if pmk > maiorFluxo: maiorFluxo = pmk.copy()

        toleranciaMaxima = 1.10
        if maiorFluxo > capacidade*toleranciaMaxima: 
            sobrecarga = (maiorFluxo - capacidade) / capacidade
            sobrecargas.append(circ["NCIR"])

        indice += sobrecarga
    # Fim for
    return indice, sobrecargas
# Fim indice

def calcularIndices(sis, k: int) -> list:
    circuitos = [c["NCIR"] for c in sis.dcircuitos]
    combinacoesContingencias = listarCombinacoesNMenosk(circuitos, k)
    totalCombinacoes = len(combinacoesContingencias)

    indices = []
    c = 1
    for combinacao in combinacoesContingencias:
        copiaSistema = copy.deepcopy(sis)

        # Excluindo os circuitos das combinacoes do sistema para o teste
        copiaSistema.dcircuitos = [c for c in copiaSistema.dcircuitos if c["NCIR"] not in combinacao]
        copiaSistema.calcularMatrizes()
        copiaSistema.emContingencia = True
        # Se acionado com g usa Linear, se com G usa Newton
        if copiaSistema.usarFluxoNewton:
            copiaSistema.resolverFluxo(True)
        else:
            copiaSistema.fluxoLinearizado()

        indiceSobrecarga, circuitosSobrecarga = indiceContingencias(copiaSistema)

        if not copiaSistema.convergiu: 
            circuitosSobrecarga = ['Não converigu']

        indices.append( (combinacao, indiceSobrecarga, circuitosSobrecarga) )

        circs = ','.join([str(h) for h in combinacao])
        indString = f'{indiceSobrecarga:.6f}'.replace('.',',')
        percString = f'{c*100/totalCombinacoes:.2f}'
        message = f'| {c: >3} / {totalCombinacoes: ^3} || {percString: >6} % || {circs:^9} - Indice: {indString:^12} | {sis.iteracoes: >5} iterações'
        print(message)
        c += 1

    return indices

def ordenar(ranking):
        
    def quicksort(lista):
        if len(lista) <= 1:
            return lista
        pivot = lista.pop()

        menor = []
        maior = []
        for l in lista:
            lValue = l[1]
            pivotValue = pivot[1]
            if lValue < pivotValue:
                menor.append(l)
            else:
                maior.append(l)
        menor = quicksort(menor)
        if not menor: menor = []
        menor.append(pivot)
        maior = quicksort(maior)
        if not maior: maior = []
        return menor + maior

    ranking = quicksort(ranking)

    return ranking

def analiseNMenosK(sis, k: int) -> list:
    indices = calcularIndices(sis, k)
    ranking = []
    zeros = []
    # Tirando os indices zeros
    for i in indices:
        iD = i[1]
        if iD == 0: 
            zeros.append(i)
            continue
        ranking.append(i)

    print('Ordenando as contingencias')
    ranking = ordenar(ranking)
    rankeados = ranking[::-1] + zeros

    mostrarTopoRanking(rankeados)

    return rankeados

def mostrarTopoRanking(ranking):
    c = 1
    for r in ranking:
        contingencia = ','.join([str(h) for h in r[0]])
        indice = f'{r[1]:.6f}'.replace('.',',')
        circs = ','.join([str(h) for h in r[2]])
        message = f'{c: >2}° | Contingência: {contingencia:^8} - Índice: {indice} - Sobrecargas: {circs:^8}'
        print(message)
        c += 1
        if c > 10: break















    
