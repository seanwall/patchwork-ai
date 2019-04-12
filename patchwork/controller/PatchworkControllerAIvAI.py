from patchwork.model.PatchworkModel import PatchworkModel
from patchwork.model.Patch import Patch
from ai.PatchworkAI import PatchworkAI
from ai.Features import FeatureWeights
from ai.Features import FeatureStateModel
from patchwork.model.Turn import BuyTurn
from patchwork.model.Turn import JumpTurn

import sys

class PatchworkControllerAIvAI():
	INTERVAL_SIZE = 5

	def __init__(self):
		self.model = PatchworkModel()
		self.ai = PatchworkAI()
		self.feature_weights = FeatureWeights()
		self.p1_feature_state = FeatureStateModel(self.model.p1, self.model.p2)
		self.p2_feature_state = FeatureStateModel(self.model.p2, self.model.p1)
		self.running = True

	def mainloop(self, num_samples):
		#run "num_samples" games and then calculate the win percentage
		p1_win = 0
		p1_running_sum = 0
		p2_running_sum = 0
		p1_win_count = 0
		p1_game_avgs = []
		p2_game_avgs = []
		p1_win_counts = []
		for i in range(num_samples):
			#reset the model for next game
			self.model = PatchworkModel()
			self.running = True

			while self.running:
				if self.model.p1_turn():
					player = self.model.p1
					other_player = self.model.p2
				else:
					player = self.model.p2
					other_player = self.model.p1

				#p1 is smart, p2 is dumb
				if self.model.p1_turn():
					turn = self.ai.choose_turn_hand_craft(self.model)
				else:
					turn = self.ai.choose_turn_random(self.model)



				if isinstance(turn, BuyTurn):
					#TEMPORARY HANDLING FOR IF THE PIECE CANT BE PLACED, NEED NEW SOLUTION FOR THIS
					if not self.ai.can_place(self.model.patch_list[turn.patch_idx], player.quilt):
						turn = JumpTurn()
					else:
						row, col, patch_orientation = self.ai.choose_placement(self.model.patch_list[turn.patch_idx], player.quilt)
						self.model.place_patch(player, patch_orientation, row, col)
				#run the turn (buy piece for buy, jump for jump), and check if patch is passed on time track
				passed_patch, passed_button_gen = turn.run(self.model)
				if passed_patch:
					row, col, patch_orientation = self.ai.choose_placement(Patch(34, [[1]], 0, 0, 0), other_player.quilt)
					self.model.place_patch(other_player, Patch(34, [[1]], 0, 0, 0), row, col)

				#if game is over, exit running loop and update p1_win counter
				if self.model.game_over():
					if self.model.p1_win() == 1:
						p1_win += 1

					#keep track of p1/p2 end scores to calculate averages at end (hoping to see progress)
					if ((i+1) % self.INTERVAL_SIZE) == 0:
						p1_game_avgs.append(p1_running_sum/self.INTERVAL_SIZE)
						p2_game_avgs.append(p2_running_sum/self.INTERVAL_SIZE)
						p1_running_sum = 0
						p2_running_sum = 0
						p1_win_count = 0

					p1_running_sum += self.model.p1.get_score()
					p2_running_sum += self.model.p2.get_score()
					if self.model.p1_win() == 1:
						p1_win_count += 1

					self.running = False

			#If there's only 1 sample just print out the basic output
			if num_samples == 2 or num_samples == 1:
				print("P1 score: " + str(self.model.p1.get_score()) + ", P2 score: " + str(self.model.p2.get_score()))
				print("P1 buttons: " + str(self.model.p1.buttons) + ", P2 buttons: " + str(self.model.p2.buttons))
				print("-------------------------------")
				print("P1 board")
				for row in range(9):
					for col in range(9):
						print(self.model.p1.quilt.board_array[row][col], end="")
					print()
				print("-------------------------------")
				print("P2 board")
				for row in range(9):
					for col in range(9):
						print(self.model.p2.quilt.board_array[row][col], end="")
					print()
				print("-------------------------------")

			if i == 0:
				print("Simulating", end="")
				sys.stdout.flush()
			elif (i % 4) == 0:
				 sys.stdout.write("\b\b\b   \b\b\b")
				 sys.stdout.flush()
			else:
				sys.stdout.write(".")
				sys.stdout.flush()

		print("Games run: " + str(num_samples))
		print("P1 wins: " + str(p1_win) + ", P2 wins: " + str(num_samples - p1_win))
		print("P1 win %: " + str((p1_win/num_samples)*100) + ", P2 win %: " + str(((num_samples - p1_win)/num_samples)*100))

		print()

		for i in range(len(self.ai.feature_weights["patch_weights_early"])):
			print("Patch ID: " + str(i + 1) +", Early Weight: " + str(self.ai.feature_weights["patch_weights_early"][i]) + ", Mid Weight: " + str(self.ai.feature_weights["patch_weights_mid"][i]) + ", Late Weight: " + str(self.ai.feature_weights["patch_weights_late"][i]))

		print()

		print("GAME AVGS: ")
		for i in range(len(p1_game_avgs)):
			print(str(i*self.INTERVAL_SIZE) + " - " + str((i*self.INTERVAL_SIZE) + self.INTERVAL_SIZE) + " | Player 1: " + str(p1_game_avgs[i]) + ", Player 2: " + str(p2_game_avgs[i]) + ", Difference: " + str(p1_game_avgs[i] - p2_game_avgs[i]))

	def mainloop_learning(self, num_samples):
		#run "num_samples" games and then calculate the win percentage
		p1_win = 0
		p1_running_sum = 0
		p2_running_sum = 0
		p1_win_count = 0
		p1_game_avgs = []
		p2_game_avgs = []
		p1_win_counts = []

		p1_button_gen_sum = 0
		p1_buttons_sum = 0
		p1_board_util_sum = 0

		p1_button_gen_sums = []
		p1_buttons_sums = []
		p1_board_util_sums = []

		p2_button_gen_sum = 0
		p2_buttons_sum = 0
		p2_board_util_sum = 0

		p2_button_gen_sums = []
		p2_buttons_sums = []
		p2_board_util_sums = []

		for i in range(num_samples):
			#reset the model for next game
			self.model = PatchworkModel()
			self.running = True

			self.p1_feature_state = FeatureStateModel(self.model.p1, self.model.p2)
			self.p2_feature_state = FeatureStateModel(self.model.p2, self.model.p1)

			while self.running:
				if self.model.p1_turn():
					player = self.model.p1
					state_model = self.p1_feature_state
					other_player = self.model.p2
				else:
					player = self.model.p2
					state_model = self.p2_feature_state
					other_player = self.model.p1

				#p1 is learning, p2 is hand crafted ai
				if self.model.p1_turn():
					#picks turn based on learned weights and updates those weights
					turn = self.ai.choose_turn_learning(self.model, self.p1_feature_state, self.feature_weights)
				else:
					turn = self.ai.choose_turn_random(self.model)

					#update weights based on p2 moves as well
					#future_state = self.ai.find_future_state(turn, self.p2_feature_state)

					#reward = self.p2_feature_state.calculate_reward(0)

					#self.feature_weights.update_feature_weights(reward, future_state.get_state_utility(self.feature_weights), self.p2_feature_state)


				#handling turn running
				if isinstance(turn, BuyTurn):
					#check if it's possible for the player to place the selected patch
					if not self.ai.can_place(self.model.patch_list[turn.patch_idx], player.quilt):
						passes_patch, passes_econ = player.will_pass_tile(other_player.position - player.position + 1, self.model.time_track)
						turn = JumpTurn(passes_patch, passes_econ)
					else:
						row, col, patch_orientation = self.ai.choose_placement(self.model.patch_list[turn.patch_idx], player.quilt)
						self.model.place_patch(player, patch_orientation, row, col)
				#run the turn (buy piece for buy, jump for jump), and update passed_patch/passed_button_gen booleans
				passed_patch, passed_button_gen = turn.run(self.model, state_model)

				#placing 1x1 patch if it was passed
				if passed_patch:
					row, col, patch_orientation = self.ai.choose_placement(Patch(34, [[1]], 0, 0, 0), other_player.quilt)
					self.model.place_patch(other_player, Patch(34, [[1]], 0, 0, 0), row, col)

				#if game is over, exit running loop and update p1_win counter
				if self.model.game_over():
					p1_rewards = self.p1_feature_state.calculate_reward(self.model.p1_win())
					p2_rewards = self.p1_feature_state.calculate_reward(-1 * self.model.p1_win())

					self.feature_weights.update_feature_weights(p1_rewards, self.p1_feature_state.get_state_utility(self.feature_weights), self.p1_feature_state)
					self.feature_weights.update_feature_weights(p2_rewards, self.p2_feature_state.get_state_utility(self.feature_weights), self.p2_feature_state)


					#CALCULATING OUTPUTS FOR PROGRESS TRACKING
					#keep track of p1/p2 end scores to calculate averages at end (hoping to see progress)
					if ((i+1) % self.INTERVAL_SIZE) == 0:
						p1_game_avgs.append(p1_running_sum/self.INTERVAL_SIZE)
						p2_game_avgs.append(p2_running_sum/self.INTERVAL_SIZE)
						p1_win_counts.append(p1_win_count)
						p1_running_sum = 0
						p2_running_sum = 0
						p1_win_count = 0

						p1_button_gen_sums.append(p1_button_gen_sum/self.INTERVAL_SIZE)
						p1_buttons_sums.append(p1_buttons_sum/self.INTERVAL_SIZE)
						p1_board_util_sums.append(p1_board_util_sum/self.INTERVAL_SIZE)

						p1_button_gen_sum = 0
						p1_buttons_sum = 0
						p1_board_util_sum = 0

						p2_button_gen_sums.append(p2_button_gen_sum/self.INTERVAL_SIZE)
						p2_buttons_sums.append(p2_buttons_sum/self.INTERVAL_SIZE)
						p2_board_util_sums.append(p2_board_util_sum/self.INTERVAL_SIZE)

						p2_button_gen_sum = 0
						p2_buttons_sum = 0
						p2_board_util_sum = 0

					if self.model.p1_win() == 1:
						p1_win_count += 1
						p1_win += 1

					p1_running_sum += self.model.p1.get_score()
					p2_running_sum += self.model.p2.get_score()

					p1_button_gen_sum += self.model.p1.quilt.button_gen
					p1_buttons_sum += self.model.p1.buttons
					p1_board_util_sum += self.ai.get_quilt_utility(self.model.p1.quilt)

					p2_button_gen_sum += self.model.p2.quilt.button_gen
					p2_buttons_sum += self.model.p2.buttons
					p2_board_util_sum += self.ai.get_quilt_utility(self.model.p2.quilt)

					#exit while loop, game is over
					self.running = False

			#If there's only 1 sample just print out the basic output
			if num_samples == 2 or num_samples == 1:
				print("P1 score: " + str(self.model.p1.get_score()) + ", P2 score: " + str(self.model.p2.get_score()))
				print("P1 buttons: " + str(self.model.p1.buttons) + ", P2 buttons: " + str(self.model.p2.buttons))
				print("-------------------------------")
				print("P1 board")
				for row in range(9):
					for col in range(9):
						print(self.model.p1.quilt.board_array[row][col], end="")
					print()
				print("-------------------------------")
				print("P2 board")
				for row in range(9):
					for col in range(9):
						print(self.model.p2.quilt.board_array[row][col], end="")
					print()
				print("-------------------------------")

			if i == 0:
				print("Simulating", end="")
				sys.stdout.flush()
			elif (i % 4) == 0:
				 sys.stdout.write("\b\b\b   \b\b\b")
				 sys.stdout.flush()
			else:
				sys.stdout.write(".")
				sys.stdout.flush()

		print()
		print("Games run: " + str(num_samples))
		print("P1 wins: " + str(p1_win) + ", P2 wins: " + str(num_samples - p1_win))
		print("P1 win %: " + str((p1_win/num_samples)*100) + ", P2 win %: " + str(((num_samples - p1_win)/num_samples)*100))

		print()

		print("WEIGHTS: ")
		print("Button Gen Weight: " + str(self.feature_weights.button_gen_weight))
		print("Board Coverage Weight: " + str(self.feature_weights.board_coverage_weight))
		print("Button Weight: " + str(self.feature_weights.buttons_weight))
		print("Player Distance Weight: " + str(self.feature_weights.player_distance_weight))


		print()

		f1 = open("ai_button_gen.txt", "w")
		f2 = open("ai_button_total.txt", "w")
		f3 = open("ai_quilt_coverage.txt", "w")
		f4 = open("ai_score.txt", "w")
		f5 = open("ai_score_diff.txt", "w")
		print("GAME AVGS: ")
		for i in range(len(p1_game_avgs)):
			print(str(i*self.INTERVAL_SIZE) + " - " + str((i*self.INTERVAL_SIZE) + self.INTERVAL_SIZE) + " | Player 1: " + str(p1_game_avgs[i]) + ", Player 2: " + str(p2_game_avgs[i]) + ", Difference: " + str(p1_game_avgs[i] - p2_game_avgs[i]) + ", P1 Wins: " + str(p1_win_counts[i]) + ", P2 Wins: " + str(self.INTERVAL_SIZE - p1_win_counts[i]) + ", P1 Win %: " + str((p1_win_counts[i]/self.INTERVAL_SIZE)*100))
			#f.write(str((p1_win_counts[i]/5)*100) + ", ")

		#print("AI TENDENCIES: ")
		for i in range(len(p1_button_gen_sums)):
			#print(str(i*self.INTERVAL_SIZE) + " - " + str((i*self.INTERVAL_SIZE) + self.INTERVAL_SIZE) + " | Button Gen: " + str(p1_button_gen_sums[i]) + ", Buttons: " + str(p1_buttons_sums[i]) + ", Board Util: " + str(p1_board_util_sums[i]))
			f1.write(str(p1_button_gen_sums[i]) + ", ")
			f2.write(str(p1_buttons_sums[i]) + ", ")
			f3.write(str(p1_board_util_sums[i]) + ", ")
			f4.write(str(p1_game_avgs[i]) + ", ")
			f5.write(str(p1_game_avgs[i] - p2_game_avgs[i]) + ", ")
		#print()

		#for i in range(len(p2_button_gen_sums)):
		#	print(str(i*self.INTERVAL_SIZE) + " - " + str((i*self.INTERVAL_SIZE) + self.INTERVAL_SIZE) + " | Button Gen: " + str(p2_button_gen_sums[i]) + ", Buttons: " + str(p2_buttons_sums[i]) + ", Board Util: " + str(p2_board_util_sums[i]))
		f1.close()
		f2.close()
		f3.close()
		f4.close()
		f5.close()
