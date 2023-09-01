pares = 0
impares = 0
x = []
for c in range(10):
     x.append((int(input("n = "))) 
     #print(c)
     if x[c] % 2 == 0:
         pares = pares + 1
         print("pares = ", pares)
     else:
         impares = impares + 1
         print("impares = ", impares)
print("Pares = ", pares, "Ímpares = ", impares)
