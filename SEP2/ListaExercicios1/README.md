# Rodar a rotina

Para rodar a rotina, basta executar o arquivo main.py

A única dependência necessária é o numpy


# Configurando a rotina

Editando o arquivo config.ini é possível configurar facilmente algumas
algumas variáveis importantes para a rotina.

 - DATA_FILE_NAME : nome do arquivo de entrada de dados
 - OUTPUT_FILE : nome do arquivo onde será gravado o resultado da rotina
 - BASE : Base PU do sistema
 - MAX_ITER : determina o número máximo de iterações 
 - TOLERANCIA : determina a tolerância do Newton Raphson


# Estrutura da rotina

O arquivo principal é o arquivo main.py.
Foram feitos 3 módulos para facilitar a melhorar a rotina.
 - exportacao.py : Rotina que guarda os resultados
 - leitura.py : Rotina de leitura de dados
 - sep.py : Rotina com várias funções do cálculo do fluxo
Foi feita também uma classe para organizar melhor as informações de cada sistema
Isso foi feito em preparação para solucionar os problemas que virão ainda no curso
 - sistema.py : Classe do sistema 





