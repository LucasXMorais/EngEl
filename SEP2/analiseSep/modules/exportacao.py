# 04/04/24 - Lucas Xavier de Morais 
# Exportando os dados do sistema
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
from datetime import datetime

def exportarSistema(output: str, sistema: dict) -> None:

    # Organizando as informacoes do sistema
    dbarras = sistema['BARRAS']
    dcircuitos = sistema['CIRCUITOS']
    pG = sistema['PG']
    qG = sistema['QG']
    sG = sistema['SG']
    perdasP = sistema['perdasP']
    perdasQ = sistema['perdasQ']
    perdasAtivasTotais = sistema['PerdasPTotais']
    perdasReativasTotais = sistema['PerdasQTotais']
    angulos = sistema['angulos']
    angDeg = sistema['angulosDeg']
    tensoes = sistema['tensoes']
    basePu = sistema['BASE']
    pCalc = sistema['pCalc']
    qCalc = sistema['qCalc']
    fluxoPkm = sistema['fluxoPkm']
    fluxoPmk = sistema['fluxoPmk']
    fluxoQkm = sistema['fluxoQkm']
    fluxoQmk = sistema['fluxoQmk']
    fluxoSkm = sistema['fluxoSkm']
    fluxoSmk = sistema['fluxoSmk']

    nbarras = len(dbarras)
    ncircuitos = len(dcircuitos)

    with open(output, 'w') as f:
        # Cabecalho
        f.write(f'{100*"="}\n')
        now: datetime = datetime.now()
        now = f'{now:%c}'
        f.write(f'{now:^100}\n')
        f.write(f'{100*"="}\n\n')
        f.write(f'{"Universidade Federal de São João Del Rei":^100}\n')
        f.write(f'{"Análise de Sistemas Elétricos de Potência II":^100}\n')
        f.write(f'{100*"-"}\n')
        f.write(f'{"Relatório do Sistema do Estudo de Caso 1":^100}\n\n')
        f.write(f'{100*"="}\n')
        f.write(f'{"Autores:":^25} {"Cássia R. A. Freitas":^25} {"Gabriel L. de Sousa":^25} {"Lucas X. Morais":^25}\n')
        f.write(f'{"Matrícula:":^25} {"190900048":^25} {"180950030":^25} {"190950011":^25}\n')
        f.write(f'{100*"="}\n\n')

        f.write(f'{100*"-"}\n')

        f.write(f'{"Relatório das potências nas barras":^100}\n')

        f.write(f'{100*"-"}\n')

        f.write(f'{"BARRA":^10}{"TENSAO":^10}{"THETA":^10}{"PI":^10}{"QI":^10}{"PG":^10}{"QG":^10}{"SG":^10}{"PD":^10}{"QD":^10}\n')
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

        perPTotal = f"{perdasAtivasTotais*basePu:.4f} MW"
        perQTotal = f"{perdasReativasTotais*basePu:.4f} MVAr"
        f.write(f'{"Total de Perdas":20}{("Perdas Ativas = "+perPTotal):^40}{"Perdas Reativas = "+perQTotal:^40}\n')

        f.write(f'{100*"-"}\n')

        f.write(f'{"Relatório das potências nas barras em PU":^100}\n')

        f.write(f'{100*"-"}\n')

        f.write(f'{"BARRA":^10}{"TENSAO":^10}{"THETA":^10}{"PI":^10}{"QI":^10}{"PG":^10}{"QG":^10}{"SG":^10}{"PD":^10}{"QD":^10}\n')
        f.write(f'{"#":^10}{"(PU)":^10}{"(DEG)":^10}{"["+(31*"_"):32}{" (PU) ":^6}{(31*"_")+"]":32}\n')

        f.write(f'{100*"-"}\n')

        for b in range(nbarras):
            f.write(f'{dbarras[b]["BARRA"]:^9}')
            v = f"{tensoes[b]:.5f}"
            f.write(f"{v:>10}")
            a = f"{angulos[b]:.5f}"
            f.write(f"{a:>10}")
            pi = f"{pCalc[b]:.4f}"
            f.write(f"{pi:>10}")
            qi = f"{qCalc[b]:.4f}"
            f.write(f"{qi:>10}")
            pg = f"{pG[b][0]:.4f}"
            f.write(f"{pg:>10}")
            qg = f"{qG[b][0]:.4f}"
            f.write(f"{qg:>10}")
            sg = f"{sG[b][0]:.4f}"
            f.write(f"{sg:>10}")
            pd = f'{dbarras[b]["PD(PU)"]:.4f}'
            f.write(f"{pd:>10}")
            qd = f'{dbarras[b]["QD(PU)"]:.4f}'
            f.write(f"{qd:>10}")
            f.write("\n")
        f.write(f'{100*"-"}\n')
        f.write(f'{"Total":50}')
        sum = 0
        for value in pG : sum += (value[0])
        sum = f"{sum:.4f}"
        f.write(f"{sum:^10}")
        sum = 0
        for value in qG : sum += (value[0])
        sum = f"{sum:.4f}"
        f.write(f"{sum:^10}")
        sum = 0
        for value in sG : sum += (value[0])
        sum = f"{sum:.4f}"
        f.write(f"{sum:^10}")
        sum = 0
        for value in dbarras : sum += (value["PD(PU)"])
        sum = f"{sum:.4f}"
        f.write(f"{sum:^10}")
        sum = 0
        for value in dbarras : sum += (value["PD(PU)"])
        sum = f"{sum:.4f}"
        f.write(f"{sum:^10}")
        f.write("\n")

        f.write(f'{100*"-"}\n')

        perPTotal = f"{perdasAtivasTotais:.4f} pu"
        perQTotal = f"{perdasReativasTotais:.4f} pu"
        f.write(f'{"Total de Perdas":20}{("Perdas Ativas = "+perPTotal):^40}{"Perdas Reativas = "+perQTotal:^40}\n')

        f.write(f'{100*"-"}\n')
        f.write(f'{100*"="}\n')
        f.write(f'{100*"-"}\n')

        f.write(f'{"Análise das potências de geração":^100}\n')

        f.write(f'{100*"-"}\n')

        f.write(f'{"BARRA":^12}{"PG":^22}{"Carga Máxima":^22}{"Carga Mínima":^22}{"Carga aceitável?":^22}\n')
        f.write(f'{"#":^12}{"(PU)":^22}{"(PU)":^22}{"(PU)":^22}{"SIM / NÃO":^22}\n')

        f.write(f'{100*"-"}\n')

        barrasAlerta = []
        for b in range(nbarras):
            if dbarras[b]["TIPO"] == "PQ": continue
            f.write(f'{dbarras[b]["BARRA"]:^12}')
            pg = f"{pG[b][0]:.4f}"
            f.write(f"{pg:^22}")
            cgmax = f'{dbarras[b]["CGmax(PU)"]:.2f}'
            f.write(f"{cgmax:^22}")
            cgmin = f'{dbarras[b]["CGmin(PU)"]:.2f}'
            f.write(f"{cgmin:^22}")
            aceit = "SIM" if ( (dbarras[b]["CGmax(PU)"] == 0) or ( np.abs(pG[b][0]) > np.abs(dbarras[b]["CGmin(PU)"]) ) and ( np.abs(pG[b][0]) < np.abs(dbarras[b]["CGmax(PU)"]) ) ) else "NÃO"
            if aceit == "NÃO" : barrasAlerta.append(dbarras[b]["BARRA"])
            f.write(f"{aceit:^22}")
            f.write("\n")

        f.write("\n")
        if barrasAlerta : 
            f.write(f"Atenção para a(s) barra(s) {barrasAlerta}\n") 
        else:
            f.write(f"Barras operando dentro dos limites de potência\n") 
        f.write("\n")

        f.write(f'{100*"-"}\n')
        f.write(f'{100*"="}\n')
        f.write(f'{100*"-"}\n')

        f.write(f'{"Relatório das potências nos circuitos":^100}\n')

        f.write(f'{100*"-"}\n')

        f.write(f'{"BARRA":^10}{"PKM":^15}{"QKM":^15}{"SKM":^15}{"PMK":^15}{"QMK":^15}{"SMK":^15}\n')
        f.write(f'{"DE":^5}{"PARA":^5}{"MW":^15}{"MVAr":^15}{"MVA":^15}{"MW":^15}{"MVAr":^15}{"MVA":^15}\n')

        f.write(f'{100*"-"}\n')

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

        f.write(f'{"Relatório das potências nos circuitos km em PU":^100}\n')

        f.write(f'{100*"-"}\n')

        f.write(f'{"BARRA":^10}{"PKM":^18}{"QKM":^18}{"SKM":^18}{"Capacidade":^18}{"Pode operar?":^18}\n')
        f.write(f'{"DE":^5}{"PARA":^5}{"["+(32*"_"):33}{" (PU) ":^6}{(32*"_")+"]":33}{"SIM / NÃO":^18}\n')

        f.write(f'{100*"-"}\n')

        linhasAlerta = []
        for b in range(ncircuitos):
            f.write(f'{dcircuitos[b]["BDE"]:^5}')
            f.write(f'{dcircuitos[b]["BPARA"]:^5}')
            pkm = f"{fluxoPkm[b][0]:.4f}"
            f.write(f"{pkm:^18}")
            qkm = f"{fluxoQkm[b][0]:.4f}"
            f.write(f"{qkm:^18}")
            skm = f"{fluxoSkm[b][0]:.4f}"
            f.write(f"{skm:^18}")
            f.write(f'{dcircuitos[b]["CAP(PU)"]:^18}')
            podeOp = "SIM" if ( (dcircuitos[b]["CAP(PU)"] - fluxoSkm[b][0]) > 0) else "NÃO"
            if podeOp == "NÃO" : linhasAlerta.append((dcircuitos[b]["BDE"], dcircuitos[b]["BPARA"]))
            f.write(f"{podeOp:^18}")
            f.write("\n")

        f.write(f'{100*"-"}\n')

        f.write(f'{"Relatório das potências nos circuitos mk em PU":^100}\n')

        f.write(f'{100*"-"}\n')

        f.write(f'{"BARRA":^10}{"PMK":^18}{"QMK":^18}{"SMK":^18}{"Capacidade":^18}{"Pode operar?":^18}\n')
        f.write(f'{"DE":^5}{"PARA":^5}{"["+(32*"_"):33}{"(PU)":^6}{(32*"_")+"]":33}{"SIM/NÃO":^18}\n')

        f.write(f'{100*"-"}\n')

        for b in range(ncircuitos):
            f.write(f'{dcircuitos[b]["BPARA"]:^5}')
            f.write(f'{dcircuitos[b]["BDE"]:^5}')
            pmk = f"{fluxoPmk[b][0]:.4f}"
            f.write(f"{pmk:^18}")
            qmk = f"{fluxoQmk[b][0]:.4f}"
            f.write(f"{qmk:^18}")
            smk = f"{fluxoSmk[b][0]:.4f}"
            f.write(f"{smk:^18}")
            f.write(f'{dcircuitos[b]["CAP(PU)"]:^18}')
            podeOp = "SIM" if ( (dcircuitos[b]["CAP(PU)"] - fluxoSmk[b][0]) > 0) else "NÃO"
            if podeOp == "NÃO" : 
                circuito = (dcircuitos[b]["BDE"], dcircuitos[b]["BPARA"])
                if circuito not in linhasAlerta: linhasAlerta.append(circuito)
            f.write(f"{podeOp:^18}")
            f.write("\n")

        f.write("\n")
        if linhasAlerta : 
            f.write(f"Atenção para a(s) linhas(s) {linhasAlerta}\n") 
        else:
            f.write(f"Linhas operando dentro dos limites de potência\n") 
        f.write("\n")

        f.close()
        print(f"Dados gravados em {output}")

        return None






