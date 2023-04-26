import pyspiel
from open_spiel.python.egt import utils
from open_spiel.python.egt import dynamics
from open_spiel.python.egt import visualization
import matplotlib.pyplot as plt

def create_rps_game():
  game_type = pyspiel.GameType(
      "rock_paper_scissors",
      "rock paper scissors",
      pyspiel.GameType.Dynamics.SIMULTANEOUS,
      pyspiel.GameType.ChanceMode.DETERMINISTIC,
      pyspiel.GameType.Information.ONE_SHOT,
      pyspiel.GameType.Utility.ZERO_SUM,
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
      ["R", "P", "S"],           # Row player actions
      ["R", "P", "S"],           # Column player actions
      [[0, -0.25, 0.5], [0.25, 0, -0.05], [-0.5, 0.05, 0]],   # Row player utilities
      [[0, 0.25, -0.5], [-0.25, 0, 0.05], [0.5, -0.05, 0]]    # Column player utilities
  )
  return game


rps_game = create_rps_game()
payoff_array = utils.game_payoffs_array(rps_game)
dyn = dynamics.SinglePopulationDynamics(payoff_array, dynamics.replicator)
ax = plt.subplot(projection="3x3")
ax.quiver(dyn)
plt.show()
ay = plt.subplot(projection="3x3")
ay.streamplot(dyn)
plt.show()

