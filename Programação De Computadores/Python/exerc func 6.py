def conv(horas, minu):
    if horas > 12:
        horas = horas - 12        
        rel = "P"
    else:
        rel = "A"
    ret = [horas, minu, rel]
    return ret
def printa(entrada):
    print(entrada[0], ":",entrada[1], " ", entrada[2],".M.")
fim = False
while fim == False:
    h = int(input("Horas = "))
    m = int(input("Minutos = "))
    errado = True
    while errado == True:
        if h > 24:
            print("Valor n suportado")
            h = int(input("Horas = "))
        elif m > 60:
            print("Valor n suportado")
            m = int(input("Minutos = "))
        else:
            errado = False
    o = conv(h, m)
    printa(o)
    
