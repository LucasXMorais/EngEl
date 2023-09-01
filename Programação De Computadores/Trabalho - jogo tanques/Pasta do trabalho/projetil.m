#
#Funcao que plota o tiro e retorna onde caiu
#Autor: Lucas Xavier de Morais
# Jun - 2019
#

function xf = projetil (x,v0,alpha,g,col)
  xf = v0^2*2*sin(alpha)*cos(alpha)/g;
  
  aux = linspace(0,xf,10000);

  y = (tan(alpha).*aux) - 0.5*g*aux.^2/(v0^2*cos(alpha)*cos(alpha));

  aux = aux + x;

  hold on;
  axis([0 1000 0 200]);
  plot(aux,y,'color',col,'linestyle','--');
  hold on;
  
  xf += x;

endfunction
