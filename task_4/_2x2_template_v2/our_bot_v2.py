import pyspiel
from task_4._2x2_template_v2.algorithm_v2 import get_best_moves_from_state
import json
import os


class OurBot(pyspiel.Bot):
    def __init__(self, player_id):
        """Initializes a uniform-random bot.

        Args:
        player_id: The integer id of the player for this bot, e.g. `0` if acting
            as the first player.
        rng: A random number generator supporting a `choice` method, e.g.
            `np.random`
        """
        pyspiel.Bot.__init__(self)
        self._player_id = player_id
        package_directory = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(package_directory, '2x2_minimax.json')
        with open(json_file, 'r') as fp:
            self.cache = json.load(fp)
    
    def restart_at(self, state):
        pass

    def player_id(self):
        return self._player_id
    
    def step(self, state):
        return get_best_moves_from_state(state, self.cache)