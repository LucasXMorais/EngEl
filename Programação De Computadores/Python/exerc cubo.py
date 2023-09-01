def drawTable(tam):
    linha = " ---"
    coluna = "|   "
    for j in range(tam):
        print(linha*tam)
        print(coluna*tam + coluna)
    print(linha*tam)
tamanho = int(input("Tamanho"))
drawTable(tamanho)
def drawCube(tam):
    linha = " ---"
    coluna = "|   "
    profund1 = "   __"
    profund2 = " /"
    profund = " /|  "
    inv = tam
    inv1 = tam
    for j in range(1,tam + 1):
        inv = inv - 1
        print("   "*inv + profund1*tam)
        print("   "*inv + profund*tam + "/|")
    for j in range(tam):
        inv1 = inv1 - 1
        print(linha*tam + profund2*tam)
        print(coluna*tam + "|" + profund*inv)
    print(linha*tam)
drawCube(tamanho)
