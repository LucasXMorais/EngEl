# 04/04/24 - Lucas Xavier de Morais 
# Exportando os dados do sistema
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
from datetime import datetime
from modules import sistema

def cabecalho(f):
    f.write(f'{100*"="}\n')
    now: datetime = datetime.now()
    now = f'{now:%c}'
    f.write(f'{now:^100}\n')
    f.write(f'{100*"="}\n\n')
    f.write(f'{"Universidade Federal de São João Del Rei":^100}\n')
    f.write(f'{"Análise de Sistemas Elétricos de Potência II":^100}\n')
    f.write(f'{100*"-"}\n')
    f.write(f'{"Relatório do Sistema do Estudo de Caso 2":^100}\n\n')
    f.write(f'{100*"="}\n')
    f.write(f'{"Autores:":^25} {"Cássia R. A. Freitas":^25} {"Gabriel L. de Sousa":^25} {"Lucas X. Morais":^25}\n')
    f.write(f'{"Matrícula:":^25} {"190900048":^25} {"180950030":^25} {"190950011":^25}\n')
    # f.write(f'{"Autor: Lucas X. Morais":^100}\n')
    # f.write(f'{"Matrícula: 190950011":^100}\n')
    f.write(f'{100*"="}\n\n')

    f.write(f'{100*"-"}\n')



def tabelaPotencias(f, sis: sistema.Sistema, pu: bool):
    dbarras = sis.dbarras
    dcircuitos = sis.dcircuitos
    pG = sis.pG
    qG = sis.qG
    sG = sis.sG
    perdasP = sis.perdasP
    perdasQ = sis.perdasQ
    perdasAtivasTotais = sis.perdasAtivasTotais
    perdasReativasTotais = sis.perdasReativasTotais
    angulos = sis.angulos
    angDeg = sis.angulosGrau
    tensoes = sis.tensoes
    basePu = sis.base
    pCalc = sis.pCalc
    qCalc = sis.qCalc
    fluxoPkm = sis.fluxoPkm
    fluxoPmk = sis.fluxoPmk
    fluxoQkm = sis.fluxoQkm
    fluxoQmk = sis.fluxoQmk
    fluxoSkm = sis.fluxoSkm
    fluxoSmk = sis.fluxoSmk
    nbarras = sis.nbarras
    ncircuitos = sis.ncircuitos

    if pu: basePu = 1

    if pu:
        f.write(f'{"Relatório das potências nas barras em PU":^100}\n')
    else:
        f.write(f'{"Relatório das potências nas barras":^100}\n')

    f.write(f'{100*"-"}\n')

    f.write(f'{"BARRA":^10}{"TENSAO":^10}{"THETA":^10}{"PI":^10}{"QI":^10}{"PG":^10}{"QG":^10}{"SG":^10}{"PD":^10}{"QD":^10}\n')
    if pu:
        f.write(f'{"#":^10}{"(PU)":^10}{"(DEG)":^10}{"["+(31*"_"):32}{" (PU) ":^6}{(31*"_")+"]":32}\n')
    else:
        f.write(f'{"#":^10}{"(PU)":^10}{"(DEG)":^10}{"MW":^10}{"MVAr":^10}{"MW":^10}{"MVAr":^10}{"MVA":^10}{"MW":^10}{"MVAr":^10}\n')

    f.write(f'{100*"-"}\n')

    for b in range(nbarras):
        f.write(f'{dbarras[b]["BARRA"]:^9}')
        v = f"{tensoes[b]:.5f}"
        f.write(f"{v:>10}")
        a = f"{angDeg[b]:.5f}"
        f.write(f"{a:>10}")
        pi = f"{pCalc[b]*basePu:.4f}"
        f.write(f"{pi:>10}")
        qi = f"{qCalc[b]*basePu:.4f}"
        f.write(f"{qi:>10}")
        pg = f"{pG[b][0]*basePu:.4f}"
        f.write(f"{pg:>10}")
        qg = f"{qG[b][0]*basePu:.4f}"
        f.write(f"{qg:>10}")
        sg = f"{sG[b][0]*basePu:.4f}"
        f.write(f"{sg:>10}")
        pd = f'{dbarras[b]["PD(PU)"]*basePu:.4f}'
        f.write(f"{pd:>10}")
        qd = f'{dbarras[b]["QD(PU)"]*basePu:.4f}'
        f.write(f"{qd:>10}")
        f.write("\n")
    f.write(f'{100*"-"}\n')
    f.write(f'{"Total":50}')
    sum = 0
    for value in pG : sum += (value[0]*basePu)
    sum = f"{sum:.4f}"
    f.write(f"{sum:^10}")
    sum = 0
    for value in qG : sum += (value[0]*basePu)
    sum = f"{sum:.4f}"
    f.write(f"{sum:^10}")
    sum = 0
    for value in sG : sum += (value[0]*basePu)
    sum = f"{sum:.4f}"
    f.write(f"{sum:^10}")
    sum = 0
    for value in dbarras : sum += (value["PD(PU)"]*basePu)
    sum = f"{sum:.4f}"
    f.write(f"{sum:^10}")
    sum = 0
    for value in dbarras : sum += (value["PD(PU)"]*basePu)
    sum = f"{sum:.4f}"
    f.write(f"{sum:^10}")
    f.write("\n")

    f.write(f'{100*"-"}\n')

    if pu:
        perPTotal = f"{perdasAtivasTotais*basePu:.4f} PU"
        perQTotal = f"{perdasReativasTotais*basePu:.4f} PU"
    else:
        perPTotal = f"{perdasAtivasTotais*basePu:.4f} MW"
        perQTotal = f"{perdasReativasTotais*basePu:.4f} MVAr"

    f.write(f'{"Total de Perdas":20}{("Perdas Ativas = "+perPTotal):^40}{"Perdas Reativas = "+perQTotal:^40}\n')

    f.write(f'{100*"-"}\n')



def analisePotenciaGeradores(f, dbarras: list[dict], pG: np.ndarray):
    f.write(f'{"Análise das potências de geração":^100}\n')

    f.write(f'{100*"-"}\n')

    f.write(f'{"BARRA":^10}{"PG":^18}{"Carga Máxima":^18}{"Carga Mínima":^18}{"Prop. de uso":^18}{"Respeita lim.?":^18}\n')
    f.write(f'{"#":^10}{"(PU)":^18}{"(PU)":^18}{"(PU)":^18}{"%":^18}{"SIM / NÃO / ALE":^18}\n')

    f.write(f'{100*"-"}\n')

    nbarras = len(dbarras)
    barrasAlerta = []
    for b in range(nbarras):
        if dbarras[b]["TIPO"] == "PQ": continue
        f.write(f'{dbarras[b]["BARRA"]:^10}')
        pg = f"{pG[b][0]:.4f}"
        f.write(f"{pg:^18}")
        cgmax = f'{dbarras[b]["CGmax(PU)"]:.2f}'
        pMax = 1
        f.write(f"{cgmax:^18}")
        cgmin = f'{dbarras[b]["CGmin(PU)"]:.2f}'
        if dbarras[b]["CGmax(PU)"] == 0:
            pMin = 0
        else:
            pMin = dbarras[b]["CGmin(PU)"] / dbarras[b]["CGmax(PU)"]
        f.write(f"{cgmin:^18}")
        pper = (pG[b][0] / dbarras[b]["CGmax(PU)"]) 
        porc = f'{(pper*100):.2f}' 
        f.write(f"{porc:^18}")
        aceit = "SIM"
        if dbarras[b]["CGmax(PU)"] != 0:
            # Se a cappacidade em pu for menor ou maior que os limites marca como
            # não atendendo aos limite. Se estiver próximo (5%), marca com alerta
            if pper < pMin * 1.05 or pper > pMax * 0.95:
                aceit = "ALE"
            if pper < pMin or pper > pMax:
                aceit = "NÃO"
        if aceit in ["NÃO", "ALE"] : barrasAlerta.append(dbarras[b]["BARRA"])
        f.write(f"{aceit:^18}")
        f.write("\n")

    f.write("\n")
    if barrasAlerta : 
        f.write(f"Atenção para a(s) barra(s) {barrasAlerta}\n") 
    else:
        f.write(f"Geração respeitando os limites\n") 
    f.write("\n")

    f.write(f'{100*"-"}\n')



def relatorioCircuitos(f, sis: sistema.Sistema, pu: bool):
    dcircuitos = sis.dcircuitos
    basePu = sis.base
    fluxoPkm = sis.fluxoPkm
    fluxoPmk = sis.fluxoPmk
    fluxoQkm = sis.fluxoQkm
    fluxoQmk = sis.fluxoQmk
    fluxoSkm = sis.fluxoSkm
    fluxoSmk = sis.fluxoSmk
    ncircuitos = sis.ncircuitos

    if pu: basePu = 1

    if pu:
        f.write(f'{"Relatório das potências em PU nos circuitos":^100}\n')
    else:
        f.write(f'{"Relatório das potências nos circuitos":^100}\n')

    f.write(f'{100*"-"}\n')

    f.write(f'{"BARRA":^10}{"PKM":^15}{"QKM":^15}{"SKM":^15}{"PMK":^15}{"QMK":^15}{"SMK":^15}\n')
    if pu:
        f.write(f'{"DE":^5}{"PARA":^5}{"["+(41*"_"):42}{" (PU) ":^6}{(41*"_")+"]":42}\n')
    else:
        f.write(f'{"DE":^5}{"PARA":^5}{"MW":^15}{"MVAr":^15}{"MVA":^15}{"MW":^15}{"MVAr":^15}{"MVA":^15}\n')

    f.write(f'{100*"-"}\n')

    ncircuitos = len(dcircuitos)
    for b in range(ncircuitos):
        f.write(f'{dcircuitos[b]["BDE"]:^5}')
        f.write(f'{dcircuitos[b]["BPARA"]:^4}')
        pkm = f"{fluxoPkm[b][0]*basePu:.4f}"
        f.write(f"{pkm:>15}")
        qkm = f"{fluxoQkm[b][0]*basePu:.4f}"
        f.write(f"{qkm:>15}")
        skm = f"{fluxoSkm[b][0]*basePu:.4f}"
        f.write(f"{skm:>15}")
        pmk = f"{fluxoPmk[b][0]*basePu:.4f}"
        f.write(f"{pmk:>15}")
        qmk = f"{fluxoQmk[b][0]*basePu:.4f}"
        f.write(f"{qmk:>15}")
        smk = f"{fluxoSmk[b][0]*basePu:.4f}"
        f.write(f"{smk:>15}")
        f.write("\n")

    f.write(f'{100*"-"}\n')



def analiseCapacidadeCircuitos(f, dcircuitos: list[dict], fluxoSkm: np.ndarray, fluxoSmk: np.ndarray):
    f.write(f'{"Relatório das potências nos circuitos km em PU":^100}\n')

    f.write(f'{100*"-"}\n')

    f.write(f'{"BARRA":^10}{"SKM":^15}{"Prop. cap.":^15}{"SMK":^15}{"Prop. cap.":^15}{"Capacidade":^15}{"Respeita lim.?":^15}\n')
    f.write(f'{"K":^5}{"M":^5}{"(PU)":^15}{"%":^15}{"(PU)":^15}{"%":^15}{"(PU)":^15}{"SIM / NÃO / ALE":^15}\n')

    f.write(f'{100*"-"}\n')

    ncircuitos = len(dcircuitos)
    linhasAlerta = []
    for b in range(ncircuitos):
        f.write(f'{dcircuitos[b]["BDE"]:^5}')
        f.write(f'{dcircuitos[b]["BPARA"]:^5}')

        cap = dcircuitos[b]["CAP(PU)"]

        skm = f"{fluxoSkm[b][0]:.4f}"
        f.write(f"{skm:^15}")

        pskm = fluxoSkm[b][0] / cap
        stringpskm = f'{(pskm*100):.2f}'
        f.write(f"{stringpskm:^15}")

        smk = f"{fluxoSmk[b][0]:.4f}"
        f.write(f"{smk:^15}")
        
        psmk = fluxoSmk[b][0] / cap
        stringpsmk = f'{(psmk*100):.2f}'
        f.write(f"{stringpsmk:^15}")

        f.write(f'{dcircuitos[b]["CAP(PU)"]:^15}')
        alert = "SIM" 
        if ( pskm > 0.95 ) or ( psmk > 0.95 ) :
            alert = "ALE"
        if ( pskm > 1 ) or ( psmk > 1 ) :
            alert = "NÃO"
        if alert in ["NÃO", "ALE"] : linhasAlerta.append((dcircuitos[b]["BDE"], dcircuitos[b]["BPARA"]))
        f.write(f"{alert:^15}")
        f.write("\n")

    f.write(f'{100*"-"}\n')

    f.write("\n")
    if linhasAlerta : 
        f.write(f"Atenção para a(s) linhas(s) {linhasAlerta}\n") 
    else:
        f.write(f"Linhas operando dentro dos limites de potência\n") 
    f.write("\n")

    f.write(f'{100*"-"}\n')



def relatorio(output: str, sis: dict):

    # Organizando as informacoes do sistema
    dbarras = sis.dbarras
    dcircuitos = sis.dcircuitos
    pG = sis.pG
    qG = sis.qG
    sG = sis.sG
    perdasP = sis.perdasP
    perdasQ = sis.perdasQ
    perdasAtivasTotais = sis.perdasAtivasTotais
    perdasReativasTotais = sis.perdasReativasTotais
    angulos = sis.angulos
    angDeg = sis.angulosGrau
    tensoes = sis.tensoes
    basePu = sis.base
    pCalc = sis.pCalc
    qCalc = sis.qCalc
    fluxoPkm = sis.fluxoPkm
    fluxoPmk = sis.fluxoPmk
    fluxoQkm = sis.fluxoQkm
    fluxoQmk = sis.fluxoQmk
    fluxoSkm = sis.fluxoSkm
    fluxoSmk = sis.fluxoSmk
    nbarras = sis.nbarras
    ncircuitos = sis.ncircuitos

    with open(output, 'w') as f:
        cabecalho(f)

        f.write(f'{100*"="}\n')

        tabelaPotencias(f, sis, False) 
        tabelaPotencias(f, sis, True) 

        f.write(f'{100*"="}\n')

        analisePotenciaGeradores(f, dbarras, pG) 

        f.write(f'{100*"="}\n')

        relatorioCircuitos(f, sis, False)

        f.write(f'{100*"-"}\n')

        relatorioCircuitos(f, sis, True)

        f.write(f'{100*"="}\n')

        analiseCapacidadeCircuitos(f, dcircuitos, fluxoSkm, fluxoSmk)

        f.close()
        print(f"Dados gravados em {output}")

def exportarSistema(output: str, sis: sistema.Sistema):

    with open(output, 'w') as f:
        f.write(f'DBAR\n')
        f.write(f'{100*"="}\n')
        cab = '  BARRA       PD(PU)    QD(PU)    Bsh(PU)    TIPO    Vesp(PU)   Oesp()   PGesp(PU) Cus($/MW) CGmin(PU) CGmax(PU)'
        f.write(f'{cab}\n')
        for b in sis.dbarras:
            f.write(f'{b["BARRA"]:^10}')
            f.write(f'{b["PD(PU)"]:^10}')
            f.write(f'{b["QD(PU)"]:^10}')
            f.write(f'{b["Bsh(PU)"]:^10}')
            f.write(f'{b["TIPO"]:^10}')
            v = f'{b["Vesp(PU)"]:.5}'
            f.write(f'{v:^10}')
            f.write(f'{b["Oesp"]:^10}')
            f.write(f'{b["PGesp(PU)"]:^10}')
            f.write(f'{b["Cus"]:^10}')
            f.write(f'{b["CGmin(PU)"]:^10}')
            f.write(f'{b["CGmax(PU)"]:^10}')
            f.write('\n')
        f.write(f'{100*"="}\n')
        f.write(f'{4*"#"}\n')

        f.write(f'DCIR\n')
        f.write(f'{100*"="}\n')
        cab = '   BDE      BPARA     NCIR      RES(PU)  REAT(PU)  SUCsh(PU) TAP(PU)  DEF(GRAUS)   L/D     CAP(PU)'
        f.write(f'{cab}\n')
        for b in sis.dcircuitos:
            f.write(f'{b["BDE"]:^10}')
            f.write(f'{b["BPARA"]:^10}')
            f.write(f'{b["NCIR"]:^10}')
            f.write(f'{b["RES(PU)"]:^10}')
            f.write(f'{b["REAT(PU)"]:^10}')
            f.write(f'{b["SUCsh(PU)"]:^10}')
            a = f'{b["TAP(PU)"]:.5}'
            f.write(f'{a:^10}')
            d = f'{b["DEF(GRAUS)"]:.5}'
            f.write(f'{d:^10}')
            f.write(f'{b["LIG(L)DESL(D)"]:^10}')
            f.write(f'{b["CAP(PU)"]:^10}')
            f.write('\n')
        f.write(f'{100*"="}\n')
        f.write(f'{4*"#"}\n')

        f.close()
        print(f"Dados gravados em {output}")
    # FIm WITH
# FIM exportar sist







