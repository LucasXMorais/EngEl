from scipy import signal
import matplotlib.pyplot as plt
num = [1.0]
den = [1.0, 3.0, 1.0, 1.0]
lti = signal.lti(num, den)
t, y = signal.step(lti)
plt.plot(t, y)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Step response for 1. Order Lowpass')
plt.grid()
plt.show()




