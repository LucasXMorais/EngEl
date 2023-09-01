%Função que calcula a distância entre dois pontos
x0 = 0;
y0 = 0;
x1 = 0;
y1 = 0;

function [dist] = calcdist(x0,y0,x1,y1);
  x = x1 - x0;
  y = y1 - y0;
  dist = sqrt(x**2+y**2);
endfunction
