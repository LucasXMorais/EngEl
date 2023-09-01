A=[0 1 0; 0 0 1; -4 -3 -2];
B=[0; 0; 1];
C=[-1 2 1];
D=[0];
sys=ss(A,B,C,D)

[num,den]=ss2tf(sys)

ft=tf(num, den)

[A,B,C,D]=tf2ss(ft)
