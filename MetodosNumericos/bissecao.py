#Método da bisseção para encontrar raízes de uma equação
#Dada uma função f(x), e um intervalo [a, b]
#Caso haja uma raíz no intervalo [a, b], é possível determinar essa raíz usando esse algorítmo
import numpy as np

# Definindo f(x):
def f(x) :
    return np.sqrt(x) - 5*np.exp(-x)

#Intervalos iniciais
a = 1
b = 2
p = 15 #Máx. iter.

#Loop para procurar a raíz 
for k in range(0,p):
    
    x_n = (a + b)/2
    
    #print(x_n)
    #print(f(x_n))
    
    if f(x_n) == 0:
        break
    
    if f(a)*f(x_n) < 0:
        b = x_n
    else:
        a = x_n