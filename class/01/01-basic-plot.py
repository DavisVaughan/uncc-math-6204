import numpy as np
import matplotlib.pylab as plt

x = np.linspace(-10, 10, 100)
y = np.sin(x)

plt.figure()
plt.plot(x, y)
plt.show()


