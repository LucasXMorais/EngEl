nome = str(input("Nome = "))
nome = nome.upper()
nome = list(nome)
rang = 2*len(nome) - 1
c1 = -1
aux1 = ''
for c in range(0,rang):
    if c <= ((rang + 1) / 2) - 1:
        aux1 = aux1 + nome[c]
        print(aux1)
        c1 = c1 + 1
    else:
        aux1 = aux1.replace(nome[c1], '') 
        print(aux1)
        c1 = c1 - 1
        
        
    
