
import random
import numpy as np

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

temperature = 0.2   # Temperature for Lenient Boltzmann Q-learning
epsilon = 0.1       # Epsilon for epsilon-greedy exploration
episodes = 10000    # Number of episodes

# Choose an action based on current state and Q-values
def choose_action(Q, state):
    # Probability of epsilon to choose random action
    if random.random() < epsilon:
        action = random.choice(list(actions.values()))
    # Probability of (1 - epsilon) to choose action with highest Q-value
    else:
        action = np.argmax(Q[state])
    return action

# Update the Q-values using Lenient Boltzmann Q-learning
def update_Q(Q, state, action, reward, next_state):
    Q[state][action] += temperature * (reward + max(Q[next_state]) - Q[state][action])

# Play a single episode of biased rock, paper, scissors
def play_episode():
    # Ramdom initial states
    state1 = random.choice(list(actions.values()))
    state2 = random.choice(list(actions.values()))

    action1 = choose_action(Q1, state1)
    action2 = choose_action(Q2, state2)

    reward1 = payoff[state1][action2]
    reward2 = payoff[state2][action1]

    next_state1 = choose_action(Q2, action1)
    next_state2 = choose_action(Q1, action2)
    update_Q(Q1, state1, action1, reward2, next_state1)
    update_Q(Q2, state2, action2, reward1, next_state2)


for i in range(episodes):
    play_episode()

print("Q-values matrix for agent 1:")
print(Q1)
print("Q-values matrix for agent 2:")
print(Q2)