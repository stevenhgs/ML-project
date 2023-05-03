import pyspiel
from open_spiel.python import rl_environment
import numpy as np
import matplotlib.pyplot as plt


def create_dispersion_game():
  game_type = pyspiel.GameType(
      "dispersion_game",
      "Dispersion Game",
      pyspiel.GameType.Dynamics.SIMULTANEOUS,
      pyspiel.GameType.ChanceMode.DETERMINISTIC,
      pyspiel.GameType.Information.ONE_SHOT,
      pyspiel.GameType.Utility.GENERAL_SUM,
      pyspiel.GameType.RewardModel.TERMINAL,
      2,        # max_num_players
      2,        # min_num_players
      True,     # provides_information_state
      True,     # provides_information_state_tensor
      False,    # provides_observation
      False,    # provides_observation_tensor
      dict()    # parameter_specification
  )
  game = pyspiel.MatrixGame(
      game_type,
      {},                   # game_parameters
      ["A", "B"],           # Row player actions
      ["A", "B"],           # Column player actions
      [[-1, -1], [1, 1]],   # Row player utilities
      [[1, 1], [-1, -1]]    # Column player utilities
  )
  return game


dispersion_game = create_dispersion_game()

print(dispersion_game)
environment = rl_environment.Environment(dispersion_game)
print(environment.observation_spec())
print(environment.reset())
print(dispersion_game.num_rows())
print(dispersion_game.player_utility(0, 1, 1))


# Define the matrix game payoff matrix
A = np.array([[4, 1],
              [3, 3]])

B = np.array([[4, 1],
              [3, 3]])

# Define the range of x and y values to plot
x = np.arange(0, 1.0, 0.05)
y = np.arange(0, 1.0, 0.05)

mesh_size = len(x)

# Create a meshgrid from the x and y values
X, Y = np.meshgrid(x, y)

# Define the differential equations for the directional field
dX = np.array([[0 for _ in range(mesh_size)] for _ in range(mesh_size)], dtype=float)
dY = np.array([[0 for _ in range(mesh_size)] for _ in range(mesh_size)], dtype=float)

for r_i in range(mesh_size):
  y_val = Y[r_i][0]
  for c_i in range(mesh_size):
    x_val = X[0][c_i]
    new_dx = x_val * (A[0][0] * y_val + A[0][1] * (1 - y_val) - (x_val * (A[0][0] * y_val + A[0][1] * (1 - y_val) + (1 - x_val) * (A[1][0] * y_val + A[1][1] * (1 - y_val)))))
    new_dy = y_val * (B[0][0] * x_val + B[0][1] * (1 - x_val) - (y_val * (B[0][0] * x_val + B[0][1] * (1 - x_val) + (1 - y_val) * (B[1][0] * x_val + B[1][1] * (1 - x_val)))))
    dX[r_i, c_i] = new_dx
    print(new_dx)
    print(dX[r_i, c_i])
    print(dX)
    dY[r_i, c_i] = new_dy

print(dX)
# Normalize the differential equations
norm = np.sqrt(dX**2 + dY**2)
dX = dX / norm
dY = dY / norm

print("all functions on MatrixGame")
print(dir(pyspiel.MatrixGame))
print(dX)
# Plot the directional field using quiver
plt.quiver(X, Y, dX, dY)

# Add labels and title to the plot
plt.xlabel('Probability of Player 1 playing Action 1')
plt.ylabel('Probability of Player 2 playing Action 1')
plt.title('Directional Field of Probabilities in Matrix Game')

# Show the plot
plt.show()