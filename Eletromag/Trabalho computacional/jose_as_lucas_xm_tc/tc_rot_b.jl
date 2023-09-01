#Tabalho Computacional de Eletromagnetismo
#Autores: José Augusto dos Santos e Lucas Xavier de Morais
#---------------------------------------------------------

#Os cálculos foram feitos individualmente para cada coordenada
#Cálculo da componente em X
function Ex(phi)
    R = ((x-r*cos(phi))^2 + (y-r*sin(phi))^2 + z^2)^(3/2)
    return (ro*r*(x - r*cos(phi)))/(kinv*R)
end

#Resolução pelo método 1/3 de Simson repetida
function simpsonx()
    h = 2*pi/n #Cálculo do intervalo
    soma = 0.0

    #Somatória dos fatores do método de 1/3 de simpson
    for i in 1:2:(n-1)        
        soma = soma + 4*Ex(h*i)
    end  

    for i in 2:2:(n-2)
        soma = soma + 2*Ex(h*i)
    end
  
    soma = soma + Ex(0) + Ex(2*pi)

    return soma*(h/3)
end

#Cálculo da componente em Y
function Ey(phi)
    R = ((x-r*cos(phi))^2 + (y-r*sin(phi))^2 + z^2)^(3/2)
    return (ro*r*(y - r*sin(phi)))/(kinv*R)
end

function simpsony()
    h = 2*pi/n 
    soma = 0.0

    for i in 1:2:(n-1)
        soma = soma + 4*Ey(h*i)
    end  

    for i in 2:2:(n-2)
        soma = soma + 2*Ey(h*i)
    end  
    
    soma = soma + Ey(0) + Ey(2*pi)

    return soma*(h/3)
end

#Cálculo da componente em Z
function Ez(phi)
    R = ((x-r*cos(phi))^2 + (y-r*sin(phi))^2 + z^2)^(3/2)
    return (ro * r * z)/(kinv*R)
end

function simpsonz()
    h = 2*pi/n 
    soma = 0.0

    for i in 1:2:(n-1)
        soma = soma + 4*Ez(h*i)
    end  

    for i in 2:2:(n-2)
        soma = soma + 2*Ez(h*i)
    end  
    
    soma = soma + Ez(0) + Ez(2*pi)

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

Exercício b)
Campo elétrico, em qualquer ponto do espaço, gerado por um anel no plano xy e z = 0.
Escolheu-se um anel cuja equação paramétrica se dá por:

A(t) = (r*cos(t), r*sin(t), 0) , Para todo t pertencente aos reais tal que 0 <= t <= 2*pi 

Dados: - Raio do anel em metros (r) 
       - Posição do cálculo em metros (x, y e z)
       - Densidade linear de carga do anel em Coulomb/metro (ro)

Obtendo como saída o campo elétrico (E) 

*É possível utilizar os prefixos do SI na entrada. 
Para um valor de 0.003 por exemplo, é possível digitar: 3m
"""

println(enunc)
println("Parâmetros de entrada")

#Solicitando ao usuário os valores de r, do ponto de observação e da densidade

global n = 100 #Precisão do método numérico

global kinv = 4*pi*8.85*(10^(-12)) #Constante usada no cálculo para deixa a fórmula mais limpa

global r = leituraEnt("r em m")

println("Ponto de observação em metros (Em coordenadas cartesianas)")
global x = leituraEnt("X em m")
global y = leituraEnt("Y em m")
global z = leituraEnt("Z em m")

global ro = leituraEnt("ro em C/m")

#Achando o resultado do problema
global compx = simpsonx()
global compy = simpsony()
global compz = simpsonz()

modulo = sqrt(compx^2 + compy^2 + compz^2)

#Mostrando o resultado do problema
resolucao = """ 
Raio : $r m
Densidade: $ro C/m
P: ($x m, $y m, $z m)

Módulo do Campo Magnético E = $modulo J
Vetor Campo Elétrico = ($compx J, $compy J, $compz J)
"""

println(resolucao)