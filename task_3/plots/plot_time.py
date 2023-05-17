import matplotlib.pyplot as plt

sizes = [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3)]
x = [2 ** (r * (c + 1) + (r + 1) * c) for r, c in sizes]
x_labels = ['1x1', '1x2', '2x2', '2x3', '3x3']

naive = [0.000423, 0.040582, 3308.053003]
cache = [0.000428, 0.004163, 0.273274, 14.717575, 4671.24731]
cache_and_sym_canonical = [0.000574, 0.005448, 0.141171, 11.202883, 2331.966138]
cache_and_sym = [0.000455, 0.002389, 0.070342, 5.066539, 825.958522]

plt.loglog(x, cache, label="Cache", linewidth='2')
plt.loglog(x, cache_and_sym_canonical, label="Cache and symmetries: strategy 1", linewidth='2')
plt.loglog(x, cache_and_sym, label="Cache and symmetries: strategy 2", linewidth='2')
plt.loglog(x[:-2], naive, label="Naive", linewidth='2')

plt.xlabel("Amount of possible states of the game", fontsize=22)
plt.ylabel("Time needed to solve the game (s)", fontsize=22)
plt.legend(fontsize=14)
plt.show()
