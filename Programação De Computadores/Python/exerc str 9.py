def conveniar(cpf):
    if len(cpf) == 14:
        cpf = cpf.replace('-', '')
        cpf = cpf.replace('.', '')
    cpf = list(cpf)
    return cpf

def dig(cpf, ver):
    soma = 0
    if ver == 1:
        arr = [0,0,0,0,0,0,0,0,0]
        mult = 10
        for c in range(0, 9):
            arr[c] = int(cpf[c])*mult
            mult = mult - 1
            soma = soma + int(arr[c])
        soma = soma % 11
        digito = 11 - soma
        if digito > 9:
            digito = 0
    if ver == 2:
        arr = [0,0,0,0,0,0,0,0,0,0]
        mult = 11
        for c in range(0, 10):
            arr[c] = int(cpf[c])*mult
            mult = mult - 1
            soma = soma + int(arr[c])
        soma = soma % 11
        digito = 11 - soma
        if digito > 9:
            digito = 0
    return digito

fim = False                
while fim == False:
    certo = False
    while certo == False:
        cpf = str(input("CPF = "))
        if len(cpf) == 14 or len(cpf) == 11 and cpf.isdigit():
            certo = True
        else:
            certo = False
        
    cpf = conveniar(cpf)
    dig1 = int(cpf[9])
    dig2 = int(cpf[10])
    if int(dig(cpf,1)) == dig1 and int(dig(cpf,2)) == dig2:
        print("CPF válido")
    else:
        print("CPF inválido!!")
