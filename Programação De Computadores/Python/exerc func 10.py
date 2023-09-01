from random import randint
game = True
while game == True:
    input("Aperte 'enter' pra jogar")
    jogo = True
    jogadas = 0
    aux = 0
    while jogo == True:
        dado = randint(2, 12)
        print(dado)
        jogadas = jogadas + 1
        if dado == 2 or dado == 3 or dado == 12:
            print("Fim de jogo")
            print(jogadas, "jogadas")
            jogo = False            
        elif dado == 7 or dado == 11:
            print("Parabens")
            jogo = False
        else:
            aux = dado
            while aux == dado:
                dado = randint(2, 12)
                jogadas = jogadas + 1
                print(dado)
                if dado == 7 or dado == 11:
                  print("Fim de jogo")
                  print(jogadas, "jogadas")
                  jogo = False

 
