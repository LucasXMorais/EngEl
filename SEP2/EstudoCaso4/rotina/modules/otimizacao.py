# 04/08/24 - Lucas Xavier de Morais 
# FLuxo de potência linearizado com perdasd
# SEP II - Engenharia Elétrica (UFSJ)
from scipy.optimize import linprog, minimize
import numpy as np
from modules import logs, latex

def fluxoOtimo(sis):

    def funcaoObjetivo():
        # Parte dos ângulos
        barras_angulos = [b['BARRA'] for b in sis.dbarras if b['TIPO'] != 'SW']
        objetivo = [0 for _ in barras_angulos]
        # Parte das potências geradas
        custo_max = 0
        for b in sis.dbarras:
            if b['TIPO'] in ['PQ']: continue
            custo = float(b["Cus"])
            if custo > custo_max: custo_max = custo
            objetivo.append(custo)
        custo_max = 4*custo_max
        # Custo de cortes
        for b in sis.dbarras:
            if float(b['PD(PU)']) != 0:
                objetivo.append(custo_max)
        return { 'f': objetivo }
    # Fim OBJETIVO

    # barras_cortes = [b['BARRA'] for b in sis.dbarras if b['PD(PU)'] != 0]
    def montarIgualdades():
        # Igualdades é dispacho e geracao
        # barras_despachos = [b['BARRA'] for b in sis.dbarras if b['TIPO'] in ['PV','SW'] ]
        barraSW = 0
        for bar in sis.dbarras:
            if bar["TIPO"] == 'SW': 
                barraSW = bar["BARRA"]
                break
        barraSW = int(barraSW)-1

        BLinear = sis.matBkmLinear
        igualdades = []
        igualdades_limites = []

        for bar, bk in zip(sis.dbarras, BLinear):
            equacao = []
            # Angulos
            c = -1
            for bkm in bk:
                c+=1 
                if c == barraSW: continue
                equacao.append(bkm)
            # Geradores

            for b in sis.dbarras:
                if b['TIPO'] == 'PQ': continue
                custo = float(b["Cus"])
                if custo == 0: continue
                ger = 0
                if b['BARRA'] == bar['BARRA']: ger = 1
                equacao.append(ger)
            # Cortes
            for b in sis.dbarras:
                if float(b['PD(PU)']) == 0: continue
                carga = 0
                if b['BARRA'] == bar['BARRA']: carga = 1
                equacao.append(carga)

            # Montando as equacoes de igualdade para cada barra
            igualdades.append(equacao)
            
            carga = 0
            for b in sis.dbarras:
                if float(b['PD(PU)']) == 0: continue
                if b['BARRA'] == bar['BARRA']: carga = b['PD(PU)']
            igualdades_limites.append(carga)

        return { 'Aeq': igualdades, 'beq': igualdades_limites }
    # Fim igualdades

    def limitesSuperioresInferiores():

        # Limites de angulos
        barras_angulos = [b['BARRA'] for b in sis.dbarras if b['TIPO'] != 'SW']
        limites = []
        limites = [(-np.pi,np.pi) for _ in barras_angulos]

        # Parte das potências geradas
        barras_despachos = [b['BARRA'] for b in sis.dbarras if b['PGesp(PU)'] != 0 or b['TIPO'] == 'SW']
        for b in sis.dbarras:
            if b['BARRA'] not in barras_despachos: continue
            capacidade_ger_max = float(b["CGmax(PU)"])
            capacidade_ger_min = float(b["CGmin(PU)"])
            lim = (capacidade_ger_min, capacidade_ger_max)
            limites.append(lim)

        # Cortes
        barras_cortes = [b['BARRA'] for b in sis.dbarras if b['PD(PU)'] != 0]
        for b in sis.dbarras:
            if b['BARRA'] not in barras_cortes: continue
            carga = float(b['PD(PU)'])
            limites.append( (0, carga) )

        return { 'limites': limites }
    # Fim LIMITES

    def montarInequacoes():
        BLinear = sis.matBkmLinear
        inequacoes = []
        inequacoes_limites = []

        barras_angulos = [b['BARRA'] for b in sis.dbarras if b['TIPO'] != 'SW']
        barras_despachos = [b['BARRA'] for b in sis.dbarras if b['PGesp(PU)'] != 0 or b['TIPO'] == 'SW']
        barras_cortes = [b['BARRA'] for b in sis.dbarras if b['PD(PU)'] != 0]

        for cir in sis.dcircuitos:
            k = int(cir['BDE'])
            m = int(cir['BPARA'])
            inequacao_km = []
            inequacao_mk = []

            # Angulos
            Bkm = -BLinear[k-1][m-1]
            for barra in barras_angulos:
                if barra == k:
                    bkm = Bkm
                    bmk = -Bkm
                else:
                    bkm = -Bkm
                    bmk = Bkm
                if barra in [k,m]: 
                    inequacao_km.append(bkm)
                    inequacao_mk.append(bmk)
                else:
                    inequacao_km.append(0)
                    inequacao_mk.append(0)

            geradores = [0 for _ in barras_despachos]
            inequacao_km += geradores
            inequacao_mk += geradores

            cargas = [0 for _ in barras_cortes]
            inequacao_km += cargas
            inequacao_mk += cargas

            # # Geradores
            # for b in sis.dbarras:
            #     if b['BARRA'] not in barras_despachos: continue
            #     # custo = float(b["Cus"])
            #     # if custo == 0: continue
            #     inequacao_km.append(0)
            #     inequacao_mk.append(0)
            # # Cortes
            # for b in sis.dbarras:
            #     if b['BARRA'] not in barras_cortes: continue
            #     inequacao_km.append(0)
            #     inequacao_mk.append(0)


            # Montando as equacoes de igualdade para cada barra
            inequacoes.append(inequacao_km)
            inequacoes.append(inequacao_mk)
            
            capacidade = float(cir['CAP(PU)'])
            # Deve ter um limite para cada direcao (km ou mk)
            inequacoes_limites.append(capacidade)
            inequacoes_limites.append(capacidade)


        return { 'Aub': inequacoes, 'bub': inequacoes_limites }
    # Fim ineq

    message = 'Iniciando otimizacao'
    logs.log(message, 'OTI')
    objetivo = funcaoObjetivo()['f']
    igual = montarIgualdades()
    igualdades = igual['Aeq']
    igualdades_limites = igual['beq']
    limites = limitesSuperioresInferiores()['limites']
    ineq = montarInequacoes()
    inequacoes = ineq['Aub']
    inequacoes_limites = ineq['bub']


    message = f'Problema de otimizacao montado'
    logs.log(message, 'OTI')
    message = f'Variaveis de decisao: {len(objetivo)}'
    logs.log(message, 'OTI')
    message = f'A_eq: {len(igualdades)} b_eq: {len(igualdades_limites)}'
    logs.log(message, 'OTI')
    message = f'A: {len(inequacoes)} b: {len(inequacoes_limites)}'
    logs.log(message, 'OTI')

    resultado = linprog(objetivo, 
                        A_ub=inequacoes,
                        b_ub=inequacoes_limites,
                        A_eq=igualdades,
                        b_eq=igualdades_limites,
                        bounds=limites)

    return resultado

def otimizar(sis):
    resultado = fluxoOtimo(sis)
    message = f'Otimizacao terminada com sucesso: {resultado.success} e mensagem: {resultado.message}'
    logs.log(message, 'OTI')
    if not resultado.success: print('Falha na otimizacao'); return

    sis.linearizadoSemPerdas = True

    barras_angulos = [b['BARRA'] for b in sis.dbarras if b['TIPO'] != 'SW']
    barras_despachos = [b['BARRA'] for b in sis.dbarras if b['PGesp(PU)'] != 0 or b['TIPO'] == 'SW']
    barras_cortes = [b['BARRA'] for b in sis.dbarras if b['PD(PU)'] != 0]
    barraSW = 0
    for bar in sis.dbarras:
        if bar["TIPO"] == 'SW': 
            barraSW = bar["BARRA"]
            break
    barraSW = int(barraSW)

    r_count = 0
    angulos_otimos = []
    tabela_latex_angulos = []
    print('ANGULOS OTIMOS')
    for b in sis.dbarras:
        if b['BARRA'] in barras_angulos:
            ang_otimo = resultado.x[r_count]*180/np.pi
            print(f'Barra {b["BARRA"]}: angulo: {ang_otimo:.4f}')
            r_count+=1
        else:
            ang_otimo = 0
            print(f'Barra {b["BARRA"]}: angulo: {0:.4f}')
        angulos_otimos.append(ang_otimo)
        message = f'Angulo da barra {b["BARRA"]}: {ang_otimo:.6f}'
        logs.log(message, 'OTI')
        tabela_latex_angulos.append( (b["BARRA"], ang_otimo) )

    despachos_otimos = []
    tabela_latex_despachos = []
    print('DESPACHOS OTIMOS')
    for b in sis.dbarras:
        if b['BARRA'] in barras_despachos:
            desp_otimo = resultado.x[r_count]
            print(f'Barra {b["BARRA"]}: Trocando despacho {b["PGesp(PU)"]} para {desp_otimo:.4f}')
            message = f'Gerador {b["BARRA"]} mudou despacho {b["PGesp(PU)"]} para {desp_otimo:.4f}'
            logs.log(message, 'OTI')
            tabela_latex_despachos.append( (b["BARRA"], desp_otimo) )
            b['PGesp(PU)'] = np.abs(desp_otimo)
            r_count+=1
        else:
            desp_otimo = 0
        despachos_otimos.append(desp_otimo)
        # Alterando despachos

    cortes_otimos = []
    tabela_latex_cortes = []
    print('CORTES')
    for b in sis.dbarras:
        if b['BARRA'] in barras_cortes:
            cut_otimo = resultado.x[r_count]
            print(f'Barra {b["BARRA"]}: Fazendo corte {b["PD(PU)"]} - {cut_otimo:.4f} = {b["PD(PU)"] - cut_otimo:.4f} ')
            message = f'Carga {b["BARRA"]} sofreu corte: {b["PD(PU)"]} - {cut_otimo:.4f} = {b["PD(PU)"] - cut_otimo:.4f}'
            logs.log(message, 'OTI')
            tabela_latex_cortes.append( (b["BARRA"], b["PD(PU)"], cut_otimo) )
            b['PD(PU)'] -= cut_otimo
            r_count+=1
        else:
            cut_otimo = 0
        cortes_otimos.append(cut_otimo)

    tables = {
            'resultado':resultado,
            'angulos':tabela_latex_angulos,
            'despachos':tabela_latex_despachos,
            'cortes':tabela_latex_cortes,
            }
    latex.optimization('resultados/tabelasOtimizacao.txt', tables, sis)





