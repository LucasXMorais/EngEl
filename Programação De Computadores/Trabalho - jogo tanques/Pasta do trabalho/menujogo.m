#
#menujogo.m - funcao para receber a quantidade de jogadores, os nomes 
#deles e as cores que eles vao usar
#Autor: Lucas Xavier de Morais
# Jun - 2019
#

function [QtdJogadores jogadores cores] = menujogo()
  #Primeiro pergunta quantos jogarao 
  while 1
    QtdJogadores = str2num(cell2mat(inputdlg('Numero de jogadores')));
    #Verificar a entrada válida de quantidade de jogadores
    if floor(QtdJogadores) != QtdJogadores || QtdJogadores <= 1 || QtdJogadores > 10 || isempty(QtdJogadores)# Checa se o valor é válido
      h = errordlg('Insira um valor válido!!');
      uiwait(h);
      continue    
    else
      break
    endif
  endwhile
  
  #Cira uma celula pra mais pra frente perguntar os nomes de cada jogador
  #mas ja dar um nome padrao de jogador para cada
  
  jogadores = cell(1,QtdJogadores);
  for c = [1:QtdJogadores]
    jogadores{1,c} = sprintf('Jogador%i',c);
  endfor
  #Permite que os jogadores coloquem seus nomes
  jogadores = inputdlg(jogadores,'Nomes',1,jogadores);  

  #Cada jogador escolhe uma cor

  w = msgbox({'0 - Vermelho','1 - Azul','2 - Preto','3 - Rosa','4 - Azul-verde','5 - Amarelo','6 - Verde','7 - Roxo','8 - Jade','9 - Laranja'});
  #Mostra as cores disponíveis e depois entra num while
  #para validar as cores
  while 1
    erro = false;
    cores = inputdlg(jogadores,'Cores',1);
    for c = [1:QtdJogadores]
      CodVerificado = str2num(cores{c,1});
      #Verifica primeiro se nao e uma string e depois se e um valor valido
      #e se nao tem dois com cores iguais
      if isempty(CodVerificado)
        erro = true;
        break
      endif
      if floor(CodVerificado) != CodVerificado || CodVerificado < 0 || CodVerificado > 9  
        erro = true;
        h = errordlg('Insira valores válidos!!');
        uiwait(h);        
        break
      endif
    endfor
    if size(cores)(1) != size(unique(cores))(1)
      h = errordlg('Cada jogador deve escolher uma cor única');
      uiwait(h);
      erro = true;
    endif
    if erro == false
      break
    endif
  endwhile  
  delete(w);
endfunction  
  
  