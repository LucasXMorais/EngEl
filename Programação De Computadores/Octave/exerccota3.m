disp('a: adição\ns: subtração\nm:multiplicação\nd: divisão\n')

op = input('Operação  ','s');

switch(op)
case{'a' 's' 'm' 'd'}
    
a = input('a = ');
b = input('b = ');

dontshow = false;

switch(op)
  case 'a'
    resp = a + b;
  case 's'
    resp = a - b;
  case 'm'
    resp = a*b;
  case 'd'
    resp = a/b;
  otherwise
    dontshow = true;
endswitch

if dontshow == false
  disp(resp)
endif

  otherwise
    disp('This is not possible!!!')
endswitch