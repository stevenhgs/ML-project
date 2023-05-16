
import numpy as np

from QLearning import QLearning
from open_spiel.python.egt import utils
from open_spiel.python.egt import dynamics
from open_spiel.python.egt import visualization
from mpltern.datasets import get_triangular_grid
import matplotlib.pyplot as plt
import matrix_games

# Generate OpenSpiel matrix game
game = matrix_games.create_biased_rock_paper_scissors_game()

# Set parameters
greedy = False          # True: epsilon-greedy Q-learning | False: lenient Boltzmann Q-learning
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

if len(row_actions) == 3:   # Three possible actions

    # Plot the directional field plots
    ax = plt.subplot(projection="ternary")

    ax.set_tlabel(game.row_action_name(0), fontsize = 20)
    ax.set_llabel(game.row_action_name(1), fontsize = 20)
    ax.set_rlabel(game.row_action_name(2), fontsize = 20)

    A = payoff[1]

    t, l, r = get_triangular_grid(22)
    grid_size = len(t)

    dt = [0 for _ in range(grid_size)]
    dl = [0 for _ in range(grid_size)]
    dr = [0 for _ in range(grid_size)]

    A = np.array(payoff[0])

    for idx in range(grid_size):
        x = np.array([t[idx], l[idx], r[idx]])

        if 0. in x:
            np.delete(t, idx, 0)
            np.delete(l, idx, 0)
            np.delete(r, idx, 0)
            np.delete(dt, idx, 0)
            np.delete(dl, idx, 0)
            np.delete(dr, idx, 0)
            continue

        Ax = A @ x  # Same as np.matmul, but faster
        xAx = np.dot(x, Ax)
        dt[idx] = (Ax[0] - xAx) * x[0]
        dl[idx] = (Ax[1] - xAx) * x[1]
        dr[idx] = (Ax[2] - xAx) * x[2]

    ax.quiver(t, l, r, dt, dl, dr)

    # Perform Q-learning
    QLearner = QLearning(learning_rate = learning_rate, discount_rate = discount_rate)
    Q1, Q2, trajectory1, trajectory2 = QLearner.learn(nb_episodes, dict_row_actions, payoff, greedy = greedy)

    x = [x for x, y, z in trajectory1]
    y = [y for x, y, z in trajectory1]
    z = [z for x, y, z in trajectory1]
    ax.plot(x, y, z, linewidth='2')

    print("Final probabilities of row player: " + str(trajectory1[-1]))

    # Plot four more trajectories if agent uses lenient Boltzmann Q-learning
    if not greedy:
        for i in range(4):
            Q1, Q2, trajectory1, trajectory2 = QLearner.learn(nb_episodes, dict_row_actions, payoff, greedy = greedy)

            x = [x for x, y, z in trajectory1]
            y = [y for x, y, z in trajectory1]
            z = [z for x, y, z in trajectory1]
            ax.plot(x, y, z, linewidth= '2')

            print("Final probabilities of row player: " + str(trajectory1[-1]))

else:                       # Two possible actions

    # Plot the directional field plots
    payoff_tensor = utils.game_payoffs_array(game)
    dyn = dynamics.MultiPopulationDynamics(payoff_tensor, dynamics.replicator)

    ax = plt.subplot(projection = "2x2")
    ax.set_xlabel("Probability of player 1 choosing " + game.row_action_name(0), fontsize = 22)
    ax.set_ylabel("Probability of player 2 choosing " + game.col_action_name(0), fontsize = 22)

    ax.quiver(dyn)

    QLearner = QLearning(learning_rate = learning_rate, discount_rate = discount_rate)
    Q1, Q2, trajectory1, trajectory2 = QLearner.learn(nb_episodes, dict_row_actions, payoff, greedy = greedy)

    x = [x for x, y in trajectory1]
    y = [x for x, y in trajectory2]
    plt.plot(x, y, linewidth = '2')

    print("Final probabilities of row player: " + str(trajectory1[-1]))

    # Plot four more trajectories if agent uses lenient Boltzmann Q-learning
    if not greedy:
        for i in range(4):
            Q1, Q2, trajectory1, trajectory2 = QLearner.learn(nb_episodes, dict_row_actions, payoff, greedy = greedy)

            x = [x for x, y in trajectory1]
            y = [x for x, y in trajectory2]
            plt.plot(x, y, linewidth= '2')

            print("Final probabilities of row player: " + str(trajectory1[-1]))

plt.show()