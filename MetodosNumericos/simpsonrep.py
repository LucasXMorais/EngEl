import numpy as np

def f(x):
    resp = x
    #resp = np.sqrt( (x**2)/(1-x**2) + 1 ) * 2*np.pi*x     
    #resp = np.cos(x)*np.sin(x)
    #resp = x**3 + 9*(x**2) + 3*x + 9 + 6*np.sqrt(x)
    return  resp

#Resolução pelo método 1/3 de Simson repetida
n = 100
limite = 2 #função varia de 0 a limite
h = (limite)/n #Cálculo do intervalo
soma = 0.0

for i in range(1,n,2):    
    soma = soma + 4*f(h*i) 

for i in range(2,n,2):
    soma = soma + 2*f(h*i)
  
soma = soma + f(0) + f(limite)

soma = soma*(h/3)

print(soma)