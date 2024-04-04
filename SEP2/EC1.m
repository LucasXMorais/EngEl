close all
clc
clear all
%% Abrindo o .txt e lendo o arquivo
Sb = 100;
filename = 'dados_sistema12B_EC1.txt';
arq = fopen(filename,'r');

i=1;

linha=fgetl(arq);

if(linha(1,1:4)=='DBAR')
  linha=fgetl(arq);
  linha=fgetl(arq);
  linha=fgetl(arq);
  while(linha(1,1:4)~='####')
    BARRA(i)=str2num(linha(1,1:5)); % Numero das barras
    PD(i)=str2num(linha(1,7:13));   % Potencia ativa da carga
    QD(i)=str2num(linha(1,15:21));  % Potencia reativa da carga
    Bsh(i)=str2num(linha(1,23:29)); % Susceptancia shunt
    if(linha(1,34:35)=='SW')
      TIPO(i)=1;            %1 se a barra for refer�ncia
    elseif (linha(1,34:35)=='PV')
      TIPO(i)=2;            %2 se a barra for PV
    elseif (linha(1,34:35)=='PQ')
      TIPO(i)=3;            %3 se a barra for PQ
    end
    Vesp(i)=str2num(linha(1,37:44));      % Tensao na barra
    Tetaesp(i)=str2num(linha(1,46:53));   % Defasagem na barra
    PGesp(i)=str2num(linha(1,55:63));     % Potencia ativa gerada
    CustoProd(i)=str2num(linha(1,65:73)); % Custo de producao
    CapGerMin(i)=str2num(linha(1,75:83)); % Capacidade de gera��o minima de pot�ncia ativa na barra
    CapGerMax(i)=str2num(linha(1,85:93)); % Capacidade de gera��o m�xima de pot�ncia ativa na barra
    i=i+1;
    linha=fgetl(arq);
  end
end

i=1;
linha=fgetl(arq); linha=fgetl(arq);
if(linha(1,1:4)=='DCIR')
  linha=fgetl(arq); linha=fgetl(arq);
  linha=fgetl(arq);
  while(linha(1,1:4)~='####')
    BDE(i)=str2num(linha(1,1:5));     % Barra de origem
    BPARA(i)=str2num(linha(1,8:12));  % Barra de destino
    NCIR(i)=str2num(linha(1,16:18));  % Numero do circuito
    RES(i)=str2num(linha(1,21:27));   % Resistencia
    REAT(i)=str2num(linha(1,30:36));  % Reatancia
    SUCsh(i)=str2num(linha(1,40:46)); % Susceptancia Shunt
    TAP(i)=str2num(linha(1,51:55));   % Tap do transformador
    DEF(i)=str2num(linha(1,58:66));   % Defasagem em graus
    if(linha(1,79)=='D')              % An�lise se a linha est� ligada ou desligada
      LIGDESL(i)=0;                   % Para a barra desligada valor 0
    elseif(linha(1,79)=='L')          % Para a barra desligada svalor 1
      LIGDESL(i)=1;
    end
    CAP(i)=str2num(linha(1,84:89));   % Capacidade de pot�ncia na barra
    i=i+1;
    linha=fgetl(arq);
  end
end
fclose(arq);

% Transferindo os dados lidos para matrizes
DBAR = [BARRA' PD' QD' Bsh' TIPO' Vesp' Tetaesp' PGesp' CustoProd' CapGerMin' CapGerMax'];
DCIR = [BDE' BPARA' NCIR' RES' REAT' SUCsh' TAP' DEF' LIGDESL' CAP'];

% Verificando quais linhas estao ligadas
linhas_ligadas = find(DCIR(:,9)==1);
DCIR = DCIR(linhas_ligadas,1:10);

% Transformando graus para radianos
DBAR(:,7) = deg2rad(DBAR(:,7));
DCIR(:,8) = deg2rad(DCIR(:,8));

% Numero de Barras e Linhas
nbus = length(DBAR);
nlin = length(DCIR);

% Definindo os Circuitos
DE = DCIR(:,1);
PARA = DCIR(:,2);

% Definindo os elementos de Ybus
rkm = DCIR(:,4);
xkm = DCIR(:,5);
akm = DCIR(:,7);
phikm = DCIR(:,8);
bshkm = DCIR(:,6)./2;
bksh = DBAR(:,4)

%% Matriz Admit�ncia
Ybus = zeros(nbus,nbus); % Inicilizando Ybus
for i = 1:nlin
    k = DE(i);
    m = PARA(i);

    ykm = 1/(rkm(i)+1j*xkm(i));

    Ybus(k, k) = Ybus(k, k) + (akm(i)^2)*ykm + 1j*bshkm(i);
    Ybus(m, m) = Ybus(m, m) + ykm + 1j*bshkm(i);
    Ybus(k, m) = Ybus(k, m) - akm(i)*ykm*(cos(-phikm(i)) + 1j*sin(-phikm(i)));
    Ybus(m, k) = Ybus(m, k) - akm(i)*ykm*(cos(+phikm(i)) + 1j*sin(+phikm(i)));
end
for k = 1 : nbus
 Ybus(k, k) = Ybus(k, k) + 1j*bksh(k);
end

Ybus(10,10)

G = real(Ybus);
B = imag(Ybus);

%% Inicializando o Metodo de Newton Raphson
% Inicialiazando as matrizes com os tipos de barras
% Chutes Iniciais
for i = 1:length(DBAR(:,7))
    if DBAR(i,5) ~= 1 % Mudando o valor de theta nas barras PQ e PV
        DBAR(i,7) = 0; % Valor de Theta
    end

    if DBAR(i,5) == 3 % Mudando o valor de theta nas barras PQ
        DBAR(i,6) = 1; % Valor de V
    end
end

% Calculando o Pesp para primeira itera��o
for k = 1:nbus
    total = 0;
    for m = 1:nbus
        soma = DBAR(m,6)*(G(k,m)*cos(DBAR(k,7)-DBAR(m,7))+B(k,m)*sin(DBAR(k,7)-DBAR(m,7)));
        total = total + soma;
    end
    Pesp(k) = DBAR(k,6)*total;
    total = 0;
end

% Calculando o Qesp para primeira itera��o
for k = 1:nbus
    total = 0;
    for m = 1:nbus
        soma = DBAR(m,6)*(G(k,m)*sin(DBAR(k,7)-DBAR(m,7))-B(k,m)*cos(DBAR(k,7)-DBAR(m,7)));
        total = total + soma;
    end
    Qesp(k) = DBAR(k,6)*total;
end

% Encontrando a varia��o de delta P e Q
DeltaP = DBAR(:,8)-DBAR(:,2)- Pesp';
DeltaQ = -DBAR(:,3)- Qesp';
%Montando o vetor com os valores de DeltaP e DeltaQ para usar no Newton
%Raphson
DeltaPQ = [DeltaP ; DeltaQ];

% Considerando uma tolerancia para o metodo de Newton Raphson
tolerancia = 10^-30;

%% M�todo de Newton Raphson
iter = 1;
while abs(max(DeltaPQ))>tolerancia

    % Montando a jacobiana
    % Calculando H
    for k=1:nbus
        total = 0;
        for m = 1:nbus
            H(k,m) = DBAR(k,6)*DBAR(m,6)*(G(k,m)*sin(DBAR(k,7)-DBAR(m,7))- B(k,m)*cos(DBAR(k,7)-DBAR(m,7)));
            soma = DBAR(m,6)*(G(k,m)*sin(DBAR(k,7)-DBAR(m,7))- B(k,m)*cos(DBAR(k,7)-DBAR(m,7)));
            total = soma + total;
        end
        H(k,k) = -DBAR(k,6)^2*B(k,k)- DBAR(k,6)*total;
    end

    % Calculando N
    for k=1:nbus
        total = 0;
        for m = 1:nbus
            N(k,m) = DBAR(k,6)*(G(k,m)*cos(DBAR(k,7)-DBAR(m,7))+ B(k,m)*sin(DBAR(k,7)-DBAR(m,7)));
            soma = DBAR(m,6)*(G(k,m)*cos(DBAR(k,7)-DBAR(m,7))+ B(k,m)*sin(DBAR(k,7)-DBAR(m,7)));
            total = soma + total;
        end
        N(k,k) = DBAR(k,6)*G(k,k)+ total;
    end

    % Calculando M
    for k=1:nbus
        total = 0;
        for m = 1:nbus
            M(k,m) = -DBAR(k,6)*DBAR(m,6)*(G(k,m)*cos(DBAR(k,7)-DBAR(m,7))+ B(k,m)*sin(DBAR(k,7)-DBAR(m,7)));
            soma = DBAR(m,6)*(G(k,m)*cos(DBAR(k,7)-DBAR(m,7))+ B(k,m)*sin(DBAR(k,7)-DBAR(m,7)));
            total = soma + total;
        end
        M(k,k) = -DBAR(k,6)^2*G(k,k)+ DBAR(k,6)*total;
    end

    % Calculando L
    for k=1:nbus
        total = 0;
        for m = 1:nbus
            L(k,m) = DBAR(k,6)*(G(k,m)*sin(DBAR(k,7)-DBAR(m,7))- B(k,m)*cos(DBAR(k,7)-DBAR(m,7)));
            soma = DBAR(m,6)*(G(k,m)*sin(DBAR(k,7)-DBAR(m,7))- B(k,m)*cos(DBAR(k,7)-DBAR(m,7)));
            total = soma + total;
        end
        L(k,k) = -DBAR(k,6)*B(k,k)+ total;
    end

    % Antes de montar a Jacobiana deve tratar das matrizes para que elas
    % Recebam os valores corretos
    for k= 1:nbus
        for m =1:nbus
            if DBAR(k,5)~= 3
                L(k,m) = 0;
                L(m,k) = 0;
                N(m,k) = 0;
                M(k,m) = 0;
            end
            if DBAR(k,5)== 1
                H(k,m) = 0;
                H(m,k) = 0;
                M(m,k) = 0;
                N(k,m) = 0;
            end
        end
    end

  for k= 1:nbus
     if DBAR(k,5)~= 3
        L(k,k) = 10^20;
     end
     if DBAR(k,5)== 1
        H(k,k) = 10^20;
     end
  end

    % Encontrando a jacobiana
    J=[H N; M L];

    % Calculando x e delta x
    x = [DBAR(:,7);DBAR(:,6)];
    Deltax = inv(J)*DeltaPQ;
    x = x + Deltax;

    % Modificando os valores de Theta e V na matriz de valores
    DBAR(:,7) = x(1:nbus,1);
    DBAR(:,6) = x(nbus+1:2*nbus,1);

    % Recalculando o delta pq
    for k = 1:nbus
        total = 0;
        for m = 1:nbus
          soma = DBAR(m,6)*(G(k,m)*cos(DBAR(k,7)-DBAR(m,7))+B(k,m)*sin(DBAR(k,7)-DBAR(m,7)));
           total = total + soma;
        end
        Pesp(k) = DBAR(k,6)*total;
    end

    for k = 1:nbus
        total = 0;
     for m = 1:nbus
         soma = DBAR(m,6)*(G(k,m)*sin(DBAR(k,7)-DBAR(m,7))-B(k,m)*cos(DBAR(k,7)-DBAR(m,7)));
          total = total + soma;
     end
     Qesp(k) = DBAR(k,6)*total;
    end

    DeltaP =DBAR(:,8)-DBAR(:,2)- Pesp';
    DeltaQ = -DBAR(:,3)- Qesp';

    % Excluindo de Delta P o m�dulo da barra SW
    % Excluindo de Delta Q o m�dulo das barras PV e SW
    for i=1:nbus
        if DBAR(i,5)~=3
            DeltaQ(i) = 0;
        end
        if DBAR(i,5)== 1
            DeltaP(i)=0;
        end
    end
    DeltaPQ = [DeltaP ; DeltaQ];
    iter = iter + 1;
    if iter >= 30
        break
    end
end
%% Calculando o fluxo de pot�ncia

for i=1:nlin
    k = DE(i);
    m = PARA(i);
    ykm = 1/(rkm(i)+1j*xkm(i));
    gkm = real(ykm);
    bkm = imag(ykm);
    Pkm(i) = ((akm(i)*DBAR(k,6))^2)*gkm -(akm(i)*DBAR(k,6))*DBAR(m,6)*gkm*cos(DBAR(k,7)-DBAR(m,7)+phikm(i))...
        -(akm(i)*DBAR(k,6))*DBAR(m,6)*bkm*sin(DBAR(k,7)-DBAR(m,7)+phikm(i));
    Pmk(i) = (DBAR(m,6)^2)*gkm -(akm(i)*DBAR(k,6))*DBAR(m,6)*gkm*cos(DBAR(m,7)-DBAR(k,7)-phikm(i))...
        -(akm(i)*DBAR(k,6))*DBAR(m,6)*bkm*sin(DBAR(m,7)-DBAR(k,7)-phikm(i));
    Qkm(i)=-((akm(i)*DBAR(k,6))^2)*(bkm + bshkm(i))+(akm(i)*DBAR(k,6))*DBAR(m,6)*bkm*cos(DBAR(k,7)-DBAR(m,7)+phikm(i))...
        -(akm(i)*DBAR(k,6))*DBAR(m,6)*gkm*sin(DBAR(k,7)-DBAR(m,7)+phikm(i));
    Qmk(i)=-((DBAR(m,6))^2)*(bkm + bshkm(i))+(akm(i)*DBAR(k,6))*DBAR(m,6)*bkm*cos(DBAR(m,7)-DBAR(k,7)-phikm(i))...
        -(akm(i)*DBAR(k,6))*DBAR(m,6)*gkm*sin(DBAR(m,7)-DBAR(k,7)-phikm(i));
end

% Calculando as perdas ativas e reativas
PerdasP = Pkm + Pmk;
PerdasQ = Qkm + Qmk;

% Potencia S
for i = 1:nlin
    Skm(i) = sqrt(Pkm(i).^2+Qkm(i).^2);
    Smk(i) = sqrt(Pmk(i).^2+Qmk(i).^2);
end

% Calculando as perdas ativas e reativas totais
PerdasPtot = sum(PerdasP);
PerdasQtot = sum(PerdasQ);
Pger = DBAR(:,2)+Pesp';
Qger = DBAR(:,3)+Qesp';

for i = 1:nbus
    Sger(i) = abs(Pger(i)+1j*Qger(i));
end
%% Imprimindo os resultados na tela
DBAR(:,7) = rad2deg(DBAR(:,7));
% fid = 1 % Mostra os resultados na tela
fid = fopen('resultadosData2.txt','wt'); % Exporta os resultados para um .txt
fprintf(fid,'%s\n\n','####################################################################################');
fprintf(fid,'%s\n','                    UNIVERSIDADE FEDERAL DE SAO JOAO DEL REI');
fprintf(fid,'%s\n\n','                  DISCIPLINA DE SISTEMAS ELETRICOS DE POTENCIA II');
fprintf(fid,'%s\n\n','####################################################################################');
fprintf(fid,'%s\n','        Grupo: Matheus de Souza Fulgencio           - Matricula: 170900039');
fprintf(fid,'%s\n','               Pedro Duque Thomaz Mour�o Elias      - Matricula: 180900026');
fprintf(fid,'%s\n\n','               Pedro Lucas Carvalho Reis e Guimares - Matricula: 170900013');
fprintf(fid,'%s\n\n','####################################################################################');
fprintf(fid,'%s\n','                                Relat�rio das Barras');
fprintf(fid,'%s\n','-----------------------------------------------------------------------------------------------');
fprintf(fid,'%s\n','Barra  Tensao    Theta      Pi         Qi        PG        QG        SG        PD        QD');
fprintf(fid,'%s\n','        (pu)    (graus)    (MW)      (MVAr)     (MW)     (MVAr)     (MVA)     (MW)     (MVAr)')
fprintf(fid,'%s\n','-----------------------------------------------------------------------------------------------');
for i = 1:nbus
fprintf(fid,'%3.1d %9.4f %9.4f %9.4f %9.4f %9.4f %9.4f %9.4f %9.4f %9.4f \n',DBAR(i,1),DBAR(i,6),DBAR(i,7),Pesp(i)*Sb,Qesp(i)*Sb,Pger(i)*Sb,Qger(i)*Sb,Sger(i)*Sb,DBAR(i,2)*Sb,DBAR(i,3)*Sb);
end
fprintf(fid,'%s\n','---------------------------------------------------------------------------------------------------')
fprintf(fid,'Total:                                     %10.4f %9.4f %9.4f %9.4f %9.4f \n',sum(Pger*Sb),sum(Qger*Sb),sum(Sger*Sb),sum(DBAR(:,2)*Sb),sum(DBAR(:,3)*Sb));
fprintf(fid,'%s\n\n','---------------------------------------------------------------------------------------------------');
fprintf(fid,'%s\n','                              Relat�rio dos Circuitos');
fprintf(fid,'%s\n','-----------------------------------------------------------------------------------------------------');
fprintf(fid,'%s\n',' Circuito   Pkm       Qkm       Skm     Circuito   Pmk       Qmk       Smk    Perdas At. Perdas Reat.');
fprintf(fid,'%s\n',' De  Para   (MW)     (MVAr)    (MVA)    De  Para   (MW)     (MVAr)    (MVA)      (MW)      (MVAr)')
fprintf(fid,'%s\n','-----------------------------------------------------------------------------------------------------');
for t = 1:nlin
fprintf(fid,'%3.1d %3.1d %9.4f %9.4f %9.4f  %3.1d %3.1d %9.4f %9.4f %9.4f %9.4f %11.4f\n',DCIR(t,1),DCIR(t,2),Pkm(t)*Sb,Qkm(t)*Sb,Skm(t)*Sb,DCIR(t,2),DCIR(t,1),Pmk(t)*Sb,Qmk(t)*Sb,Smk(t)*Sb,PerdasP(t)*Sb,PerdasQ(t)*Sb);
end
fprintf(fid,'%s\n','-----------------------------------------------------------------------------------------------------');
fprintf(fid,'Total de Perdas:                                                             %9.4f   %9.4f\n',PerdasPtot*Sb,PerdasQtot*Sb);
fprintf(fid,'%s\n\n','-----------------------------------------------------------------------------------------------------');
fprintf(fid,'%s\n','An�lise de Pot�ncia nas Barras');
fprintf(fid,'%s\n','-------------------------------');
fprintf(fid,'%s\n','Barra   PG       CGmax');
fprintf(fid,'%s\n','       (pu)      (pu)');
fprintf(fid,'%s\n','-------------------------------');
for t = 1:nbus
fprintf(fid,'%3.1d %9.4f %9.4f\n',DBAR(t,1),Pger(t),DBAR(t,11));
end
fprintf(fid,'%s\n\n','-------------------------------')
fprintf(fid,'%s\n','        An�lise de Pot�ncia nas Linhas');
fprintf(fid,'%s\n','----------------------------------------------');
fprintf(fid,'%s\n','Circuito   Skm      Circuito  Smk       CAP');
fprintf(fid,'%s\n','De  Para   (pu)     De Para   (pu)      (pu)');
fprintf(fid,'%s\n','----------------------------------------------');
for t = 1:nlin
fprintf(fid,'%3.1d %3.1d %9.4f %3.1d %3.1d %10.4f %9.4f\n',DCIR(t,1),DCIR(t,2),Skm(t),DCIR(t,2),DCIR(t,1),Smk(t),DCIR(t,10));
end
fclose(fid);
