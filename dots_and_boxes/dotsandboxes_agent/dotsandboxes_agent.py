#!/usr/bin/env python3
# encoding: utf-8
"""
dotsandboxes_agent.py

Extend this class to provide an agent that can participate in a tournament.

Created by Pieter Robberechts, Wannes Meert.
Copyright (c) 2022 KU Leuven. All rights reserved.
"""

import sys
import argparse
import logging
import random
import numpy as np
import pyspiel
from open_spiel.python.algorithms import evaluate_bots
import time

from open_spiel.python.algorithms import mcts


logger = logging.getLogger('be.kuleuven.cs.dtai.dotsandboxes')


def get_agent_for_tournament(player_id):
    """Change this function to initialize your agent.
    This function is called by the tournament code at the beginning of the
    tournament.

    :param player_id: The integer id of the player for this bot, e.g. `0` if
        acting as the first player.
    """
    my_player = Agent(player_id)
    return my_player


class Agent(pyspiel.Bot):
    """Agent template"""

    def __init__(self, player_id):
        """Initialize an agent to play Dots and Boxes.

        Note: This agent should make use of a pre-trained policy to enter
        the tournament. Initializing the agent should thus take no more than
        a few seconds.
        """
        # mcts parameters
        self.uct_c = 2
        self.rollout_count = 1
        self.max_simulations = 80
        self.seed = None
        self.rng = np.random.RandomState(self.seed)
        self.evaluator = mcts.RandomRolloutEvaluator(self.rollout_count, self.rng)
        self.solve = True
        self.verbose = False
        dotsandboxes_game_string = (
        "dots_and_boxes(num_rows=7,num_cols=7)")
        game = pyspiel.load_game(dotsandboxes_game_string)

        self.bot = mcts.MCTSBot(
                        game,
                        self.uct_c,
                        self.max_simulations,
                        self.evaluator,
                        random_state=self.rng,
                        solve=self.solve,
                        verbose=self.verbose)
        self.player_id = player_id 


        # dit moet gecalled worden precies?
        pyspiel.Bot.__init__(self)


    def set_bot(self, num_rows, num_cols):
        dotsandboxes_game_string = (
        f"dots_and_boxes(num_rows={num_rows},num_cols={num_cols})")
        game = pyspiel.load_game(dotsandboxes_game_string)
        self.bot = mcts.MCTSBot(
                        game,
                        self.uct_c,
                        self.max_simulations,
                        self.evaluator,
                        random_state=self.rng,
                        solve=self.solve,
                        verbose=self.verbose)


    def restart_at(self, state):
        """Starting a new game in the given state.

        :param state: The initial state of the game.
        """
        game_parameters = state.get_game().get_parameters()
        num_rows = game_parameters['num_rows']
        num_cols = game_parameters['num_cols']
        self.set_bot(num_rows, num_cols)
        print('bot restarted')



    def inform_action(self, state, player_id, action):
        """Let the bot know of the other agent's actions.

        :param state: The current state of the game.
        :param player_id: The ID of the player that executed an action.
        :param action: The action which the player executed.
        """
        self.bot.inform_action(state, player_id, action)

    def step(self, state):
        """Returns the selected action in the given state.

        :param state: The current state of the game.
        :returns: The selected action from the legal actions, or
            `pyspiel.INVALID_ACTION` if there are no legal actions available.
        """
        # Plays random action, change with your best strategy
        return self.bot.step(state)


def test_api_calls():
    """This method calls a number of API calls that are required for the
    tournament. It should not trigger any Exceptions.
    """
    start = time.time()
    dotsandboxes_game_string = (
        "dots_and_boxes(num_rows=2,num_cols=2)")
    game = pyspiel.load_game(dotsandboxes_game_string)
    bots = [get_agent_for_tournament(player_id) for player_id in [0,1]]
    returns = evaluate_bots.evaluate_bots(game.new_initial_state(), bots, np.random)
    assert len(returns) == 2
    assert isinstance(returns[0], float)
    assert isinstance(returns[1], float)
    print("SUCCESS!")
    end = time.time()
    print(f'game took {end - start}s to run')


def main(argv=None):
    test_api_calls()


if __name__ == "__main__":
    sys.exit(main())

