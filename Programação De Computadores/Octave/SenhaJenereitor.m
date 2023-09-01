markers = ['?','*','&','@','!','+','/','#','$','%','=','|'];
pass = ['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M','n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z','0','1','2','3','4','5','6','7','8','9'];

senha = input('Senha - (Dê atencao aos maiusculos e minusculos) = ','s');

while 1
  perg = input('usar seu própio código? (s/n)','s');
  switch perg
  case 'n'      
    code = ceil(rand(1,3).*9);
    break
  case 's'
    while 2 
      code = input('Código');
      if length(code) == 3         
        error = false;
      else
        error = true;
      endif
      if error == false
        break
      endif
    endwhile
    break
  endswitch
         
endwhile

codf = code;
c = 1;
letra = 1;
senha_nova = "";
mais = 0;
m = 0;

while c <= length(senha) 
  
  if length(senha_nova) == c + mais
    letra += 1; 
  endif
  
  c2 = 1;
  while 1
    if strcmp(senha(c),pass(c2))
      break
    else
      c2 += 1;
    endif
  endwhile
  
  c2 = c2 * code(1) + code(2) - code(3);
  usemarker = false;
  useneg = false;
  
  while 1
    if c2 >= 63
      c2 -= 62;
      usemarker = true;
      m += 1;
    else
      break
    endif
  endwhile
  
  while 1 
    if c2 <= 0 
      useneg = true;
      c2 = 62 + c2;
    else 
      break
    endif
  endwhile
  
  if usemarker == false && useneg == false
    senha_nova(letra+mais) = pass(c2);
  elseif usemarker == true
    senha_nova(letra+mais) = pass(c2);
    mais += 1;
    if m > 12
      m -= 12;
    endif
    senha_nova(letra+mais) = markers(m);
  elseif useneg == true
    senha_nova(letra+mais) = pass(c2);
    mais += 1;
    senha_nova(letra+mais) = '(';    
  endif
  
  c += 1;
  letra += 1;
  
  code = [code(3),code(1),code(2)];
  
endwhile

disp(strcat(num2str(codf(1)),num2str(codf(2)),num2str(codf(3))))
disp(senha_nova)