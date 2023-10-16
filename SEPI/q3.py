import numpy as np

# Define as funções do sistema de equações (altere conforme necessário)
def f(x):
    return np.array([x[0]**2 + x[1]*x[0] - 10, x[1] + 3*x[0]*(x[1]**2) - 57])

# Define a matriz Jacobiana das funções (altere conforme necessário)
def jacobian(x):
    return np.array([[2*x[0] + x[1], x[0]],
                     [3*(x[1]**2)     , 1 + 6*x[0]*x[1]]])

# Função para resolver o sistema pelo método de Newton
def newton_system_solver(f, jacobian, x0, tol=1e-3, max_iter=100):
    x = x0
    for i in range(max_iter):
        print(i)
        print(f(x))
        print(jacobian(x))
        delta_x = np.linalg.solve(jacobian(x), -f(x))
        print(delta_x)
        x = x + delta_x
        print(x)
        if np.linalg.norm(delta_x) < tol:
            return x
    raise Exception("O método de Newton não convergiu.")

# Chute inicial
x0 = np.array([1.5, 2.5])

# Chama a função do solver
resultado = newton_system_solver(f, jacobian, x0)
print("Resultado:", resultado)
