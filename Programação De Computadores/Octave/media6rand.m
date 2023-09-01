x = [1:100];
axis = [100,0,10,0];

for i = [1:100]
  r = floor(6*rand(1,10) + 1);
  cont(i) = sum(r == 6);
  
  if i >= 2
    media(i) = (cont(i) + media(i-1))/i;
  else
    media(i) = cont(i);
  endif
  
  hold on;
  plot(x(i),cont(i),'-r')
  plot(x(i),media(i),'-b')
  pause(0.1);
  hold off;
  
endfor
