#Comparação de resultados usando gráficos

import numpy as np
import matplotlib.pyplot as plt

#4sin(x) , 0 <= x <= pi, + -6x/pi + 6, pi < x <= 2pi
px = [0, np.pi/4, np.pi/2, np.pi/3, np.pi, 4, 3*np.pi/2, 5.5, 2*np.pi]
fx = [0, 4*np.sin(np.pi/4), 4*np.sin(np.pi/2), 4*np.sin(np.pi/3), 1, (16/np.pi) - 4,  2, (20/np.pi) - 4, 4]

#cos(x)
#px = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
#fx = [np.cos(0.1),np.cos(0.2),np.cos(0.3),np.cos(0.4),np.cos(0.5),np.cos(0.6),np.cos(0.7),np.cos(0.8),np.cos(0.9),np.cos(1)]

#ln( x + x^2 ) * x^(5-2x)
#px = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
#fx = [-3.4982*10**-5, -8.6935*10**-4, -4.7119*10**-3, -0.0123, -0.0179, -5.8596*10**-3, 0.0481, 0.1707, 0.3829, 0.6931, 1.0933, 1.5595, 2.0558, 2.5407, 2.9739]

#2x^3 + x^4
#px = [-3, -2, -1, 0, 1, 2]
#fx = [27, 0, -1, 0, 3, 32]

def f(x):
    return 4*np.sin(x) if x <= np.pi else (4/np.pi)*x - 4   
    #return np.cos(x)
    #return np.log(x + x**2) * x**(5-2*x)
    #return 2*x**3 + x**4

def div(px, fx):
    #div de grau 0, div(xi) = f(xi)    

    divs = []
    aux = []
   
    #GRAU 0
    for i in range(len(px)):    
        aux.append(fx[i])
        
    divs.append(aux)
    
    for g in range(1, len(px)): 
        
        aux = []
                          
        for i in range(len(px)-g):
            aux.append( ( divs[g-1][i] - divs[g-1][i+1] ) / ( px[i] - px[i+g] ) )
        
        divs.append(aux)
        
    return divs

def newton(divs,px,x):
    
    soma = divs[0][0]
    
    for i in range(1,len(divs)):
        
        mult = 1
        
        for j in range(i):
            mult *= x - px[j]
            
        soma += divs[i][0]*mult
        
    return soma

def lagrange(px, fx, x, k):
    
    num = 1.0
    den = 1.0
    
    for j in range(len(px)):
        if j != k:
            num *= x - px[j]
            den *= px[k] - px[j] 
    
    return (num*fx[k]) / den
 
def linear(px, fx, x):
   
    a = []
    b = []
    
    a.append(px[0])
    a.append(fx[0])
    b.append(px[1])
    b.append(fx[1])
    
    for l in range(1, len(px)):
        #Defindo o intervalo
        if x > b[0]: 
            a[0] = px[l]
            a[1] = fx[l]
            b[0] = px[l+1]
            b[1] = fx[l+1]
        else:
            break  
        
    return ( ( a[1] - b[1] ) / ( a[0] - b[0] ) ) * x + ( b[1] - ( ( a[1] - b[1] )* b[0] ) / ( a[0] - b[0] ) )
         
x =  np.arange(px[0], px[-1], (px[-1] - px[0]) / 10**3)
lin = []
lagr = []
newt = []
func = []

for i in range(len(x)):
    
    #Linear
    lin.append(linear(px, fx, x[i]))
    
    #Lagrange
    L = 0.0
 
    for j in range(len(px)):
        L += lagrange(px, fx, x[i], j)
  
    lagr.append(L)
    
    #Newton
    newt.append(newton(div(px,fx) , px , x[i]))
    
    #Função exemplo
    func.append(f(x[i]))#Caso seja a função cos(x)
    
plt.plot(x, lin, linewidth = 5.)
plt.plot(x, lagr, linewidth = 3.75)
plt.plot(x, newt, linewidth = 2.5)
plt.plot(x, func, linewidth = 1.25)
plt.show()
    
    
    