import pyspiel
from absl import app
import time
import sys


def flip_over_x_axis(filled_in_nums, n_r, n_c):
    nb_horizontal_lines = n_c * (n_r + 1)
    flipped_filled_in_nums = []
    for num in filled_in_nums:
        # extra is 1 if it is a vertical line else 0
        extra = 1 if num >= nb_horizontal_lines else 0
        # this is to map the vertical lines so that it starts from 0 as well
        mapped_num = num - (nb_horizontal_lines * extra)
        row_index = (mapped_num // (n_c + extra))
        middle_row_index = (n_r - extra) / 2
        flip = int(2 * (middle_row_index - row_index)) * (n_c + extra)
        flipped_num = mapped_num + flip
        # map the flipped num back to a vertical line if it was one
        flipped_num += (nb_horizontal_lines * extra)
        flipped_filled_in_nums.append(flipped_num)
    return flipped_filled_in_nums


def flip_over_y_axis(filled_in_nums, n_r, n_c):
    nb_horizontal_lines = n_c * (n_r + 1)
    flipped_filled_in_nums = []
    for num in filled_in_nums:
        # extra is 1 if it is a vertical line else 0
        extra = 1 if num >= nb_horizontal_lines else 0
        # this is to map the vertical lines so that it starts from 0 as well
        mapped_num = num - (nb_horizontal_lines * extra)
        column_index = (mapped_num % (n_c + extra))
        middle_column_index = (n_c - 1 + extra) / 2
        distance_to_middle_column_index = middle_column_index - column_index
        flip = int(2 * distance_to_middle_column_index)
        flipped_num = mapped_num + flip
        # map the flipped num back to a vertical line if it was one
        flipped_num += (nb_horizontal_lines * extra)
        flipped_filled_in_nums.append(flipped_num)
    return flipped_filled_in_nums


def rotate_90_degrees(filled_in_nums, n):
    nb_horizontal_lines = n * (n + 1)
    rotated_filled_in_nums = []
    for num in filled_in_nums:
        if num >= nb_horizontal_lines: # this is vertical line
            mapped_num = num - nb_horizontal_lines
            r_i = mapped_num // (n + 1)
            c_i = mapped_num % (n + 1)
            rotated_num = n * (c_i + 1) - 1 - r_i
            rotated_filled_in_nums.append(rotated_num)
        else: # this is a horizontal line
            r_i = num // n
            c_i = num % n
            rotated_num = (n - r_i) + ((n + 1) * c_i)
            rotated_filled_in_nums.append(rotated_num + nb_horizontal_lines)
    return rotated_filled_in_nums


def filled_in_nums_to_bitmap(filled_in_nums):
    bit_map = 0
    for digit in filled_in_nums:
        flag = 1 << digit
        bit_map |= flag
    return bit_map


def add_symmetries_to_cache(cache, value, state, n_r, n_c):
    points = get_points(state)
    info_string = state.history_str()
    if info_string == '': 
        return 0
    split_info_string = info_string.split(', ')
    filled_in_nums = [int(digit) for digit in split_info_string]
    # normal key
    key = (filled_in_nums_to_bitmap(filled_in_nums), points, state.current_player())
    cache[key] = value
    # flipped key horizontal
    flipped_over_x_nums = flip_over_x_axis(filled_in_nums, n_r, n_c)
    key_flipped_over_x = (filled_in_nums_to_bitmap(flipped_over_x_nums), points, state.current_player())
    cache[key_flipped_over_x] = value

    if n_r == n_c:  # square field (6 extra symmetries)
        rotated_nums_90 = rotate_90_degrees(filled_in_nums, n_r)
        key90 = (filled_in_nums_to_bitmap(rotated_nums_90), points, state.current_player())
        cache[key90] = value
        flipped_over_x_nums_90 = flip_over_x_axis(rotated_nums_90, n_r, n_c)
        key_flipped_over_x_90 = (filled_in_nums_to_bitmap(flipped_over_x_nums_90), points, state.current_player())
        cache[key_flipped_over_x_90] = value
        rotated_nums_180 = rotate_90_degrees(rotated_nums_90, n_r)
        key180 = (filled_in_nums_to_bitmap(rotated_nums_180), points, state.current_player())
        cache[key180] = value
        flipped_over_x_nums_180 = flip_over_x_axis(rotated_nums_180, n_r, n_c)
        key_flipped_over_x_180 = (filled_in_nums_to_bitmap(flipped_over_x_nums_180), points, state.current_player())
        cache[key_flipped_over_x_180] = value
        rotated_nums_270 = rotate_90_degrees(rotated_nums_180, n_r)
        key270 = (filled_in_nums_to_bitmap(rotated_nums_270), points, state.current_player())
        cache[key270] = value
        flipped_over_x_nums_270 = flip_over_x_axis(rotated_nums_270, n_r, n_c)
        key_flipped_over_x_270 = (filled_in_nums_to_bitmap(flipped_over_x_nums_270), points, state.current_player())
        cache[key_flipped_over_x_270] = value
    else:  # rectangular field (2 extra symmetries)
        flipped_over_y_nums = flip_over_y_axis(filled_in_nums, n_r, n_c)
        key_flipped_over_y = (filled_in_nums_to_bitmap(flipped_over_y_nums), points, state.current_player())
        cache[key_flipped_over_y] = value
        flipped_over_x_and_y_nums = flip_over_y_axis(flipped_over_x_nums, n_r, n_c)
        key_flipped_over_x_and_y = (filled_in_nums_to_bitmap(flipped_over_x_and_y_nums), points, state.current_player())
        cache[key_flipped_over_x_and_y] = value


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


def start_minimax(start_state, start_maximizing_player_id, num_rows, num_cols):
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
            value = state.player_return(maximizing_player_id)
            add_symmetries_to_cache(cache, value, state, num_rows, num_cols)
            return value

        player = state.current_player()
        if player == maximizing_player_id:
            selection = max
        else:
            selection = min
        values_children = [_minimax(state.child(action), maximizing_player_id) for action in state.legal_actions()]
        output = selection(values_children)
        add_symmetries_to_cache(cache, output, state, num_rows, num_cols)
        return output
    
    result = _minimax(start_state, start_maximizing_player_id)
    print('\ncache + symmetries:')
    print(f'num_rows: {num_rows}, num_cols: {num_cols}')
    print(f'number explored nodes: {nb_nodes}')
    print(f'cache size: {sys.getsizeof(cache)}')
    print(f'number of keys stored: {nb_nodes}')
    return result


def minimax_search(game,
                   num_rows,
                   num_cols,
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
    v = start_minimax(state.clone(), maximizing_player_id, num_rows, num_cols)
    return v


def main(_):
    start = time.perf_counter()

    games_list = pyspiel.registered_names()
    assert "dots_and_boxes" in games_list
    num_rows = 2
    num_cols = 2
    game_string = f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})"

    print("Creating game: {}".format(game_string))
    game = pyspiel.load_game(game_string)

    value = minimax_search(game, num_rows, num_cols)

    if value == 0:
        print("It's a draw")
    else:
        winning_player = 1 if value == 1 else 2
        print(f"Player {winning_player} wins.")

    end = time.perf_counter()
    print("Game took: " + str(end - start) + " s")


if __name__ == "__main__":
    app.run(main)
