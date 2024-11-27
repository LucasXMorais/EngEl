# Lucas Xavier de Morais
# 27/11/24 - Programas para a expansão de sistemas
# PLANEJAMENTO - Engenharia Elétrica (UFSJ)
import numpy as np
import copy

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

def candidatos(sis, nivel_tensao):

    #Obtem todos os niveis de tensao
    barras_do_nivel = []
    for b in sis.dbarras:
        print(b, nivel_tensao)
        if b['VBase'] == nivel_tensao: barras_do_nivel.append(b["BARRA"])

    candidatos = combinacoes(barras_do_nivel, 2)
    print(candidatos, len(candidatos))

    # Calcula as distâncias dos candidatos
    candidatos_retorno = []
    for cand in candidatos:
        cand_de = cand[0]
        cand_para = cand[1]
        bDE = sis.getBarra(cand_de)
        posDE = (bDE['x'], bDE['y'])
        bPARA = sis.getBarra(cand_para)
        posPARA = (bPARA['x'], bPARA['y'])
        distancia = np.sqrt( (posDE[0] - posPARA[0])**2 + (posDE[1] - posPARA[1])**2 )
        distancia *= 1.2 

        if distancia > 180: continue

        for c in sis.dcircuitos:
            bde = c['BDE']
            bpara = c['BPARA']
            tipo = 'E'
            if cand == [bde, bpara] or cand == [bpara, bde]: tipo = 'R'

        if tipo == 'E': 
            candidatos_retorno.append( (cand_de, cand_para, distancia, tipo) )
            # candidatos_retorno.append( (cand_de, cand_para, distancia, 'R') )
            # candidatos_retorno.append( (cand_de, cand_para, distancia, 'R') )
        else:
            candidatos_retorno.append( (cand_de, cand_para, distancia, 'R') )
            # candidatos_retorno.append( (cand_de, cand_para, distancia, 'R') )

    return candidatos_retorno

    

