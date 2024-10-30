# Lucas Xavier de Morais 
# 15/04/24 - Programa para gravar dados formatados para Latex
from modules import sistema

def tabela(f, cabecalho: int, dados: list, caption: str, numero: int):

    numCol = len(dados[0])

    f.write('\\begin{table}\n')
    f.write('\\centering\n')
    tabularEnv = '{' + (' c '*numCol) + '}\n' 
    f.write('\\begin{tabular}'+tabularEnv)
    f.write(' \\hline\n')
    count = 1
    for line in dados:
        f.write(' ')
        j = 1
        for l in line:
            string = f'{l} & '
            if j == len(line): string = f'{l} '
            f.write(string)
            j += 1
        f.write("\\\\")
        f.write('\n')
        if count >= cabecalho : f.write(' \\hline\n')
        count += 1
    f.write('\\end{tabular}\n')
    captionString = f'{caption}'
    f.write('\caption{' + captionString + '}\n')
    tableNum = f'table:{numero}'
    f.write('\label{' + tableNum + '}\n')
    f.write('\\end{table}\n')

def contingenciasLatex(output: str, ranking: list):
    with open(output, 'w') as f:
        dados = []
        cabecalho = ['\#', 'Contingência', 'Índice de Sobrecarga', 'Circuitos em sobrecarga']
        dados.append(cabecalho)
        c = 1
        for r in ranking:
            contingencia = ','.join([str(h) for h in r[0]])
            indice = f'{r[1]:.6f}'.replace('.',',')
            sobrecargas = ','.join([str(h) for h in r[2]])
            dados.append([ str(c), contingencia, indice, sobrecargas ])
            c += 1
        tabela(f, 1, dados, 'Tabela de contingências', 1)


def exportarLatex(latexFile: str, sistema: sistema.Sistema, correcoes: list):

    with open(latexFile, 'w') as f:

        # Criando tabelas de angulos e tensoes
        dados = []
        cabecalho = ['Barra', 'Ângulo', 'Tensão (PU)', 'Base de tensão (kV)']
        dados.append(cabecalho)
        unidades = [' ', 'grau', 'pu']
        dados.append(unidades)
        for k, a, t in zip(sistema.dbarras, sistema.angulosGrau, sistema.tensoes):
            dados.append([k['BARRA'], f'{a:.4f}'.replace('.',','), f'{t:.4f}'.replace('.',','), k['VBase']])
        tabela(f, 2, dados, 'Tabela de tensão e defasagem por barra', 1)

        f.write('\n\n')

        # Criando tabela de potência de geração 
        dados = []
        cabecalho = ['Barra', 'PG(PU)', 'CGmax(PU)']
        dados.append(cabecalho)
        unidades = [' ', 'PU', 'PU']
        dados.append(unidades)
        for k, p, q, s in zip(sistema.dbarras, sistema.pG, sistema.qG, sistema.sG):
            dados.append( [ k['BARRA'], f'{p[0]:.2f}', f'{k["CGmax(PU)"]:.2f}' ] )
        tabela(f, 2, dados, 'Potência de geração', 2)

        f.write('\n\n')

        # Juntanod as duas numa só
        dados = []
        cabecalho = ['Barra', 'Ângulo', 'Tensão', 'PG', 'QG', 'SG']
        dados.append(cabecalho)
        unidades = [' ', 'grau', 'pu', 'MW', 'Mvar', 'MVA']
        dados.append(unidades)
        for k, a, t, p, q, s in zip(sistema.dbarras, sistema.angulosGrau, sistema.tensoes, sistema.pG, sistema.qG, sistema.sG):
            dados.append( [ k['BARRA'], f'{a:.4f}'.replace('.',','), f'{t:.4f}'.replace('.',','), f'{p[0]*sistema.base:.4f}'.replace('.',','), f'{q[0]*sistema.base:.4f}'.replace('.',','), f'{s[0]*sistema.base:.4f}'.replace('.',',') ] )
        tabela(f, 2, dados, 'Ângulos, Tensões e Potências de geração por barra', 3)

        f.write('\n\n')

        # Tabela de correções por iteração
        dados = []
        cabecalho = ['Iteração', 'Correção', 'Valor atualizado']
        dados.append(cabecalho)
        for i, c in zip(range(len(correcoes)), correcoes):
            dados.append( [ i, f'{c[0]:.6f}', f'{c[1]:.6f}'] )
        tabela(f, 1, dados, 'Correções aplicadas', 4)

        f.write('\n\n')

        # Criando tabela de fluox de potência ativa
        dados = []
        cabecalho = ['NCIR', 'BDE', 'BPARA', 'PKM(kVA)', 'PMK(kVA)', 'Cap. Máx.(kVA)', '\% de Sobrecarga']
        dados.append(cabecalho)
        for c, k, m in zip(sistema.dcircuitos, sistema.fluxoPkm, sistema.fluxoPmk):
            violacao = 0
            capacidade = c['CAP(PU)']
            maior = k[0]
            if m[0] > maior: maior = m[0]
            if maior >= capacidade:
                violacao = ((maior - capacidade) / capacidade) * 100
            dados.append( [ c['NCIR'], c['BDE'], c['BPARA'], f'{k[0]*sistema.base:.2f}'.replace('.',','), f'{m[0]*sistema.base:.2f}'.replace('.',','), f'{c["CAP(PU)"]*sistema.base:.2f}'.replace('.',','), f'{violacao:.2f}\%'.replace('.',',') ])
        tabela(f, 1, dados, 'Fluxos de potência', 5)

        f.write('\n\n')

        # Criando tabela de fluox de potência ativa com % de uso
        dados = []
        cabecalho = ['NCIR', 'BDE', 'BPARA', 'PKM(kVA)', 'PMK(kVA)', 'Cap. Máx.(kVA)', '\% de uso']
        dados.append(cabecalho)
        for c, k, m in zip(sistema.dcircuitos, sistema.fluxoPkm, sistema.fluxoPmk):
            puso = 0
            capacidade = c['CAP(PU)']
            maior = k[0]
            if m[0] > maior: maior = m[0]
            puso = (maior / capacidade) * 100
            dados.append( [ c['NCIR'], c['BDE'], c['BPARA'], f'{k[0]*sistema.base:.2f}'.replace('.',','), f'{m[0]*sistema.base:.2f}'.replace('.',','), f'{c["CAP(PU)"]*sistema.base:.2f}'.replace('.',','), f'{puso:.2f}\%'.replace('.',',') ])
        tabela(f, 1, dados, 'Fluxos de potência', 5)

        f.write('\n\n')

        # Criando tabela de fluox de potência ativa
        dados = []
        cabecalho = ['NCIR', 'BDE', 'BPARA', 'SKM(kVA)', 'SMK(kVA)', 'Cap. Máx.(kVA)', '\% de Sobrecarga']
        dados.append(cabecalho)
        for c, k, m in zip(sistema.dcircuitos, sistema.fluxoSkm, sistema.fluxoSmk):
            violacao = 0
            capacidade = c['CAP(PU)']
            maior = k[0]
            if m[0] > maior: maior = m[0]
            if maior >= capacidade:
                violacao = ((maior - capacidade) / capacidade) * 100
            dados.append( [ c['NCIR'], c['BDE'], c['BPARA'], f'{k[0]*sistema.base:.2f}'.replace('.',','), f'{m[0]*sistema.base:.2f}'.replace('.',','), f'{c["CAP(PU)"]*sistema.base:.2f}'.replace('.',','), f'{violacao:.2f}\%'.replace('.',',') ])
        tabela(f, 1, dados, 'Fluxos de potência', 5)

        f.write('\n\n')

        # Criando tabela de fluox de potência ativa com % de uso
        dados = []
        cabecalho = ['NCIR', 'BDE', 'BPARA', 'SKM(kVA)', 'SMK(kVA)', 'Cap. Máx.(kVA)', '\% de uso']
        dados.append(cabecalho)
        for c, k, m in zip(sistema.dcircuitos, sistema.fluxoSkm, sistema.fluxoSmk):
            puso = 0
            capacidade = c['CAP(PU)']
            maior = k[0]
            if m[0] > maior: maior = m[0]
            puso = (maior / capacidade) * 100
            dados.append( [ c['NCIR'], c['BDE'], c['BPARA'], f'{k[0]*sistema.base:.2f}'.replace('.',','), f'{m[0]*sistema.base:.2f}'.replace('.',','), f'{c["CAP(PU)"]*sistema.base:.2f}'.replace('.',','), f'{puso:.2f}\%'.replace('.',',') ])
        tabela(f, 1, dados, 'Fluxos de potência', 5)

        f.write('\n\n')

def optimization(output: str, tables: dict, sis):
    with open(output, 'w') as f:

        resultado = tables['resultado']
        # Inequacoes
        # Printando resultados
        dados = []
        cabecalho = ['NCIRC', 'DE', 'PARA', 'Resultado marginal', 'Lâmbda']
        dados.append(cabecalho)
        circ = 0
        i = 0
        for r, m in zip(resultado.ineqlin.residual, resultado.ineqlin.marginals):
            i += 1
            ncir = sis.dcircuitos[circ]['NCIR']
            bde = sis.dcircuitos[circ]['BDE']
            bpara = sis.dcircuitos[circ]['BPARA']
            dados.append([ ncir, bde, bpara, f'{r:.4f}'.replace('.',','), f'{m:.4f}'.replace('.',',') ])
            if i == 2:
                circ+=1
                i=0
        tabela(f, 1, dados, 'Resultados inequacoes', 1)

        # Printando resultados sem marginal
        dados = []
        cabecalho = ['NCIRC', 'DE', 'PARA', 'Lâmbda']
        dados.append(cabecalho)
        circ = 0
        i = 0
        for m in resultado.ineqlin.marginals:
            i += 1
            ncir = sis.dcircuitos[circ]['NCIR']
            bde = sis.dcircuitos[circ]['BDE']
            bpara = sis.dcircuitos[circ]['BPARA']
            dados.append([ ncir, bde, bpara, f'{m:.4f}'.replace('.',',') ])
            if i == 2:
                circ+=1
                i=0
        tabela(f, 1, dados, 'Resultados inequacoes', 1)

        # Igualdades
        # Printando resultados
        dados = []
        cabecalho = ['GER. BARRA' , 'Resultado marginal', 'Lâmbda']
        dados.append(cabecalho)
        for b, r, m in zip(sis.dbarras, resultado.eqlin.residual, resultado.eqlin.marginals):
            barra = b['BARRA']
            dados.append([ barra, f'{r:.4f}'.replace('.',','), f'{m:.4f}'.replace('.',',') ])
        tabela(f, 1, dados, 'Resultados igualdades', 1)

        # Printando resultados sem marginal
        dados = []
        cabecalho = ['GER. BARRA' , 'Lâmbda']
        dados.append(cabecalho)
        for b, m in zip(sis.dbarras, resultado.eqlin.marginals):
            barra = b['BARRA']
            dados.append([ barra, f'{m:.4f}'.replace('.',',') ])
        tabela(f, 1, dados, 'Resultados igualdades', 1)

        # Limites
        # Printando resultados
        barras_angulos = [b['BARRA'] for b in sis.dbarras if b['TIPO'] != 'SW']
        barras_despachos = [b['BARRA'] for b in sis.dbarras if b['PGesp(PU)'] != 0 or b['TIPO'] == 'SW']
        barras_cortes = [b['BARRA'] for b in sis.dbarras if b['PD(PU)'] != 0]
        barraSW = 0
        for bar in sis.dbarras:
            if bar["TIPO"] == 'SW': 
                barraSW = bar["BARRA"]
                break
        barraSW = int(barraSW)
        dados = []
        cabecalho = ['Variavel' , 'Resultado marginal superior', 'Lâmbda superior', 'Resultado marginal inferior', 'Lâmbda inferior']
        dados.append(cabecalho)
        theta = '\\theta'
        bar = -1
        r_count = 0
        #angulos
        for b in sis.dbarras:
            ang = theta + str(b['BARRA'])
            if b['BARRA'] in barras_angulos:
                ur = f'{resultado.upper.residual[r_count]:.4f}'.replace('.',',')
                um = f'{resultado.upper.marginals[r_count]:.4f}'.replace('.',',')
                lr = f'{resultado.lower.residual[r_count]:.4f}'.replace('.',',')
                lm = f'{resultado.lower.marginals[r_count]:.4f}'.replace('.',',')
                r_count+=1
            else:
                continue
            dados.append([ ang, ur, um, lr, lm ])

        #despachos
        for b in sis.dbarras:
            ger = 'G' + str(b['BARRA'])
            if b['BARRA'] in barras_despachos:
                ur = f'{resultado.upper.residual[r_count]:.4f}'.replace('.',',')
                um = f'{resultado.upper.marginals[r_count]:.4f}'.replace('.',',')
                lr = f'{resultado.lower.residual[r_count]:.4f}'.replace('.',',')
                lm = f'{resultado.lower.marginals[r_count]:.4f}'.replace('.',',')
                r_count+=1
                dados.append([ ger, ur, um, lr, lm ])

        #cortes
        for b in sis.dbarras:
            cut = 'BARRA ' + str(b['BARRA'])
            if b['BARRA'] in barras_cortes:
                ur = f'{resultado.upper.residual[r_count]:.4f}'.replace('.',',')
                um = f'{resultado.upper.marginals[r_count]:.4f}'.replace('.',',')
                lr = f'{resultado.lower.residual[r_count]:.4f}'.replace('.',',')
                lm = f'{resultado.lower.marginals[r_count]:.4f}'.replace('.',',')
                r_count+=1
                dados.append([ cut, ur, um, lr, lm ])
        tabela(f, 1, dados, 'Resultados Limites', 1)
        # Fim tabela limites


        # Printando resultados sem marginal
        dados = []
        cabecalho = ['Variavel' , 'Lâmbda superior', 'Lâmbda inferior']
        dados.append(cabecalho)
        theta = '\\theta'
        bar = -1
        barras_angulos = [b['BARRA'] for b in sis.dbarras if b['TIPO'] != 'SW']
        barras_despachos = [b['BARRA'] for b in sis.dbarras if b['PGesp(PU)'] != 0 or b['TIPO'] == 'SW']
        barras_cortes = [b['BARRA'] for b in sis.dbarras if b['PD(PU)'] != 0]
        barraSW = 0
        for bar in sis.dbarras:
            if bar["TIPO"] == 'SW': 
                barraSW = bar["BARRA"]
                break
        barraSW = int(barraSW)
        dados = []
        cabecalho = ['Variavel' , 'Resultado marginal superior', 'Lâmbda superior', 'Resultado marginal inferior', 'Lâmbda inferior']
        dados.append(cabecalho)
        theta = '\\theta'
        bar = -1
        r_count = 0
        #angulos
        for b in sis.dbarras:
            ang = theta + str(b['BARRA'])
            if b['BARRA'] in barras_angulos:
                um = f'{resultado.upper.marginals[r_count]:.4f}'.replace('.',',')
                lm = f'{resultado.lower.marginals[r_count]:.4f}'.replace('.',',')
                r_count+=1
                dados.append([ ang, um, lm ])

        #despachos
        for b in sis.dbarras:
            ger = 'G' + str(b['BARRA'])
            if b['BARRA'] in barras_despachos:
                um = f'{resultado.upper.marginals[r_count]:.4f}'.replace('.',',')
                lm = f'{resultado.lower.marginals[r_count]:.4f}'.replace('.',',')
                r_count+=1
                dados.append([ ger, um, lm ])

        for b in sis.dbarras:
            cut = 'BARRA ' + str(b['BARRA'])
            if b['BARRA'] in barras_cortes:
                um = f'{resultado.upper.marginals[r_count]:.4f}'.replace('.',',')
                lm = f'{resultado.lower.marginals[r_count]:.4f}'.replace('.',',')
                r_count+=1
                dados.append([ cut, um, lm ])
        tabela(f, 1, dados, 'Resultados Limites', 1)
        # Fim tabela limites

        # ANGULOS
        dados = []
        cabecalho = ['Barra' , 'Ângulo Ótimo']
        dados.append(cabecalho)
        for r in tables['angulos']:
            b = r[0]
            ang = f'{r[1]:.4f}'.replace('.',',')
            dados.append([ b, ang ])
        tabela(f, 1, dados, 'Resultados Ângulos Ótimos', 1)

        # DESPACHOS
        dados = []
        cabecalho = ['Barra' , 'Despacho Ótimo']
        dados.append(cabecalho)
        for r in tables['despachos']:
            b = r[0]
            desp = f'{r[1]:.4f}'.replace('.',',')
            dados.append([ b, desp ])
        tabela(f, 1, dados, 'Resultados Despachos Ótimos', 1)

        # CORTES
        dados = []
        cabecalho = ['Barra' , 'Carga Atual', 'Corte', 'Nova Carga', '\% de corte']
        dados.append(cabecalho)
        for r in tables['cortes']:
            b = r[0]
            pd = float(r[1])
            cut = float(r[2])
            new_pd = pd - cut
            cut_percentage = f'{(cut / pd) * 100:.2f} \%'.replace('.',',')
            dados.append([ b, f'{pd:.4f}'.replace('.',','), f'{cut:.4f}'.replace('.',','), f'{new_pd:.4f}'.replace('.',','), cut_percentage ])
        tabela(f, 1, dados, 'Resultados de Cortes de Carga', 1)





