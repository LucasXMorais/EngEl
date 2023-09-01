def divisor(aux):
    n = 0
    while aux > 10:
        aux = aux/10
        n = n + 1
    return n

def subt(aux1, pot):
    aux1 = aux1 % (10 ** pot)
    return aux1
def fator(aux3, menos, pot):
    aux3 = aux3 - menos
    aux3 = aux3 / (10 ** pot)
    return aux3
n = int(input("n = "))
ni = ""
f = -1
aux2 = n
while f <= 1 + divisor(n):
    fat = fator(n, subt(n, divisor(n)), divisor(n))
    n = subt(n, divisor(n))
    fat = int(fat)
    ni = str(fat) + ni
    f = f + 1
ni = int(ni)    
print(ni)
test = ni*2
print(test)

    
