close all
clear all
clc

%Item 3, considerando uma carga de 120%
%Leitura de dados
arq = fopen('dados_sistema12B_EC4.txt','r');
linha = fgetl(arq);
var_f=1;
cont=1;
p_base=100;


% Leitura dos dados de barra (Tabela DBAR)
if(linha(1,1:4) == 'DBAR')
    linha = fgetl(arq);
    linha = fgetl(arq);
    linha = fgetl(arq);
    while(linha(1,1:4) != '####')
    BARRA(cont) = str2double(linha(1,1:5));
    PD(cont) = str2double(linha(1,7:14));
    QD(cont) = str2double(linha(1,15:22));
    Bsh(cont) = str2double(linha(1,23:32));
      if(linha(1,34:35) == 'SW')
            TIPO(cont) = 1;
         elseif (linha(1,34:35) == 'PV')
            TIPO(cont) = 2;
         elseif (linha(1,34:35) == 'PQ')
            TIPO(cont) = 3;
       end
     Vesp(cont) = str2double(linha(1,37:49));
     thetaesp(cont) = (pi/180)*(str2double(linha(1,50:57))); %theta esperado em rad
     PGesp(cont) = str2double(linha(1,58:65));
     Cus(cont) = str2double(linha(1,67:73));
     CGMin(cont) = str2double(linha(1,75:83));
     CGMax(cont) = str2double(linha(1,85:93));
     cont = cont + 1;
     linha = fgetl(arq);
     end
end
linha = fgetl(arq);
linha = fgetl(arq);
PD=PD*1.2; % carga de 120% de acordo com o item 3
cont = 1;

% Leitura dos dados dos circuitos
if (linha(1,1:4) == 'DCIR')
    linha = fgetl(arq);
    linha = fgetl(arq);
    linha = fgetl(arq);
    while (linha(1,1:4) ~= '####')
        BDE(cont) = str2double(linha(1,1:6));
        BPARA(cont) = str2double(linha(1,6:13));
        NCIRC(cont) = str2double(linha(1,13:18));
        RES(cont) = str2double(linha(1,20:28));
        REAT(cont) = str2double(linha(1,28:36));
        SUCsh(cont) = str2double(linha(1,36:46));
        TAP(cont) = str2double(linha(1,48:58));
        DEF(cont) = (pi/180)*(str2double(linha(1,59:70))); %Defasagem do trafo em rad
        if (linha(1,79) == 'L')
            LIG_DESL(cont) = 1;
        else
            LIG_DESL(cont) = 0;
        end
        CAP(cont) = str2double(linha(1,81:89)); % capacidade de transmissao de potencia da linha
        cont = cont + 1;
        linha = fgetl(arq);
    end
end
%Número de barras
nbarras = size(BARRA,2);
%Número de circuitos
ncircuitos = size(BDE,2);
%Barras com carga
b_carga=find(PD!=0);
ncarga=size(b_carga,2);
%Número de geradores
ngerador=size(find(TIPO==2),2)+size(find(TIPO==1),2);
b_ger=find(TIPO!=3);
%Número de variáveis do problema
nvariaveis=ngerador+nbarras+ncarga-1;
%Número de restrições de igualdade
nigualdade=nbarras;
%Número de restrições de desigualdade (Limite de geração)
nd_geracao=2*ngerador;
%Número de restrições de desigualdade (Limite de capacidade de fluxo)
nd_fluxo=2*ncircuitos;

%Coeficientes de fx para os valores de theta
for cont1=1:nbarras
 if TIPO(cont1)!=1
    fx(var_f)=0;
    var_f=var_f+1;
    elseif
    ref=cont1;
  endif
endfor

%Acrescentando as potências
for cont1=1:nbarras
 if TIPO(cont1)!=3
    fx(var_f)=Cus(cont1);
    var_f=var_f+1;
  endif
endfor

%Acrescentando as cargas
for cont1=1:nbarras
 if PD(cont1)>0
    fx(var_f)=100;
    var_f=var_f+1;
  endif
endfor


%Cálculo da YBUS
ybus=zeros(nbarras,nbarras);
for ic = 1:ncircuitos
    % Barra na posição k
    k = BDE(ic);
    % Barra na posição m
    m = BPARA(ic);
    % if para pegar somente as barras ligadas
    if LIG_DESL(ic)==1
        % Admitância com resistÊncia
        ykm = 1/(REAT(ic)*i);
        % Elemento da posição k,k
        ybus(k,k) = ybus(k,k) + ykm;
        % Elemeneto da posição k,m
        ybus(k,m) = -ykm + ybus(k,m);
        % Elemento da posição m,k
        ybus(m,k) = -ykm + ybus(m,k);
        % Elemento da posição m,m
        ybus(m,m) = ybus(m,m) + ykm ;
    endif
end

gbus = real(ybus);  %Matriz condutância
bbus = imag(ybus);  %Matriz susceptância
eq_p=zeros(nbarras,nbarras+ngerador);

%Coeficientes das restrições de igualdade (theta)
for barra=1:nbarras
      for cont1=1:ncircuitos
        if BDE(cont1)==barra
          eq_p(barra,BDE(cont1))=-(1/REAT(cont1))+eq_p(barra,BDE(cont1));
          eq_p(barra,BPARA(cont1))=(1/REAT(cont1))+eq_p(barra,BPARA(cont1));

        endif
        if BPARA(cont1)==barra
        eq_p(barra,BPARA(cont1))=-(1/REAT(cont1))+eq_p(barra,BPARA(cont1));
          eq_p(barra,BDE(cont1))=(1/REAT(cont1))+eq_p(barra,BDE(cont1));
        endif
      endfor
endfor
eq_p=[eq_p zeros(nbarras,ncarga)];
cont2=ngerador+nbarras+1;
for cont1=1:nbarras
  if PD(cont1)!=0
    eq_p(cont1,cont2)=1;
    cont2=cont2+1;
  endif
endfor
%Coeficientes das restrições de igualdade (potência)
%For para retirar a coluna da barra de referência e acrescentar a potência gerada
a=nbarras+1;
for cont1=1:nbarras
  if TIPO(cont1)!=3
    eq_p(cont1,a)=1;
    a=1+a;
  endif
endfor
    if ref==1
    coef_ig=eq_p(:,2:nbarras+ngerador+ncarga);
  elseif
    coef_ig=[eq_p(:,(1:ref-1)) eq_p(:,(ref+1:nbarras+ngerador+ncarga))];
  endif
b=PD';

%Restrições de desigualdade - Limite de geração
eq_des=zeros(nd_geracao+nd_fluxo,nbarras+ngerador);

a=nbarras+1;
for cont1=1:2:2*ngerador
    eq_des(cont1,a)=1;
    eq_des(cont1+1,a)=-1;
    a=1+a;
endfor
b2=[];
for cont1=1:nbarras
  if TIPO(cont1)!=3
    b2=[b2;CGMax(cont1)];
    b2=[b2;CGMin(cont1)];
   endif
endfor

for cont1=1:ncircuitos
   b2=[b2;CAP(cont1)];
   b2=[b2;CAP(cont1)];
endfor
cont1=1;
a=0;
for barra=(2*ngerador+1):2:nd_geracao+nd_fluxo
     eq_des(barra,BDE(cont1))=(1/REAT(cont1));
     eq_des(barra,BPARA(cont1))=-(1/REAT(cont1));
     eq_des(barra+1,BDE(cont1))=-eq_des(barra,BDE(cont1));
     eq_des(barra+1,BPARA(cont1))=-eq_des(barra,BPARA(cont1));
     cont1=cont1+1;
endfor
if ref==1
    coef_des=eq_des(:,2:nbarras+ngerador);
  elseif
    coef_des=[eq_des(:,(1:ref-1)) eq_des(:,(ref+1:nbarras+ngerador))];
endif
coef_des=[coef_des zeros((nd_geracao+nd_fluxo),ncarga)];
A=[coef_ig;coef_des];
b=[b;b2];

ctype='S';
for cont1=1:size(coef_ig,1)-1
ctype=[ctype 'S'];
endfor
for cont1=1:size(coef_des,1)
ctype=[ctype 'U'];
endfor

vartype='C';
for cont1=1:nvariaveis-1
  vartype=[vartype 'C'];
endfor

%Para minimizar a função fx
s=1;

%Limites inferior e superior
lb=[];
ub=[];
for cont1=1:nbarras-1
lb=[lb;-pi];
ub=[ub;pi];
end
for cont1=1:ngerador
lb=[lb;0];
ub=[ub;inf];
end
for cont1=1:ncarga
lb=[lb;0];
ub=[ub;PD(b_carga(cont1))];
endfor

%Função de solução - Programação linear
[xopt,fopt,ernum,extra]=glpk(fx,A,b,lb,ub,ctype,vartype,s);

for cont1=1:nbarras-1
ang_graus(cont1,1)=xopt(cont1)*180/pi;
endfor

cont2=0;
Pg=zeros(nbarras,1);
%Fluxo DC sem perdas
%Potência gerada com FPO
for cont1=1:nbarras
  if TIPO(cont1)!=3
    Pg(cont1)=xopt(nbarras+cont2);
    cont2=cont2+1;
  endif
endfor
%Potência do corte da carga com FPO
for cont1=1:nbarras
  if PD(cont1)!=0
    Pr(cont1)=xopt(nbarras+cont2);
    cont2=cont2+1;
  endif
endfor


P=Pg-PD'+Pr';
if ref==1
    P_l=P(2:nbarras,1);
endif
if (ref!=1)
    P_l=[P((1:ref-1),:);P((ref+1:nbarras),:)];
endif
if (ref==1)
    B_l=(bbus(2:nbarras,2:nbarras));
endif
if (ref!=1)
    B=([bbus(:,(1:ref-1)) bbus(:,(ref+1:nbarras))]);
    B_l=[B((1:ref-1),:);B((ref+1:nbarras),:)];
endif

cont=1;
theta_DC=-inv(B_l)*P_l;
theta_DC_graus=theta_DC*180/pi;


    for i = 1 : nbarras
        if TIPO(i) ~= 1
            theta_FPO_g(i) = ang_graus(cont);
            theta_dc_r(i)=theta_DC(cont);
            cont = cont +1;
        else
            theta_FPO_g(i) = 0;
            theta_dc_r(i)=0;
        end
    end
%ângulo nas barras
theta_FPO_r=theta_FPO_g*pi/180;
theta_FPO_g;
theta_dc_r;
theta_dc_g=theta_dc_r*180/pi;

%Fluxo de potência em cada circuitos
for i = 1 : ncircuitos
    Pkm(i) = (theta_FPO_r(BDE(i))-theta_FPO_r(BPARA(i)))*(1/REAT(i));
    Pmk(i) = (theta_FPO_r(BPARA(i))-theta_FPO_r(BDE(i)))*(1/REAT(i));
end
%Potência injetada
P=zeros(1,nbarras);
for barra=1:nbarras
      for cont1=1:ncircuitos
        if BDE(cont1)==barra
          P(barra)=(1/REAT(cont1))*(theta_FPO_r(BDE(cont1))-theta_FPO_r(BPARA(cont1)))+P(barra);
        endif
        if BPARA(cont1)==barra
          P(barra)=(1/REAT(cont1))*(theta_FPO_r(BPARA(cont1))-theta_FPO_r(BDE(cont1)))+P(barra);
        endif
      endfor
endfor

fprintf('\n')
disp('=========================================================================================================')
disp('                                    Informações Das Barras')
disp('=========================================================================================================')
disp('  Barra   Ang. DC     Ang. FPO         Pi          PG FPO      PD (inicial)   PD (cortada)')
disp('          (graus)     (graus)         (MW)          (MW)         (MW)            (MW)               ')
disp('=========================================================================================================')
for k = 1 : nbarras
   fprintf('%3d%14.4f%12.4f%14.4f%14.4f%14.4f%14.4f\n', BARRA(k),theta_dc_g(k),theta_FPO_g(k),P(k)*100,Pg(k)*100,PD(k)*100,Pr(k)*100)
end

fprintf('\n')
fprintf('\n')
disp('============================================')
disp('      Informações Dos Circuitos')
disp('============================================')
disp('  De     Para      Pkm          Pmk ')
disp('                    MW           MW')
disp('============================================')
for k = 1 : ncircuitos
fprintf('%3d%8d%13.4f%13.4f\n',BDE(k),BPARA(k), Pkm(k)*100,   100*Pmk(k))
end
fprintf('\n')
fprintf('\n')

custo=fopt*100-100*sum(Pr)*100;

disp('=================================================')
disp('      Custo de geração com a otimização')
disp('=================================================')
fprintf('              $%.3f',custo)
fprintf('\n')
fprintf('\n')
fprintf('\n')

disp('=============================')
disp('      Lambda    ')
disp('=============================')
disp(' Barra      Lambda')
disp('=============================')
for k = 1 :nbarras
   fprintf('%3d%15.3f\n', BARRA(k),extra.lambda(k))
end
fprintf('\n')
fprintf('\n')

disp('=====================================')
disp('         Mi (Geradores)    ')
disp('=====================================')
disp(' Barra      Pg        -Pg')
disp('=====================================')
cont=1;
for k = nbarras+1:2:nd_geracao+nbarras
   fprintf('%4d%12.3f%12.3f\n', b_ger(cont),extra.lambda(k),extra.lambda(k+1))
   cont=cont+1;
end
fprintf('\n')
fprintf('\n')
disp('=====================================')
disp('          Mi (fluxo)    ')
disp('=====================================')
disp(' Circ.    Mi-km       Mi-mk')
disp('=====================================')
cont=1;
for k = nd_geracao+nbarras+1:2:nd_geracao+nbarras+nd_fluxo
   fprintf('%3d%12.3f%12.3f\n',cont,extra.lambda(k),extra.lambda(k+1))
   cont=cont+1;
end
fprintf('\n')
fprintf('\n')
b_sem_ref=[];
for cont1=1:nbarras
  if BARRA(cont1)!=ref
   b_sem_ref=[b_sem_ref BARRA(cont1)];
  endif
endfor
disp('==================================')
disp(' Mi [lb,ub] - Ângulo(-pi e pi)   ')
disp('==================================')
disp(' Barra      Mi[lb,ub]')
disp('==================================')

for k = 1 :nbarras-1
   fprintf('%3d%15.3f\n',b_sem_ref(k), extra.redcosts(k))
end
fprintf('\n')
fprintf('\n')

disp('==================================')
disp(' Mi [lb,ub] - Gerador (0 e inf)   ')
disp('==================================')
disp(' Barra      Mi[lb,ub]')
disp('==================================')
cont=1;
for k = nbarras :nbarras+ngerador-1
   fprintf('%3d%15.3f\n', b_ger(cont), extra.redcosts(k))
   cont=cont+1;
end
fprintf('\n')
fprintf('\n')

disp('==================================')
disp(' Mi [lb,ub] - Carga (0 e PD)   ')
disp('==================================')
disp(' Barra      Mi[lb,ub]')
disp('==================================')
cont=1;
for k = nbarras+ngerador :nbarras+ngerador+ncarga-1
   fprintf('%3d%15.3f\n', b_carga(cont), extra.redcosts(k))
   cont=cont+1;
end
fprintf('\n')
fprintf('\n')

