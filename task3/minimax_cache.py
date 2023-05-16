import time
import pyspiel
from absl import app


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
        state_hash = state_to_bitmap(state)
        if cache.get(state_hash) is not None:
            return cache[state_hash]

        nonlocal nb_nodes
        nb_nodes += 1
        if state.is_terminal():
            cache[state_hash] = state.player_return(maximizing_player_id)
            print(state)
            print(cache[state_hash])
            return state.player_return(maximizing_player_id)

        player = state.current_player()
        if player == maximizing_player_id:
            selection = max
        else:
            selection = min
        values_children = [_minimax(state.child(action), maximizing_player_id) for action in state.legal_actions()]
        output = selection(values_children)
        cache[state_hash] = output
        return output
    
    result = _minimax(start_state, start_maximizing_player_id)
    print(f'explored {nb_nodes} nodes')
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
    game_string = "dots_and_boxes(num_rows=2,num_cols=2)"

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
