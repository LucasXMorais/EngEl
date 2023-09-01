clear all;
close all;
clc;

R = 3;
L = 1;
C = 1/2;

A = [-R/L -1/L; 1/C 0];
B = [1/L; 0];
C = [1 0];
D = 0;

sys = ss(A,B,C,D);

t = 0:0.01:50;

%u = sin(t);
u = ones(1,size(t,2));

x0 = [1; 2];

[y, t, x] = lsim(sys, u, t, x0);

figure()
plot(t,y);

figure()
plot(t,x(:,1));
hold on
plot(t,x(:,2));

figure()
plot(t,u);