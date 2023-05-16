import task3.minimax_cache_and_symmetry as minimax_cache_and_symmetry
import pyspiel


num_rows = 8
num_cols = 4

game_string = (f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols},"
                "utility_margin=true)")
game = pyspiel.load_game(game_string)
empty_state = game.new_initial_state()
print(dir(empty_state))
print(empty_state.__sizeof__())
print("\n")
print(dir(game))


def fill_in_nums(game, nums):
    state = game.new_initial_state()
    for num in nums:
        state = state.child(num)
    return state

nums = [0, 5, 50, 25, 36]
flipped_nums = minimax_cache_and_symmetry.flip_over_y_axis(nums, num_rows, num_cols)

state = fill_in_nums(game, nums)
print('state')
print(state)

flipped_state = fill_in_nums(game, flipped_nums)
print('flipped_state')
print(flipped_state)
