clc
close all
clear all
s = tf('s');
P = bodeoptions;
P.FreqUnits = 'Hz';

% Circuito RC no domínio da frequência // Circuito passa baixa com frequencia = 60Hz
# Considerando R*C = 1/(2*pi*f)
# Usando um capacitor C = 1uf;
# R = 1/(2*pi*60*1u) = 2,652k;
R = 2.652e3;
C = 1.0e-6;
Hs = 1/(R*C*s + 1);
figure(1)
bodeplot(Hs,P);grid on;
