# 24/06/24 - Lucas Xavier de Morais 
# Análise de fluxo de potência
# SEP II - Engenharia Elétrica (UFSJ)
from modules import *
# IMPORTANTE: USAR NUMPY VERSÃO < 2.* 
# pip install --force-reinstall -v "numpy==1.*"

def main():
    app.iniciar()

    sis = app.carregarSistema()

    exibir.resumoSistema(sis)

    app.menu(sis)
# Fim main
    

if __name__ == '__main__':

    main()



