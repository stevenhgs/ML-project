import random
import numpy as np

print('test')

actions = {"rock":      0,
           "paper":     1,
           "scissors":  2}

# Payoff table
payoff = np.array([[0,      -0.25,  0.5     ],
                   [0.25,   0,      -0.05   ],
                   [-0.5,   0.05,   0       ]])

# Initialize Q-values matrices for each agent
Q1 = np.zeros((3, 3))
Q2 = np.zeros((3, 3))

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

# Play a single episode of biased rock, paper, scissors
def play_episode():
    # Ramdom initial states
    state1 = random.choice(list(actions.values()))
    state2 = random.choice(list(actions.values()))

    action1 = choose_action(Q1, state1)
    action2 = choose_action(Q2, state2)

    P1 = [0, 0, 0]
    P1[action1] = 1 - exploration_rate
    P1 = [x + exploration_rate/3 for x in P1]
    trajectory1.append(P1)

    P2 = [0, 0, 0]
    P2[action2] = 1 - exploration_rate
    P2 = [x + exploration_rate/3 for x in P2]
    trajectory2.append(P2)

    reward1 = payoff[action1][action2]
    reward2 = payoff[action2][action1]

    next_state1 = choose_action(Q1, action1)
    next_state2 = choose_action(Q2, action2)
    update_Q(Q1, state1, action1, reward1, next_state1)
    update_Q(Q2, state2, action2, reward2, next_state2)


for episode in range(episodes):
    play_episode()
    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

print("Q-values matrix for agent 1:")
print(Q1)
print("Q-values matrix for agent 2:")
print(Q2)
