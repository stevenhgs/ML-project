from Games.Game import Game
import random


class Learner:
    def __init__(self, alpha: float, gamma: float, epsilon: float):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def learn(self, game: Game, nb_episodes: int):
        nb_of_states = len(game.states)
        nb_of_actions = len(game.actions)
        q_table = [[0 for _ in range(nb_of_actions)] for _ in range(nb_of_states)]

        state_to_row_index = dict()
        row_index_to_state = dict()
        for i, state in enumerate(game.states):
            state_to_row_index[state] = i
            row_index_to_state[i] = state

        col_index_to_action = dict()
        action_to_col_index = dict()
        for i, action in enumerate(game.actions):
            col_index_to_action[i] = action
            action_to_col_index[action] = i

        # handle illegal actions in states
        for state in game.states:
            for c_i in range(nb_of_actions):
                action = col_index_to_action[c_i]
                if action not in game.state_to_actions[state]:
                    q_table[state_to_row_index[state]][c_i] = None

        for _ in range(nb_episodes):
            game.reset()
            done = False

            while not done:
                state = game.current_state
                if random.uniform(0, 1) < self.epsilon:
                    action = random.choice(game.state_to_actions[state])
                else:
                    _, best_col_index = Learner.get_best_q_val_and_action(q_table[state_to_row_index[state]])
                    action = col_index_to_action[best_col_index]

                new_state, reward, done = game.step(action)
                best_q_val_new_state, _ = Learner.get_best_q_val_and_action(q_table[state_to_row_index[new_state]])
                old_q_val = q_table[state_to_row_index[state]][action_to_col_index[action]]
                q_table[state_to_row_index[state]][action_to_col_index[action]] = old_q_val + self.alpha * (reward + self.gamma * best_q_val_new_state - old_q_val)

        return q_table, row_index_to_state, col_index_to_action

    @staticmethod
    def get_best_q_val_and_action(arr):
        best_val = float('-inf')
        best_val_index = None

        for i, val in enumerate(arr):
            if val is None:
                continue
            if val > best_val:
                best_val = val
                best_val_index = i
            elif val == best_val and random.uniform(0, 1) < 0.5:  # if the values are the same chose one of the two randomly
                best_val = val
                best_val_index = i
        return best_val, best_val_index
