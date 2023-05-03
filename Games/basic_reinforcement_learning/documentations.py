import pyspiel
import matrix_games

print("all functions on MatrixGame")
all_methods = dir(pyspiel.MatrixGame)

for method in all_methods:
    print(method)

prisoners_dilemma = matrix_games.create_prisoners_dilemma_game()


print(pyspiel.MatrixGame.__dict__)
print(prisoners_dilemma.row_utilities())
print(prisoners_dilemma.col_utilities())