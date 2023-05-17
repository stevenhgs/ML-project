import matplotlib.pyplot as plt

sizes = [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3)]
x = [2 ** (r * (c + 1) + (r + 1) * c) for r, c in sizes]
x_labels = ['1x1', '1x2', '2x2', '2x3', '3x3']

naive = [65, 13700, 1302061345]
cache = [16, 142, 5346, 194749, 29598515]
cache_and_sym_canonical = [6, 54, 753, 49762, 3712138]
cache_and_sym = [6, 54, 753, 49762, 3712138]

plt.loglog(x, cache, label="Cache", linewidth='2')
plt.loglog(x, cache_and_sym_canonical, label="Cache and symmetries: strategy 1", linewidth='2')
plt.loglog(x, cache_and_sym, label="Cache and symmetries: strategy 2", linewidth='2')
plt.loglog(x[:-2], naive, label="Naive", linewidth='2')

plt.xlabel("Amount of possible states of the game", fontsize=22)
plt.ylabel("Amount of nodes expanded", fontsize=22)
plt.legend(fontsize=14)
plt.show()
