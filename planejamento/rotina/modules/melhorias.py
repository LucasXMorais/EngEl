# Lucas Xavier de Morais
# 27/11/24 - Programas para a expansão de sistemas
# PLANEJAMENTO - Engenharia Elétrica (UFSJ)
import numpy as np
import configparser
import copy
from modules import otimizacao

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

# Calcula o indice de sobrecarga
def indiceMelhorias(sis):
    indice = 0
    sobrecargas = []
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
    return indice
# Fim indice

#Calcula todos os indices e exclui as possibilidades que estouram o limite
def calcularIndices(sis, k: int, candidatos: list) -> list:
    circuitos = [c[0] for c in candidatos]
    combinacoesMelhorias = listarCombinacoesNMenosk(circuitos, k)
    totalCombinacoes = len(combinacoesMelhorias)
    print(f'Foram encontrados {totalCombinacoes} combinações')
    # print(combinacoesMelhorias)

    # ATENCAO - CÒDIGO HORROROSO A FRENTE
    # Exclui combinações equivalentes
    combinacoes_unicas = []
    combinacoes_unicas_pares = []
    print(f'Organizando Os dados')
    for comb in combinacoesMelhorias:
        # Pega os pares de cada id
        pares = []
        for comb_id in comb:
            for c in candidatos:
                if c[0] == comb_id:
                    par = ( c[1], c[2] )
                    break
            pares.append(par)
        
        # Ordenando todas as combinações para achar melhor
        lista_aux = []
        while len(pares) >= 1:
            menor_de = pares[0][0]
            menor_para = pares[0][1]
            menor_index = 0
            count = 0
            for par in pares:
                par_de = par[0]
                par_para = par[1]
                if par_de < menor_de and par_para < menor_para:
                    menor_de = par_de
                    menor_para = par_para
                    menor_index = count
                count += 1
            #tira o menor da lista de pares
            pares.pop(menor_index)
            lista_aux.append( (menor_de, menor_para) )
        # termina com o vetor ordenado
        # ta muito feio isso rs
        pares = lista_aux

        combinacao_equivalente = False
        for par in combinacoes_unicas_pares:
            if par == pares: 
                combinacao_equivalente = True
                break

        if not combinacao_equivalente:
            combinacoes_unicas_pares.append(pares)
            combinacoes_unicas.append(comb)
    # Fim de combinações equivalentes
    # print(combinacoes_unicas_pares)
    # combinacoesMelhorias = combinacoes_unicas_pares
    combinacoesMelhorias = combinacoes_unicas
    totalCombinacoes = len(combinacoesMelhorias)
    # print(totalCombinacoes)

    print(f'Iniciando o processo')
    indices = []
    count = 1
    for combinacao_pares in combinacoesMelhorias:
        # print(count)
        copiaSistema = copy.deepcopy(sis)

        # Incluindo os circuitos de melhorias
        proximo_circuito = 0
        for c in copiaSistema.dcircuitos:
            if c["NCIR"] > proximo_circuito:
                proximo_circuito = c["NCIR"]
        #Fim for
        proximo_circuito += 1

        # Pegando a reatancia media. Por enquanto deixando fixo em 138
        reatancia = copiaSistema.reatancias_medias[1][1]

        # Pega os pares de cada id
        lista_combinacoes = []
        custo_total = 0
        for comb_id in combinacao_pares:
            #pega as informações de cada combinação
            for c in candidatos:
                if comb_id == c[0]:
                    novo_cir_de = c[1]
                    novo_cir_para = c[2]
                    distancia = c[3]
                    reatancia_circuito = reatancia * distancia
                    custo_total += c[4]
                    lista_combinacoes.append( ( novo_cir_de, novo_cir_para ) )
                    break

            # Montando o circuito novo
            circuito = {
                'BDE' : novo_cir_de,
                'BPARA' : novo_cir_para,
                'NCIR' : proximo_circuito,
                'RES(PU)' : 0,
                'REAT(PU)' : reatancia_circuito,
                'SUCsh(PU)' : 0,
                'TAP(PU)' : 1.0,
                'DEF(GRAUS)' : 0.0,
                'LIG(L)DESL(D)' : 'L',
                'CAP(PU)' : 1.25
            }

            copiaSistema.dcircuitos.append(circuito)
            proximo_circuito += 1
        # Fim todos os circuitos novos
        # Recalculando e fazendo fluxo linearizado
        copiaSistema.ncircuitos = len(copiaSistema.dcircuitos)
        copiaSistema.calcularMatrizes()
        copiaSistema.emContingencia = False

        # Respeita um custo máximo
        if custo_total < 20000:
            # Otimizando o sistema
            corte = otimizacao.otimizar(copiaSistema, True)

            # Pula se houve corte de carga
            indiceSobrecarga = 0
            if not corte: 
                # copiaSistema.calcularMatrizes()
                copiaSistema.resolverFluxo(True)
                # copiaSistema.fluxoLinearizado()

                indiceSobrecarga = indiceMelhorias(copiaSistema)

        circs = ','.join([str(h) for h in lista_combinacoes])
        indString = f'{indiceSobrecarga:.6f}'.replace('.',',')
        corte_string = f'{corte:.4f}'.replace('.',',')
        percString = f'{count*100/totalCombinacoes:.2f}'
        message = f'| {count: >3} / {totalCombinacoes: ^3} || {percString: >6} % || {circs:^9} - Indice: {indString:^12} | {sis.iteracoes: >2} iterações | Corte: {corte_string: >2} | Custo: {custo_total: >2}'
        print(message)
        count += 1

        # Pula onde precisou de cortar
        if corte: continue
        # Pula opções que deram sobrecarga mesmo com otimizacao
        if indiceSobrecarga > 0: continue

        if not copiaSistema.convergiu: 
            circuitosSobrecarga = ['Não converigu']

        indices.append( (lista_combinacoes, custo_total, indiceSobrecarga) )


    # print(indices)

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

def analiseNMenosK(sis, k: int, candidatos) -> list:
    indices = calcularIndices(sis, k, candidatos)
    # print(len(indices))
    print('Ordenando as melhorias')
    ranking = ordenar(indices)
    mostrarTopoRanking(ranking)
    return ranking

def mostrarTopoRanking(ranking):
    # print(ranking)
    c = 1
    for r in ranking:
        melhoria = ','.join([str(h) for h in r[0]])
        custo = f'{r[1]:.2f}'.replace('.',',')
        indice = f'{r[2]:.6f}'.replace('.',',')
        message = f'{c: >2}° | Melhoria: {melhoria:^8} - Custo: {custo} - Índice: {indice} '
        print(message)
        c += 1
        if c > 10: break

