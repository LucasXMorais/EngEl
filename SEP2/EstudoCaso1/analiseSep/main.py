# 25/03/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
from modules import *
import configparser

def main() -> None:
    config = configparser.ConfigParser()
    config.read('config.ini')

    print('Iniciando Leitura de dados')
    arquivo = config['FILE']['DATA_FILE_NAME']
    dbarras, dcircuitos = leitura.lerDados(arquivo)
    base = float(config['PU']['BASE'])
    # Armazenando os dados do sistema na classe Sistema
    sistemaInicial = Sistema(dbarras, dcircuitos, arquivo, base)

    print('Calculando as variáveis')
    sistemaInicial.resolverFluxo()

    print('Calculando as potências e fluxos de potência:')
    # Aqui as potências, fluxos e etc, são calculads dentro da classe para limpar o código e já gaurdar essas informações
    sistemaInicial.calcularPotencias()

    output = config['FILE']['OUTPUT_FILE']
    print(f'Montando o arquivo {output}')

    exportacao.exportarSistema(output, sistemaInicial)

    return None

if __name__ == '__main__':
    main()



