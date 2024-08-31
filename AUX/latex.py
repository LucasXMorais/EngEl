# Lucas Xavier de Morais 
# 38/04/24 - Programa para gravar dados formatados para Latex

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


def main():
    latexFile = './tabela.md'
    with open(latexFile, 'w') as f:

        # Criando tabelas de angulos e tensoes
        dados = []
        cabecalho = ['K','12K','15K','20K','25K','30K','40K','50K','65K','80K','100K','140K','200K' ]
        dados.append(cabecalho)
        unidades = ['6K','8K','10K','12K','15K','20K','25K','30K','40K','50K','65K','80K','100K','140K' ]
        dados.append(unidades)
        dados.append( [350, 510, 650, 840, 1060, 1340, 1700, 2200, 2800, 3900, 5800, 9200] )
        dados.append( [210, 440, 650, 840, 1060, 1340, 1700, 2200, 2800, 3900, 5800, 9200] )
        dados.append( [ '', 300, 540, 840, 1060, 1340, 1700, 2200, 2800, 3900, 5800, 9200] )
        dados.append( [ '',  '', 320, 710, 1060, 1340, 1700, 2200, 2800, 3900, 5800, 9200] )
        dados.append( [ '',  '',  '', 430,  870, 1340, 1700, 2200, 2800, 3900, 5800, 9200] )
        dados.append( [ '',  '',  '',  '',  500, 1100, 1700, 2200, 2800, 3900, 5800, 9200] )
        dados.append( [ '',  '',  '',  '',   '',  660, 1350, 2200, 2800, 3900, 5800, 9200] )
        dados.append( [ '',  '',  '',  '',   '',   '',  850, 1700, 2800, 3900, 5800, 9200] )
        dados.append( [ '',  '',  '',  '',   '',   '',   '', 1100, 2200, 3900, 5800, 9200] )
        dados.append( [ '',  '',  '',  '',   '',   '',   '',   '', 1450, 3500, 5800, 9200] )
        dados.append( [ '',  '',  '',  '',   '',   '',   '',   '',   '', 2400, 5800, 9200] )
        dados.append( [ '',  '',  '',  '',   '',   '',   '',   '',   '',   '', 4500, 9200] )
        dados.append( [ '',  '',  '',  '',   '',   '',   '',   '',   '',   '', 2000, 9100] )
        dados.append( [ '',  '',  '',  '',   '',   '',   '',   '',   '',   '',   '', 4000] )
        tabela(f, 1, dados, 'Tabela de tensão e defasagem por barra', 1)

        f.write('\n\n')


if __name__ == '__main__':
    main()
