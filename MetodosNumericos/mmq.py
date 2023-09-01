import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt

def resSist(a,b): # Resolução de sistemas usando o método de Gauss-Siedel 
    #Nmr máx de iterações e tolerância
    maxIter = 50
    tol = 10**(-15)

    #Erro relativo e passo de iteração
    erroRel = 1.0
    k = 1

    #Dimensão do sistema
    n = len(a)

    #Variáveis
    somaPar = 0.0

    #Vetores coluna (Entradas)

    #Se entradas == 0
    xk = np.zeros((n,1))

    #Se entradas != 0
    #x1, x2, x3, x4, x5, x6 = [1, 2, 3, 4, 5, 6]
    #xk = np.array([[x1],[x2],[x3],[x4],[x5],[x6]], dtype = float)

    xk1 = np.copy(xk)

    #Executando
    while k < maxIter:
        
        for i in range(n):
            somaPar = b[i]
            
            for j in range(n):
                if i != j:
                    somaPar = somaPar - a[i,j]*xk[j]
            
            xk[i] = somaPar/a[i,i]
            
        #Erro relativo
        erroRel = la.norm(xk - xk1, np.inf)/la.norm(xk, np.inf)
        
        if erroRel <= tol: break
        
        xk1 = np.copy(xk)
            
        k += 1
        
    return xk 

def prodEsc(A, B):#Produto escalar entre duas matrizes/vetores
    
    prod = 0.
    
    for i in range(len(A)):
        prod += A[i]*B[i]
        
    return prod

def phi(x, grau):
    
    #phi1 = 1
    #phi2 = x
    
    return x**grau

def g(x, mmq):
    
    soma = 0.
    
    for i in range(len(mmq)):
        soma += (mmq[i]) * (x**i)
        
    return soma

#px = [0., 0.25, 0.5, 0.75, 1.]
#fx = [1, 1.284, 1.6487, 2.117, 2.7183]

#4sin(x) , 0 <= x <= pi, + -6x/pi + 6, pi < x <= 2pi
#px = [0, np.pi/4, np.pi/2, np.pi/3, np.pi, 4, 3*np.pi/2, 5.5, 2*np.pi]
#fx = [0, 4*np.sin(np.pi/4), 4*np.sin(np.pi/2), 4*np.sin(np.pi/3), 1, (16/np.pi) - 4,  2, (20/np.pi) - 4, 4]

#sin(x)
#px = []
#fx = []
#for i in range(11):
#    px.append((2*np.pi/10)*i)
#    fx.append(np.sin(px[i]))

#ln( x + x^2 ) * x^(5-2x)
#px = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
#fx = [-3.4982*10**-5, -8.6935*10**-4, -4.7119*10**-3, -0.0123, -0.0179, -5.8596*10**-3, 0.0481, 0.1707, 0.3829, 0.6931, 1.0933, 1.5595, 2.0558, 2.5407, 2.9739]

px = [-1, 0, 1, 2]
fx = [0, -1, 0, 7]

grau = 3

phis = []

for i in range(0,grau+1):
    phisAux = []
    for j in range(len(px)):
        phisAux.append(phi(px[j], i))
    phis.append(phisAux)    
    
PHI = [] #Deve ser uma matriz quadrada do tipo grau x grau
for i in range(grau+1):
    PHIAux = []
    for j in range(grau+1):
        PHIAux.append(prodEsc(phis[i],phis[j]))
    PHI.append(PHIAux)
PHI = np.array(PHI, dtype = float)

FX = [] #Deve ser uma matriz coluna do tipo grau x 1
for i in range(grau+1):
    for j in range(len(fx)):
        FXAux = [prodEsc(phis[i],fx)]
    FX.append(FXAux)
FX = np.array(FX, dtype = float)

mmq = resSist(PHI,FX)

x =  np.arange(px[0], px[-1], (px[-1] - px[0]) / 10**3)
gx = []
for i in range(len(x)):
    gx.append(g(x[i],mmq))

plt.plot(x, gx)
plt.show()