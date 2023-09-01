#Interpolação linear
#Método usado para aproximar uma função dado um intervalo de valores
#Nesse exmeplo, usado pra aproximar o valor da tg(x), dados os pontos:
# x    |    1     |     1.1     |     1.2     |     1.3     |
#tg(x) |  1.5574  |    1.9648   |    2.5722   |    3.6021   |

#Se quisermos encontrar o valo aproximado de tg(x1) para qualquer valor no intervalo [1, 1.3]:
#Lineariza-se uma função pegando os valores dos intervalos que abrangem x1
#Ex: se quisermos calcular o valor de tg(1.07), fazemos uma função do tipo f(x) = ax + b,
#sendo que os ponto analizados seriam (1, 1.5574) e (1.1, 1.9648)

def P(a, b, x):
    return ( ( a[1] - b[1] ) / ( a[0] - b[0] ) ) * x + ( b[1] - ( ( a[1] - b[1] )* b[0] ) / ( a[0] - b[0] ) )

pontos = [[1, 1.5574], [1.1, 1.9648], [1.2, 2.5722], [1.3, 3.6021]]

print("Cálculo aproximado da tg(x) para todo x e [1, 1.3] ")

while 1: 
    try:
        x = float(input("x : "))
        
        if x < 1 or x > 1.3 : 
            print("Valor inválido") 
        else: 
            break
    except:
        print("Valor inválido")
    
a = pontos[0]
b = pontos[1]   
    
for i in range(1, len(pontos)):
    #Defindo o intervalo
    if x > b[0]: 
        a = pontos[i]
        b = pontos[i+1]
    else:
        break  
    
print( P(a, b, x) )   