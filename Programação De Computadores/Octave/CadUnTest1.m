#{
function retval = perg(texto)
  disp(texto);
  retval = input();
endfunction


cadastro = {
           nome = '';#Maior q 3       
           idade = 0;#entre 0 e 150
           salario = 0;#maior q zero
           sexo = '';#f ou m
           est_civ = '';#solt, cas, div, viuv     
           }
#}

perg_cad = {'Nome', 'Idade', 'Salário', 'Sexo', 'est_civ'};           
resp = ['',0,0,'',''];

for i = 1:length(perg_cad);  
  resp(i) = input(perg_cad(i));
endfor

for i = 1:rows (perg_cad)
  cadastro.(perg_cad(i,:)) = resp(i);
endfor

#Failure