# Lucas X. de Morais
# 14/08/24 - Questão 1
from scipy.optimize import linprog, minimize
import numpy as np

def b():
    print('B)')
    # Como é Max, devo colocar negativo
    objetivo = [-4, -3]
    inequacoes = [
            [1, 3],
            [2, 2],
            ]
    inequacoes_limites = [7, 8]
    igualdades = [[1, 1]]
    igualdades_limites = [3.5]
    x1_limites = (0, 2)
    x2_limites = (0, 5)

    resultado = linprog(objetivo, 
                        A_ub=inequacoes,
                        b_ub=inequacoes_limites,
                        A_eq=igualdades,
                        b_eq=igualdades_limites,
                        bounds=[
                            x1_limites,
                            x2_limites
                            ])
    
    print("Valor ótimo:", -resultado.fun)
    print(f'Solução: x1 = {resultado.x[0]} e x2 = {resultado.x[1]} ')
    print("Sucesso:", resultado.success)
    print("Mensagem:", resultado.message)


def c():
    # Para um afunção quadrada tem que formar a matriz quadrada
    # 1/2 x^T * Q * x + c^T*x
    # [x1, x2] * [[x1^2, x1*x2],[x2*x1, x2^2]] * [[x1],[x2]]

    print('C)')
    # Função objetivo, definindo o Q
    def objetivo(x):
        Q = np.array([[8, 0], 
                      [0, 10]])
        return 0.5 * np.dot(x.T, np.dot(Q, x))

    # >=
    def inequacoes1(x):
        # 2x1 + x2 <= 2,55
        return 2.55 - (2*x[0] + 1*x[1])  # Note: The constraint is written as g(x) >= 0

    # =
    def igualdades1(x):
        # 2x1 + 4x2 = 7
        return 2*x[0] - 4*x[1] - 7  # Note: The constraint is written as h(x) = 0

    # Initial guess for the variables
    x0 = np.array([0.0, 0.0])   

    # Define the constraints in dictionary form
    restricoes = [{'type': 'ineq', 'fun': inequacoes1},
               {'type': 'eq', 'fun': igualdades1}]

    # Call the minimize function
    resultado = minimize(objetivo, x0, method='SLSQP', constraints=restricoes)

    print("Valor ótimo:", resultado.fun)
    print(f'Solução: x1 = {resultado.x[0]} e x2 = {resultado.x[1]} ')
    print("Sucesso:", resultado.success)
    print("Mensagem:", resultado.message)






