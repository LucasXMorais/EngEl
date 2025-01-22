# Lucas Xavier de Morais
# 27/11/24 - Programas para a expansão de sistemas
# PLANEJAMENTO - Engenharia Elétrica (UFSJ)
import time
import progressbar
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
        print(f'Combinações {i+1} a {i+1}')
        lista += combinacoes(circuitos, i+1)
    return lista

# Calcula o indice de sobrecarga
def indiceMelhorias(sis):
    indice = 0
    folga = 0
    for circ, km, mk in zip(sis.dcircuitos, sis.fluxoPkm, sis.fluxoPmk):
        pkm = km[0]
        pmk = mk[0]
        sobrecarga = 0
        capacidade = circ["CAP(PU)"]
        maiorFluxo = pkm.copy()
        if pmk > maiorFluxo: maiorFluxo = pmk.copy()

        # Tolerancia máxima permitida 2% a mais só por enquanto
        toleranciaMaxima = 1.02
        # toleranciaMaxima = 1.10
        folga_circuito = 0
        if maiorFluxo > capacidade*toleranciaMaxima: 
            # SOBRECARGA
            sobrecarga = (maiorFluxo - capacidade) / capacidade

        indice += sobrecarga

        # FOLGA
        folga_circuito = (capacidade - maiorFluxo) / capacidade

        if folga_circuito > 0 : folga += folga_circuito
    if folga < 0: folga = np.abs(folga)
    # Fim for
    return (indice, folga)
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


    # Inicializando barra de status - Demora muito para 6
    # bar = progressbar.ProgressBar(max_value=totalCombinacoes)
    iterator_barra_status = 1
    start_time = time.perf_counter()

    for comb in combinacoesMelhorias:

        # Pega os pares de cada id
        pares = []
        for comb_id in comb:
            for c in candidatos:
                if c[0] == comb_id:
                    par = ( c[1], c[2] )
                    break
            pares.append(par)

            #atualiza barra

        
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

        # time.sleep(0.01)
        # bar.update(iterator_barra_status)
        iterator_barra_status+=1
        print(f'\rOrganizando dados | Total {totalCombinacoes} - {iterator_barra_status * 100 / totalCombinacoes :.2f} % ', end="", flush=True)
    # FIm todas combinações

    # Calculate elapsed time
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    elapsed_time_minutes = 0
    if elapsed_time > 60: elapsed_time_minutes = int(f'{elapsed_time/60:.0f}')
    print("")
    if elapsed_time_minutes > 0:
        print(f"Time elapsed: {elapsed_time_minutes} minutes {elapsed_time - (elapsed_time_minutes*60):.2f} seconds")
    else:
        print(f"Time elapsed: {elapsed_time:.6f} seconds")

    combinacoesMelhorias = combinacoes_unicas
    totalCombinacoes = len(combinacoesMelhorias)

    print(f'Iniciando o processo')
    
    # Inicializando barra de status
    bar = progressbar.ProgressBar(max_value=totalCombinacoes)
    iterator_barra_status = 1

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
        numero_de_pares = 0
        for comb_id in combinacao_pares:
            #pega as informações de cada combinação
            for c in candidatos:
                if comb_id == c[0]:
                    novo_cir_de = c[1]
                    novo_cir_para = c[2]
                    distancia = c[3]
                    reatancia_circuito = reatancia * distancia
                    custo_total += c[4]
                    numero_de_pares += 1
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

                retorno_indices = indiceMelhorias(copiaSistema)
                indiceSobrecarga = retorno_indices[0]
                folgasSobrecarga = retorno_indices[1]

        circs = ','.join([str(h) for h in lista_combinacoes])
        indString = f'{indiceSobrecarga:.6f}'.replace('.',',')
        corte_string = f'{corte:.4f}'.replace('.',',')
        percString = f'{count*100/totalCombinacoes:.2f}'
        message = f'| {count: >3} / {totalCombinacoes: ^3} || {percString: >6} % || {circs:^9} - Indice: {indString:^12} | {sis.iteracoes: >2} iterações | Corte: {corte_string: >2} | Custo: {custo_total: >2}'
        # print(message)
        count += 1

        if not copiaSistema.convergiu: 
            circuitosSobrecarga = ['Não converigu']

        time.sleep(0.01)
        bar.update(iterator_barra_status)
        iterator_barra_status+=1

        # Separando apenas para organização
        # Pula onde precisou de cortar
        if corte: continue
        # Pula opções que deram sobrecarga mesmo com otimizacao
        if indiceSobrecarga > 0: continue

        # Incluindo custo do bay de ligação
        custo_total = custo_total + ( numero_de_pares * 7000 )
        indices.append( (lista_combinacoes, custo_total, indiceSobrecarga, folgasSobrecarga) )
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
    print("")
    print('Ordenando as melhorias')
    # Fazendo um ranking com o indice baseado na folga
    ranking_organizado = []
    for r in indices:
        # Quanto menor a folga maior o indice
        indice_custo_folga = r[1] / r[3]
        ranking_organizado.append( (r[0],
                                    indice_custo_folga,
                                    r[2], 
                                    r[3], 
                                    r[1]) )
    ranking = ordenar(ranking_organizado)
    mostrarTopoRanking(ranking)
    return ranking

def mostrarTopoRanking(ranking):
    # print(ranking)
    c = 1
    for r in ranking:
        melhoria = ','.join([str(h) for h in r[0]])
        custo_folga = f'{r[1]:.2f}'.replace('.',',')
        # indice = f'{r[2]:.6f}'.replace('.',',')
        folgas = f'{r[3]:.4f}'.replace('.',',')
        custo = f'{r[4]:.2f}'.replace('.',',')
        custo_total = f'{r[4]*len(r[0]):.2f}'.replace('.',',')
        message = f'{c: >2}° | Melhoria: {melhoria:^8} - Custo de Folga: {custo_folga} - Custo: {custo} - Índice Folga: {folgas} '
        print(message)
        c += 1
        if c > 10: break

def calcularTempoObsolescencia(sis, ranking: list) -> list:

    count = 0
    total_testes = 20 # Testa 20 na esperança de encontrar pelo menos 10
    # Incluindo os circuitos de melhorias
    validade = []
    for melhoria in ranking:

        #Faz uma cópia do sistema para aplicar a melhoria
        copiaSistema = copy.deepcopy(sis)

        combinacoes_melhoria = melhoria[0]
        lista_combinacoes = []
        # Encontra o número do próximo circuito à ser adicionado
        proximo_circuito = 0
        for c in copiaSistema.dcircuitos:
            if c["NCIR"] > proximo_circuito:
                proximo_circuito = c["NCIR"]
        proximo_circuito += 1
        for combinacao_pares in combinacoes_melhoria:

            # Pegando a reatancia media. Por enquanto deixando fixo em 138
            reatancia = copiaSistema.reatancias_medias[1][1]

            # Pega os pares de cada id para inserir os circuitos novos
            custo_total = 0
            numero_de_pares = 0

            novo_cir_de = combinacao_pares[0]
            novo_cir_para = combinacao_pares[1]

            bDE = copiaSistema.getBarra(novo_cir_de)
            posDE = (bDE['x'], bDE['y'])
            bPARA = copiaSistema.getBarra(novo_cir_para)
            posPARA = (bPARA['x'], bPARA['y'])
            distancia = 1.2 * np.sqrt( (posDE[0] - posPARA[0])**2 + (posDE[1] - posPARA[1])**2 )
            reatancia_circuito = reatancia * distancia

            numero_de_pares += 1
            lista_combinacoes.append( ( novo_cir_de, novo_cir_para ) )

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

        copiaSistema.ncircuitos = len(copiaSistema.dcircuitos)
        copiaSistema.calcularMatrizes()
        copiaSistema.emContingencia = False

        # Limitar o total de iterações
        ano_limite = 50
        incremento_carga = 1.034 # 3,4% de aumento por ano
        # ano_atual = 0
        corte = 0
        # print(lista_combinacoes, ano_atual)
        foi_corte = False
        foi_sobrecarga = False
        for ano in range(ano_limite):

            #Incrementando a carga anualmente
            for b in copiaSistema.dbarras:
                b["PD(PU)"] = b["PD(PU)"]*incremento_carga
                b["QD(PU)"] = b["QD(PU)"]*incremento_carga
            # FIM FOR

            # TESTAR O SISTEMA

            # Otimizando o sistema
            corte = otimizacao.otimizar(copiaSistema, True)

            # Interrompe se houve corte de carga
            foi_corte = False
            if corte: 
                foi_corte = True
                break

            # Analize de sobrecarga
            indiceSobrecarga = 0
            copiaSistema.resolverFluxo(True)
            # copiaSistema.fluxoLinearizado()
            
            retorno_indices = indiceMelhorias(copiaSistema)
            indiceSobrecarga = retorno_indices[0]

            # Pula opções que deram sobrecarga mesmo com otimizacao
            foi_sobrecarga = False
            if indiceSobrecarga > 0:
                foi_sobrecarga = True
                break

            # Só incrementa o ano se deu certo
            # ano_atual = ano + 1
        # FIM FOR TODOS OS ANOS
        # print(lista_combinacoes, ano)

        validade.append( (lista_combinacoes, ano) )

        circs = ','.join([str(h) for h in lista_combinacoes])
        message = f'| {count: >2} / {total_testes: ^3} || {circs:^30} - Anos de Incremento: {ano:^4} | Terminou por => Corte: {foi_corte: >2} Sobrecarga: {foi_sobrecarga: >2} '
        print(message)
        count += 1
        if count > total_testes: break # Limitando a 10 

    print(validade)

    #TODO
    # Pegando o ranking dos melhores
    print('Ordenando as melhorias')
    # Fazendo um ranking com o indice baseado na folga
    # validade_organizado = []
    # for v in validade:
    #     # Quanto menor a folga maior o indice
    #     indice_custo_folga = r[1] / r[3]
    #     ranking_organizado.append( (r[0],
    #                                 indice_custo_folga,
    #                                 r[2], 
    #                                 r[3], 
    #                                 r[1]) )
    # ranking = ordenar(ranking_organizado)
    # mostrarTopoRanking(ranking)
    # return ranking

    # c = 1
    # for r in ranking:
    #     melhoria = ','.join([str(h) for h in r[0]])
    #     custo_folga = f'{r[1]:.2f}'.replace('.',',')
    #     # indice = f'{r[2]:.6f}'.replace('.',',')
    #     folgas = f'{r[3]:.4f}'.replace('.',',')
    #     custo = f'{r[4]:.2f}'.replace('.',',')
    #     custo_total = f'{r[4]*len(r[0]):.2f}'.replace('.',',')
    #     message = f'{c: >2}° | Melhoria: {melhoria:^8} - Custo de Folga: {custo_folga} - Custo: {custo} - Índice Folga: {folgas} '
    #     print(message)
    #     c += 1
    #     if c > 10: break

    return validade

