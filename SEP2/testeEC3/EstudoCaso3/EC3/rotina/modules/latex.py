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










