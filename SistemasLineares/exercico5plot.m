clear all, close all, clc

disp("Plot do exercício 5")

y0 = 0; %Condição inicial nula
tspan = linspace(0,25,500); %Defindo o período no qual a função vai ser plotada

%Entrada = u1
[T Y1] = ode45(@(t,y)exercicio5(t,y,1,0), tspan, y0);
plot(T,Y1, "linewidth", 2, "color", "b")
hold on

%Entrada = u2
[T Y2] = ode45(@(t,y)exercicio5(t,y,0,1), tspan, y0);
plot(T,Y2, "linewidth", 2, "color", "r")
hold on

%Entrada = u1 + u2
[T Y12] = ode45(@(t,y)exercicio5(t,y,1,1), tspan, y0);
plot(T,Y12, "linewidth", 2, "color", "m")
hold on

%Testando linearidade do sistema
Y3 = Y1+Y2;
plot(T,Y3, "linewidth", 1.5, "color", "k", "linestyle", "--")
hold on

%Tentando entender o erro da soma das funções. Procurando o erro médio...
totalErr = 0;
err = 0;
j = 0;
for i = [1:500]
  if Y12(i) != 0 && Y1(i) != Y2(i)
    j = j+1;
    err = abs((Y1(i)+Y2(i)-Y12(i)))/abs(Y12(i));
    totalErr = totalErr + err;
  end
end
Erro = totalErr/j;
disp(sprintf('Erro médio: %.8f',Erro))

%alguns detalhes estéticos...
set(gca, "linewidth", 1.5, "fontsize", 15) 
xlabel('t',"fontsize", 20)
ylabel('y',"fontsize", 20)
title('Simulação temporal',"fontsize", 30)
legend('u1', 'u2', 'u1 + u2', 'y1 + y2')