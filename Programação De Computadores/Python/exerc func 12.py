from random import randint 
def randLet(pal):
    tam = len(pal) - 1
    pal = list(pal)
    letra = randint(0, tam)
    randomLetter = pal[letra]
    return randomLetter

palavra = str(input("Palavra = "))
tamanho = len(palavra)
c = 0
novaPalavra = ''
while c < tamanho:
    letra = randLet(palavra)
    novaPalavra = novaPalavra + letra
    print(novaPalavra)
    palavra = list(palavra)
    g = 0
    for g in range(0, len(palavra)):
        if letra == palavra[g]:
            palavra = palavra.pop(letra)
            break
            
print("-------")
print(novaPalavra)

    

