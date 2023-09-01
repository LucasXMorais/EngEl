sal = float(input("salário = "))
if sal <= 280 :
    perc = 0.2
    aum = perc*sal
    salf = sal + aum
elif sal <= 700 :
      perc = 0.15
      aum = perc*sal
      salf = sal + aum
elif sal <= 1500 :
          perc = 0.1
          aum = perc*sal
          salf = sal + aum
else :
          perc = 0.05
          aum = perc*sal
          salf = sal + aum
print("Salário anterior = ",sal)
print("Percentual = ",perc)
print("Valor do aumento = ",aum)
print("Novo salário = ",salf)


    
