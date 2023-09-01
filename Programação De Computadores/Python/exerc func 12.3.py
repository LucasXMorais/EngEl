from random import shuffle
def shuffled(pal):
    pal = list(pal)
    shuffle(pal)
    return ''.join(pal)
palavra = str(input("Palavra = "))
print(shuffled(palavra))
