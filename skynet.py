import sys

# from enum import Enum
from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.emulator import Emulator
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate, gen_cards

RAISE_AMOUNT = 10
DEPTH_LIMIT = 0  # depth limit for the Heuristic Minimax.
RAISE_PROB = 0.70  # If Monte Carlo's algorithm evaluates our hand to have a winning probability >= 0.7, always raise.
# If raise is not possible, then call.
CALL_PROB = 0.4  # If winning probability >= 0.4 but < 0.7 , simply call.
# The above probability were derived from reinforcement learning and found to be the most optimal.


class Skynet(BasePokerPlayer):
    # Default constructor to instantiate Skynet AI
    def __init__(self):
        super(BasePokerPlayer, self).__init__()
        self.raise_prob = RAISE_PROB
        self.call_prob = CALL_PROB

    # Additional constructor for the purpose of reinforcement learning.
    # def __init__(self, raise_prob, call_prob):
    #     super(BasePokerPlayer, self).__init__()
    #     self.raise_prob = raise_prob
    #     self.call_prob = call_prob

    def declare_action(self, valid_actions, hole_card, round_state):
        # return self.hMinimaxDecision(round_state, hole_card, valid_actions, DEPTH_LIMIT)
        return self.getOptimalAction(hole_card, round_state, valid_actions)  # Use Monte Carlo algorithm to decide best action

    # Our current evaluation strategy : Monte Carlo's Algorithm
    def getOptimalAction(self, hole_card, round_state, valid_actions):
        # if we are at the river, then always call.
        if round_state['round_count'] == 3:
            return valid_actions[1]["action"]  # call

        win_rate = estimate_hole_card_win_rate(nb_simulation=1000, nb_player=2, hole_card=gen_cards(hole_card),
                                                   community_card=gen_cards(round_state['community_card']))

        if win_rate >= self.raise_prob:  # if win_rate more than raise_prob, then always raise if possible. Otherwise, call.
            if len(valid_actions) == 3:
                action = valid_actions[2]  # raise
            else:
                action = valid_actions[1]  # call
        elif win_rate >= self.call_prob:
            action = valid_actions[1]  # call
        else:  # if win_rate is less than call_prob, then just fold.
            action = valid_actions[0]  # fold
        return action["action"]

    # Our initial proposed strategy of Depth-Limited Heuristic Minimax search.
    def hMinimaxDecision(self, round_state, hole_card, valid_actions, depth_limit):
        emulator = Emulator()
        maxUtility = -sys.maxsize - 1
        maxAction = valid_actions[0]["action"]  # assume first action to have the highest utility
        for a in valid_actions:
            # evaluates utility of every action via backwards induction and choose the best action
            utility = self.hMinValue(emulator.apply_action(round_state, a["action"], RAISE_AMOUNT)[0],
                                     hole_card, 0, depth_limit, a["action"], emulator)
            if utility > maxUtility:
                maxUtility = utility  # keep tracks of the maximum utility and its corresponding action
                maxAction = a["action"]
        return maxAction

    # Function to evaluate the utility of a MIN node
    def hMinValue(self, round_state, hole_card, depth, limit, prevAction, emulator):
        if depth == limit:  # cut-off test. If true, stop Minimax and use Heuristic
            return self.evaluateHeuristic(hole_card, round_state['community_card'], prevAction)
        utility = sys.maxsize
        for a in emulator.generate_possible_actions(round_state):
            utility = min(utility,
                          self.hMaxValue(emulator.apply_action(round_state, a["action"], RAISE_AMOUNT)[0],
                                         hole_card, depth + 1, limit, prevAction, emulator))
        return utility

    # Function to evaluate the utility of a MAX node
    def hMaxValue(self, round_state, hole_card, depth, limit, prevAction, emulator):
        if depth == limit:  # cut-off test. If true, stop Minimax and use Heuristic
            return self.evaluateHeuristic(hole_card, round_state['community_card'], prevAction)
        utility = -sys.maxsize - 1
        for a in emulator.generate_possible_actions(round_state):
            utility = max(utility,
                          self.hMinValue(emulator.apply_action(round_state, a["action"], RAISE_AMOUNT)[0],
                                         hole_card, depth + 1, limit, prevAction, emulator))
        return utility

    # Function to terminate Minimax search and use heuristic. Incomplete.
    def evaluateHeuristic(self, hole_card, community_card, prevAction):
        win_rate = 1  # evaluate_win_rate(1000, 2 , gen_cards(hole_card), gen_cards(community_card))
        if win_rate >= RAISE_PROB:
            targetAction = "raise"
        elif win_rate >= CALL_PROB:
            targetAction = "call"
        else:
            targetAction = "fold"
        if prevAction == targetAction:
            return 1
        else:
            return 0

    def receive_game_start_message(self, game_info):
        game_info['player_num'] = 2

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return Skynet()

# Following are our proposed multiplier tables to evaluate win rate
# class handRank(Enum):
#     HIGH_CARD = 1
#     PAIR = 4
#     TWO_PAIR = 20
#     THREE_OF_A_KIND = 105
#     STRAIGHT = 355
#     FLUSH = 1070
#     FULL_HOUSE = 5300
#     FOUR_OF_A_KIND = 1.0
#     STRAIGHT_FLUSH = 1.0
#     ROYAL_FLUSH = 1.0
#
#
# class cardStrength(Enum):
#     ACE_VALUE = 14
#     KING_VALUE = 13
#     QUEEN_VALUE = 12
#     JACK_VALUE = 11
#     TEN_VALUE = 10
#     NINE_VALUE = 9
#     EIGHT_VALUE = 8
#     SEVEN_VALUE = 7
#     SIX_VALUE = 6
#     FIVE_VALUE = 5
#     FOUR_VALUE = 4
#     THREE_VALUE = 3
#     TWO_VALUE = 2
