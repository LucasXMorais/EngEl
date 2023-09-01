n = input('Please insert a number - ');
arr = [1:n];

#Printing each row at a time by using a for loop inside
#a while one

i = 1;

while i <= n;
    prin_line = '';
    for k = [1:i];
      if i >= 10;
        prin_line = strcat(prin_line,num2str(i));
      else;
        prin_line = cstrcat(prin_line,num2str(i),' ');
      endif
    endfor
    disp(prin_line)
    i += 1;
endwhile

#Second time

i = n - 1;

for i = [i:-1:1];
    prin_line = '';
    for k = [1:i];
      if i >= 10;
        prin_line = cstrcat(prin_line,num2str(i));        
      else;      
        prin_line = cstrcat(prin_line,num2str(i),' ');
      endif
    endfor
    disp(prin_line)
    i -= 1;
endfor