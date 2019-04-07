import math

from patchwork.model.PatchworkModel import PatchworkModel
from patchwork.model.Turn import JumpTurn
from patchwork.model.Turn import BuyTurn
from patchwork.model.Patch import Patch
from patchwork.model.Player import Player

import random

class PatchworkAI():
	LEARNING_RATE = .01
	DISCOUNT_FACTOR = .1

	def __init__(self):
		self.feature_weights = []
		self.initialize_weights()

	#initialize feature weights to 0
	def initialize_weights(self):
		for i in range(34):
			self.feature_weights.append(float(0))

	#initial state utility, weight for each patch multiplied by state (state being if the player purchased that patch or not)
	#right now this will just learn a general value for each patch
	#TODO, different feature state list than just a list of patch ids
	def get_state_utility(self, patch_state_list):
		util = 0
		for idx in range(len(patch_state_list)):
			#add the weight of the current patch to the state utility
			util += self.feature_weights[idx] * patch_state_list[idx]

		return util


	#TODO: scale value for winning based on how much the final score was
	def calculate_reward(self, passed_1x1, button_gen, won):
		reward = 0
		if passed_1x1:
			reward += 5
		
		reward += button_gen

		if won == 1:
			reward += 100
		elif won == -1:
			reward -= 100

		return reward

	def update_feature_weights(self, state_reward, future_state_util, curr_state_util, patch_state_list):

		#update feature weights:
		#wi = wi + a(r + y(U(S')-U(S))xi
		#where:
		#wi is in self.feature_weights[i]
		#a is constant LEARNING_RATE
		#r is given as state_reward - the reward of the current state (see __ for these rewards)
		#y is constant DISCOUNT_FACTOR
		#U(S') is given as future_state_util (see get_state_utility())
		#U(S) is given as curr_state_util
		#xi is in patch_state_list[i]
		for i in range(len(self.feature_weights)):
			prev_weight = self.feature_weights[i]
			updated_weight = prev_weight + ((self.LEARNING_RATE)*(state_reward + (((self.DISCOUNT_FACTOR)*future_state_util) - curr_state_util)))*patch_state_list[i]
			self.feature_weights[i] = updated_weight

	def choose_turn_random(self, model):
		turns = model.get_turns()
		#if there is an available move that isnt a jump turn, have a reduced chance of selecting jump
		if not isinstance(turns[0], JumpTurn):
			#10% chance to select jump move
			if random.random() <= .1:
				turn = turns[len(turns) - 1]
			#90% chance to randomly select an available buy move
			else:
				turn = turns[random.randint(0, (len(turns) - 2))]
		else:
			turn = turns[0]
		return turn

	#basic AI that picks the patch with the greatest econ gen value
	def choose_turn_hand_craft(self, model):
		turns = model.get_turns()
		best_turn = turns[0]

		if isinstance(best_turn, JumpTurn):
			return best_turn

		if model.p1_turn():
			player = model.p1
		else:
			player = model.p2

		#if player is early in the game go for button generation
		if player.position < 30:
			#know if we get here the current best_turn is a buy turn
			for turn in turns:
				#if it's a buy turn, check the patch econ gen value
				if isinstance(turn, BuyTurn):
					patch = model.patch_list[turn.patch_idx]

					if patch.button_gen > model.patch_list[best_turn.patch_idx].button_gen:
						best_turn = turn
		#else go for patches that take up the most space
		else:
			#know if we get here the current best_turn is a buy turn
			for turn in turns:
				#if it's a buy turn, check the patch space coverage
				if isinstance(turn, BuyTurn):
					patch = model.patch_list[turn.patch_idx]

					if patch.get_area_coverage() > model.patch_list[best_turn.patch_idx].get_area_coverage():
						best_turn = turn

		#if isinstance(best_turn, BuyTurn):
		#	print(model.patch_list[best_turn.patch_idx].button_gen)
		return best_turn

	def choose_turn_learning(self, model, passed_patch, passed_econ):
		if model.p1_turn():
			player = model.p1
		else:
			player = model.p2

		turns = model.get_turns()
		best_turn = turns[0]

		if not isinstance(best_turn, JumpTurn):

			best_patch_id = best_turn.patch_id
			next_best_patch_state_list = list(player.quilt.patch_counts)
			next_best_patch_state_list[best_patch_id] = next_best_patch_state_list[best_patch_id] + 1
			#best next state util to compare against, if move is found with a higher next state util, choose that move
			best_next_state_util = self.get_state_utility(next_best_patch_state_list)

			#check utility for each next state for each of the turns
			for turn in turns:
				if isinstance(turn, BuyTurn):
					patch_id = turn.patch_id

					next_patch_state_list = list(player.quilt.patch_counts)

					next_patch_state_list[patch_id] = next_patch_state_list[patch_id] + 1

					next_state_util = self.get_state_utility(next_patch_state_list)

					if next_state_util > best_next_state_util:
						best_next_state_util = next_state_util
						best_turn = turn

			#once turn has been found, update weights
			button_gen = 0
			if passed_econ:
				button_gen = player.quilt.button_gen
			reward = self.calculate_reward(passed_patch, button_gen, False)
		else:
			next_best_patch_state_list = list(player.quilt.patch_counts)
			best_next_state_util = self.get_state_utility(next_best_patch_state_list)
			button_gen = 0
			if passed_econ:
				button_gen = player.quilt.button_gen
			reward = self.calculate_reward(passed_patch, button_gen, False)


		self.update_feature_weights(reward, best_next_state_util, self.get_state_utility(player.quilt.patch_counts), player.quilt.patch_counts)

		return best_turn

	#Check if piece can be placed anywhere on the board
	def can_place(self, patch, quilt):
		for row in range(9):
			for col in range(9):
				for flip in range(2):
					if flip == 1:
						patch.flip()
					for orientation in range(4):
						patch.rotate_cw()
						#if can place, place patch on a copy of the quilt and calculate utility
						if quilt.valid_placement(patch, row, col):
							return True
		return False

	def choose_placement(self, patch, quilt):
		#for row in range(len(patch.orientation)):
		#	for col in range(len(patch.orientation[row])):
		#		print (patch.orientation[row][col], end="")
		#	print()
		#print()

		#keep track of best placement value found so far
		best_utility_so_far = float("-inf")
		row_placement = 0
		col_placement = 0
		patch_orientation = patch.copy()

		for row in range(9):
			for col in range(9):
				for flip in range(2):
					if flip == 1:
						patch.flip()
					for orientation in range(4):
						patch.rotate_cw()
						#if can place, place patch on a copy of the quilt and calculate utility
						if quilt.valid_placement(patch, row, col):
							quilt_copy = quilt.copy()
							quilt_copy.place_patch(patch, row, col)

							#if utility better than previous best, update info
							quilt_util = self.get_quilt_utility(quilt_copy)
							if quilt_util > best_utility_so_far:

								#print("New Best: " + str(quilt_util))
								#print("Orientation:")
								#print("Row: " + str(row) + " Col: " + str(col))
								#for row2 in range(len(patch.orientation)):
								#	for col2 in range(len(patch.orientation[row2])):
								#		print(patch.orientation[row2][col2], end ="")
								#	print()

								best_utility_so_far = quilt_util
								row_placement = row
								col_placement = col
								patch_orientation = patch.copy()

					

		if math.isinf(best_utility_so_far):
			return False
		else:
			#print("Row: " + str(row_placement) + ", Col: " + str(col_placement))
			patch = patch_orientation
			return row_placement, col_placement, patch_orientation

	#calculate how "good" the given quilt is. 
	#"goodness" is calculated by summing the number of adjacent tiles that are 
	#open for each open tile. Using this heuristic encourages placement that maintains the maximum
	#amount of open area for the quilt.
	def get_quilt_utility(self, quilt):
		quilt_utility = 0
		for row in range(len(quilt.board_array)):
			for col in range(len(quilt.board_array[row])):
				tile_value = 0
				#if the tile is an open tile, check for surrounding open tiles
				if not quilt.board_array[row][col] == 1:
					if not (row - 1) < 0:
						if quilt.board_array[row - 1][col] == 0:
							tile_value += 1
					if not (row + 1) > 8:
						if quilt.board_array[row + 1][col] == 0:
							tile_value += 1
					if not (col -1) < 0:
						if quilt.board_array[row][col - 1] == 0:
							tile_value += 1
					if not (col + 1) > 8:
						if quilt.board_array[row][col + 1] == 0:
							tile_value += 1

				quilt_utility += tile_value
		return quilt_utility

