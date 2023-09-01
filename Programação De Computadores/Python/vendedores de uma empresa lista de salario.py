vendas = []
ven = int(input("Nmr de vendedores = "))
func = []
for j in range(ven):
    ji = j + 1
    print("Func",ji)
    func.append(str(input("")))
print("Insira as vendas brutas dos vendedores")
for c in range(ven):
    print("Vendas do vendedor(a) ",func[c])
    vendas.append(int(input("")))
sal = []
for g in range(ven):
    aux = 0
    aux = vendas[g]*0.09 + 200
    sal.append(aux)
tab = []
k = 200
tab2 = []
for d in range(9):
    tab2.append(0)
    tab.append(k)
    k = k + 100
for a in range(ven):
    cont = -1
    g = 200
    while g < sal[a]:        
        g = g + 100
        #cont = cont + 1
        if g == 1200:
            break
        cont = cont + 1
    tab2[cont] = tab2[cont] + 1
for f in range(9):
    ger = f*100 + 299
    if f == 8:
        print(tab2[f]," vendedore(s) mais que ",tab[f])
        break
    print(tab2[f]," vendedore(s) entre ",tab[f]," - ",ger)
for h in range(ven):
    print(func[h]," recebe ",sal[h])
