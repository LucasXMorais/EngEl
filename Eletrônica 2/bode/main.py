import matplotlib.pyplot as plt
import numpy as np

def Gs(s):
    return -100 / ( s + 100 ) # a
    # return 1000 * ( (s + 1) / ( (s**2) + (110*(s)) + 1000 ) ) # b
    # return 10 * ( (s + 10) / ( (s**2) + (3*s) ) ) # c
    # return -100 * ( s / ( (s**3) + (12*(s**2)) + (21*s) + 10 ) ) # d
    # return 30 * ( (s + 10) / ( (s**2) + (3*s) + 50 ) ) # e
    # return 4 * ( ( (s**2) + s + 25 ) / ( (s**3) + (100*(s**2)) ) ) # f
    # return ( 20 * (( (s/150) + 1 ) / ( ( (s/10) + 1 ) * ( (s/1500) + 1 ) ) ) )

def modGs(w):
    s = (1j)*w
    return np.abs(Gs(s))

def phiGs(w):
    s = (1j)*w
    return np.angle(Gs(s))

if __name__ == '__main__':
    modules = []
    angles = []

    omegas = np.logspace(-1, 6, 1000)

    for w in omegas:
        modules.append(20*np.log10(modGs(w)))
        angles.append(phiGs(w))

    figure, axis = plt.subplots(2, 1)

    axis[0].semilogx(omegas, modules)
    axis[0].set_title('Modulo')

    axis[1].semilogx(omegas, angles)
    axis[1].set_title('Fase')

    plt.subplots_adjust(hspace=0.3)
    plt.show()

    

    
