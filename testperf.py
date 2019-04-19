import sys

from raise_player import RaisedPlayer

sys.path.insert(0, './pypokerengine/api/')
import game
setup_config = game.setup_config
start_poker = game.start_poker
import time
from argparse import ArgumentParser


""" =========== *Remember to import your agent!!! =========== """
from randomplayer import RandomPlayer
from skynet import Skynet
""" ========================================================= """

""" Example---To run testperf.py with random warrior AI against itself. 

$ python testperf.py -n1 "Random Warrior 1" -a1 RandomPlayer -n2 "Random Warrior 2" -a2 RandomPlayer
"""

def reinforcementLearning():
	max_payoff = - 1000
	best_raise_prob = 1
	for i in range(50, 85):
		raise_prob = i/100.0
		random_pot, skynet_pot = testperf1("John WongRaiser", RaisedPlayer(), "Andrew Skynet", Skynet(raise_prob, .4))
		current_payoff = skynet_pot - random_pot
		print("Using raise_prob: " + str(raise_prob) + ", " + "Payoff: " + str(current_payoff))
		if current_payoff > max_payoff:
			max_payoff = current_payoff
			best_raise_prob = raise_prob
		print("Current best raise_prob = " + str(best_raise_prob) + " with payoff = " + str(max_payoff) + "\n\n")
	print("================================================================")
	print("Best raise_prob = " + str(best_raise_prob) + " with payoff = " + str(max_payoff))


def testperf1(agent_name1, agent1, agent_name2, agent2):

	# Init to play 500 games of 1000 rounds
	num_game = 10
	max_round = 20
	initial_stack = 10000
	smallblind_amount = 20

	# Init pot of players
	agent1_pot = 0
	agent2_pot = 0

	# Setting configuration
	config = setup_config(max_round=max_round, initial_stack=initial_stack, small_blind_amount=smallblind_amount)
	
	# Register players
	config.register_player(name=agent_name1, algorithm=agent1)
	config.register_player(name=agent_name2, algorithm=agent2)
	# config.register_player(name=agent_name1, algorithm=agent1())
	# config.register_player(name=agent_name2, algorithm=agent2())
	

	# Start playing num_game games
	for game in range(1, num_game+1):
		print("Game number: " + str(game))
		game_result = start_poker(config, verbose=0)
		agent1_pot = agent1_pot + game_result['players'][0]['stack']
		agent2_pot = agent2_pot + game_result['players'][1]['stack']

	print("\nAfter playing {} games of {} rounds, the results are: ".format(num_game, max_round))
	# print("\n Agent 1's final pot: ", agent1_pot)
	print(agent_name1 + "'s final pot: " + str(agent1_pot))
	print(agent_name2 + "'s final pot: " + str(agent2_pot))

	return agent1_pot, agent2_pot
	# print("\n ", game_result)
	# print("\n Random player's final stack: ", game_result['players'][0]['stack'])
	# print("\n " + agent_name + "'s final stack: ", game_result['players'][1]['stack'])

	if (agent1_pot<agent2_pot):
		print("\n Congratulations! " + agent_name2 + " has won.")
	elif(agent1_pot>agent2_pot):
		print("\n Congratulations! " + agent_name1 + " has won.")
		# print("\n Random Player has won!")
	else:
		Print("\n It's a draw!") 


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-n1', '--agent_name1', help="Name of agent 1", default="Your agent", type=str)
    parser.add_argument('-a1', '--agent1', help="Agent 1", default=RandomPlayer())    
    parser.add_argument('-n2', '--agent_name2', help="Name of agent 2", default="Your agent", type=str)
    parser.add_argument('-a2', '--agent2', help="Agent 2", default=RandomPlayer())    
    args = parser.parse_args()
    return args.agent_name1, args.agent1, args.agent_name2, args.agent2

if __name__ == '__main__':
	name1, agent1, name2, agent2 = parse_arguments()
	start = time.time()
	testperf(name1, agent1, name2, agent2)
	end = time.time()

	print("\n Time taken to play: %.4f seconds" %(end-start))