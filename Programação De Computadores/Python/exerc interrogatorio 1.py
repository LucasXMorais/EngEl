perguntas = ["Telefonou para vítima?","Esteve no local do crime?","Mora perto da vítima?","Devia para a vítima?","Já trabalhou com a vítima?"]
print("Responda 's' para sim e 'n' para não")
i = 0
tot = 0
for i in range(5):
    pro = False
    print(perguntas[i])
    while pro == False: 
        resp = str(input("Resp = "))
        if resp != "s" and resp != "n":
            print("Resp inválida")
        elif resp == "s" or resp == "n":
            if perguntas[i] != perguntas[4]:
                print("Próxima pergunta")
            pro = True
    if resp == "s":
        tot = tot + 1
if tot < 2:
    print("Inocente")
elif tot == 2:
    print("Suspeito")
elif tot < 5:
    print("Cúmplice")
else:
    print("Assassino")
        
