#Interpolação de Newton usando operadores diferenciais

import numpy as np

px = [0.2, 0.3, 0.4, 0.5, 0.6]
fx = [np.cos(0.2),np.cos(0.3),np.cos(0.4),np.cos(0.5),np.cos(0.6)]
x = 0.35

# px = [-1., .0, 2.]
# fx = [4., 1., -1.]
# x = 0.35

def div(px, fx):
    #Maior grau é len(pontos) - 1
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

def pol(divs,px,x):
    
    soma = divs[0][0]
    
    for i in range(1,len(divs)):
        
        mult = 1
        
        for j in range(i):
            mult *= x - px[j]
            
        soma += divs[i][0]*mult
        
    return soma

def eqpol(divs,px): ##### Comentar quando quiser o polinômio #####
    
    pol = str(divs[0][0])
    
    for i in range(1,len(divs)):
        
        mult = ""
        
        for j in range(i):
            mult += " * "
            mult += "[ x - ( " + str(px[j]) + " )]"
            
        pol += " + { ( " + str(divs[i][0]) + " ) " + mult + " } "
        
    return pol

# def eqpol(divs,px): ##### FORMATAÇÃO PARA FÓRMULA EXCEL #####
#   
#     pol = str(divs[0][0])
#   
#     for i in range(1,len(divs)):
#       
#         mult = ""
#       
#         for j in range(i):
#             mult += "*"
#             mult += "(F3-(" + str(px[j]) + "))"
#           
#         pol += "+((" + str(divs[i][0]) + ")" + mult + ")"
#        
#     return pol

#print(eqpol(div(px,fx),px))
print(pol(div(px,fx),px,x))