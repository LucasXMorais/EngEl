axis([0,10,0,10]);

steps = 0.1
#x = [1:0.1:5];
#y = [1:0.1:2];

base = rectangle('Position',[0,0,10,1]);
tank1 = rectangle('Position',[1,1,1,1]);
#tank2 = rectangle('Position',[8,1,1,1]);
#cannon1 = rectangle('Position',[1.7,1.4,1,0.2]);

for x = [1:steps:5]; 
  tank1 = rectangle('Position', [x,1,1,1]); 
  tank1Aux = tank1;
  clf(tank1);
  drawnow();   
endfor
#{
while (x);
  i = 1
  if kbhit();
    i = i + 1
    tank1 = rectangle('Position',[i,1,1,1]);
  endif
endwhile
#}

