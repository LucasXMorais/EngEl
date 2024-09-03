# 19/07/24 - Lucas Xavier de Morais 
# Comparando 2 sistemas diferentes
# SEP II - Engenharia Elétrica (UFSJ)

def sistemas(SISTEMAS: list):
    A = SISTEMAS[0]
    B = SISTEMAS[1]
    print('Comparando sistemas')

    print('Comparando dados de barras')
    Aaux = A[0]
    Baux = B[0]
    for a, b in zip(Aaux, Baux):
        for aKey, bKey in zip(a, b):
            Aval = a[aKey]
            Bval = b[bKey]
            if Aval != Bval: 
                print(f'Barra {a["BARRA"]} mudou {aKey} de {Aval} -> {Bval}')
    
    print('Comparando dados de circuitos')
    Aaux = A[1]
    Baux = B[1]
    for a, b in zip(Aaux, Baux):
        for aKey, bKey in zip(a, b):
            Aval = a[aKey]
            Bval = b[bKey]
            if Aval != Bval: 
                print(f'Circuito {a["NCIR"]} mudou {aKey} de {Aval} -> {Bval}')


