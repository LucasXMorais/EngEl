def piramide(topo):
    cod = str(topo)
    cod = cod + " "
    cod = topo*cod
    return cod

n = int(input("N = "))
i = 0
while i <= n:
    o = str(i)
    o = o + " "
    o = o*i
    i = i + 1
    print(o)
b = 0
while b <= n:
    linha = piramide(b)
    print(linha)
    b = b + 1
 
    

