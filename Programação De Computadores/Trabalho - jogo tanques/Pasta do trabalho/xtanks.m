#
#Funcao que recebe a posicao dos tanques
#Autor: Lucas Xavier de Morais
# Jun - 2019
#

function [x_pos] = xtanks (QtdJogadores,jog)
  
  while 1 
    x_pos = inputdlg(jog,'Posição x dos tanques');  
    erro = false;
    for c = [1:QtdJogadores]
      x1 = x_pos{c,1};      
      if str2num(x1) < 0 || str2num(x1) > 990 || isempty(str2num(x1)) 
        h = errordlg('Insira valores válidos!!');
        uiwait(h);
        erro = true;        
        break
      endif
    endfor

    #Verifica se nenhum tanque ocupa o mesmo lugar que outro
    for c = [1:QtdJogadores]
      x1 = x_pos{c,1};
      for j = [1:QtdJogadores]
        x2 = x_pos{j,1};
        if str2num(x2) >= (str2num(x1) - 10) && str2num(x2) <= (str2num(x1) + 10) 
          if j != c
            h = errordlg({'Os tanques não podem ocupar o mesmo espaço'});
            uiwait(h);
            erro = true;
            break
          endif
        endif
      endfor
      if erro == true
        break
      endif
    endfor
    
    if erro == false
      break
    endif
  endwhile
  
endfunction