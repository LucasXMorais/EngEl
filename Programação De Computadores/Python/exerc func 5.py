def somaImposto(taxa, custo):
    taxa = taxa/100
    custo = custo + (custo*taxa)
    return custo
prod = float(input("Preço = "))
imp = float(input("Taxa = "))
soma = somaImposto(imp, prod)
dif = soma - prod
print("O produto sofreu uma alteração de R$",dif," e com o imposto custa R$",soma)
