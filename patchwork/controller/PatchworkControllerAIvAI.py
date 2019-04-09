from patchwork.model.PatchworkModel import PatchworkModel
from patchwork.model.Patch import Patch
from ai.PatchworkAI import PatchworkAI
from patchwork.model.Turn import BuyTurn
from patchwork.model.Turn import JumpTurn

import sys

class PatchworkControllerAIvAI():
	def __init__(self):
		self.model = PatchworkModel()
		self.ai = PatchworkAI()
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
					if ((i+1) % 100) == 0:
						p1_game_avgs.append(p1_running_sum/100)
						p2_game_avgs.append(p2_running_sum/100)
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

		print("PATCH WEIGHTS: ")
		for i in range(len(self.ai.feature_weights)):
			print("Patch ID: " + str(i + 1) +", Weight: " + str(self.ai.feature_weights[i]))

		print()

		print("GAME AVGS: ")
		for i in range(len(p1_game_avgs)):
			print(str(i*100) + " - " + str((i*100) + 100) + " | Player 1: " + str(p1_game_avgs[i]) + ", Player 2: " + str(p2_game_avgs[i]) + ", Difference: " + str(p1_game_avgs[i] - p2_game_avgs[i]))

	def mainloop_learning(self, num_samples):
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

			#state info for learning. This keeps track of what each player's last move did to the state. These
			#are things that are hidden from the current board state, so need to be exposed in some way at the state.
			#TODO This is a dumb way to do this
			p1_passed_patch = False
			p1_passed_econ = False

			p2_passed_patch = False
			p2_passed_econ = False

			while self.running:
				if self.model.p1_turn():
					player = self.model.p1
					other_player = self.model.p2
				else:
					player = self.model.p2
					other_player = self.model.p1

				#p1 is learning, p2 is hand crafted ai
				if self.model.p1_turn():
					#picks turn based on learned weights and updates those weights
					turn = self.ai.choose_turn_learning(self.model, p1_passed_patch, p1_passed_econ)
				else:
					turn = self.ai.choose_turn_random(self.model)

					#update weights based on p2 moves as well
					p2_button_gen = 0
					if p2_passed_econ:
						p2_button_gen = player.quilt.button_gen

					curr_state_util = self.ai.get_state_utility(player.quilt.patch_counts)
					if isinstance(turn, BuyTurn):
						future_patch_state_list = list(player.quilt.patch_counts)
						future_patch_state_list[turn.patch_id] = future_patch_state_list[turn.patch_id] + 1
						future_state_util = self.ai.get_state_utility(future_patch_state_list)
						reward = self.ai.calculate_reward(p2_passed_patch, p2_button_gen, 0)
					else:
						future_patch_state_list = list(player.quilt.patch_counts)
						future_state_util = self.ai.get_state_utility(future_patch_state_list)
						reward = self.ai.calculate_reward(p2_passed_patch, p2_button_gen, 0)

					self.ai.update_feature_weights(reward, future_state_util, curr_state_util, player.quilt.patch_counts)

				if isinstance(turn, BuyTurn):
					#TEMPORARY HANDLING FOR IF THE PIECE CANT BE PLACED, NEED NEW SOLUTION FOR THIS
					if not self.ai.can_place(self.model.patch_list[turn.patch_idx], player.quilt):
						turn = JumpTurn()
					else:
						row, col, patch_orientation = self.ai.choose_placement(self.model.patch_list[turn.patch_idx], player.quilt)
						self.model.place_patch(player, patch_orientation, row, col)
				#run the turn (buy piece for buy, jump for jump), and update passed_patch/passed_button_gen booleans
				passed_patch, passed_button_gen = turn.run(self.model)
				if self.model.p1_turn():
					p1_passed_patch = passed_patch
					p1_passed_econ = passed_button_gen
				else:
					p2_passed_patch = passed_patch
					p2_passed_econ = passed_button_gen

				if passed_patch:
					row, col, patch_orientation = self.ai.choose_placement(Patch(34, [[1]], 0, 0, 0), other_player.quilt)
					self.model.place_patch(other_player, Patch(34, [[1]], 0, 0, 0), row, col)

				#if game is over, exit running loop and update p1_win counter
				if self.model.game_over():
					#update weights one last time
					if self.model.p1_win() == 1:
						p1_win += 1
						win_reward = self.ai.calculate_reward(p1_passed_patch, self.model.p1.quilt.button_gen, 0)
						lose_reward = self.ai.calculate_reward(p2_passed_patch, self.model.p2.quilt.button_gen, 0)

						#win/lose reward passed in as next state value, not sure if this is the right way to do this.
						self.ai.update_feature_weights(win_reward, 25 + self.model.p1.get_score(), self.ai.get_state_utility(self.model.p1.quilt.patch_counts), self.model.p1.quilt.patch_counts)
						self.ai.update_feature_weights(lose_reward, -25 + self.model.p2.get_score(), self.ai.get_state_utility(self.model.p2.quilt.patch_counts), self.model.p2.quilt.patch_counts)
					elif self.model.p1_win() == -1:
						win_reward = self.ai.calculate_reward(p2_passed_patch, self.model.p2.quilt.button_gen, 0)
						lose_reward = self.ai.calculate_reward(p1_passed_patch, self.model.p1.quilt.button_gen, 0)

						#win/lose reward passed in as next state value, not sure if this is the right way to do this.
						self.ai.update_feature_weights(win_reward, 25 + self.model.p2.get_score(), self.ai.get_state_utility(self.model.p2.quilt.patch_counts), self.model.p2.quilt.patch_counts)
						self.ai.update_feature_weights(lose_reward, -25  + self.model.p1.get_score(), self.ai.get_state_utility(self.model.p1.quilt.patch_counts), self.model.p1.quilt.patch_counts)

					#keep track of p1/p2 end scores to calculate averages at end (hoping to see progress)
					if ((i+1) % 10) == 0:
						p1_game_avgs.append(p1_running_sum/10)
						p2_game_avgs.append(p2_running_sum/10)
						p1_win_counts.append(p1_win_count)
						p1_running_sum = 0
						p2_running_sum = 0
						p1_win_count = 0

					if self.model.p1_win() == 1:
						p1_win_count += 1

					p1_running_sum += self.model.p1.get_score()
					p2_running_sum += self.model.p2.get_score()
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

		print("PATCH WEIGHTS: ")
		for i in range(len(self.ai.feature_weights["patch_weights"])):
			print("Patch ID: " + str(i + 1) +", Weight: " + str(self.ai.feature_weights["patch_weights"][i]))

		print()

		f = open("p1_progress.txt", "w")
		print("GAME AVGS: ")
		for i in range(len(p1_game_avgs)):
			print(str(i*10) + " - " + str((i*10) + 10) + " | Player 1: " + str(p1_game_avgs[i]) + ", Player 2: " + str(p2_game_avgs[i]) + ", Difference: " + str(p1_game_avgs[i] - p2_game_avgs[i]) + ", P1 Wins: " + str(p1_win_counts[i]) + ", P2 Wins: " + str(10 - p1_win_counts[i]) + ", P1 Win %: " + str((p1_win_counts[i]/10)*100))
			f.write(str((p1_win_counts[i]/10)*100) + ", ")
		f.close()
