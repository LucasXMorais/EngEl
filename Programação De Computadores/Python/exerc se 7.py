a = int(input("a = "))
b = int(input("b = "))
c = int(input("c = "))
if a < b or a < c :
    if b > c :
        maior = b
    else :     
        maior = c 
else :
    maior = a

if a > b or a > c :
    if b < c :
        menor = b
    else :
        menor = c
else :
    menor = a

print("Menor valor = ",menor)
print("Maior valor = ",maior)
input()    
    
