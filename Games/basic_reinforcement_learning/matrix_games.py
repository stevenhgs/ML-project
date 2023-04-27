
import pyspiel

def create_biased_rock_paper_scissors_game():
  game_type = pyspiel.GameType(
      "biased_rock_paper_scissors",
      "Biased Rock, Paper, Scissors",
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
      {},                                                   # game_parameters
      ["Rock", "Paper", "Scissors"],                        # row_action_names
      ["Rock", "Paper", "Scissors"],                        # col_action_names
      [[0, -0.25, 0.5], [0.25, 0, -0.05], [-0.5, 0.05, 0]], # Row player utilities
      [[0, 0.25, -0.5], [-0.25, 0, 0.05], [0.5, -0.05, 0]]  # Column player utilities
  )
  return game

def create_dispersion_game():
  game_type = pyspiel.GameType(
      "matching_pennies",
      "Matching Pennies",
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
      ["A", "B"],           # row_action_names
      ["A", "B"],           # col_action_names
      [[-1, -1], [1, 1]],   # Row player utilities
      [[1, 1], [-1, -1]]    # Column player utilities
  )
  return game

def create_battle_of_the_sexes_game():
  game_type = pyspiel.GameType(
      "battle_of_the_sexes",
      "Battle of the Sexes",
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
      ["Opera", "Movie"],   # row_action_names
      ["Opera", "Movie"],   # col_action_names
      [[3, 2], [0, 0]],     # Row player utilities
      [[0, 0], [2, 3]]      # Column player utilities
  )
  return game

def create_prisoners_dilemma_game():
  game_type = pyspiel.GameType(
      "prisoners_dilemma",
      "Prisoner's dilemma",
      pyspiel.GameType.Dynamics.SIMULTANEOUS,
      pyspiel.GameType.ChanceMode.DETERMINISTIC,
      pyspiel.GameType.Information.ONE_SHOT,
      pyspiel.GameType.Utility.GENERAL_SUM,
      pyspiel.GameType.RewardModel.TERMINAL,
      2,        # max num players
      2,        # min_num_players
      True,     # provides_information_state
      True,     # provides_information_state_tensor
      False,    # provides_observation
      False,    # provides_observation_tensor
      dict()    # parameter_specification
  )
  game = pyspiel.MatrixGame(
      game_type,
      {},                       # game_parameters
      ["Cooperate", "Defect"],  # row_action_names
      ["Cooperate", "Defect"],  # col_action_names
      [[-1, -1], [-4, 0]],       # Row player utilities
      [[0, -4], [-3, -3]]       # Column player utilities
  )
  return game

def get_actions(game):
    row_actions = []
    col_actions = []

    for row in range(game.num_rows()):
        row_actions.append(game.row_action_name(row))

    for col in range(game.num_cols()):
        col_actions.append(game.col_action_name(col))

    return row_actions, col_actions

