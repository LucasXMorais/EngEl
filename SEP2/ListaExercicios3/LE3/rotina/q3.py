# Lucas X. de Morais
# 14/08/24 - Questão 1
from scipy.optimize import linprog, minimize
import numpy as np

def a():
    objetivo = [6, 3.5, 5]
    inequacoes = [
            [-0.55, -0.6, -0.75],
            [-0.15, -0.4, -0.18],
            ]
    inequacoes_limites = [-2480, -560]
    mg_limites = (0, 1500)
    sp_limites = (0, 1600)
    ba_limites = (0, 1800)
    igualdades = [
            [1, 1, 1]
            ]
    igualdades_limites = [4000]

    resultado = linprog(objetivo, 
                        A_ub=inequacoes,
                        b_ub=inequacoes_limites,
                        A_eq=igualdades,
                        b_eq=igualdades_limites,
                        bounds=[
                            mg_limites,
                            sp_limites,
                            ba_limites
                            ])
    
    print(f'Valor ótimo R${resultado.fun} ')
    print(f'Solução: mg = {resultado.x[0]} g | sp = {resultado.x[1]} g | ba = {resultado.x[2]} g ')
    print("Sucesso:", resultado.success)
    print("Mensagem:", resultado.message)

