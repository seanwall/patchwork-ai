from patchwork.model.Player import Player

class FeatureWeights():
	LEARNING_RATE = .01
	DISCOUNT_FACTOR = .1

	def __init__(self):
		self.patch_weights_early = []
		self.patch_weights_mid = []
		self.patch_weights_late = []

		for i in range(34):
			self.patch_weights_early.append(float(0))
			self.patch_weights_mid.append(float(0))
			self.patch_weights_late.append(float(0))

	def update_feature_weights(self, reward, future_state_util, state_model):
		for i in range(len(self.patch_weights_early)):
			prev_weight = self.patch_weights_early[i]
			curr_state_util = state_model.get_state_utility(self)
			state_reward = state_model.calculate_reward(0)
			self.patch_weights_early[i] = prev_weight + ((self.LEARNING_RATE)*(state_reward + (((self.DISCOUNT_FACTOR)*future_state_util) - curr_state_util)))*state_model.patch_list_early[i]

		for i in range(len(self.patch_weights_mid)):
			prev_weight = self.patch_weights_mid[i]
			curr_state_util = state_model.get_state_utility(self)
			state_reward = state_model.calculate_reward(0)
			self.patch_weights_mid[i] = prev_weight + ((self.LEARNING_RATE)*(state_reward + (((self.DISCOUNT_FACTOR)*future_state_util) - curr_state_util)))*state_model.patch_list_mid[i]

		for i in range(len(self.patch_weights_late)):
			prev_weight = self.patch_weights_mid[i]
			curr_state_util = state_model.get_state_utility(self)
			state_reward = state_model.calculate_reward(0)
			self.patch_weights_late[i] = prev_weight + ((self.LEARNING_RATE)*(state_reward + (((self.DISCOUNT_FACTOR)*future_state_util) - curr_state_util)))*state_model.patch_list_late[i]

	
class FeatureStateModel():
	def __init__(self, player):
		self.patch_list_early = []
		self.patch_list_mid = []
		self.patch_list_late = []
		self.passed_patch = False
		self.passed_econ = False
		self.player = player

		for i in range(34):
			self.patch_list_early.append(float(0))
			self.patch_list_mid.append(float(0))
			self.patch_list_late.append(float(0))

	def add_patch(self, patch_id):
		if self.player.position < 30:
			self.patch_list_early[patch_id] += 1
		elif self.player.position < 60:
			self.patch_list_mid[patch_id] += 1
		else:
			self.patch_list_late[patch_id] += 1


	def get_state_utility(self, weights):
		util = 0
		#if position < 25:
		for idx in range(len(weights.patch_weights_early)):
				#add the weight of the current patch to the state utility
			util += weights.patch_weights_early[idx] * self.patch_list_early[idx]

		#elif position < 45:
			#for idx in range(len(patch_state_list_mid)):
			util += weights.patch_weights_early[idx] * self.patch_list_early[idx]
		#else:
			#for idx in range(len(patch_state_list_late)):
			util += weights.patch_weights_early[idx] * self.patch_list_early[idx]

		return util

	#TODO: scale value for winning based on how much the final score was
	def calculate_reward(self, won):
		#reward = 0
		#if passed_1x1:
			#reward += 2
		
		reward = self.player.quilt.button_gen

		if won == 1:
			reward += 100
		elif won == -1:
			reward -= 100

		return reward
