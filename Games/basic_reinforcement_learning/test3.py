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
A = np.array([[-1, 1],
              [1, -1]])

B = np.array([[-1, 1],
              [1, -1]])

# Define the range of x and y values to plot
x = np.arange(0, 1.0, 0.05)
y = np.arange(0, 1.0, 0.05)

mesh_size = len(x)

# Create a meshgrid from the x and y values
X, Y = np.meshgrid(x, y)

print(Y)

# Define the differential equations for the directional field
dX = np.array([[0 for _ in range(mesh_size)] for _ in range(mesh_size)], dtype=float)
dY = np.array([[0 for _ in range(mesh_size)] for _ in range(mesh_size)], dtype=float)

for y_i in range(20):
  y1 = 0.05 * y_i
  y2 = 1 - y1
  for x_i in range(20):
    x1 = 0.05 * x_i
    x2 = 1 - x1

    Ay1 = A[0][0] * y1 + A[0][1] * y2
    xTAy = (x1 * (A[0][0] * y1 + A[0][1] * y2) + x2 * (A[1][0] * y1 + A[1][1] * y2))
    dX_val = x1 * (Ay1 - xTAy)

    Bx1 = B[0][0] * x1 + B[0][1] * x2
    yTBx = (y1 * (B[0][0] * x1 + B[0][1] * x2) + y2 * (B[1][0] * x1 + B[1][1] * x2))
    dY_val = y1 * (Bx1 - yTBx)

    dX[y_i][x_i] = dX_val
    dY[y_i][x_i] = dY_val
    

print(dX)
# Normalize the differential equations
norm = np.sqrt(dX**2 + dY**2)

print(dX)
# Plot the directional field using quiver
plt.quiver(X, Y, dX, dY)

# Add labels and title to the plot
plt.xlabel('Probability of Player 1 playing Action 1')
plt.ylabel('Probability of Player 2 playing Action 1')
plt.title('Directional Field of Probabilities in Matrix Game')

# Show the plot
plt.show()