#
#Funcao para checar se o tiro acertou alguem
#Autor: Lucas Xavier de Morais
#
# Jun - 2019
#Autor: Lucas Xavier de Morais
#

#'quem' e a variavel que indicar quem esta atirando
function [infojog morte] = checktiro (xf,infojog,quem)
  for j = 1:length(infojog)
    #verifica se o tiro nao caiu no lugar de alguem que ja foi atingido
    if infojog(j).dead == false
      #Checa a area de cada tanque e compara se o tiro ciua la
      if xf >= str2num(infojog(j).x) && xf <= (str2num(infojog(j).x) + 10 )
        if j != quem
          #Nesse caso outro jogador foi atingido
          #Informa e da um ponto a quem acertou
          k = msgbox({infojog(quem).nome,' acertou ',infojog(j).nome});
          uiwait(k);
          infojog(j).dead = 1;
          infojog(quem).pontos = infojog(quem).pontos + 1;
          morte = true;
          break
        else
          #Nesse caso o jogador se acertou e todos ganham 1 ponto menos ele
          k = msgbox({infojog(quem).nome,' se acertou'});
          uiwait(k);
          infojog(quem).dead = 1;
          morte = true;
          for h = 1:length(infojog)
            if h != quem              
              infojog(h).pontos = infojog(h).pontos + 1;
            endif
          endfor
          break
        endif
      else
        morte = false;
      endif
    endif
  endfor
  
endfunction
