# 24/06/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
from modules import *

def main():
    app.iniciar()

    sis = app.carregarSistema()

    exibir.resumoSistema(sis)

    app.menu(sis)
# Fim main
    

if __name__ == '__main__':

    main()



