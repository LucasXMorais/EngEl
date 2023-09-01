def mes(m):
    m = m - 1
    meses = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novmebro","dezembro"]
    mesEsc = meses[m]
    return mesEsc

def leituraData(date, inim):
    day = date[0:2]
    month = date[2+inim:4+inim]
    year = date[4+(2*inim):]
    fdate = [day, month, year]
    return fdate
    
data = str(input("Inserir data no formato DD/MM/AAAA"))

if len(data) == 8:#sem barras
    data = leituraData(data, 0)
    dia = int(data[0])
    mes1 = int(data[1])
    ano = int(data[2])
    if mes1 > 12 or dia >=32:
        print("Error")
    else:
        print(dia," de ", mes(mes1), " de ",ano)
elif len(data) == 10:#com barras
    if data[2] != "/" and data[5] != "/":
        print("Error 1")
    else:
        data = leituraData(data, 1)
        dia = int(data[0])
        mes1 = int(data[1])
        ano = int(data[2])
        if mes1 > 12 or dia >= 32 or ano >= 2019:
            print("Error")
        else:
            print(dia," de ", mes(mes1), " de ",ano)
else:
    print("Corrigir a data")
    

