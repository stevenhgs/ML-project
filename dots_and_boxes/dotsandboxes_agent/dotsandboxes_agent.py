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
from open_spiel.python.algorithms import mcts
import time

import collections
import json
import os


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


def get_2x2_bitmap_from_filled_in_nums_with_offsets(filled_in_nums, n_r, n_c, r_o, c_o):
    """
    This method return the bitmap of a 2x2 dots and boxes game cut out of an nxm dots and boxes game with a row offset and column offset.
    filled_in_nums should be a set, for time complexity.
    n_r is the number of rows of cells in the game.
    n_c is the number of cols of cells in the game.
    r_o is the row offset.
    c_o is the column offset.
    """
    bitmap = 0
    number_of_horizontal_lines = (n_r + 1) * n_c
    
    _2x2_nums = []
    # get horizontal lines
    for e in range(6):
        r_i = e // 2
        c_i = e % 2
        num_to_find = (r_o * n_c) + (r_i * n_c) + c_o + c_i
        if num_to_find in filled_in_nums:
            bitmap |= 1 << e
            _2x2_nums.append(e)
    
    # get vertical lines
    for e in range(6):
        r_i = e // (2 + 1)
        c_i = e % (2 + 1)
        num_to_find = (r_o * (n_c + 1)) + (r_i * (n_c + 1)) + c_o + c_i + number_of_horizontal_lines
        if num_to_find in filled_in_nums:
            bitmap |= 1 << (e + 6)
            _2x2_nums.append(e + 6)

    return bitmap


def remap_nums_from_2x2_to_nrxnc_with_offset(nums, n_r, n_c, r_o, c_o):
    """
    This method returns the remapped nums from a 2x2 dots and boxes game to a nrxnc dots and boxes game with given offsets.
    n_r is the number of rows of cells in the game.
    n_c is the number of cols of cells in the game.
    r_o is the row offset.
    c_o is the column offset.
    """
    remapped_nums = []
    nb_of_horizontal_lines = (n_r + 1) * n_c
    nb_horizontal_lines_2x2 = 2 * (2 + 1)
    for num in nums:
        if num >= nb_horizontal_lines_2x2:  # vertical 3x3 line
            val = num - nb_horizontal_lines_2x2
            r_i = val // (2 + 1)
            c_i = val % (2 + 1)
            remapped_num = (r_o * (n_c + 1)) + (r_i * (n_c + 1)) + c_o + c_i + nb_of_horizontal_lines
            remapped_nums.append(remapped_num)
        else:
            r_i = num // 2
            c_i = num % 2
            remapped_num = (r_o * n_c) + (r_i * n_c) + c_o + c_i
            remapped_nums.append(remapped_num)
    return remapped_nums



def get_best_moves_from_state(state, state_to_actions_and_values):
    """
    This method gets the best move for a state from a mxn dots and boxes game.
    This method cuts out every 2x2 grid of the given state and holds all the actions with the best values.
    Then it takes a random action out of the actions which occurs the most.
    state_to_actions_and_values should be a dictionary. The keys of this dictionary should be the bitmap of a 2x2 dots and boxes game.
    the values of this dictionary has two elements.
    The first element are the best actions to take in a given 2x2 state.
    The second element is the maximum points which can still be scored from a given 2x2 state if both players play optimally.
    """
    info_string = state.history_str()
    if info_string == '':
        filled_in_nums = set()
    else:
        split_info_string = info_string.split(', ')
        filled_in_nums = {int(digit) for digit in split_info_string}

    game_parameters = state.get_game().get_parameters()
    n_r = game_parameters['num_rows']
    n_c = game_parameters['num_cols']
    
    current_best_actions = list()
    current_best_value = float("-inf")
    for r_o in range(n_r - 2 + 1):
        for c_o in range(n_c - 2 + 1):
            bitmap = get_2x2_bitmap_from_filled_in_nums_with_offsets(filled_in_nums, n_r, n_c, r_o, c_o)
            if bitmap == 4095:  # completely filled in 2x2
                continue
            best_actions, best_value = state_to_actions_and_values[str(bitmap)]
            best_value = int(best_value)

            if best_value > current_best_value:
                best_actions_remapped = remap_nums_from_2x2_to_nrxnc_with_offset(best_actions, n_r, n_c, r_o, c_o)
                current_best_actions = list(best_actions_remapped)
                current_best_value = best_value
            elif best_value == current_best_value:
                best_actions_remapped = remap_nums_from_2x2_to_nrxnc_with_offset(best_actions, n_r, n_c, r_o, c_o)
                current_best_actions.extend(best_actions_remapped)
    
    count = collections.defaultdict(int)
    for action in current_best_actions:
        count[action] += 1
    
    highest_count_actions = []
    highest_count = float('-inf')
    for action, nb_occurences in count.items():
        if nb_occurences > highest_count:
            highest_count_actions = [action]
        elif nb_occurences == highest_count:
            highest_count_actions.append(action)
    
    return random.choice(highest_count_actions)


class OurBot(pyspiel.Bot):
    def __init__(self, player_id):
        """Initializes a uniform-random bot.

        Args:
        player_id: The integer id of the player for this bot, e.g. `0` if acting
            as the first player.
        rng: A random number generator supporting a `choice` method, e.g.
            `np.random`
        """
        pyspiel.Bot.__init__(self)
        self._player_id = player_id
        package_directory = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(package_directory, '2x2_minimax.json')
        with open(json_file, 'r') as fp:
            self.cache = json.load(fp)

    def restart_at(self, state):
        pass

    def player_id(self):
        return self._player_id
    
    def step(self, state):
        return get_best_moves_from_state(state, self.cache)


class Agent(pyspiel.Bot):
    """Agent template"""

    def __init__(self, player_id):
        """Initialize an agent to play Dots and Boxes.

        Note: This agent should make use of a pre-trained policy to enter
        the tournament. Initializing the agent should thus take no more than
        a few seconds.
        """
        self.bot = OurBot(player_id)
        self.player_id = player_id 
        pyspiel.Bot.__init__(self)

        # mcts parameters in case n_r or n_c is 1
        self.uct_c = 2
        self.rollout_count = 9
        self.max_simulations = 10
        self.seed = None
        self.rng = np.random.RandomState(self.seed)
        self.evaluator = mcts.RandomRolloutEvaluator(self.rollout_count, self.rng)
        self.solve = True
        self.verbose = False

    def set_bot(self, num_rows, num_cols):
        if num_rows == 1 or num_cols == 1:
            print(f'num_rows: {num_rows}, num_cols: {num_cols}, one is 1 so setting mcts')
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
        else:
            print(f'num_rows: {num_rows}, num_cols: {num_cols}, none is 1 setting template')
            self.bot = OurBot(self.player_id)

    def restart_at(self, state):
        """Starting a new game in the given state.

        :param state: The initial state of the game.
        """
        game_parameters = state.get_game().get_parameters()
        num_rows = game_parameters['num_rows']
        num_cols = game_parameters['num_cols']
        self.set_bot(num_rows, num_cols)

    def inform_action(self, state, player_id, action):
        """Let the bot know of the other agent's actions.

        :param state: The current state of the game.
        :param player_id: The ID of the player that executed an action.
        :param action: The action which the player executed.
        """
        pass

    def step(self, state):
        """Returns the selected action in the given state.

        :param state: The current state of the game.
        :returns: The selected action from the legal actions, or
            `pyspiel.INVALID_ACTION` if there are no legal actions available.
        """
        # Plays random action, change with your best strategy
        print(f'gotten state, we are player {self.player_id + 1} (v2)')
        print(state)
        return self.bot.step(state)


def test_api_calls():
    """This method calls a number of API calls that are required for the
    tournament. It should not trigger any Exceptions.
    """
    start = time.time()
    dotsandboxes_game_string = (
        "dots_and_boxes(num_rows=7,num_cols=7)")
    game = pyspiel.load_game(dotsandboxes_game_string)
    bots = [get_agent_for_tournament(player_id) for player_id in [0,1]]
    returns = evaluate_bots.evaluate_bots(game.new_initial_state(), bots, np.random)
    assert len(returns) == 2
    assert isinstance(returns[0], float)
    assert isinstance(returns[1], float)
    print("SUCCESS!")
    end = time.time()
    bots[0].restart_at(game.new_initial_state())
    dotsandboxes_game_string = (
        "dots_and_boxes(num_rows=1,num_cols=7)")
    game = pyspiel.load_game(dotsandboxes_game_string)
    bots[0].restart_at(game.new_initial_state())
    dotsandboxes_game_string = (
        "dots_and_boxes(num_rows=7,num_cols=7)")
    game = pyspiel.load_game(dotsandboxes_game_string)
    bots[0].restart_at(game.new_initial_state())
    dotsandboxes_game_string = (
        "dots_and_boxes(num_rows=7,num_cols=1)")
    game = pyspiel.load_game(dotsandboxes_game_string)
    bots[0].restart_at(game.new_initial_state())
    print(f'game took {end - start}s to run')


def main(argv=None):
    test_api_calls()


if __name__ == "__main__":
    sys.exit(main())

