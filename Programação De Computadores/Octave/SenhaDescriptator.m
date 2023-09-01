markers = ['?','*','&','@','!','+','/','#','$','%','=','|'];
pass = ['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M','n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z','0','1','2','3','4','5','6','7','8','9'];

senha = input('Senha  ','s');
senha = strcat(senha,'_');

while 1 
  code = input('Código  ');
  if length(code) == 3 
    for c = 1:3
      if code(c) < 1 || code(c) > 9
        error = true;
        break
      else
        error = false;
      endif
    endfor
  else
    error = true;
  endif
  if error == false
    break
  endif
endwhile

c = 1;
letra = 0;
marcadores = 0;

while c <= length(senha) - 1 
  for n = 1:length(pass)
    if strcmp(senha(c),pass(n))   
      parte = senha(c);
      markhere = false;
      neg = false;      
      letra += 1;
      if senha(c+1) != '_'
        for n1 = 1:length(markers)
          if strcmp(senha(c+1),markers(n1))
            parte = strcat(parte,markers(n1));
            marcadoresusados(marcadores+1) = markers(n1);         
            c += 1;
            marcadores += 1;
            break
          endif
        endfor
        if strcmp(senha(c+1),'(')
          neg = true;
          parte = strcat(parte,'(');
          c += 1;
        endif
        break
      endif
      break
    endif
  endfor
  
  if neg == false  
    n2 = length(parte);
    if n2 == 1
      n = (n - code(2) + code(3)) / code(1);
    elseif n2 == 2
      if length(marcadoresusados) == 1
        for n1 = 1:length(markers)
          if strcmp(marcadoresusados(1),markers(n1))
            break
          endif
        endfor
        n = (n + (n1*62) + code(3) - code(2)) / code(1);
      elseif length(marcadoresusados) > 1
        for n1 = 1:length(markers)
          if strcmp(markers(n1),marcadoresusados(end-1))
            break
          endif
        endfor
        
        for n12 = 1:length(markers)
          if strcmp(markers(n12),marcadoresusados(end))
            break
          endif
        endfor
        
        if n12 > n1
          n1 = n12 - n1;
        else
          n1 = (n12 + length(markers)) - n1;
        endif
        
        n = (n + (n1*62) + code(3) - code(2)) / code(1);
      endif                  
    endif
  else
    n = ((n + code(3) - code(2)) - 62) / code(1);
  endif
  
  descriptografado(letra) = pass(n);
  
  code = [code(3),code(1),code(2)];
  
  c += 1;
  
endwhile

disp(descriptografado)







