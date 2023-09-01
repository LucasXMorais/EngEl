a = float(input("Número a = "))
b = float(input("Número b = "))
print("Para fazer uma operação, escreva o que quer fazer. Escreva 'soma' por exemplo")
#per = str(input("Qual operação deseja senhor(a)?"))
sa = False
while sa == False:
 per = str(input("Qual operação deseja senhor(a)?"))
 if per == "soma":
     print('{} + {} = {}'.format(a, b, a+b))
     sa = True
 elif per == "subtracao":
     print("{} - {} = {}".format(a, b, a-b))
     sa = True
 elif per == "multiplicacao":
     print("{} x {} = {}".format(a, b, a*b))
     sa = True
 elif per == "divisao":
     print("{} / {} = {}".format(a, b, a/b))
     sa = True
 elif per == "exponenciacao":
     print("{} elev {} = {}".format(a, b, a**b))
     sa = True
 elif per == "resto":
     print("{} // {} = {}".format(a, b, a//b))
     sa = True
 else:
     print("Operação inválida")
     sa = False
    


    
    
