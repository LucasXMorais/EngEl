dia = int(input("Nmr int correspondente ao dia da semana = "))
dia = dia - 1 
dias = [ "Domingo" , "Segunda" , "Terça" , "Quarta" , "Quinta" , "Sexta" , "Sábado"]
achou = 0
for x in range(7):
   if x == dia :
     print(dias[dia])
     achou = 1
if achou == 0 :
    print("Nmr inválido")
