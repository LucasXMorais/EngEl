clear
clc
disp("Como passar do espaço de estados para função de transferência");

%Declarando as matrizes do sistema
A=[0 1 0;0 0 1;-4 -3 -2];
B=[0;0;1];
C=[-1 2 1];
D=0;

%Montando a representação em espaço de estados.
sistema=ss(A,B,C,D)


% A partir da representação é possível obter a função de transferência.

[num,den]=ss2tf(sistema);
 
% num-> contém os coeficientes do numerador.

%den-> contém os coeficientes do denominador.

disp("Montando a função de transferência");

ftr=tf(num,den)


disp("A partir da função de transferência podemos obter outra representação em espaço de estados, diferente, porém equivalente à primeira.");

[A1,B1,C1,D1]=tf2ss(ftr)
