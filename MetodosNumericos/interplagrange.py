#Interpolação método de Lagrange
#Método usado para aproximar uma função dado um intervalo de valores
#Nesse exmeplo, usado pra aproximar o valor da tg(x), dados os pontos:
# x    |    1     |     1.1     |     1.2     |     1.3     |
#tg(x) |  1.5574  |    1.9648   |    2.5722   |    3.6021   |

pontos = [[1, 1.5574], [1.1, 1.9648], [1.2, 2.5722], [1.3, 3.6021]]

def L(pontos, x, i):
    
    num = 1.0
    den = 1.0
    
    for j in range(len(pontos)):
        if j != i:
            num *= x - pontos[j][0]
            den *= pontos[i][0] - pontos[j][0] 
    
    return (num*pontos[i][1]) / den
        

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
    
#P que é a soma dos "L"s  
P = 0.0
 
for i in range(len(pontos)):
    P += L(pontos, x, i)
    
print(P)   