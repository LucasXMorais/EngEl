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
        lista += combinacoes(circuitos, nmenos)
    return lista

def indiceContingencias(sis) -> float:
    indice = 0
    for circ, km, mk in zip(sis.dcircuitos, sis.fluxoSkm, sis.fluxoSmk):
        skm = km[0]
        smk = mk[0]
        sobrecarga = 0
        capacidade = circ["CAP(PU)"]
        maiorFluxo = skm.copy()
        if smk > maiorFluxo: maiorFluxo = smk.copy()

        if maiorFluxo > capacidade: 
            sobrecarga = (maiorFluxo - capacidade) / capacidade

        indice += sobrecarga
    # Fim for
    return indice
# Fim indice

def analise(sis, nmenos: int) -> list:
    contingencias = []
    circuitos = [c["NCIR"] for c in sis.dcircuitos]
    combinacoesContingencias = listarCombinacoesNMenosk(circuitos, nmenos)
    totalCombinacoes = len(combinacoesContingencias)

    indices = []
    c = 1
    for combinacao in combinacoesContingencias:
        copiaSistema = copy.deepcopy(sis)

        # Excluindo os circuitos das combinacoes do sistema para o teste
        copiaSistema.dcircuitos = [c for c in copiaSistema.dcircuitos if c["NCIR"] not in combinacao]
        copiaSistema.calcularMatrizes()
        copiaSistema.resolverFluxo(True)

        indiceSobrecarga = indiceContingencias(copiaSistema)

        if not copiaSistema.convergiu: 
            # print(f'Cálculo Newton não convergiu sem o circuito {combinacao}')
            indiceSobrecarga = 0

        indices.append( (combinacao, indiceSobrecarga) )

        # message = f'{c} - Tirando o(s) circuitos {combinacao} - Indice: {indiceSobrecarga} | {c*100/totalCombinacoes:.2f}%'
        circs = ','.join([str(h) for h in combinacao])
        # print(circs)
        message = f'{c:^3} - {circs:^10} - Indice: {indiceSobrecarga:^20} | {c*100/totalCombinacoes:.2f} %'
        print(message)
        c += 1


    return indices

        


    
