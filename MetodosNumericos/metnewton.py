#Método de Newton para encontrar raízes de uma função f(x)
#g(x) = x - f(x)/f'(x)  !!!Até ter atingido a tolerância

import numpy as np

def f(x) : 
    return np.sin(x)

def df(x) :
    return np.cos(x)

#Defiindo tolerância e max iter
tol = 10**(-15)
maxIter = 50
xk1 = 5.5
err = 0.0

for i in range(0, maxIter):
    xk = xk1 - ( f(xk1)/df(xk1) )
    
    err = abs(xk - xk1)/abs(xk)
    
    print(xk)
    
    if err <= tol :
        break
    
    xk1 = xk
    
#print(xk)