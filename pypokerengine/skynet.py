from pypokerengine.players import BasePokerPlayer
import random as rand
import pprint

from pypokerengine.utils.card_utils import estimate_hole_card_win_rate


def estimate_win_rate(hole_card, community_card):
    print("a")
    pass


class SkyNet(BasePokerPlayer):

  def declare_action(self, valid_actions, hole_card, round_state):

      # valid_actions format => [raise_action_pp = pprint.PrettyPrinter(indent=2)
      # hole_card and community_card find win rate

      community_card = round_state['community_card']
      win_rate = estimate_win_rate(hole_card, community_card)

      if win_rate < 0.5:
          action = valid_actions[0] #fetch fold
      elif win_rate < 0.8:
          action = valid_actions[1] #fetch call
      else:
          action = valid_actions[2] #fetch raise

      return action["action"]


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
  return RandomPlayer()
