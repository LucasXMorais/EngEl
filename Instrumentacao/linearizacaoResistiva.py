import matplotlib.pyplot as plt

def line(Rx, R):
    return ( Rx * R ) / ( Rx + R )


resistores = [1, 10, 100, 500, 1000, 5000, 10000]
Rxs = [x for x in range(1,100)]

sensibilidade = []
for R in resistores:
    mensurando = []
    for Rx in Rxs:
        mensurando.append(line(Rx, R))

    sensibilidade.append(mensurando)

c = 0
for s in sensibilidade:
    plt.plot(Rxs, s, label=str(resistores[c]))
    c+=1

plt.legend()
plt.show()






