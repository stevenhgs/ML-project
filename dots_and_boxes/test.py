import time
import pyspiel
from absl import app


num_rows, num_cols = 2, 2  # Number of squares
game_string = (f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols},"
                "utility_margin=true)")
game = pyspiel.load_game(game_string)

state = game.new_initial_state()
print('split')
print(state.information_state_string())
print(state.information_state_string().split(', '))
print('end_split')

state = state.child(0)
print(type(state))
print(dir(pyspiel.DotsAndBoxesState))
for i in range(1, 12):
    print(i)
    print(state.child(i))
    print(state.child(i).__hash__())
    print(state.serialize())
    print(state.child(i).information_state_string())
    print(state.child(i).information_state_string().split(', '))
    print(state.current_player())
    print(state.child(i).current_player())

s = game.new_initial_state()
for i in range(12):
    s = s.child(i)
print(s.history_str())
print(s.to_string())
print(s.player_return(0))


def state_to_bitmap(state):
    info_string = state.history_str()
    if info_string == '':
        return 0
    split_info_string = info_string.split(', ')
    info_digits = [int(digit) for digit in split_info_string]
    bit_map = 0
    for digit in info_digits:
        flag = 1 << digit
        bit_map |= flag
    return bit_map


