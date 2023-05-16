import pyspiel
import random

def get_2x2_bitmap_from_filled_in_nums_with_offsets(filled_in_nums, n_r, n_c, r_o, c_o):
    """
    filled_in_nums should be a set, for time complexity.
    n_r is the number of rows of cells in the game.
    """
    bitmap = 0
    number_of_horizontal_lines = (n_r + 1) * n_c
    
    _2x2_nums = []
    # get horizontal lines
    for e in range(6):
        r_i = e // 2
        c_i = e % 2
        num_to_find = (r_o * n_c) + (r_i * n_c) + c_o + c_i
        if num_to_find in filled_in_nums:
            bitmap |= 1 << e
            _2x2_nums.append(e)
    
    # get vertical lines
    for e in range(6):
        r_i = e // (2 + 1)
        c_i = e % (2 + 1)
        num_to_find = (r_o * (n_c + 1)) + (r_i * (n_c + 1)) + c_o + c_i + number_of_horizontal_lines
        if num_to_find in filled_in_nums:
            bitmap |= 1 << (e + 6)
            _2x2_nums.append(e + 6)

    return bitmap


def remap_nums_from_2x2_to_nrxnc_with_offset(nums, n_r, n_c, r_o, c_o):
    remapped_nums = []
    nb_of_horizontal_lines = (n_r + 1) * n_c
    nb_horizontal_lines_2x2 = 2 * (2 + 1)
    for num in nums:
        if num >= nb_horizontal_lines_2x2:  # vertical 3x3 line
            val = num - nb_horizontal_lines_2x2
            r_i = val // (2 + 1)
            c_i = val % (2 + 1)
            remapped_num = (r_o * (n_c + 1)) + (r_i * (n_c + 1)) + c_o + c_i + nb_of_horizontal_lines
            remapped_nums.append(remapped_num)
        else:
            r_i = num // 2
            c_i = num % 2
            remapped_num = (r_o * n_c) + (r_i * n_c) + c_o + c_i
            remapped_nums.append(remapped_num)
    return remapped_nums



def get_best_moves_from_state(state, state_to_actions_and_values):
    info_string = state.history_str()
    if info_string == '':
        filled_in_nums = set()
    else:
        split_info_string = info_string.split(', ')
        filled_in_nums = {int(digit) for digit in split_info_string}

    game_parameters = state.get_game().get_parameters()
    n_r = game_parameters['num_rows']
    n_c = game_parameters['num_cols']
    
    current_best_actions = list()
    current_best_value = float("-inf")
    for r_o in range(n_r - 2 + 1):
        for c_o in range(n_c - 2 + 1):
            bitmap = get_2x2_bitmap_from_filled_in_nums_with_offsets(filled_in_nums, n_r, n_c, r_o, c_o)
            if bitmap == 4095:  # completely filled in 2x2
                continue
            best_actions, best_value = state_to_actions_and_values[str(bitmap)]
            best_value = int(best_value)

            if best_value >= current_best_value:
                best_actions_remapped = remap_nums_from_2x2_to_nrxnc_with_offset(best_actions, n_r, n_c, r_o, c_o)
                current_best_actions = list(best_actions_remapped)
            elif best_value == current_best_value:
                best_actions_remapped = remap_nums_from_2x2_to_nrxnc_with_offset(best_actions, n_r, n_c, r_o, c_o)
                current_best_actions.extend(best_actions_remapped)
    
    return random.choice(current_best_actions)


def print_state_of_2x2(filled_in_nums):
    game_string = (f"dots_and_boxes(num_rows={2},num_cols={2},"
                    "utility_margin=true)")
    game = pyspiel.load_game(game_string)
    state = game.new_initial_state()
    for num in filled_in_nums:
        state = state.child(num)
    print(state)
