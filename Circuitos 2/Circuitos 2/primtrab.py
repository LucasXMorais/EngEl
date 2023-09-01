import scipy.io as scipy
from scipy import signal as sg
import matplotlib.pyplot as plt
import numpy as np

mat = scipy.loadmat("./dados_trabalho.mat")

dictT = mat['t']
dictSinal = mat['y']

t = []
sinal = []

for i in range(len(dictT)):
    t.append(dictT[i][0])
    sinal.append(dictSinal[i][0])

num = [1]
dem = [tau,1]
sys = sg.TransferFunction(num,dem)  
#Função onde Hs = 1 / (R*C*s + 1)

plt.figure(1)
plt.plot(t,sinal,label='Sinal Original', color='blue')


simu = primOrdem(sinal,t)
simu.simular(degrau,t)
plt.figure(1)
plt.plot(simu.ts,simu.ys,label='Sistema Simulado', color='red')
plt.legend()
plt.show()