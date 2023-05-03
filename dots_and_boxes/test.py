import time
import pyspiel
from absl import app

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


def get_points(state):
    state_string = s.to_string()
    player_1_points = 0
    player_2_points = 0
    for char in state_string:
        if char == '1':
            player_1_points += 1
        elif char == '2':
            player_2_points += 1
    return player_1_points, player_2_points


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
    print(bin(state_to_bitmap(state.child(i))))
    print(state.child(i))
    print(state.child(i).__hash__())
    print(state.serialize())
    print(state.child(i).information_state_string())
    print(state.child(i).information_state_string().split(', '))
    print(state.current_player())
    print(state.child(i).current_player())

s = game.new_initial_state()
for i in range(12):
    if i in [0, 1, 4, 5]:
        continue
    s = s.child(i)
    print(s.to_string())
    print(s.player_return(0))
    print(s.player_return(1))
    print(get_points(s))
    print(s.rewards())

s = s.child(0)
print(s.to_string())
print(s.player_return(0))
print(s.player_return(1))
print(get_points(s))
print(s.rewards())
s = s.child(1)
print(s.to_string())
print(s.player_return(0))
print(s.player_return(1))
print(get_points(s))
print(s.rewards())
s = s.child(4)
print(s.to_string())
print(s.player_return(0))
print(s.player_return(1))
print(get_points(s))
print(s.rewards())
s = s.child(5)
print(s.to_string())
print(s.player_return(0))
print(s.player_return(1))
print(get_points(s))
print(s.rewards())

print(s.history_str())
print(s.to_string())
print(s.rewards())
print(s.player_reward(0))
print(s.player_reward(1))


print(bin(state_to_bitmap(s)))
