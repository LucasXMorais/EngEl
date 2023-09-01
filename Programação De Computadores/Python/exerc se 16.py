print("ax**2 + bx + c")
a = float(input("a = "))
if a != 0:
    print(a,"x**2 + bx + c")
    b = float(input("b = "))
    print(a,"x**2 +",b,"x + c")
    c = float(input("c = "))
    print(a,"x**2 +",b,"x +",c)
    delta = b**2 - 4*a*c
    if delta < 0:
        print("Não possui raízes reais")
    else:
        x1 = (-1*b + delta**(1/2))/ (2*a)
        x2 = (-1*b - delta**(1/2))/ (2*a)
        if delta == 0:
            print("Possui apenas uma raíz real = ", x1)
        else:
            print("Raiz 1 = ", x1)
            print("Raiz 2 = ", x2)
else:
    if b != 0:        
        resp = (-1*c)/ b
        print("Não é uma equação de segundo grau")
        print("Sua raíz é ", resp)
    else:
        print("Essa é uma função constante cujo k = ", c)
