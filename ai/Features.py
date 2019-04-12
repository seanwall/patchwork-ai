from patchwork.model.Player import Player
from patchwork.model.QuiltBoard import QuiltBoard

class FeatureWeights():
	LEARNING_RATE = .005
	DISCOUNT_FACTOR = .1

	def __init__(self):
		self.button_gen_weight = 0
		self.board_coverage_weight = 0
		self.buttons_weight = 0
		self.player_distance_weight = 0

	def update_feature_weights(self, reward, future_state_util, state_model):
		curr_state_util = state_model.get_state_utility(self)

		self.button_gen_weight = self.button_gen_weight + (self.LEARNING_RATE*(reward + (self.DISCOUNT_FACTOR*future_state_util) - curr_state_util)*state_model.player.quilt.button_gen)
		self.board_coverage_weight = self.board_coverage_weight + (self.LEARNING_RATE*(reward + (self.DISCOUNT_FACTOR*future_state_util) - curr_state_util)*state_model.player.quilt.calculate_board_coverage())
		self.buttons_weight = self.buttons_weight + (self.LEARNING_RATE*(reward + (self.DISCOUNT_FACTOR*future_state_util) - curr_state_util)*state_model.player.buttons)
		self.player_distance_weight = self.player_distance_weight + (self.LEARNING_RATE*(reward + (self.DISCOUNT_FACTOR*future_state_util) - curr_state_util)*(state_model.other_player.position - state_model.player.position))

		#print()
		#print(self.button_gen_weight)
		#print(self.board_coverage_weight)
		#print(self.buttons_weight)
		#print(self.player_distance_weight)
#Patch weight class used to generalize weights over patch features
class PatchWeight():

	def __init__(self):
		self.button_gen_weight = 0
		self.cost_weight = 0
		self.time_cost_weight = 0
		self.coverage_weight = 0

	def get_patch_utility(patch):
		util = 0

		util += self.button_gen_weight * patch.button_gen
		util += self.cost_weight * patch.cost
		util += self.time_cost_weight * patch.time_cost
	
class FeatureStateModel():
	def __init__(self, player, other_player, button_gen = None, buttons = None, board_coverage = None, dist_to_player = None):
		#self.patch_list_early = []
		#self.patch_list_mid = []
		#self.patch_list_late = []
		#self.passed_patch = False
		#self.passed_econ = False



		#used to get all necessary state info:
		#button gen
		#buttons
		#board coverage
		#distance to other player
		self.player = player
		self.other_player = other_player
		self.button_gen = None
		self.buttons = None
		self.board_coverage = None
		self.dist_to_player = None

		#Used when calculating future board states, so there isnt any messing with players/quilts/etch
		if button_gen is not None:
			self.button_gen = button_gen
		if buttons is not None:
			self.buttons = buttons
		if board_coverage is not None:
			self.board_coverage = board_coverage
		if dist_to_player is not None:
			self.dist_to_player = dist_to_player	

	#def add_patch(self, patch_id):
	#	if self.player.position < 30:
	#		self.patch_list_early[patch_id] += 1
	#	elif self.player.position < 60:
	#		self.patch_list_mid[patch_id] += 1
	#	else:
	#		self.patch_list_late[patch_id] += 1


	def get_state_utility(self, weights):
		util = 0


		#constructed w/ necessary info for future states
		if self.button_gen is not None and self.buttons is not None and self.board_coverage is not None and self.dist_to_player is not None:
			util += self.button_gen * weights.button_gen_weight
			util += self.board_coverage/10 * weights.board_coverage_weight
			util += self.buttons/3 * weights.buttons_weight
			util += self.dist_to_player * weights.player_distance_weight
		#going off of player info 
		#TODO might not even need this i dunno
		else:
			util += self.player.quilt.button_gen * weights.button_gen_weight
			util += self.player.quilt.calculate_board_coverage()/10 * weights.board_coverage_weight
			util += self.player.buttons/3 * weights.buttons_weight
			util += (self.other_player.position - self.player.position) * weights.player_distance_weight

		return util

	#TODO: scale value for winning based on how much the final score was
	def calculate_reward(self, won):
		#reward = 0
		#if passed_1x1:
			#reward += 2
		
		#reward = self.player.quilt.button_gen
		reward = 0
		if won == 1 or won == -1:
			reward = self.player.get_score()
		#elif won == -1:
			#reward -= self.player.buttons

		return reward
