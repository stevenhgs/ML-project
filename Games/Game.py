class Game:
    def __init__(self,
                 start_state,
                 states: list,
                 actions: list,
                 state_to_actions: dict,
                 state_to_reward: dict,
                 state_action_to_state: dict,
                 end_states: set):
        self.current_state = start_state
        self.start_state = start_state
        self.states = states
        self.actions = actions
        self.state_to_actions = state_to_actions
        self.state_to_reward = state_to_reward
        self.state_action_to_state = state_action_to_state
        self.end_states = end_states

    def reset(self):
        self.current_state = self.start_state

    def step(self, action):
        self.current_state = self.state_action_to_state[(self.current_state, action)]
        return self.current_state, self.state_to_reward[self.current_state], self.current_state in self.end_states
