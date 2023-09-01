#
#Funcao para transformar as cores em codigos rgb
#Autor: Lucas Xavier de Morais
# Jun - 2019
#

function [cod_cores] = rgbcores (QtdJogadores,cores)
  RGB_Cores = {[1 0 0],[0 0 1],[0 0 0],[1 0 0.5],[0 1 1],[1 1 0],[0 1 0],[0.8 0 0.8],[0 1 0.5],[1 0.5 0]};   
  
  for c = [1:QtdJogadores]
    aux = str2num(cores{c,1}) + 1;
    cores{c,1} = RGB_Cores{1,aux};
  endfor
  
  cod_cores = cores;    
endfunction
