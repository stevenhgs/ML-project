import pyspiel


num_rows = 2
num_cols = 2

game_string = (f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols},"
                "utility_margin=true)")
game = pyspiel.load_game(game_string)
empty_state = game.new_initial_state()
state = empty_state.child(0)

print(dir(empty_state))
print(state.action_to_string(1, 11))
print(state.get_game())
print(dir(game))
print(game.get_parameters())