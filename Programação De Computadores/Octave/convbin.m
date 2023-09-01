ent = num2str(input('Entre um valor binário - '));
num = 0;
c1 = 0;
c2 = length(ent);

while 1  
  aux = str2num(ent(c2)) * (2^c1);
  num += aux;
  c1 += 1;
  c2 -= 1;
  if c2 == 0
    break
  endif
endwhile

disp(num)