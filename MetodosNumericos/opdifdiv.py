# Operador Diferenças Divididas para calcular a interpolação de Newton
# Dada a table abaixo:
# x  |  -1    0    1    2    3
#f(x)|   1    1    0   -1   -2

import numpy as np

x = [0.2,0.3,0.4]
fx = [np.cos(0.2),np.cos(0.3),np.cos(0.4)]

def div(x, fx):
    #Maior grau é len(pontos) - 1
    #div de grau 0, div(xi) = f(xi)    

    divs = []
    aux = []
   
    #GRAU 0
    for i in range(len(x)):    
        aux.append(fx[i])
        
    divs.append(aux)
    
    for g in range(1, len(x)): 
        
        aux = []
                          
        for i in range(len(x)-g):
            aux.append( ( divs[g-1][i] - divs[g-1][i+1] ) / ( x[i] - x[i+g] ) )
        
        divs.append(aux)
        
    return divs

print(div(x, fx))
    