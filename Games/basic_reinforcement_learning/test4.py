import egtplot
import numpy as np
import matplotlib.pyplot as plt


A = [[0], [-0.25], [0.5],
    [0.25], [0], [-0.05],
    [-0.5], [0.05], [0]]


simplex = egtplot.plot_static(A)
plt.show()