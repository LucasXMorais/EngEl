# 04/04/24 - Lucas Xavier de Morais 
# Exportando os dados do sistema
# SEP II - Engenharia Elétrica (UFSJ)
from datetime import datetime

def exportarSistema(fileOutput, sistema) -> None:

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

    with open(fileOutput, 'w') as f:
        # Cabecalho
        f.write(f'{100*'='}\n')
        now: datetime = datetime.now()
        now = f'{now:%c}'
        f.write(f'{now:^100}\n')
        f.write(f'{100*'='}\n\n')
        f.write(f'{'Relatório do Sistema em Questão':^100}\n\n')
        f.write(f'{100*'='}\n')
        f.write(f'{'Autores:':^25} {'Cássia':^25} {'Gabriel':^25} {'Lucas X. Morais':^25}\n')
        f.write(f'{'Matrícula:':^25} {'Cássia':^25} {'Gabriel':^25} {'190950011':^25}\n')
        f.write(f'{100*'='}\n\n')

        f.write(f'{100*'-'}\n')

        f.write(f'{'Relatório das potências nas barras':^100}\n')

        f.write(f'{100*'-'}\n')

        f.write(f'{'BARRA':^10}{'TENSAO':^10}{'THETA':^10}{'PI':^10}{'QI':^10}{'PG':^10}{'QG':^10}{'SG':^10}{'PD':^10}{'QD':^10}\n')
        f.write(f'{'#':^10}{'(PU)':^10}{'(DEG)':^10}{'MW':^10}{'MVAr':^10}{'MW':^10}{'MVAr':^10}{'MVA':^10}{'MW':^10}{'MVAr':^10}\n')

        f.write(f'{100*'-'}\n')

        nbarras = len(dbarras)
        for b in range(nbarras):
            f.write(f'{dbarras[b]['BARRA']:^10}')
            v = f'{tensoes[b]:.6f}'
            f.write(f'{v:^10}')
            a = f'{angulos[b]:.6f}'
            f.write(f'{a:^10}')
            pi = f'{pCalc[b]*basePu:.4f}'
            f.write(f'{pi:^10}')
            qi = f'{qCalc[b]*basePu:.4f}'
            f.write(f'{qi:^10}')
            pg = f'{pG[b][0]*basePu:.4f}'
            f.write(f'{pg:^10}')
            qg = f'{qG[b][0]*basePu:.4f}'
            f.write(f'{qg:^10}')
            sg = f'{sG[b][0]*basePu:.4f}'
            f.write(f'{sg:^10}')
            pd = f'{dbarras[b]['PD(PU)']*basePu:.4f}'
            f.write(f'{pd:^10}')
            qd = f'{dbarras[b]['QD(PU)']*basePu:.4f}'
            f.write(f'{qd:^10}')
            f.write('\n')
        f.write(f'{100*'-'}\n')
        f.write(f'{'Total':50}')
        sum = 0
        for value in pG : sum += (value[0]*basePu)
        sum = f'{sum:.2f}'
        f.write(f'{sum:^10}')
        sum = 0
        for value in qG : sum += (value[0]*basePu)
        sum = f'{sum:.2f}'
        f.write(f'{sum:^10}')
        sum = 0
        for value in sG : sum += (value[0]*basePu)
        sum = f'{sum:.2f}'
        f.write(f'{sum:^10}')
        sum = 0
        for value in dbarras : sum += (value['PD(PU)']*basePu)
        sum = f'{sum:.2f}'
        f.write(f'{sum:^10}')
        sum = 0
        for value in dbarras : sum += (value['PD(PU)']*basePu)
        sum = f'{sum:.2f}'
        f.write(f'{sum:^10}')
        f.write('\n')

        f.write(f'{100*'-'}\n')

        perPTotal = f'{perdasAtivasTotais*basePu:.4f} MW'
        perQTotal = f'{perdasReativasTotais*basePu:.4f} MVAr'
        f.write(f'{'Total de Perdas':20}{('Perdas Ativas = '+perPTotal):^40}{'Perdas Reativas = '+perQTotal:^40}\n')

        f.write(f'{100*'-'}\n')

        f.write(f'{'Relatório das potências nas barras em PU':^100}\n')

        f.write(f'{100*'-'}\n')

        f.write(f'{'BARRA':^10}{'TENSAO':^10}{'THETA':^10}{'PI':^10}{'QI':^10}{'PG':^10}{'QG':^10}{'SG':^10}{'PD':^10}{'QD':^10}\n')
        f.write(f'{'#':^10}{'(PU)':^10}{'(DEG)':^10}{'['+(31*'_'):32}{' (PU) ':^6}{(31*'_')+']':32}\n')

        f.write(f'{100*'-'}\n')

        nbarras = len(dbarras)
        for b in range(nbarras):
            f.write(f'{dbarras[b]['BARRA']:^10}')
            v = f'{tensoes[b]:.6f}'
            f.write(f'{v:^10}')
            a = f'{angulos[b]:.6f}'
            f.write(f'{a:^10}')
            pi = f'{pCalc[b]:.4f}'
            f.write(f'{pi:^10}')
            qi = f'{qCalc[b]:.4f}'
            f.write(f'{qi:^10}')
            pg = f'{pG[b][0]:.4f}'
            f.write(f'{pg:^10}')
            qg = f'{qG[b][0]:.4f}'
            f.write(f'{qg:^10}')
            sg = f'{sG[b][0]:.4f}'
            f.write(f'{sg:^10}')
            pd = f'{dbarras[b]['PD(PU)']:.4f}'
            f.write(f'{pd:^10}')
            qd = f'{dbarras[b]['QD(PU)']:.4f}'
            f.write(f'{qd:^10}')
            f.write('\n')
        f.write(f'{100*'-'}\n')
        f.write(f'{'Total':50}')
        sum = 0
        for value in pG : sum += (value[0])
        sum = f'{sum:.2f}'
        f.write(f'{sum:^10}')
        sum = 0
        for value in qG : sum += (value[0])
        sum = f'{sum:.2f}'
        f.write(f'{sum:^10}')
        sum = 0
        for value in sG : sum += (value[0])
        sum = f'{sum:.2f}'
        f.write(f'{sum:^10}')
        sum = 0
        for value in dbarras : sum += (value['PD(PU)'])
        sum = f'{sum:.2f}'
        f.write(f'{sum:^10}')
        sum = 0
        for value in dbarras : sum += (value['PD(PU)'])
        sum = f'{sum:.2f}'
        f.write(f'{sum:^10}')
        f.write('\n')

        f.write(f'{100*'-'}\n')

        perPTotal = f'{perdasAtivasTotais:.4f} pu'
        perQTotal = f'{perdasReativasTotais:.4f} pu'
        f.write(f'{'Total de Perdas':20}{('Perdas Ativas = '+perPTotal):^40}{'Perdas Reativas = '+perQTotal:^40}\n')

        f.write(f'{100*'-'}\n')
        f.write(f'{100*'='}\n')
        f.write(f'{100*'-'}\n')

        f.write(f'{'Análise dos fluxos nas barras':^100}\n')

        f.write(f'{100*'-'}\n')

        f.write(f'{'BARRA':^13}{'PG':^29}{'Carga Máxima':^29}{'Carga Mínima':^29}\n')
        f.write(f'{'#':^13}{'(PU)':^29}{'(PU)':^29}{'(PU)':^29}\n')

        f.write(f'{100*'-'}\n')

        for b in range(nbarras):
            f.write(f'{dbarras[b]['BARRA']:^13}')
            pg = f'{pG[b][0]:.8f}'
            f.write(f'{pg:^29}')
            cgmax = f'{dbarras[b]['CGmax(PU)']:.8f}'
            f.write(f'{cgmax:^29}')
            cgmin = f'{dbarras[b]['CGmin(PU)']:.8f}'
            f.write(f'{cgmin:^29}')
            f.write('\n')

        f.write(f'{100*'-'}\n')
        f.write(f'{100*'='}\n')
        f.write(f'{100*'-'}\n')

        f.write(f'{'Relatório das potências nos circuitos':^100}\n')

        f.write(f'{100*'-'}\n')

        f.write(f'{'BARRA':^10}{'PKM':^15}{'QKM':^15}{'SKM':^15}{'PMK':^15}{'QMK':^15}{'SMK':^15}\n')
        f.write(f'{'DE':^5}{'PARA':^5}{'MW':^15}{'MVAr':^15}{'MVA':^15}{'MW':^15}{'MVAr':^15}{'MVA':^15}\n')

        f.write(f'{100*'-'}\n')

        for b in range(nbarras):
            f.write(f'{dcircuitos[b]['BDE']:^5}')
            f.write(f'{dcircuitos[b]['BPARA']:^5}')
            pkm = f'{fluxoPkm[b][0]*basePu:.6f}'
            f.write(f'{pkm:^15}')
            qkm = f'{fluxoQkm[b][0]*basePu:.6f}'
            f.write(f'{qkm:^15}')
            skm = f'{fluxoSkm[b][0]*basePu:.6f}'
            f.write(f'{skm:^15}')
            pmk = f'{fluxoPmk[b][0]*basePu:.6f}'
            f.write(f'{pmk:^15}')
            qmk = f'{fluxoQmk[b][0]*basePu:.6f}'
            f.write(f'{qmk:^15}')
            smk = f'{fluxoSmk[b][0]*basePu:.6f}'
            f.write(f'{smk:^15}')
            f.write('\n')

        f.write(f'{100*'-'}\n')

        f.write(f'{'Relatório das potências nos circuitos em PU':^100}\n')

        f.write(f'{100*'-'}\n')

        f.write(f'{'BARRA':^10}{'PKM':^15}{'QKM':^15}{'SKM':^15}{'PMK':^15}{'QMK':^15}{'SMK':^15}\n')
        f.write(f'{'DE':^5}{'PARA':^5}{'['+(41*'_'):42}{' (PU) ':^6}{(41*'_')+']':42}\n')

        f.write(f'{100*'-'}\n')

        for b in range(nbarras):
            f.write(f'{dcircuitos[b]['BDE']:^5}')
            f.write(f'{dcircuitos[b]['BPARA']:^5}')
            pkm = f'{fluxoPkm[b][0]*basePu:.6f}'
            f.write(f'{pkm:^15}')
            qkm = f'{fluxoQkm[b][0]*basePu:.6f}'
            f.write(f'{qkm:^15}')
            skm = f'{fluxoSkm[b][0]*basePu:.6f}'
            f.write(f'{skm:^15}')
            pmk = f'{fluxoPmk[b][0]*basePu:.6f}'
            f.write(f'{pmk:^15}')
            qmk = f'{fluxoQmk[b][0]*basePu:.6f}'
            f.write(f'{qmk:^15}')
            smk = f'{fluxoSmk[b][0]*basePu:.6f}'
            f.write(f'{smk:^15}')
            f.write('\n')

        f.close()
        print(f'Dados gravados em {fileOutput}')







