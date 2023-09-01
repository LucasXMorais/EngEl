def div10(a):
    b = a
    c = 0
    if a < 0:
        b = a*(-1)
    while b > 1:
        b = b/10
        c = c + 1
    return c
sair = False
while sair == False:
    n = int(input("N = "))
    print(n," tem ",div10(n)," digitos")
    
    
    
    
