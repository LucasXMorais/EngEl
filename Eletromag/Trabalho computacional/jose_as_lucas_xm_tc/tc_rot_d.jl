#Tabalho Computacional de Eletromagnetismo
#Autores: José Augusto dos Santos e Lucas Xavier de Morais
#---------------------------------------------------------

#Cálculo da componente em X
function Bx(t)
    R = ((xp-xa-(t*(xb-xa)))^2 + (yp-ya-(t*(yb-ya)))^2 + (zp-za-(t*(zb-za)))^2)^(3/2)
    return u0*I*( yb*(zp - za - t*(zb-za)) - ya*(zp - t*(zb-za)) + za*(yp - t*(yb-ya)) - zb*(yp - ya - t*(yb-ya)) )/(4*pi*R)
end

#Resolução pelo método 1/3 de Simson repetida
function simpsonx()
    h = 1/n #Cálculo do intervalo
    soma = 0.0

    for i in 1:2:(n-1)
        soma = soma + 4*Bx(h*i)
    end  

    for i in 2:2:(n-2)
        soma = soma + 2*Bx(h*i)
    end
  
    soma = soma + Bx(0) + Bx(1)

    return soma*(h/3)
end

#Cálculo da componente em Y
function By(t)
    R = ((xp-xa-(t*(xb-xa)))^2 + (yp-ya-(t*(yb-ya)))^2 + (zp-za-(t*(zb-za)))^2)^(3/2)
    return u0*I*( zb*(xp - xa - t*(xb-xa)) - za*(xp - t*(xb-xa)) + xa*(zp - t*(zb-za)) - xb*(zp - za - t*(zb-za)) )/(4*pi*R)
end

#Resolução pelo método 1/3 de Simson repetida
function simpsony()
    h = 1/n #Cálculo do intervalo
    soma = 0.0

    for i in 1:2:(n-1)
        soma = soma + 4*By(h*i)
    end  

    for i in 2:2:(n-2)
        soma = soma + 2*By(h*i)
    end  
    
    soma = soma + By(0) + By(1)

    return soma*(h/3)
end

#Cálculo da componente em Z
function Bz(t)
    R = ((xp-xa-(t*(xb-xa)))^2 + (yp-ya-(t*(yb-ya)))^2 + (zp-za-(t*(zb-za)))^2)^(3/2)
    return u0*I*( xb*(yp - ya - t*(yb-ya)) - xa*(yp - t*(yb-ya)) + ya*(xp - t*(xb-xa)) - yb*(xp - xa - t*(xb-xa)) )/(4*pi*R)
end

#Resolução pelo método 1/3 de Simson repetida
function simpsonz()
    h = 1/n #Cálculo do intervalo
    soma = 0.0

    for i in 1:2:(n-1)
        soma = soma + 4*Bz(h*i)
    end  

    for i in 2:2:(n-2)
        soma = soma + 2*Bz(h*i)
    end  
    
    soma = soma + Bz(0) + Bz(1)

    return soma*(h/3)
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

Exercício d)
Campo magnético gerado por uma linha filamentar, representada por um segmento de reta arbitrário.

Dados: - Corrente elétrica em Ámperes (I)
       - Posição inicial da linha em metros (Ponto A)
       - Posição final da linha em metros (Ponto B)
       - Posição do cálculo em metros (Ponto P)

*A posição deve estar em coordenadas cartesianas

Obtendo como saída o campo magnético (B) 

*É possível utilizar os prefixos do SI na entrada. 
Para um valor de 0.003 por exemplo, é possível digitar: 3m
"""

println(enunc)
println("Parâmetros de entrada")

#Solicitando ao usuário os valores de I, dos pontos A, B e P
global n = 100 #Precisão

global u0 = 4*pi*10^-7

#solicitando as entradas para o usuário
global I = leituraEnt("I")

println("Ponto inicial da linha em metros (Em coordenadas cartesianas)")
global xa = leituraEnt("XA")
global ya = leituraEnt("YA")
global za = leituraEnt("ZA")

println("Ponto final da linha em metros (Em coordenadas cartesianas)")
global xb = leituraEnt("XB")
global yb = leituraEnt("YB")
global zb = leituraEnt("ZB")

println("Ponto do cálculo em metros (Em coordenadas cartesianas)")
global xp = leituraEnt("XP")
global yp = leituraEnt("YP")
global zp = leituraEnt("ZP")

#Achando o resultado do problema
global compx = simpsonx()
global compy = simpsony()
global compz = simpsonz()

modulo = sqrt(compx^2 + compy^2 + compz^2)

#Mostrando o resultado do problema
resolucao = """ 
Corrente: $I A

A: ($xa m, $ya m, $za m)
B: ($xb m, $yb m, $zb m)
P: ($xp m, $yp m, $zp m)

Módulo do Campo Magnético B = $modulo T
Vetor Campo Mágnético = ($compx T, $compy T, $compz T)
"""

println(resolucao)

