alunos = []
alunos1 = []
d = 0
nmral = int(input("Número de alunos = "))
for c in range(nmral):
    notas = []
    media = 0
    n = 0
    print("Aluno",c," = ")
    alunos.append(str(input("")))
    for i in range(4):
        n = i + 1
        print("Nota",n," = ")
        notas.append(int(input("")))
        media = media + notas[i]
    media = media/4
    alunos1.append(media)
print(alunos)
print(alunos1)
aprovados = []
for j in range(nmral):
    if alunos1[j] >= 7:
        aprovados.append(alunos[j])
print("Aprovados - ",aprovados)
print("Número de alunos aprovados - ",len(aprovados))

        
