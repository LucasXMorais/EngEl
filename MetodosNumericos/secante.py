#Método da secante para encontrar raízes de uma função f(x)
#É um método derivado do método de Newton
#é usado quando a derivada é muito complexa
#g(x)  = ( xk2 * f(xk1) - xk1 * f(xk2) ) / ( f(xk1) -  f(xk2) )

import numpy as np

def f(x) : 
    return np.sin(x)

#Defiindo tolerância e max iter
tol = 10**(-15)
maxIter = 50

#Intervalo [5, 7]
xk1 = 5.0
xk2 = 7.0

err = 0.0

for i in range(0, maxIter):
    xk = ( xk2 * f(xk1) - xk1 * f(xk2) ) / ( f(xk1) -  f(xk2) )
    
    err = abs(xk - xk1)/abs(xk)
    
    print(xk)
    
    if err <= tol :
        break
    
    xk2 = xk1
    xk1 = xk
    
#print(xk)