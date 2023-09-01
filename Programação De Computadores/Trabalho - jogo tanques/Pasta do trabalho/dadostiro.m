#
#Funcao para receber os dados dos tiros dos jogadores
#Autor: Lucas Xavier de Morais
# Jun - 2019
#

function [v0 alpha] = dadostiro()

  while 1
    tiro = inputdlg({'Velocidade inicial','angulo em graus'},'0 < v0 <= 100 e 0 < teta < 180');
    v0 = str2num(tiro{1});
    alpha = str2num(tiro{2});

    if v0 <= 0 || v0 > 100 || isempty(v0) || alpha < 0 || alpha > 180 || isempty(alpha)
      h = errordlg('Insira valores válidos')
      uiwait(h);
    else
      break
    endif
  endwhile

  #Converte de graus para radiano
  alpha = pi*alpha/180;

endfunction
