# Copyright 2019 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""MCTS example for dots and boxes based on: https://github.com/deepmind/open_spiel/blob/master/open_spiel/python/examples/mcts.py"""

import collections
import random
import sys

from absl import app
from absl import flags
import numpy as np

from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import uniform_random
import pyspiel

import _2x2_template_v1.our_bot as our_bot
import _2x2_template_v2.our_bot_v2 as our_bot_v2
import time

_KNOWN_PLAYERS = [
    # A generic Monte Carlo Tree Search agent.
    "mcts1",

    # A generic Monte Carlo Tree Search agent.
    "mcts2",

    # our sliding window implementation
    "sliding",

    # our sliding window implementation a bit tweaked
    "sliding_v2",

    # A generic random agent.
    "random"
]

n_r = 7
n_c = 7
flags.DEFINE_string("game", f"dots_and_boxes(num_rows={n_r},num_cols={n_c},"
                    "utility_margin=true)", "Name of the game.")

# change players here
flags.DEFINE_enum("player1", "sliding", _KNOWN_PLAYERS, "Who controls player 1.")
flags.DEFINE_enum("player2", "sliding_v2", _KNOWN_PLAYERS, "Who controls player 2.")
# PARAMETER FOR MCTS1
flags.DEFINE_integer("uct_c1", 2, "UCT's exploration constant.")
flags.DEFINE_integer("rollout_count1", 1, "How many rollouts to do.")
flags.DEFINE_integer("max_simulations1", 80, "How many simulations to run.")
# PARAMETER FOR MCTS2
flags.DEFINE_integer("uct_c2", 2, "UCT's exploration constant.")
flags.DEFINE_integer("rollout_count2", 10, "How many rollouts to do.")
flags.DEFINE_integer("max_simulations2", 1000, "How many simulations to run.")

flags.DEFINE_integer("num_games", 100, "How many games to play.")
flags.DEFINE_integer("seed", None, "Seed for the random number generator.")
flags.DEFINE_bool("random_first", False, "Play the first move randomly.")
flags.DEFINE_bool("solve", True, "Whether to use MCTS-Solver.")
flags.DEFINE_bool("quiet", False, "Don't show the moves as they're played.")
flags.DEFINE_bool("verbose", False, "Show the MCTS stats of possible moves.")

FLAGS = flags.FLAGS


def _opt_print(*args, **kwargs):
  if not FLAGS.quiet:
    print(*args, **kwargs)


def _init_bot(bot_type, game, player_id):
  """Initializes a bot by type."""
  rng = np.random.RandomState(FLAGS.seed)
  if bot_type == "mcts1":
    print("preparing mcts1")
    evaluator = mcts.RandomRolloutEvaluator(FLAGS.rollout_count1, rng)
    return mcts.MCTSBot(
        game,
        FLAGS.uct_c1,
        FLAGS.max_simulations1,
        evaluator,
        random_state=rng,
        solve=FLAGS.solve,
        verbose=FLAGS.verbose)
  if bot_type == "sliding":
    print("preparing our_bot")
    return our_bot.OurBot(player_id)
  if bot_type == "sliding_v2":
    print("preparing our_bot")
    return our_bot_v2.OurBot(player_id)
  if bot_type == "mcts2":
    print("preparing mcts2")
    evaluator = mcts.RandomRolloutEvaluator(FLAGS.rollout_count2, rng)
    return mcts.MCTSBot(
        game,
        FLAGS.uct_c2,
        FLAGS.max_simulations2,
        evaluator,
        random_state=rng,
        solve=FLAGS.solve,
        verbose=FLAGS.verbose)
  if bot_type == "random":
    print("preparing random")
    return uniform_random.UniformRandomBot(player_id, rng)
  raise ValueError("Invalid bot type: %s" % bot_type)


def _get_action(state, action_str):
  for action in state.legal_actions():
    if action_str == state.action_to_string(state.current_player(), action):
      return action
  return None


def _play_game(game, bots, initial_actions):
  """Plays one game."""
  state = game.new_initial_state()
  # _opt_print("Initial state:\n{}".format(state))

  history = []

  if FLAGS.random_first:
    assert not initial_actions
    initial_actions = [state.action_to_string(
        state.current_player(), random.choice(state.legal_actions()))]
    print(f'initial actions: {initial_actions}')

  while not state.is_terminal():
    current_player = state.current_player()

    # Decision node: sample action for the single current player
    bot = bots[current_player]
    action = bot.step(state)
    action_str = state.action_to_string(current_player, action)
    # _opt_print("Player {} sampled action: {}".format(current_player, action_str))

    for i, bot in enumerate(bots):
      if i != current_player:
        bot.inform_action(state, current_player, action)
    history.append(action_str)
    state.apply_action(action)

    # _opt_print("Next state:\n{}".format(state))

  # Game is now done. Print return for each player
  returns = state.returns()
  # print("Returns:", " ".join(map(str, returns)), ", Game actions:"," ".join(history))

  for bot in bots:
    bot.restart()

  return returns, history


def main(argv):
  start = time.time()
  game = pyspiel.load_game(FLAGS.game)
  if game.num_players() > 2:
    sys.exit("This game requires more players than the example can handle.")
  bots = [
      _init_bot(FLAGS.player1, game, 0),
      _init_bot(FLAGS.player2, game, 1),
  ]
  histories = collections.defaultdict(int)
  overall_returns = [0, 0]
  overall_wins = [0, 0]
  game_num = 0
  try:
    for game_num in range(FLAGS.num_games):
      print(f'playing game {game_num + 1}')
      returns, history = _play_game(game, bots, argv[1:])
      histories[" ".join(history)] += 1
      for i, v in enumerate(returns):
        overall_returns[i] += v
        if v > 0:
          overall_wins[i] += 1
  except (KeyboardInterrupt, EOFError):
    game_num -= 1
    print("Caught a KeyboardInterrupt, stopping early.")
  print("Number of games played:", game_num + 1)
  print("Number of distinct games played:", len(histories))
  print("Players:", FLAGS.player1, FLAGS.player2)
  print("Overall wins", overall_wins)
  print("Overall returns", overall_returns)
  end = time.time()
  print(f"took {end - start}s to run")


if __name__ == "__main__":
  app.run(main)
  