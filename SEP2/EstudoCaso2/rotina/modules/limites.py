# 13/07/24 - Lucas Xavier de Morais 
# Funções de cálculo de limites
# SEP II - Engenharia Elétrica (UFSJ)
import numpy as np
import configparser
from modules import sistema

def limiteTensao(tensaoKV: str, tensaoPU: str) -> str:
    tensaoNominal = int(tensaoKV)
    tensaoOperacao = float(tensaoPU)

    if tensaoNominal < 230:
        if tensaoOperacao >= 0.95 and tensaoOperacao <= 1.05: return "SIM"
        return "NAO"
    match tensaoNominal:
        case 230:
            if tensaoOperacao >= 0.95 and tensaoOperacao <= 1.05: return "SIM"
            return "NAO"
        case 345:
            if tensaoOperacao >= 0.95 and tensaoOperacao <= 1.05: return "SIM"
            return "NAO"
        case 440:
            if tensaoOperacao >= 0.95 and tensaoOperacao <= 1.046: return "SIM"
            return "NAO"
        case 500:
            if tensaoOperacao >= 1.00 and tensaoOperacao <= 1.10: return "SIM"
            return "NAO"
        case 525:
            if tensaoOperacao >= 0.95 and tensaoOperacao <= 1.048: return "SIM"
            return "NAO"
        case 765:
            if tensaoOperacao >= 0.90 and tensaoOperacao <= 1.046: return "SIM"
            return "NAO"
    return "ERR"
# Fim TENSAO

