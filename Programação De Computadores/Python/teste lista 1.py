pares = 0
impares = 0
lista = []
n = int(input("n = "))
for c in range(n):
    lista.append(int(input("n = ")))
print("lista = ",len(lista))
for i in range(len(lista)):
    print(lista[i])
    if lista[i] % 2 == 0:
        pares = pares + 1
        print("Pares = ",pares)
    else:
        impares = impares + 1
        print("Ímpares = ",impares)
print(lista)
print("Pares = ",pares)
print("Ímpares = ",impares)
