#Tabalho Computacional de Eletromagnetismo
#Responsáveis: João Marcos de Paula Stefani e
#Hamiltom Luiz da Fonseca

disp("Exercicio b")

disp("Digite o valor de r")
r = input ("r : ");

disp("Digite o valor de x")
x = input("x : ");

disp("Digite o valor de y")
y = input("y : ");

disp("Digite o valor de z")
z = input("z : ");

disp("Digite o valor de p")
ro = input("ro : ");

n = 50;

#X   
h = 2*pi/n;
 
somax = 0;
    
for i =  1:2:(n-1) 
  phi = h*i;
  R = ((x-r*cos(phi))^2 + (y-r*sin(phi))^2 + z^2)^(3/2);
  respostax = (ro*r*(x - r*cos(phi)))/(4*pi*8.85*(10^(-12))*R);
  somax = somax + 4*respostax;
end  

for i = 2:2:(n-2)
  phi = h*i;
  R = ((x-r*cos(phi))^2 + (y-r*sin(phi))^2 + z^2)^(3/2);
  respostax = (ro*r*(x - r*cos(phi)))/(4*pi*8.85*(10^(-12))*R);
  somax = somax + 2*respostax;
end
  
R = ((x-r*cos(0))^2 + (y-r*sin(0))^2 + z^2)^(3/2);
respostax = (ro*r*(x - r*cos(0)))/(4*pi*8.85*(10^(-12))*R);   
somax = somax + respostax;
    
R = ((x-r*cos(2*pi))^2 + (y-r*sin(2*pi))^2 + z^2)^(3/2);
respostax = (ro*r*(x - r*cos(2*pi)))/(4*pi*8.85*(10^(-12))*R);
somax = somax + respostax;

somax =  somax*(h/3)
 
#Y  
somay = 0;
    
for i =  1:2:(n-1) 
  phi = h*i;
  R = ((x-r*cos(phi))^2 + (y-r*sin(phi))^2 + z^2)^(3/2);
  respostay = (ro*r*(y - r*sin(phi)))/(4*pi*8.85*(10^(-12))*R);
  somay = somay + 4*respostay;
end  

for i = 2:2:(n-2)
  phi = h*i;
  R = ((x-r*cos(phi))^2 + (y-r*sin(phi))^2 + z^2)^(3/2);
  respostay = (ro*r*(y - r*sin(phi)))/(4*pi*8.85*(10^(-12))*R);
  somay = somay + 2*respostay;
end
  
R = ((x-r*cos(0))^2 + (y-r*sin(0))^2 + z^2)^(3/2);
respostay = (ro*r*(y - r*sin(0)))/(4*pi*8.85*(10^(-12))*R);   
somay = somay + respostay;
    
R = ((x-r*cos(2*pi))^2 + (y-r*sin(2*pi))^2 + z^2)^(3/2);
respostay = (ro*r*(y - r*sin(2*pi)))/(4*pi*8.85*(10^(-12))*R);
somay = somay + respostay;

somay =  somay*(h/3)

#Z 
somaz = 0;
    
for i =  1:2:(n-1) 
  phi = h*i;
  R = ((x-r*cos(phi))^2 + (y-r*sin(phi))^2 + z^2)^(3/2);
  respostaz = (ro * r * z)/(4*pi*8.85*(10^(-12))*R);
  somaz = somaz + 4*respostaz;
end  

for i = 2:2:(n-2)
  phi = h*i;
  R = ((x-r*cos(phi))^2 + (y-r*sin(phi))^2 + z^2)^(3/2);
  respostax = (ro*r*(x - r*cos(phi)))/(4*pi*8.85*(10^(-12))*R);
  somaz = somaz + 2*respostaz;
end
  
R = ((x-r*cos(0))^2 + (y-r*sin(0))^2 + z^2)^(3/2);
respostaz = (ro * r * z)/(4*pi*8.85*(10^(-12))*R);
somaz = somaz + respostaz;
    
R = ((x-r*cos(2*pi))^2 + (y-r*sin(2*pi))^2 + z^2)^(3/2);
respostaz = (ro * r * z)/(4*pi*8.85*(10^(-12))*R);
somaz = somaz + respostaz;

somaz =  somaz*(h/3)

modulo = sqrt(somax^2 + somay^2 + somaz^2)
