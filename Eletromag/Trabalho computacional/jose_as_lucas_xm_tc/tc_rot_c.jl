#Tabalho Computacional de Eletromagnetismo
#Autores: José Augusto dos Santos e Lucas Xavier de Morais
#---------------------------------------------------------

#Cálculo do campo magnético
function B()
    u0 = 4 * pi * 10^-7 
    return (u0*I)/(2*pi*r)
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

Exercício c)
Campo magnético gerado por uma linha filamentar infinitamente longa localizada em x = y = 0.

Dados: - Corrente Elétrica em A (I) 
       - Distância em relação ao filamento em m (r)

Obtendo como saída o campo magnético (B)

*É possível utilizar os prefixos do SI na entrada. 
Para um valor de 0.003 por exemplo, é possível digitar: 3m
"""

println(enunc)
println("Parâmetros de entrada")

#Solicitando ao usuário os valores de I e r
global I = leituraEnt("I")

global r = leituraEnt("r")

#Achando o resultado do problema
global resultado = B()

#Mostrando o resultado do problema
resolucao = """ 
Corrente : $I A
Distância: $r m

Módulo do Campo Magnético = $resultado T
"""
println(resolucao)