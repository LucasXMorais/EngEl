import numpy as np

l = 270*10**(-6)
c = 270*10**(-9)

def f(r):
    return ((-r*c)+np.sqrt(r*c**(2)+4*l*c))/(2*l*c)

print(1200*2*np.pi)

for r in range(100000):
    r *= 0.01
    w1 = f(r)
    if w1 >= 1200*2*np.pi*0.95 and w1 <= 1200*2*np.pi*1.05:
        err = abs(w1-1200*2*np.pi)/1200*2*np.pi
        print(w1, r, err)
