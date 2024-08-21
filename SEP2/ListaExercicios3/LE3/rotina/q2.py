# Lucas X. de Morais
# 14/08/24 - Questão 1
from scipy.optimize import linprog, minimize
import numpy as np

def c():
    print('C)')
    objetivo = [1.2, 1.15]
    inequacoes = [
            [-300, -200],
            [28, 10]
            ]
    inequacoes_limites = [-350, 32]
    x_limites = (0, None)
    y_limites = (0, None)

    resultado = linprog(objetivo, 
                        A_ub=inequacoes,
                        b_ub=inequacoes_limites,
                        bounds=[
                            x_limites,
                            y_limites
                            ])
    
    print("Valor ótimo:", resultado.fun)
    print(f'Solução: x1 = {resultado.x[0]} e x2 = {resultado.x[1]} ')
    print("Sucesso:", resultado.success)
    print("Mensagem:", resultado.message)

