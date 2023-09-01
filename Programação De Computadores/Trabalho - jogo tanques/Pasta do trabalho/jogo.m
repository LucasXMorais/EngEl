#
#jogo.m - arquivo principal
#Jogo de tanques - Professor Vinicius Cota
#Autor: Lucas Xavier de Morais
# Jun - 2019
#

h = msgbox('Sejam bem-vindos ao Battle Of Tanks');
uiwait(h)
while 1 
 #Inicia ou acaba o jogo
 start = questdlg('Começar / Sair','Inicio','Comecar','Sair','Comecar');
 switch start
   case 'Comecar'
     while 1  
       [QtdJogadores jogadores cores] = menujogo();    
       cod_cores = rgbcores(QtdJogadores,cores);
       #Estrutura para armazenar as informacoes dos jogadores  
       infojog = struct('nome',jogadores,'x',0,'cor',cod_cores,'dead',0,'pontos',0);
  
       axis([0 1000 0 200]);
       #continuarlgc e uma variavel logica vai ser util mais a frente 
       #mas serve para continuar o jogo após cada rodada
       continuarlgc = true;
  
       while 2
         #Esse próximo if é uma rodada
         if continuarlgc == true;
           #Seleciona qual sera a gravidade usada
           grav = questdlg('quer jogar na Terra, Lua ou Marte?','Escolha do terreno','Terra','Lua','Marte','Terra');
           switch grav
             case 'Terra'
               g = 9.807;
             case 'Lua'
               g = 1.62;
             case 'Marte'
               g = 3.711;
           endswitch
          
           #Entra na funcao xtanks que serve para perguntar ao jogadores
           #a posicao de seus tanques 
           [x_tank] = xtanks(QtdJogadores,jogadores);        
           for c = 1:QtdJogadores
             infojog(c).x = x_tank{c};
          endfor
          
           #jogador e mortos sao importantes para respectivamente
           #definir quem vai atirar e quantos estao mortos
           jogador = 1;
           mortos = 0;
         
           #'Rescussita' os jogadores após cada rodada
           for c = 1:QtdJogadores
             infojog(c).dead = 0;
           endfor
         
           #Desenha os tanques e os nomes dos jogadores
           clf;         
           for c = [1:QtdJogadores]           
             tank(str2num(infojog(c).x),0,infojog(c).cor);
             text(str2num(infojog(c).x),20,infojog(c).nome,'color',infojog(c).cor);
           endfor    
        
           while 3 #Controle da rodada
             while 4 #Controle do tiro atual
               if infojog(jogador).dead == 0;
                 h = msgbox({'Tiro de ',infojog(jogador).nome});
                 uiwait(h);              
                 [v0 alpha] = dadostiro();                
                 
                 #Desenha de novo os tannques a cada tiro porem
                 #agora nao desenha quem foi atingido 
                 clf;              
                 for c = [1:QtdJogadores]
                   if infojog(c).dead == 0
                     tank(str2num(infojog(c).x),0,infojog(c).cor);
                     text(str2num(infojog(c).x),20,infojog(c).nome,'color',infojog(c).cor);
                   endif
                 endfor
                                
                 #'x' e uma variavel para determinar a posicao inicial do tiro
                 #que e a posicao do tanque + 5 p/ o tiro sair do meio do tanque               
                 x = str2num(infojog(jogador).x) + 5;
                 #Entra na funcao que vai de fato atirar
                 xf = projetil(x,v0,alpha,g,infojog(jogador).cor);             
                 [infojog morte] = checktiro(xf,infojog,jogador);        
                 
                 y = 180;
                 for c = [1:QtdJogadores]
                   placar = strcat(infojog(c).nome,':',num2str(infojog(c).pontos));
                   text(750,y,placar,'color','k');
                   y -= 8;
                 endfor
                 if morte == true
                   mortos += 1;
                 endif
                
                 #Verifica se soboru só um vivo, se sim fala que ele ganhou a rodada               
                 if QtdJogadores - 1 == mortos
                   for c = 1:QtdJogadores
                     if infojog(c).dead == 0
                       h = msgbox({infojog(c).nome,'venceu essa rodada'});
                       uiwait(h);
                       fimrod = true;
                       break
                     endif
                   endfor
                   break
                 endif
               endif
                  
               #Depois de cada tiro passa para o proximo jogador
               #ou reseta para um para acertar a vez de quem esta jogando
               if jogador == QtdJogadores
                 jogador = 1;
               else
                jogador += 1;
               endif        
             endwhile
               
             if fimrod == true
               continuar = questdlg('Continuar?','Continuar o jogo','Sim','Nao','Sim');
               if continuar == 'Sim'
                 continuarlgc = true;
               elseif continuar == 'Nao'
                 [vencedores pontuacao] = CalculoPontos(infojog,QtdJogadores);
                 #Checa se houve empate e permite que os jogadores continuem o
                 #jogo ou acabem em um empate
                 if length(vencedores) > 1
                   fimEmpate = questdlg({'Houve um empate entre',vencedores.nomes,'Quer encerrar o jogo mesmo assim?'},'Empate','Sim','Nao','Sim');
                   switch (fimEmpate)
                     case 'Sim'
                       empate = true;
                       continuarlgc = false;
                   case 'Nao'
                       empate = false;
                       continuarlgc = true;
                   endswitch
                 else
                   empate = false;
                   continuarlgc = false;
                 endif
               endif
               break
             endif
           endwhile      
         else
           break        
         endif  
       endwhile
       
       #Confere quem fez mais pontos e mostra que ele foi o vencedor       
       [vencedores pontuacao] =  CalculoPontos(infojog,QtdJogadores);    
       if empate == false
         texto = strcat('O(A) Vencedor(a):',vencedores(1).nomes);
         h = msgbox({texto,strcat(num2str(pontuacao),' pontos')})
         uiwait(h);
       else         
         pontuacaofinal = strcat(pontuacao,'pontos');
         h = msgbox({'Vencedor(es)',vencedores.nomes,pontuacaofinal});
         uiwait(h);
       endif
       break
     endwhile
   case 'Sair'
     h = msgbox('Obg por jogar. Espero que tenha se divertido')
     uiwait(h)
     break
 endswitch
endwhile
## Begin savepath auto-created section, do not edit
## End savepath auto-created section
