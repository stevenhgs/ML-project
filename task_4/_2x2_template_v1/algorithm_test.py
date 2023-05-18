import algorithm
import pyspiel
import json

n_r = 8
n_c = 5
game_string = (f"dots_and_boxes(num_rows={n_r},num_cols={n_c},"
                    "utility_margin=true)")
game = pyspiel.load_game(game_string)
state = game.new_initial_state()
nums_to_fill_in = [0, 5, 3, 6, 9, 26, 23, 56]

for num in nums_to_fill_in:
    state = state.child(num)

print(state)

with open('dots_and_boxes/_3x3_try/state_to_best_actions_and_gain_cache_2x2.json', 'r') as fp:
    cache = json.load(fp)


for r_o in range(n_r - 2 + 1):
    for c_o in range(n_c - 2 + 1):
        bitmap = algorithm.get_2x2_bitmap_from_filled_in_nums_with_offsets(nums_to_fill_in, n_r, n_c, r_o, c_o)
        print(bitmap)
        print(cache[str(bitmap)])


print(algorithm.get_best_moves_from_state(state, cache))

