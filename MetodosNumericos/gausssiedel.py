################
#Método de Gauss-Siedel
################

#O método de Gauss-Siedel é muito mais eficiente que o método de Jacobi

#Método de Gauss-Siedel resolve um sistema linear aproximando o valor linha por linha.
#Exemplo, dado um sistema linear do tipo: A[nxn] * x[nx1] = B[nx1]
#O método de Gauss-Siedel resolve esse sistema da seguinte forma:

#x1(1) = ( b1 - a12*x2(0) - a13*x3(0) ... a1n*xn(0) ) / a11
#x2(1) = ( b2 - a21*x1(1) - a23*x3(0) ... a2n*xn(0) ) / a22
#x3(1) = ( b3 - a31*x1(1) - a32*x2(1) ... a3n*xn(0) ) / a33
#...
#xn(1) = ( bn - an1*x1(1) - an2*x2(1) ... a1n*xn(0) ) / ann
#
#x1(2) = ( b1 - a12*x2(1) - a13*x3(1) ... a1n*xn(1) ) / a11
#x2(2) = ( b2 - a21*x1(2) - a23*x3(1) ... a2n*xn(1) ) / a22
#x3(2) = ( b3 - a31*x2(2) - a32*x2(2) ... a3n*xn(1) ) / a33
#...
#xn(2) = ( bn - an1*x1(2) - an2*x2(2) ... a1n*xn(1) ) / ann
#Repetindo esses passos até atingir uma tolerância 

import numpy as np
from numpy import linalg as la

#Nmr máx de iterações e tolerância
maxIter = 50
tol = 10**(-15)

#Erro relativo e passo de iteração
erroRel = 1.0
k = 1

#Matriz A
a = np.array([[13, 3, 2, 1, 0, 0],
              [3, 11, 3, 2, 1, 0],
              [2, 3, 11, 3, 2, 1],
              [1, 2, 3, 11, 3, 2],
              [0, 1, 2, 3, 11, 3],
              [0, 0, 1, 2, 3, 12]], dtype = float)

#Vetor B
b1, b2, b3, b4, b5, b6 = [0, 5, 1, 9, 3, 9]
b = np.array([[b1],[b2],[b3],[b4],[b5],[b6]], dtype = float)

#a = np.array([[4, 0.24, -0.08], [0.09, 3, -0.15], [0.04, -0.08, 4]], dtype = float) 
#b = np.array([[8], [9], [20]], dtype = float) 

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

print("------ Solução Final ------")
for i in range(n): print("x"+str(i+1)+" : "+str(float(xk[i])))
print("Número de iterações: ",k)
    
