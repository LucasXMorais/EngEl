a = float(input("a = "))
b = float(input("b = "))
c = float(input("c = "))    
if a + b >= c and a + c >= b:
   if a == b and b == c:
       print("Equilátero")
   elif a == b or b == c or a == c:
       print("Isóceles")
   else:
       print("Escaleno")
else:
    print("Não é um triângulo")
       
