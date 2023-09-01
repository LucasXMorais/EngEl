def countRight(tentativa,senha):
    acertos = [0,0] #o primeiro é para acerto de números e o segundo de posição
    conv = [int(d) for d in str(tentativa)]
    for i in [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]:
        
import random
#print(random.randint(2,5))
tam = random.randint(2,5)
numb = []
for i in range(tam):
    numb.append(random.randint(-1,9))
print('A senha tem {} digitos'.format(tam))
fim = False
while fim == False:
    cod = 0
    if len(cod) != tam:
        cod = int(input())
    else:
        if cod == int(numb):
            print('Fim de jogo. Voce venceu!')
            fim = True
        else:
