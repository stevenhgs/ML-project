import time
import pyspiel
from absl import app
from collections import defaultdict


def get_points(state):
    state_string = state.to_string()
    player_1_points = 0
    player_2_points = 0
    for char in state_string:
        if char == '1':
            player_1_points += 1
        elif char == '2':
            player_2_points += 1
    return player_1_points, player_2_points


def state_to_bitmap(state):
    points = get_points(state)
    info_string = state.history_str()
    if info_string == '':
        return 0, points, state.current_player()
    split_info_string = info_string.split(', ')
    info_digits = [int(digit) for digit in split_info_string]
    bit_map = 0
    for digit in info_digits:
        flag = 1 << digit
        bit_map |= flag
    return bit_map, points, state.current_player()


def start_minimax(start_state, start_maximizing_player_id):
    cache = dict()
    nb_nodes = 0
    state_to_action_cache = dict()

    def _minimax(state, maximizing_player_id):
        """
        Implements a min-max algorithm

        Arguments:
        state: The current state node of the game.
        maximizing_player_id: The id of the MAX player. The other player is assumed
            to be MIN.

        Returns:
        The optimal value of the sub-game starting in state
        """
        nonlocal nb_nodes
        state_hash = state_to_bitmap(state)
        if cache.get(state_hash) is not None:
            return cache[state_hash]

        """
        if len(state.legal_actions()) == 1:
            print('one move left')
            print(state)
            print(f'players turn: {state.current_player()}')
            print(state.child(state.legal_actions()[0]))
            print(state.child(state.legal_actions()[0]).player_return(maximizing_player_id))
            print('end')
        """

        nb_nodes += 1
        if nb_nodes % 10000 == 0:
            print(nb_nodes)
        if state.is_terminal():
            points1, points2 = get_points(state)
            cache[state_hash] = points1 - points2
            print(state)
            print(f'players turn: {state.player_reward(maximizing_player_id)}')
            print(cache[state_hash])
            return cache[state_hash]

        player = state.current_player()
        if player == maximizing_player_id:
            selection = max
            factor = 1
        else:
            selection = min
            factor = -1
        
        # part to get the best action
        points1, points2 = get_points(state)
        current_points_difference = points1 - points2
        current_best_value = None
        best_actions = []
        values_children = []
        for action in state.legal_actions():
            value = _minimax(state.child(action), maximizing_player_id)
            values_children.append(value)
            if current_best_value is None or value * factor > current_best_value:
                best_actions = [action]
                current_best_value = value * factor
            elif _minimax(state.child(action), maximizing_player_id) * factor == current_best_value:
                best_actions.append(action)
        max_points_to_gain = current_best_value - (current_points_difference * factor)
        state_to_action_cache[state_hash] = (best_actions, max_points_to_gain)

        output = selection(values_children)
        cache[state_hash] = output
        return output
    
    result = _minimax(start_state, start_maximizing_player_id)
    sanitized_cache = defaultdict(list)
    for key, val in state_to_action_cache.items():
        bitmap, _, _ = key
        sanitized_cache[bitmap] = val
    
    import json
    with open('dots_and_boxes/3x3_try/state_to_best_actions_and_gain_cache_3x3.json', 'w') as fp:
        json.dump(sanitized_cache, fp)
    print(nb_nodes, ' nodes visited')
    return result


def minimax_search(game,
                   state=None,
                   maximizing_player_id=None,
                   state_to_key=lambda state: state):
    """Solves deterministic, 2-players, perfect-information 0-sum game.

    For small games only! Please use keyword arguments for optional arguments.

    Arguments:
      game: The game to analyze, as returned by `load_game`.
      state: The state to run from.  If none is specified, then the initial state is assumed.
      maximizing_player_id: The id of the MAX player. The other player is assumed
        to be MIN. The default (None) will suppose the player at the root to be
        the MAX player.

    Returns:
      The value of the game for the maximizing player when both player play optimally.
    """
    game_info = game.get_type()

    if game.num_players() != 2:
        raise ValueError("Game must be a 2-player game")
    if game_info.chance_mode != pyspiel.GameType.ChanceMode.DETERMINISTIC:
        raise ValueError("The game must be a Deterministic one, not {}".format(
            game.chance_mode))
    if game_info.information != pyspiel.GameType.Information.PERFECT_INFORMATION:
        raise ValueError(
            "The game must be a perfect information one, not {}".format(
                game.information))
    if game_info.dynamics != pyspiel.GameType.Dynamics.SEQUENTIAL:
        raise ValueError("The game must be turn-based, not {}".format(
            game.dynamics))
    if game_info.utility != pyspiel.GameType.Utility.ZERO_SUM:
        raise ValueError("The game must be 0-sum, not {}".format(game.utility))

    if state is None:
        state = game.new_initial_state()
    if maximizing_player_id is None:
        maximizing_player_id = state.current_player()
    v = start_minimax(state.clone(),maximizing_player_id)
    return v


def main(_):
    start = time.time()

    games_list = pyspiel.registered_names()
    assert "dots_and_boxes" in games_list
    game_string = "dots_and_boxes(num_rows=3,num_cols=3)"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)

    value = minimax_search(game)

    if value == 0:
        print("It's a draw")
    else:
        winning_player = 1 if value == 1 else 2
        print(f"Player {winning_player} wins.")

    end = time.time()
    print("Game took: " + str(end - start) + " s")


if __name__ == "__main__":
    app.run(main)
