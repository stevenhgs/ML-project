import collections
from Games.Game import Game
from Learners.Learner import Learner


nb_rows = 10
nb_cols = 10

start_state = (0, 0)
states = list()
actions = list()
state_to_actions = collections.defaultdict(list)
state_to_reward = dict()
state_action_to_state = dict()
end_states = set()

# set states
for r_i in range(nb_rows):
    for c_i in range(nb_cols):
        states.append((r_i, c_i))

# set actions
actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
# set state to actions
for state in states:
    # 0: up, 1: right, 2: down, 3: left
    if state[0] > 0:  # up is possible
        state_to_actions[state].append((-1, 0))
    if state[0] < nb_rows - 1:  # down is possible
        state_to_actions[state].append((1, 0))
    if state[1] < nb_cols - 1:  # right is possible
        state_to_actions[state].append((0, 1))
    if state[1] > 0:  # left is possible
        state_to_actions[state].append((0, -1))

# set rewards
for state in states:
    state_to_reward[state] = -1
state_to_reward[(nb_rows // 2, nb_cols // 2)] = 10

# set state action to state
for state, possible_actions in state_to_actions.items():
    for action in possible_actions:
        state_action_to_state[(state, action)] = (state[0] + action[0], state[1] + action[1])
end_states = {(nb_rows // 2, nb_cols // 2)}

game = Game(start_state, states, actions, state_to_actions, state_to_reward, state_action_to_state, end_states)
learner = Learner(alpha=0.75, gamma=1, epsilon=0.8)
q_table, row_index_to_state, col_index_to_action = learner.learn(game, nb_episodes=10000)

action_to_emoji = {
    (-1, 0): "⬆️",
    (1, 0): "⬇️",
    (0, -1): "⬅️",
    (0, 1): "➡️"
}

policy = [[None for _ in range(nb_cols)] for _ in range(nb_rows)]
for r_i, row in enumerate(q_table):
    state = row_index_to_state[r_i]
    highest_val, highest_val_index = float('-inf'), None
    for c_i, val in enumerate(row):
        if val is None:
            continue
        if val > highest_val:
            highest_val = val
            highest_val_index = c_i
    policy[state[0]][state[1]] = action_to_emoji[col_index_to_action[highest_val_index]]

for row in policy:
    print(''.join(row))
