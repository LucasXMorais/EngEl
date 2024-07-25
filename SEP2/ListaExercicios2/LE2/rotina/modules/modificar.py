# 13/07/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)

def valorDicionario(dicionario: dict) -> tuple:
    data = []
    index = 0
    for key in dicionario:
        index += 1
        data.append( (index, key, dicionario[key]) )
        print(f'{index} - {key}')
    while True:
        campo = input('Insira o número do campo a ser trocado: ')
        if campo.isnumeric():
            campo = int(campo)-1
            if campo <= len(data):
                key = data[campo][1]
                valor = input(f'Novo valor do campo {key}: ')
                if valor == 'q' or valor == 'Q': return ('q','q')
                tipo = data[campo][2]
                if isinstance(tipo, int): valor = int(valor)
                if isinstance(tipo, float): valor = float(valor)
                if isinstance(tipo, str): valor = str(valor)
                # dicionario[key] = valor
                return (key, valor)
        if campo == 'q' or campo == 'Q': return ('q','q')


