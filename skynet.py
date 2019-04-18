import sys

from enum import Enum
from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.emulator import Emulator
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate, gen_cards

RAISE_AMOUNT = 10
DEPTH_LIMIT = 0
RAISE_PROB = 0.75
CALL_PROB = 0.4


class Skynet(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        action = self.hMinimaxDecision(round_state, hole_card, valid_actions, DEPTH_LIMIT)
        return action

    def hMinimaxDecision(self, round_state, hole_card, valid_actions, depth_limit):
        maxUtility = -sys.maxsize - 1
        maxAction = valid_actions[0]["action"]  # assume first action to have the highest utility
        for a in valid_actions:
            utility = self.hMinValue(Emulator.apply_action(Emulator(), round_state, a["action"], RAISE_AMOUNT)[0],
                                     hole_card, 0, depth_limit, a["action"])
            if utility > maxUtility:
                maxUtility = utility
                maxAction = a["action"]
        return maxAction

    def hMinValue(self, round_state, hole_card, depth, limit, prevAction):
        if depth == limit:
            return self.evaluateHeuristic(hole_card, round_state['community_card'], prevAction)
        utility = sys.maxsize
        for a in Emulator.generate_possible_actions(Emulator(), round_state):
            utility = min(utility,
                          self.hMaxValue(Emulator.apply_action(Emulator(), round_state, a["action"], RAISE_AMOUNT)[0],
                                         hole_card, depth + 1, limit, prevAction))
        return utility

    def hMaxValue(self, round_state, hole_card, depth, limit, prevAction):
        if depth == limit:
            return self.evaluateHeuristic(hole_card, round_state['community_card'], prevAction)
        utility = -sys.maxsize - 1
        for a in Emulator.generate_possible_actions(Emulator(), round_state):
            utility = max(utility,
                          self.hMinValue(Emulator.apply_action(Emulator(), round_state, a["action"], RAISE_AMOUNT)[0],
                                         hole_card, depth + 1, limit, prevAction))
        return utility

    def evaluateHeuristic(self, hole_card, community_card, prevAction):
        win_rate = estimate_hole_card_win_rate(1000, 2, gen_cards(hole_card), gen_cards(community_card))
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
        pass

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


class handRank(Enum):
    HIGH_CARD = 1
    PAIR = 4
    TWO_PAIR = 20
    THREE_OF_A_KIND = 105
    STRAIGHT = 355
    FLUSH = 1070
    FULL_HOUSE = 5300
    FOUR_OF_A_KIND = 1.0
    STRAIGHT_FLUSH = 1.0
    ROYAL_FLUSH = 1.0


class cardStrength(Enum):
    ACE_VALUE = 14
    KING_VALUE = 13
    QUEEN_VALUE = 12
    JACK_VALUE = 11
    TEN_VALUE = 10
    NINE_VALUE = 9
    EIGHT_VALUE = 8
    SEVEN_VALUE = 7
    SIX_VALUE = 6
    FIVE_VALUE = 5
    FOUR_VALUE = 4
    THREE_VALUE = 3
    TWO_VALUE = 2
