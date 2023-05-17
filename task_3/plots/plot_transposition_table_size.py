import matplotlib.pyplot as plt

sizes = [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3)]
x = [2 ** (r * (c + 1) + (r + 1) * c) for r, c in sizes]
x_labels = ['1x1', '1x2', '2x2', '2x3', '3x3']

cache = [640, 4696, 147552, 10485856, 1342177368]
cache_and_sym_canonical = [360, 2272, 36960, 2621536, 167772256]
cache_and_sym = [640, 4696, 147552, 10485856, 1342177368]

plt.loglog(x, cache, label="Cache", linewidth='2')
plt.loglog(x, cache_and_sym_canonical, label="Cache and symmetries: strategy 1", linewidth='2')
plt.loglog(x, cache_and_sym, label="Cache and symmetries: strategy 2", linewidth='2')

plt.xlabel("Amount of possible states of the game", fontsize=22)
plt.ylabel("The size of the transposition table (B)", fontsize=22)
plt.legend(fontsize=14)
plt.show()
