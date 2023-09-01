a = float(input("Número a = "))
b = float(input("Número b = "))
print("Para fazer uma operação, escreva o que quer fazer. Escreva 'soma' por exemplo")
end = False
sa = False
while sa == False:
 per = str(input("Qual operação deseja senhor(a)?"))
 if per == "soma":
     print('{} + {} = {}'.format(a, b, a+b))
 elif per == "subtracao":
     print("{} - {} = {}".format(a, b, a-b))
 elif per == "multiplicacao":
     print("{} x {} = {}".format(a, b, a*b))
 elif per == "divisao":
     print("{} / {} = {}".format(a, b, a/b))
 elif per == "exponenciacao":
     print("{} elev {} = {}".format(a, b, a**b))
 elif per == "resto":
     print("{} // {} = {}".format(a, b, a//b))
 elif per == "troca":
     a = float(input("Número a = "))
     b = float(input("Número b = "))     
 elif per == "fim":
     sa = True
 else:
     print("Operação inválida")
    


    
    
