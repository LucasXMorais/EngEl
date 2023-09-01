usr_sen = load('usrpass');
while 1
  prompt = inputdlg({'Usuario','Senha'});  
  while 1 
    for c = 1:size(usr_sen)(1,1)
      if strcmp(prompt{1,1},usr_sen{c,1})
        break
      endif
    endfor
    while 1
      if strcmp(usr_sen{c,2},prompt{1,2})
        #funcao que contem o programa
      else
        h = msgbox('Senha errada');
        uiwait(h);
      endif
    endwhile
  endwhile
endwhile
