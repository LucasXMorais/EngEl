def altura(h, b):
    c = 0
    altura = "|" + (b-2)*" " + "|"
    barra = "|" + (b-2)*" " + "|"
    for c in range(1,h):
        barra = barra + "\n" + altura
    return barra        
        
def base(b):
    c = 0
    base = "-"
    for c in range(0,(b - 1)):
        base = base + "-"
    return base

h = float(input("Altura = "))
b = float(input("Base = "))

if h < 1:
    h = 1
elif h > 20:
    h = 20
h = round(h)

if b < 1:
    b = 1
elif b > 20:
    b = 20
b = round(b)
print(base(b))
print(altura(h, b))
print(base(b))

    
    
