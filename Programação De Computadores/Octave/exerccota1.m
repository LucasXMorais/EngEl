disp('Insira os valores de a, b e c de uma função de segundo grau')

fimprog = false;
while fimprog == false;

  a = input('a: ');
  b = input('b: ');
  c = input('c: ');

  titulo = strcat(num2str(a),'X^2 + ',num2str(b),'X + ',num2str(c));

  disp('Defina um domínio para a sua função');
  ini = input('Início do domínio ');
  fim = input('Fim do domínio ');

  x = linspace(ini,fim,1000);

  y = a*(x.**2) + b.*x + c;

  plot(x,y,'k')
  title(titulo);
  xlabel('x');
  ylabel('y');

  findor = input('Deseja finalizar o programa? (s/n)','s');
  if findor == 's';
    fimprog = true;
  endif
endwhile