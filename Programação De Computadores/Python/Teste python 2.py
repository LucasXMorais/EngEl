
#soma de valores pares entre o intervalo fornecido

s = 0
a = int(input("Valor de A: "))
b = int(input("Valor de B: "))
x = a%2
print("resto divisão por 2 = ",x)
# somente calcula se o a for impar
if a%2 != 0:
    a = int(a/2) * 2
    print("Valor de a após primeiro calculo: ",a)
    
while (a<=b):
    s = s +a
    a = a +2
    print("s= ",s," a= ",a)
    
print(s)

