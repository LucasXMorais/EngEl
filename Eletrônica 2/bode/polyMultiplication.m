%   # a e b devem ser listas do tipo 1xn e 1xm respect. 
%   # a ideia é encontrar uma lista que indica a multiplicação de dois polinômios represnetados pela lista
%   # onde os valores nas listas são os parâmetros dos polinômios e a posição do número é o grau da variável adicionado de um
%   # a = [xa, ya, za] representa a = xa*s^0 + ya*s^1 + za*s^2 
clear all; close all; clc; clf;
function ret = polyMult(a, b)
    pol = zeros(1,length(a)+length(b)-1)

    for n = [1:length(a)]
        for m = [1:length(b)]
            pol(n+m-1) = pol(n+m-1) + (a(n)*b(m))
        endfor
    endfor

    ret = pol
endfunction

pola = [1, 2, 3];
polb = [2, 5];

d = polyMult(pola, polb)