
%Vetor que contem todos os pontos divididos em linhas e suas coordenadas em colunas
vetor = input('Coloque os valores de x e y em um vetor sendo\ncada ponto uma linha:');

i = size(vetor)(1);

distancia = 0;

for c = [1:i-1];
  distancia += calcdist(vetor(c,1),vetor(c,2),vetor(c+1,1),vetor(c+1,2));
endfor

disp(distancia);
