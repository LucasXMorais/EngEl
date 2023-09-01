import matplotlib.pyplot as plt
import random

vetor = []

for i in range(100):
	num = random.randint(0,50)
	vetor.append(num)
	
plt.title('Boxplot')
plt.boxplot(vetor)
plt.show()