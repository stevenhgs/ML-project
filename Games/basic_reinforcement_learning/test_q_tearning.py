
import pyspiel
import numpy as np

from QLearning import QLearning
import matrix_games

import pdb

QLearner = QLearning(learning_rate = 0.1, discount_rate = 0.99,initial_exploration_rate = 1)
prisoners_dilemma = matrix_games.create_prisoners_dilemma_game()

row_actions, col_actions = matrix_games.get_actions(prisoners_dilemma)

dict_row_actions = {}
for i, action in enumerate(row_actions):
    dict_row_actions[action] = i

nb_episodes = 10000

payoff = []
payoff.append(prisoners_dilemma.row_utilities())
payoff.append(prisoners_dilemma.col_utilities())
payoff = np.array(payoff)

Q1, Q2, trajectory1, trajectory2 = QLearner.learn(nb_episodes, dict_row_actions, payoff)

pdb.set_trace()