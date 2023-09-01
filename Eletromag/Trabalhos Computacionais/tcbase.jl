#Tabalho Computacional de Eletromagnetismo
#Autores: José Augusto dos Santos e Lucas Xavier de Morais
#---------------------------------------------------------

#Declarando Função
function f(r,d,ro)
    return r + d + ro
end

#Apresentação do problema
enunc = """
Trabalho Computacional 

Alunos:
José Augusto dos Santos
Lucas Xavier de Morais

Exercício a)
Campo elétrico gerado no eixo central de um anel carregado uniformemente.

Dados: - Raio do anel (r) 
       - Distância do ponto de observação ao centro do anel (d)
       - Densidade linear de carga do anel (ro)

Obtendo como saída o módulo do campo elétrico (E)  

"""

print(enunc)
print("Favor entrar os parâmetros de entrada\n")

#Solicitando ao usuário os valores de r, z, e ro
#Caso não seja um valor numérico, avisar do erro ao usuário e zerar as variáveis
r = 0.0
d = 0.0
ro = 0.0

try 
    println("Raio do anel (r): ")
    global r = parse(Float64, readline())
catch
    print("Valor inválido!\nDefinindo r = 0\n")
end

try 
    println("Distância do centro (d): ")
    global d = parse(Float64, readline())
catch
    print("Valor inválido!\nDefinindo d = 0\n")
end  

try 
    println("Densidade linear (ro): ")
    global ro = parse(Float64, readline())
catch
    print("Valor inválido!\nDefinindo ro = 0\n")
end   

#Achando o resultado do problema
resposta = f(r,d,ro)

#Mostrando o resultado do problema
print("\nCampo Elétrico E = $resposta J")
