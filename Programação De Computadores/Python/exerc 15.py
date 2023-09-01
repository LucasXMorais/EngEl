ganho = float(input("Ganho/h = "))
hrs = int(input("Horas no mes = "))
a = ganho*hrs
b = a*0.11
c = a*0.08
d = a*0.05
print("Bruto = ",a)
print("Imposto de Renda = ",b)
print("INSS = ",c)
print("Sindicato = ",d)
e = a - b - c - d
print("Salário líquido = ",e)

