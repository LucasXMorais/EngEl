import numpy as np
import matplotlib.pyplot as plt
import cmath

Xs = 0.88

#Tensão do terminal à vazio 
Ea = (1500/np.sqrt(3))

#Determinando Os valores nominais para encontrar a corrente de operação em plena carga do gerador
Smax = 470*1000
Pmax = Smax*0.85
Vmax = 1000
Inom = Pmax/Vmax

#Valores de variação para a corrente até o valor de plena carga com 101 pontos
Ia = [0.0]
for i in range(0,100):
    Ia.append(Inom*((i+1)/100))

#Ãngulo da carga com fp atrasado em radianos
thetaAtr = np.arccos(0.85)*(cmath.pi/180)

#Calculando a tensão terminal para todos os pontos
VtAtr = []
for i in Ia:
    VtAtr.append( (np.sqrt((Ea**2) - ((Xs*i*np.cos(thetaAtr))**2)) - (Xs*i*np.sin(thetaAtr))) * np.sqrt(3) )

plt.plot(Ia,VtAtr)
plt.xlabel("Corrente de Linha")
plt.ylabel("Tensão terminal")
plt.title("Tensão terminal x Corrente de linha - Carga com fp = 0.85 atrasado")
plt.show()

#Ãngulo da carga com fp atrasado em radianos
thetaAd = np.arccos(-0.85)*(cmath.pi/180)

#Calculando a tensão terminal para todos os pontos
VtAd = []
for i in Ia:
    VtAd.append( (np.sqrt((Ea**2) - ((Xs*i*np.cos(thetaAd))**2)) + (Xs*i*np.sin(thetaAd))) * np.sqrt(3) )

plt.plot(Ia,VtAd)
plt.xlabel("Corrente de Linha")
plt.ylabel("Tensão terminal")
plt.title("Tensão terminal x Corrente de linha - Carga com fp = 0.85 adiantado")
plt.show()