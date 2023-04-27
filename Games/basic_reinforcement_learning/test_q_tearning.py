
import pyspiel

from QLearning import QLearning
import matrix_games

import pdb

QLearner = QLearning(learning_rate = 0.1, discount_rate = 0.99,initial_exploration_rate = 1)
prisoners_dilemma = matrix_games.create_prisoners_dilemma_game()

row_actions, col_actions = matrix_games.get_actions(prisoners_dilemma)

nb_episodes = 10000


#pdb.set_trace()