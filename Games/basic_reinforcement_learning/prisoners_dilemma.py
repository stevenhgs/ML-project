import random
import numpy as np
import matplotlib.pyplot as plt

import pdb

actions = {"cooperate":     0,
           "defect":        1}

# Payoff table
payoff = np.array([[[-1, -1], [-4, 0]],
                    [[0, -4], [-3, -3]]])

# Initialize Q-values matrices for each agent
Q1 = np.zeros((2, 2))
Q2 = np.zeros((2, 2))

episodes = 10000    # Number of episodes

learning_rate = 0.1             # Alpha
discount_rate = 0.99            # Gamma

exploration_rate = 1            # Epsilon
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001  # Decay rate

trajectory1 = []
trajectory2 = []

# Choose an action based on current state and Q-values
def choose_action(Q, state):
    # Probability of epsilon to choose random action
    if random.random() < exploration_rate:
        action = random.choice(list(actions.values()))
    # Probability of (1 - epsilon) to choose action with highest Q-value
    else:
        action = np.argmax(Q[state])
    return action

# Update the Q-values using epsilon-greedy Q-learning
def update_Q(Q, state, action, reward, next_state):
    Q[state][action] += learning_rate * (reward + discount_rate * max(Q[next_state]) - Q[state][action])

state1 = random.choice(list(actions.values()))
state2 = random.choice(list(actions.values()))

for episode in range(episodes):
    action1 = choose_action(Q1, state1)
    action2 = choose_action(Q2, state2)

    P1 = [0, 0]
    P1[np.argmax(Q1[action1])] = 1 - exploration_rate
    P1 = [x + exploration_rate / 2 for x in P1]
    trajectory1.append(P1)

    P2 = [0, 0]
    P2[np.argmax(Q2[action2])] = 1 - exploration_rate
    P2 = [x + exploration_rate / 2 for x in P2]
    trajectory2.append(P2)

    reward1 = payoff[action1][action2][0]
    reward2 = payoff[action1][action2][1]

    update_Q(Q1, state1, action1, reward1, action1)
    update_Q(Q2, state2, action2, reward2, action2)

    state1 = action1
    state2 = action2

    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

print("Q-values matrix for agent 1:")
print(Q1)
print("Q-values matrix for agent 2:")
print(Q2)

# Define the matrix game payoff matrix
A = np.array([[payoff[0][0][0], payoff[0][1][0]],
             [payoff[1][0][0], payoff[1][1][0]]])

B = np.array([[payoff[0][0][1], payoff[1][0][1]],
             [payoff[0][1][1], payoff[1][1][1]]])

# Define the range of x and y values to plot
x = np.arange(0, 1.0, 0.05)
y = np.arange(0, 1.0, 0.05)

mesh_size = len(x)

# Create a meshgrid from the x and y values
X, Y = np.meshgrid(x, y)

# print(Y)

# Define the differential equations for the directional field
dX = np.array([[0 for _ in range(mesh_size)] for _ in range(mesh_size)], dtype=float)
dY = np.array([[0 for _ in range(mesh_size)] for _ in range(mesh_size)], dtype=float)

for y_i in range(20):
    y1 = 0.05 * y_i
    y2 = 1 - y1
    for x_i in range(20):
        x1 = 0.05 * x_i
        x2 = 1 - x1

        Ay1 = A[0][0] * y1 + A[0][1] * y2
        xTAy = (x1 * (A[0][0] * y1 + A[0][1] * y2) + x2 * (A[1][0] * y1 + A[1][1] * y2))
        dX_val = x1 * (Ay1 - xTAy)

        Bx1 = B[0][0] * x1 + B[0][1] * x2
        yTBx = (y1 * (B[0][0] * x1 + B[0][1] * x2) + y2 * (B[1][0] * x1 + B[1][1] * x2))
        dY_val = y1 * (Bx1 - yTBx)

        dX[y_i][x_i] = dX_val
        dY[y_i][x_i] = dY_val

# print(dX)
# Normalize the differential equations
norm = np.sqrt(dX ** 2 + dY ** 2)

# print(dX)
# Plot the directional field using quiver
plt.quiver(X, Y, dX, dY)

x, y = zip(*trajectory1)
plt.plot(x, y)

# Add labels and title to the plot
plt.xlabel('Probability of Player 1 playing Action 1')
plt.ylabel('Probability of Player 2 playing Action 1')
plt.title('Directional Field of Probabilities in Matrix Game')

# Show the plot
plt.show()
