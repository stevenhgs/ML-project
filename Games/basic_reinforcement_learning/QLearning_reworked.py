import pdb

import numpy as np
import random

class QLearning:
    def __init__(self,
                 learning_rate,
                 discount_rate,
                 initial_exploration_rate):
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.initial_exploration_rate = initial_exploration_rate
        self.max_exploration_rate = initial_exploration_rate
        self.min_exploration_rate = 0.01
        self.exploration_decay_rate = 0.001

    def set_exploration_decay_rate(self, decay_rate):
        self.exploration_decay_rate = decay_rate

    @staticmethod
    def choose_action(Q, actions, exploration_rate):
        # Probability of epsilon to choose random action
        if random.random() < exploration_rate:
            action = random.choice(list(actions.values()))
        # Probability of (1 - epsilon) to choose action with highest Q-value
        else:
            action = np.argmax(Q)
        return action

    # Update the Q-values using epsilon-greedy Q-learning
    def update_q(self, Q, action, reward):
        Q[action] += self.learning_rate * (reward + self.discount_rate * max(Q) - Q[action])

    def learn(self, episodes, actions, payoff):
        exploration_rate = self.initial_exploration_rate
        nb_actions = len(actions)

        Q1 = np.zeros((nb_actions))
        Q2 = np.zeros((nb_actions))

        trajectory1 = []
        trajectory2 = []

        for episode in range(episodes):
            action1 = self.choose_action(Q1, actions, exploration_rate)
            action2 = self.choose_action(Q2, actions, exploration_rate)

            P1 = [0 for i in range(nb_actions)]
            P1[np.argmax(Q1)] = 1 - exploration_rate
            P1 = [x + exploration_rate / nb_actions for x in P1]
            trajectory1.append(P1)

            P2 = [0 for i in range(nb_actions)]
            P2[np.argmax(Q2)] = 1 - exploration_rate
            P2 = [x + exploration_rate / nb_actions for x in P2]
            trajectory2.append(P2)

            reward1 = payoff[0][action1][action2]
            reward2 = payoff[1][action1][action2]

            self.update_q(Q1, action1, reward1)
            self.update_q(Q2, action2, reward2)

            exploration_rate = self.min_exploration_rate + \
                               (self.max_exploration_rate - self.min_exploration_rate) * np.exp(-self.exploration_decay_rate * episode)

        return Q1, Q2, trajectory1, trajectory2
