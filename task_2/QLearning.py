import pdb

import numpy as np
import random

class QLearning:
    def __init__(self,
                 learning_rate,
                 discount_rate):
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.initial_exploration_rate = 1
        self.max_exploration_rate = self.initial_exploration_rate
        self.min_exploration_rate = 0.01
        self.exploration_decay_rate = 0.001
        self.initial_temperature = 80
        self.temperature_decay_rate = 0.01

    def set_exploration_decay_rate(self, decay_rate):
        self.exploration_decay_rate = decay_rate

    @staticmethod
    def epsilon_greedy(Q, actions, exploration_rate):
        # Probability of epsilon to choose random action
        if random.random() < exploration_rate:
            action = random.choice(list(actions.values()))
        # Probability of (1 - epsilon) to choose action with highest Q-value
        else:
            action = np.argmax(Q)

        probabilities = [0 for i in range(len(actions))]
        probabilities[np.argmax(Q)] = 1 - exploration_rate
        probabilities = [x + exploration_rate / len(actions) for x in probabilities]

        return action, probabilities

    @staticmethod
    def boltzmann_exploration(Q, actions, temperature):
        exp_q = np.exp(Q / temperature)
        probabilities = exp_q / np.sum(exp_q)

        action = np.random.choice((len(actions)), p = probabilities)

        return action, probabilities

    def update_q(self, Q, action, reward):
        Q[action] += self.learning_rate * (reward + self.discount_rate * max(Q) - Q[action])

    def learn(self, episodes, actions, payoff, greedy):
        exploration_rate = self.initial_exploration_rate
        temperature = self.initial_temperature
        nb_actions = len(actions)

        Q1 = 4 * np.random.rand(nb_actions) - 4 * np.random.rand(nb_actions)
        Q2 = 4 * np.random.rand(nb_actions) - 4 * np.random.rand(nb_actions)

        trajectory1 = []
        trajectory2 = []

        for episode in range(episodes):
            if(greedy):
                action1, probabilities1 = self.epsilon_greedy(Q1, actions, exploration_rate)
                action2, probabilities2 = self.epsilon_greedy(Q2, actions, exploration_rate)

                exploration_rate = self.min_exploration_rate + \
                                   (self.max_exploration_rate - self.min_exploration_rate) * np.exp(
                    -self.exploration_decay_rate * episode)
            else:
                action1, probabilities1 = self.boltzmann_exploration(Q1, actions, temperature)
                action2, probabilities2 = self.boltzmann_exploration(Q2, actions, temperature)

                temperature = max(temperature - self.temperature_decay_rate, 0.01)

            trajectory1.append(probabilities1)
            trajectory2.append(probabilities2)

            reward1 = payoff[0][action1][action2]
            reward2 = payoff[1][action1][action2]

            self.update_q(Q1, action1, reward1)
            self.update_q(Q2, action2, reward2)

        return Q1, Q2, trajectory1, trajectory2
