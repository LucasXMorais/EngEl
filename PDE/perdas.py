import numpy as np

D = 5.0
R = 1.5*(10^(-2))
miR = 1.0
Rcc = 0.1204
H = 12.0

D12 = D*np.sqrt(2) #=D21=D23=D32 !!!NESSE EXERCÍCIO APENAS
D13 = D*2
D23 = D*np.sqrt(2)

D12l = np.sqrt(((2*H + 2*D)^2)+D^2)
D13l = np.sqrt(((2*H)^2)+D^2)
D23l = np.sqrt(((2*H + 2*D)^2)+D^2)

Labc = np.matrix([[((miR/4)+np.log(1/R)), (np.log(1/D12), (np.log(1/D13)))], 
                [(np.log(1/D12), ((miR/4)+np.log(1/R)), (np.log(1/D12)))]
                ])