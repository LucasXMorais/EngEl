clear all, close all, clc

disp("Exemplo do uso da função ode45");

y0=0; % condição inicial.
Tspan=[0 5]; % tempo de simulação, definir um tempo suficientemente grande para que o sistema atinja o regime permanente.

[T,Y] = ode45(@Exercicioode45,Tspan,y0); % a saída T guarda o vetor de tempo usado pela ODE, bem como a sequência de valores de y que são solução para o seu problema. 


plot(T, Y, "linewidth", 5) 
% plota os valores de T no eixo horizontal e os valores de Y no eixo vertical.
% linewidth aumenta a espessura da curva para ficar mais visível.

set(gca, "linewidth", 4, "fontsize", 12) 

% faz o contorno da caixa ficar mais visível com números maiores


xlabel('t') %identificando o eixo horizontal 
ylabel('y')%identificando o eixo vertical

title('Simulação temporal')