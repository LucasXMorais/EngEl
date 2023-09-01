def drawTable(tam):
    linha = " ---"
    coluna = "|   "
    for j in range(tam):
        print(linha*tam)
        print(coluna*tam + coluna)
    print(linha*tam)
drawTable(2)
