#Cálculo da componente em X
function Ex(x)
    return x^2
end

#Resolução pelo método 1/3 de Simson repetida
function simpsonx()
    h = 1/n #Cálculo do intervalo
    soma = 0.0

    for i in 1:2:(n-1)        
        soma = soma + 4*Ex(h*i)
    end  

    for i in 2:2:(n-2)
        soma = soma + 2*Ex(h*i)
    end
  
    soma = soma + Ex(0) + Ex(1)

    return soma*(h/3)
end

function simpsonp()
    h = 1/n #Cálculo do intervalo
    soma = 0.0

    for i in 1:2:(n-1)        
        soma = soma + 4*Ex(h*i)
    end  

    for i in 2:2:(n-2)
        soma = soma + 2*Ex(h*i)
    end
  
    #soma = soma + Ex(0) + Ex(1)

    return soma*(h/3)
end

function trap()
    h = 1/n #Cálculo do intervalo
    soma = 0.0

    for i in 1:(n-1)
        soma = soma + 2*Ex(h*i)
    end
  
    soma = soma + Ex(0) + Ex(1)

    return soma*(h/2)
end



global n = 1000

println(simpsonx())
println(simpsonp())
println(trap())
println(1/3)