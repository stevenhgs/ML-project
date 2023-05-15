import algorithm
import pyspiel

n_r = 8
n_c = 5
game_string = (f"dots_and_boxes(num_rows={n_r},num_cols={n_c},"
                    "utility_margin=true)")
game = pyspiel.load_game(game_string)
state = game.new_initial_state()
nums_to_fill_in = [0, 5, 3, 6, 9, 26, 23, 35, 48, 20, 62, 48, 72, 73]

for num in nums_to_fill_in:
    state = state.child(num)

print(state)



for r_o in range(n_r - 3):
    for c_o in range(n_c - 3):
        algorithm.get_3x3_bitmap_from_filled_in_nums_with_offsets_(nums_to_fill_in, n_r, n_c, r_o, c_o)

