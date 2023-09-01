#
#Funcao que desenha os tanques com as cores escolhidas pelos jogadores
#Autor: Lucas Xavier de Morais
# Jun - 2019
#

function tank (x,y,col)
  hold on;
  axis([0 1000 0 200]);
  rectangle('position',[x,y,10,3],'facecolor',col,'edgecolor',col);
  hold off;
endfunction
