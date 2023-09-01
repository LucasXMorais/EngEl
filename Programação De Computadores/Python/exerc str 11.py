def printarPalavra(pal):
    printa = '_'
    for c in range(len(pal) - 1):
        printa = '_' + printa
    return printa
def juntar(pal):
    retorno = ''
    for i in range(len(pal)):
        retorno = retorno + pal[i]
    return retorno

import random
lista_de_palavras = ['fogo','guerra','almeida','samsung','coca','caneta','violão','borda','casa','fila','dance','mundo','trono']
print("Wanna play a game?")
palavraEscolhida = random.randint(0,(len(lista_de_palavras) - 1))
palavraEscolhida = lista_de_palavras[palavraEscolhida]
palavraEscolhida = list(palavraEscolhida)
print("Ok, vambora!!")
print("Essa palavra tem {} letras".format(len(palavraEscolhida)))
printado = list(printarPalavra(palavraEscolhida))
fim = False
c = 1
chances = 6
acerto = 0
while fim == False:
    print(juntar(printado))
    letra = str(input("Letra {} = ".format(c)))
    c = c + 1
    checking = True
    i = 0
    while checking == True:
        if i == len(palavraEscolhida):
            enc = False
            break
        if letra == palavraEscolhida[i]:
            enc = True
            break
        i = i + 1
    if enc == True:
        for j in range(len(palavraEscolhida)):
            if letra == palavraEscolhida[j]:
                printado[j] = letra.upper()
                acerto = acerto + 1
        if acerto == len(palavraEscolhida):
            palFinal = juntar(printado)
            print(palFinal.upper())
            print("Voce conseguiu!!!")
            break
    else:
        chances = chances - 1
        print("Letra errada. Voce agora tem {} chances".format(chances))
        if chances == 0:
            print("Fim de Jogo!")
            break
        
