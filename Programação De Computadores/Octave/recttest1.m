axis([0,10,0,10]);

floor = rectangle('Position',[0,0,10,1]);

smo = 0.1;
vel = 0.0001;
rect1 = rectangle('Position',[1,1,1,1]);

for x = [1:smo:3];
  delete(rect1);
  #drawnow();
  rect1 = rectangle('Position',[x,1,1,1]);
  drawnow();
  pause(vel);
endfor
