
import numpy as np

from QLearning import QLearning
import matplotlib.pyplot as plt
import matrix_games

# Generate OpenSpiel matrix game
game = matrix_games.create_dispersion_game()

# Set parameters
greedy = True           # True: epsilon-greedy Q-learning | False: lenient Boltzmann Q-learning
learning_rate = 0.05    # Learning rate for Q-learning
discount_rate = 0.1     # Discount rate for Q-learning
nb_episodes = 10000     # Amount of episodes to train agent

# Get actions of matrix game
row_actions, col_actions = matrix_games.get_actions(game)

# Place actions into dictionary
dict_row_actions = {}
for i, action in enumerate(row_actions):
    dict_row_actions[action] = i

# Get payoff table of matrix game
payoff = []
payoff.append(game.row_utilities())
payoff.append(game.col_utilities())
payoff = np.array(payoff)

# Perform Q-learning
QLearner = QLearning(learning_rate = learning_rate, discount_rate = discount_rate)
Q1, Q2, trajectory1, trajectory2 = QLearner.learn(nb_episodes, dict_row_actions, payoff, greedy = False)

print("Final probabilities of row player: " + str(trajectory1[-1]))
print("Final probabilities of column player: " + str(trajectory2[-1]))

# Plot learning trajectories
ax = plt.subplot()

if len(row_actions) == 3:   # Three possible actions
    p1 = [p1 for p1, p2, p3 in trajectory1]
    p2 = [p2 for p1, p2, p3 in trajectory1]
    p3 = [p3 for p1, p2, p3 in trajectory1]

    ax.plot(range(nb_episodes), p1, label = game.row_action_name(0), linewidth= '2')
    ax.plot(range(nb_episodes), p2, label = game.row_action_name(1), linewidth= '2')
    ax.plot(range(nb_episodes), p3, label = game.row_action_name(2), linewidth='2')

else:                       # Two possible actions
    p1 = [p1 for p1, p2 in trajectory1]
    p2 = [p2 for p1, p2 in trajectory1]

    ax.plot(range(nb_episodes), p1, label = game.row_action_name(0), linewidth= '2')
    ax.plot(range(nb_episodes), p2, label = game.row_action_name(1), linewidth= '2')

ax.set_xlabel("Episodes", fontsize = 35)
ax.set_ylabel("Probability to choose action", fontsize = 35)
ax.legend(fontsize = 28)

plt.show()
