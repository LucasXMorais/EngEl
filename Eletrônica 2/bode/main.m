% ==========================================================================
%
%          CONSTRUÇÃO DE FILTRO ATIVO A PARTIR DE AMAX E AMIN
%
% O seguinte script foi montado para proporcionar um circuito baseado em amax e amin.
% O programa utiliza uma função própria de diagrama de bode cirada pelo autor.
% A fim de evitar conflitos com o pacote de controle do octave, a função capaz
% de executar o diagrama de bode foi denominada bodeS.
% Para utilizar a função bodeS, basta entrar com uma função onde o 
% único parâmetro passado funcionaria como 's' de um função de transferência.
% Essa função de transferência pode ser uma função anônima ou uma função comum.
% 
% Autor: Lucas Xavier de Morais - 190950011
% Data: 28/06/23
% 
% ==========================================================================

clear all; close all; clc; clf;

function ret = sPrim(wn) %Função para gerar a string de primeira ordem
  ret = strcat('(s+(' , num2str(wn) , '))' );
endfunction

function ret = sSeg(wn, csi) %Função para gerar a string de segunda ordem
  ret = strcat('(s^2+(' , num2str(2*csi*wn) , ')*s+(' , num2str(wn^2) , '))');
endfunction

function ret = bodeS(H) %Função para calcular o bode que retorna os módulos, fase e domínio do diagrama de bode dada uma função de transferência
  ret.omegas = logspace(-2, 8, 100000);

  ret.modules = ones(1,length(ret.omegas));
  ret.angles = ones(1,length(ret.omegas));

  for i = [1:length(ret.omegas)]
    w = ret.omegas(i);
    s = j*w;
    aux = H(s);
    ret.modules(i) = 20*log10(abs(aux));
    ret.angles(i) = angle(aux);
  endfor
endfunction

function ret = getCsis(polos) %Função retorna uma lista com os csis dado uma lista de polos
  for p = [1:length(polos)]
    ret(p) = abs(atan(real(polos(p)) / abs(polos(p))));
  endfor
endfunction

% Simples validação de entrada de dados. Há a opção do usuário utilizar os valores padrões para facilitar os testes 
% do código, permitindo mais facilmente alterar o tipo e arquitetura do filtro.
while 1 
    try 
      %Entrada de dados
      default = input('Usar valores padrao? 1 - Sim, 2 - Nao'); 
      if (default == 1) 
        % Valores padrões para facilitar os testes.
        amax = 1
        amin = 25
        fp = 10000
        wp = 2*pi*fp
        fs = 15000
        ws = 2*pi*fs
        ganho = 1
        while 1 % Permitindo ao usuário a escolha do tipo e arquitetura do filtro com uma validação de dados simples.
          try 
            tipo = input('Qual o tipo de filtro: 1 - Butterworth ; 2 - Chebyschev : ' );
            arquitetura = input('Qual a arquitetura: 1 - Sallem-Key ; 2 - MFB : ' );
            break
          catch
            printf('Valores invalidos!\n');
          end_try_catch
        endwhile
        break 
      endif

      % Entradas de dados
      amax = input('Amax [db] = ');
      amin = input('Amin [db] = ');
      fp = input('fp [Hz] = ');
      wp = 2*pi*fp;
      fs = input('fs [Hz] = ');
      ws = 2*pi*fs;
      ganho = input('Ganho K [V/V] = ');
      tipo = input('Qual o tipo de filtro: 1 - Butterworth ; 2 - Chebyschev : ' );
      arquitetura = input('Qual a arquitetura: 1 - Sallem-Key ; 2 - MFB : ' );
      break
    catch
      printf('Valores invalidos!\n');
    end_try_catch
endwhile

%Cálculo de epsilon
epsilon = sqrt( (10^(amax/10)) - 1 );

switch tipo
  case 1 % Butterworth
    ordem = ceil( (log10(((10^(amin/10)) - 1) / (epsilon^2))) / ( 2*log10(fs/fp) ) );

    w0 = wp*((1/epsilon)^(1/ordem));
    angulos = [ pi/(2*ordem) : pi/ordem : (pi/2)]; % Gerando uma lista com os ângulos dos primeiros polos antes dos conjugados
    for p = [1:length(angulos)] %Cálculo dos polos a partir dos ângulos
      polos(p) = w0*( (-sin(angulos(p))) + (j*cos(angulos(p))) );
    endfor

    % Inicia o processo do cáclulo do diagrama de bode, primeiro fazendo do polo de primeira ordem separado
    csis = getCsis(polos); %Gera os csis

    funcStr = ""; % Gerando a função de transferência através de uma string
    if (floor(ordem/2) != ordem/2) 
      funcStr = strcat("(",sPrim(polos(end)));
    else 
      funcStr = ("(1");
    endif

    for i = [1:length(polos)-1] % diagrama de bode para os polos conjugados
      funcStr = strcat(funcStr , "*" ,sSeg(w0, csis(i)));
    endfor

    % Transforma a função de transfrência de string para um função anônima capaz de funcionar com o bode
    funcStr = strcat("@(s)",num2str(ganho*(w0^ordem)), '/', funcStr, ")"); 
    T = str2func(funcStr);

    bodes = bodeS(T);

  case 2 % Chebyschev
    ordem = ceil( acosh(sqrt(((10^(amin/10)) - 1) / (epsilon^2))) / acosh(fs/fp));

    for p = [1:ceil(ordem/2)] %Cálculo dos polos do modelo de Chebyschev
      A = (((2*p)-1)/ordem)*(pi/2);
      B = (1/ordem)*asinh(1/epsilon);
      polos(p) = (-wp*sin(A)*sinh(B)) + (j*wp*cos(A)*cosh(B));

    endfor

    csis = getCsis(polos); %Gera os csis

    % Inicia o processo do cáclulo do diagrama de bode, primeiro fazendo do polo de primeira ordem separado
    funcStr = ""; % Gerando a função de transferência através de uma string
    if (floor(ordem/2) != ordem/2) 
      funcStr = strcat("(",sPrim(polos(end)));
    else 
      funcStr = ("(1");
    endif

    for i = [1:length(polos)-1] % diagrama de bode para os polos conjugados
      funcStr = strcat(funcStr , "*" ,sSeg(abs(polos(i)), csis(i)));
    endfor

    % Transforma a função de transfrência de string para um função anônima capaz de funcionar com o bode
    funcStr = strcat("@(s)",num2str(ganho*(wp^ordem)/(epsilon*(2^(ordem-1)))), '/', funcStr, ")"); 
    T = str2func(funcStr);

    bodes = bodeS(T);

  otherwise
    disp('Erro! Tipo invalido');
endswitch

circuito = [];
%Definição do ganho por estágio
if (ganho == 1) 
  ganhoEstagio = 1;
else 
  if (floor(ordem/2) != ordem/2) %Verifica se o número de polos é par ou ímpar 
    ganhoEstagio = ( (k^(2/(ordem-1))) );
  else
    ganhoEstagio = ( (k^(2/(ordem))) );
  endif 
endif

switch arquitetura
  case 1 %Sallem-Key

    for i = [1:length(csis)-1]
      umMenosGanho = 1 - ganhoEstagio;
      %Cálculo de n
      Q = 1 / (2*csis(i));
      Q24 = 4*(Q^2);
      n = (Q24) / (1 - (Q24*umMenosGanho));
      n = 1.25*n; %Aplicando o fator de segurança para n;

      if (ganho != 1) %Checando a segunda condição para n
          aux = (-1) / umMenosGanho;
          if (n != aux) n *= 1.05; endif %Aumentar mais 5%
      endif

      %Cálculo de m
      a = 1 + ( 2*n*umMenosGanho ) + ( n*umMenosGanho )^2;
      b = 2 + ( 2*n*umMenosGanho ) - (n/(Q^2));
      raizDeDelta = sqrt((b^2) - (4*a));
      m1 = ((-b) + raizDeDelta) / (2*a);
      m2 = ((-b) - raizDeDelta) / (2*a);
      m = m1;
      if (m2 > m1) m = m2; endif

      %Cálculo dos capacitores
      circuito(i).c2 = 10^(-8); %Capacitor c2 de 10nF
      circuito(i).c1 = n*circuito(i).c2; %Capacitor c1

      circuito(i).r2 = 1 / ( circuito(i).c2*abs(polos(i))*sqrt(m*n) ); %Resistor r2
      circuito(i).r1 = m*circuito(i).r2; %Resistor r1

      circuito(i).c = 0; circuito(i).r = 0; circuito(i).r3 = 0;
    endfor 

    imgArqPath = 'bloco_2_ord_SK.png'; % Marcador para identificar e depois abrir a imagem da arquitetura correta

  case 2 %MFB

    ganhoEstagio = -ganhoEstagio;
    for i = [1:length(csis)-1]
      umMenosGanho = 1 - ganhoEstagio;
      %Cálculo de n
      Q = 1 / (2*csis(i));
      n = (4*(Q^2))*umMenosGanho;
      n = 1.25*n; %Aplicando o fator de segurança para n;

      %Cálculo de m
      a = umMenosGanho^2;
      b = ( 2*umMenosGanho ) - (n/(Q^2));
      raizDeDelta = sqrt((b^2) - (4*a));
      m1 = ((-b) + raizDeDelta) / (2*a);
      m2 = ((-b) - raizDeDelta) / (2*a);
      m = m1;
      if (m2 > m1) m = m2; endif

      %Cálculo dos capacitores
      circuito(i).c2 = 10^(-8); %Capacitor c2 de 10nF
      circuito(i).c1 = n*circuito(i).c2; %Capacitor c1

      circuito(i).r2 = 1 / ( circuito(i).c2*abs(polos(i))*sqrt(m*n) ); %Resistor r2
      circuito(i).r3 = m*circuito(i).r2; %Resistor r3
      circuito(i).r1 = (-circuito(i).r2) / ganhoEstagio; %Resistor r1

      circuito(i).c = 0; circuito(i).r = 0;
    endfor 
    
    imgArqPath = 'bloco_2_ord_MFB.png'; % Marcador para identificar e depois abrir a imagem da arquitetura correta

  otherwise
    disp('Erro! Arquitetura invalida');
endswitch

%Plot do diagrama de bode
figure(1, "name", "Diagrama de Bode");
subplot (2, 1, 1)
semilogx(bodes.omegas, bodes.modules);
title('Módulo');
subplot (2, 1, 2)
semilogx(bodes.omegas, bodes.angles);
title('Fase');

%String que mostra a função de transferência 
numerador = funcStr(1:(index(funcStr,'/')-1));
denominador = funcStr((index(funcStr,'/')+1):end);
disp(''); disp('FUNCAO DE TRANSFERENCIA'); disp(''); disp(funcStr);
%disp(numerador),disp('---------------------------'),disp(denominador);

%Estágio de primeira ordem com ganho unitário
circuito(end+1).c = 10^(-8);
circuito(end).r = 1 / (abs(polos(end))*circuito(end).c);
circuito(end).r1 = 0; circuito(end).r2 = 0; circuito(end).r3 = 0;
circuito(end).c1 = 0; circuito(end).c2 = 0;

% Mostrando os módulos para o circuito
printf('\n ========================= \n');
printf('O circuito deverá ser montado a partir dos valores de componentes citados a seguir.\n');
printf('Cada estágio está descrito baseado em sua ordem.\n');
printf('O estágio de primeira ordem possui 1 resistor e 1 capacitor, dispostos conforme a figura titulada "Estágio de Primeira Ordem".\n');
printf('O estágio de segunda ordem possui 3 resistores e 2 capacitores dispostos conforme a figura titulada "Estágio de Segunda Ordem".\n');

figure(2, "name", " Estágio de Primeira Ordem");
imshow('primeira_ordem.png');
figure(3, "name", " Estágio de Segunda Ordem");
imshow(imgArqPath);

% Mostrando os componentes por estágio
estg = 1;
for i = circuito
  printf('Estagio %d\n',estg);
  if estg == length(circuito) 
    fprintf('Estagio de primeira ordem\n');
    fprintf('R = %e e C = %e\n', i.r, i.c);
  else
    fprintf('Estagio de segunda ordem\n');
    if arquitetura == 1
      fprintf('R1 = %f , R2 = %f\n', i.r1, i.r2);
    else
      fprintf('R1 = %f , R2 = %f , R3 = %f\n', i.r1, i.r2, i.r3);
    endif
    fprintf('C1 = %e , C2 = %e\n', i.c1, i.c2);
  endif
  estg += 1;
endfor