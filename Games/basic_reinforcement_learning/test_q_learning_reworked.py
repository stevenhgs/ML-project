import pyspiel
import numpy as np

from QLearning_reworked import QLearning
import matrix_games

import pdb

QLearner = QLearning(learning_rate=0.01, discount_rate=0, initial_exploration_rate=0.1)
custom_game = matrix_games.create_biased_rock_paper_scissors_game()

row_actions, col_actions = matrix_games.get_actions(custom_game)

dict_row_actions = {}
for i, action in enumerate(row_actions):
    dict_row_actions[action] = i

nb_episodes = 100000

payoff = []
payoff.append(custom_game.row_utilities())
payoff.append(custom_game.col_utilities())
payoff = np.array(payoff)

Q1, Q2, trajectory1, trajectory2 = QLearner.learn(nb_episodes, dict_row_actions, payoff)

print('Q1')
print(Q1)
print(trajectory1[-1])
print('Q2')
print(Q2)
print(trajectory2[-1])