u = 125;
t = linspace(0,500,1000);
A = pi/6;
h = 3;
g = 32;

x = u.*t*cos(A);

y = -g.*(t.^2)*1/2 + u.*t*sin(A) + h;

plot(x,y);
plot(350,10);