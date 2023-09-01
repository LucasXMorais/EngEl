import numpy as np

#c1 = c2 = 270nF
c = 270*10**(-9)

def w1(r1,r2):
    return ((-1)*((1/(r2*c))+(1/(r1*c))+(1/(r2*c)))-np.sqrt((((1/(r2*c))+(1/(r1*c))+(1/(r2*c)))**2)-4*(1/(r1*r2*c**2))))/2

def w2(r1,r2):
    return ((-1)*((1/(r2*c))+(1/(r1*c))+(1/(r2*c)))+np.sqrt((((1/(r2*c))+(1/(r1*c))+(1/(r2*c)))**2)-4*(1/(r1*r2*c**2))))/2

#w1 = 1200 rad/s e w2 = 2400 rad/s

for i in range(1,100):
    r1=i*1
    for j in range(1,100):
        r2=j*1
        omega1=w1(r1,r2)
        omega2=w2(r1,r2)
        errMed=((abs(omega1-1200)/1200)+(abs(omega2-2400)/2400))/2
        print(omega1, omega2, r1, r2, errMed)
        #if omega1>=1200*0.9 and omega1<=1200*1.1 and omega2>=2400*0.9 and omega2<=2400*1.1:
            #errMed=((abs(omega1-1200)/1200)+(abs(omega2-2400)/2400))/2
            #print(omega1, omega2, r1, r2, errMed)

        

