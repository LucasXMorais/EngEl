check = False
while check == False:
    produto = str(input("combustível = "))
    if produto == "A":
        litros = float(input("Quantos litros? "))
        preco = litros*1.90
        if litros <= 20:
            tot = preco*0.97
        else:
            tot = preco*0.95
        check = True
    elif produto == "G":
        litros = float(input("Quantos litros?"))
        preco = litros*2.50
        if litros <= 20:
            tot = preco*0.96
        else:
            tot = preco*0.94
        check = True
print("Litros: ",litros," L")
print("Valor a ser pago: R$ ",tot)
