import numpy as np
import matplotlib.pyplot as plt

def readDataFile(path):
    with open(path) as f:
        data = []
        for line in f:
            if line != '' : data.append(float(line[:-1]))
    return data

tempo = readDataFile('./time.dat')
dados = readDataFile('./data.dat')

janelasDeTempo = [[60 , 100],
                  [127, 170],
                  [182, 228],
                  [240, 257],
                  [280, 330],
                  [354, 390],
                  [396, 433],
                  [440, 472]]

# plt.plot(tempo, dados)
# plt.title('Dados iniciais adiquiridos')
# plt.xlabel('Tempo')
# plt.ylabel('Tensao (V)')
# plt.show()

mediaTensaoMedida = []
desvioPadrao = []
for w in janelasDeTempo:
    indexJanelaInicio = tempo.index(w[0])
    indexJanelaFinal = tempo.index(w[1])

    dadosDaJanela = dados[indexJanelaInicio:indexJanelaFinal]
    mediaTensaoMedida.append(sum(dadosDaJanela)/len(dadosDaJanela))

valoresCorrente = np.array([0.042,
                            0.095,
                            0.149,
                            0.201,
                            0.251,
                            0.299,
                            0.347,
                            0.399])

# Adicione uma coluna de uns ao array x para representar o termo constante (b) na equação linear
X = np.column_stack((valoresCorrente, np.ones_like(valoresCorrente)))

# Calcule os coeficientes 'a' e 'b' usando a fórmula dos mínimos quadrados
coefficients = np.linalg.lstsq(X, mediaTensaoMedida, rcond=None)[0]

# Os coeficientes 'a' e 'b' são armazenados na variável coefficients
a, b = coefficients

# Use a função ajustada para prever os valores de 'y'
y_pred = a * valoresCorrente + b

# Plote os dados e a linha de ajuste
# plt.scatter(valoresCorrente, mediaTensaoMedida, label='Dados reais')
# c = 0
# for v in mediaTensaoMedida:
#     plt.annotate(f'{v:.4f}', (valoresCorrente[c], v+0.05))
#     c += 1
plt.plot(valoresCorrente, y_pred, label='Curva de calibração estática', color='red')
plt.legend()
plt.axis((0, 0.5, 0, 2.3))
plt.xlabel('Mensurando')
plt.ylabel('Saida')
plt.show()













