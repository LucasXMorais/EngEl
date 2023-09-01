#
#Funcao que calcula a pontuacao pra verificar se houve empate
#Autor: Lucas Xavier de Morais
# Jun - 2019
#

function [vencedores pontuacao] = CalculoPontos (infojog,QtdJogadores)
       pont = 0;
       for c = 1:QtdJogadores
         if infojog(c).pontos > pont
           pont = infojog(c).pontos;
         endif
       endfor
       i = 1;
       for c = 1:QtdJogadores         
         if infojog(c).pontos == pont
           vencedores(i).nomes = infojog(c).nome;
           i += 1;
         endif
       endfor
       pontuacao = pont;

endfunction
