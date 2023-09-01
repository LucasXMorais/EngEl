nome = str(input("Nome = "))
nome = nome.upper()
print(nome)
nome = list(nome)
print(nome)
#c = 0
novo_nome = []
print(novo_nome)
tam = len(nome) - 1
print(tam)
aux = tam
print(aux)
print(nome[aux])
for c in range(0, len(nome)):
    novo_nome.append(nome[aux])
    aux = aux - 1
print(novo_nome)
    
    
