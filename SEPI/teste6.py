#Lucas Morais
# 05/09

import numpy as np

def p1(t1,t3,v3):
    return 1.05*(-5.6603*np.cos(t1)+30.1886*np.sin(t1) + v3*(-2.8301*np.cos(t1-t3)+15.0943*np.sin(t1-t3)))

def p3(t1,t3,v3):
    return v3*(1.05*(-2.8301*np.cos(t3-t1)+15.0943*np.sin(t3-t1)) + (-0.9433*np.cos(t3)+5.0314*np.sin(t3)))

def q3(t1,t3,v3):
    return v3*(1.05*(-2.8301*np.sin(t3-t1)+15.0943*np.cos(t3-t1)) + (-0.9433*np.sin(t1-t3)+5.0314*np.cos(t1-t3)))


def p1t1(t1,t3,v3):
    return 1.05*(5.6603*np.sin(t1)+30.1886*np.cos(t1) + v3*(2.8301*np.sin(t1-t3)+15.0943*np.cos(t1-t3)))

def p3t1(t1,t3,v3):
    return v3*1.05*(2.8301*np.sin(t3-t1)+15.0943*np.cos(t3-t1))

def q3t1(t1,t3,v3):
    return v3*(1.05*(-2.8301*np.cos(t3-t1)-15.0943*np.sin(t3-t1)) + (-0.9433*np.cos(t1-t3)-5.0314*np.sin(t1-t3)))


def p1t3(t1,t3,v3):
    return 1.05*v3*(2.8301*np.sin(t1-t3)+15.0943*np.cos(t1-t3))

def p3t3(t1,t3,v3):
    return v3*(1.05*(2.8301*np.sin(t3-t1)+15.0943*np.cos(t3-t1)) + (0.9433*np.sin(t3)+5.0314*np.cos(t3)))

def q3t3(t1,t3,v3):
    return v3*(1.05*(-2.8301*np.cos(t3-t1)-15.0943*np.sin(t3-t1)) + (-0.9433*np.cos(t1-t3)-5.0314*np.sin(t1-t3)))


def p1v3(t1,t3,v3):
    return 1.05*(-2.8301*np.cos(t1-t3)+15.0943*np.sin(t1-t3))

def p3v3(t1,t3,v3):
    return (1.05*(-2.8301*np.cos(t3-t1)+15.0943*np.sin(t3-t1)) + (-0.9433*np.cos(t3)+5.0314*np.sin(t3)))

def q3v3(t1,t3,v3):
    return (1.05*(-2.8301*np.sin(t3-t1)+15.0943*np.cos(t3-t1)) + (-0.9433*np.sin(t1-t3)+5.0314*np.cos(t1-t3)))
 

t1 = 0
t3 = 0
v3 = 1

tol = 0.03 

erro = 0
maxIter = 10000
iter = 0
var = np.zeros((3,1))

while (iter < maxIter):
    p1i = p1(t1,t3,v3)
    p3i = p3(t1,t3,v3)
    q3i = q3(t1,t3,v3)

    fxi = np.array([[p1i],
                    [p3i],
                    [q3i]])
    
    max = p1i
    for val in fxi:
        if (np.abs(val) > np.abs(max)): max = val

    if np.abs(max) < tol : break

    p1t1i = p1t1(t1,t3,v3)
    p3t1i = p3t1(t1,t3,v3)
    q3t1i = q3t1(t1,t3,v3)

    p1t3i = p1t3(t1,t3,v3)
    p3t3i = p3t3(t1,t3,v3)
    q3t3i = q3t3(t1,t3,v3)
    
    p1v3i = p1v3(t1,t3,v3)
    p3v3i = p3v3(t1,t3,v3)
    q3v3i = q3v3(t1,t3,v3)

    ji = np.array([[p1t1i, p3t1i, q3t1i],
                    [p1t3i, p3t3i, q3t3i],
                    [p1v3i, p3v3i, q3v3i],])

    var = np.dot(-1*np.linalg.inv(ji),fxi)

    t1 += var[0][0]
    t3 += var[1][0]
    v3 += var[2][0]

    iter += 1
    print(iter)

print(var)

