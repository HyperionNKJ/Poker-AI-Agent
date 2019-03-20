from pypokerengine.players import BasePokerPlayer

hand_rank = {
    "High_Card": 0.1,
    "Pair": 0.2,
    "Two_Pair": 0.3,
    "Three_Of_a_Kind": 0.4,
    "Straight": 0.5,
    "Flush": 0.6,
    "Full_House": 0.7,
    "Four_Of_a_Kind": 0.8,
    "Straight_Flush": 0.9,
    "Royal_Flush": 1.0
}


class SkyNet(BasePokerPlayer):

    def estimate_pre_flop(self, first_card_value, second_card_value, first_card_suit, second_card_suit):
        if first_card_value == second_card_value:
            win_rate = hand_rank["Two_Pair"]
        elif (first_card_value - second_card_value) < abs(5):
            win_rate = 0.35
        else:
            win_rate = hand_rank["High_Card"] * max(first_card_value, second_card_value)

        if first_card_suit == second_card_suit:
            win_rate = 0.6
        return win_rate

    def estimate_flop(self, first_card_value, second_card_value, first_card_suit, second_card_suit, community_card):
        common_card = 0
        win_rate = 0
        # Three of a kind
        if first_card_value == second_card_value and self.count_common_cards(community_card, first_card_value) == 1:
            win_rate = 0.7
        return win_rate

    def count_common_cards(self, community_card, card_value):
        count = 0
        for card in community_card:
            if card[1] == card_value:
                count += 1
        return count

    def estimate_win_rate(self, hole_card, community_card, round):
        first_card = hole_card[0]
        second_card = hole_card[1]

        first_card_suit = first_card[0]
        second_card_suit = second_card[0]
        first_card_value = first_card[1]
        second_card_value = second_card[1]

        if round == 0:  # pre-flop
            return self.estimate_pre_flop(first_card_value, second_card_value, first_card_suit, second_card_suit)
        elif round == 1:  # flop
            return self.estimate_flop(first_card_value, second_card_value, first_card_suit, second_card_suit,
                                      community_card)
        elif round == 2:  # turn
            return self.estimate_flop(first_card_value, second_card_value, first_card_suit, second_card_suit,
                                      community_card)
        elif round == 3:  # river
            return self.estimate_flop(first_card_value, second_card_value, first_card_suit, second_card_suit,
                                      community_card)


def declare_action(self, valid_actions, hole_card, round_state):
    # valid_actions format => [raise_action_pp = pprint.PrettyPrinter(indent=2)
    # hole_card and community_card find win rate

    round = round_state['round_count']
    community_card = round_state['community_card']

    win_rate = self.estimate_win_rate(hole_card, community_card, round)

    print("Inside declare_action: " + win_rate)
    
    if win_rate < 0.5:
        action = valid_actions[0]  # fetch fold
    elif win_rate < 0.8:
        action = valid_actions[1]  # fetch call
    else:
        action = valid_actions[2]  # fetch raise

    return action['action']


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
    return SkyNet()
