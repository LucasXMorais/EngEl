#Tabalho Computacional de Eletromagnetismo
#Autores: José Augusto dos Santos e Lucas Xavier de Morais
#---------------------------------------------------------

#Cálculo do módulo do campo elétrico
function E()
    return (ro*r*z)/(2*8.85*(10^-12)*(z^2 + r^2)^(3/2))
end
#Função que interpreta prefixos SI 
function leituraEnt(parametro)

    println("$parametro: ")

    mult = 1
    
    entrada = readline()

    prefixos = ["Y", "Z", "E", "P", "T", "G", "M", "k", "h", "da", "d", "c", "m", "u", "n", "p", "f", "a", "z", "y"]
    valores = [10^24, 10^21, 10^18, 10^15, 10^12, 10^9, 10^6, 10^3, 10^2, 10, 10^-1, 10^-2, 10^-3, 10^-6, 10^-9, 10^-12, 10^-15, 10^-18, 10^-21, 10^-24]

    try 
        for i in 1:length(prefixos)
            if string(entrada[end]) === prefixos[i]
                if string(entrada[end]) == "a" && string(entrada[end-1]) == "d" && length(entrada) != 1
                    entrada = entrada[1:end-2]
                    mult = valores[10]
                else
                    entrada = entrada[1:end-1]
                    mult = valores[i]
                end
            end
        end

        entrada = parse(Float64, entrada)
        entrada = entrada*mult
    catch
        println("Valor inválido!\nDefinindo $parametro = 0")
        entrada = 0
    end

    return entrada
end

#Apresentação do problema
enunc = """
Trabalho Computacional 

Alunos:
José Augusto dos Santos
Lucas Xavier de Morais

Exercício a)
Campo elétrico gerado no eixo central de um anel carregado uniformemente.

Dados: - Raio do anel em metros (r) 
       - Distância em relação ao centro do anel em metros (z)
       - Densidade linear de carga do anel em Coulomb/metro (ro)

Obtendo como saída o módulo do campo elétrico (E)  

*É possível utilizar os prefixos do SI na entrada. Se quiser colocar 3mA por exemplo,
digite: 3m
"""

println(enunc)
println("Favor entrar os parâmetros de entrada")

#Solicitando ao usuário os valores de r, z, e ro

global r = leituraEnt("r")

global z = leituraEnt("z")

global ro = leituraEnt("ro")

#Achando o resultado do problema
global resultado = E()

#Mostrando o resultado do problema
resolucao = """ 
Raio : $r m
Distância: $z m
Densidade: $ro C/m

Vetor Campo Elétrico = ( $resultado J )âz
Módulo do Campo Elétrico = $( abs(resultado) ) J
"""

println(resolucao)