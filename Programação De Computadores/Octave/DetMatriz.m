while 1
  #Preciso receber uma matriz quadrada de tamanho maior ou igual a 2
  matriz = input('Insira a matriz quadrada:  ');
  if size(matriz)(1) == size(matriz)(2) && length(matriz) >= 2
    break
  endif
endwhile

#Determinante = a11„11 + a12„12 + ... + a1n„1n
#„ij = (-1)^(i+j)det√ij
#√ij È a matriz A sem a linha i e a coluna j

coluna_atual = 1;
determinante = 0;

while coluna_atual <= length(matriz)
  mat_aux = zeros(size(matriz)(1)-1,size(matriz)(1)-1)
endwhile  