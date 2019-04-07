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
				if turn.run(self.model):
					row, col, patch_orientation = self.ai.choose_placement(Patch(100, [[1]], 0, 0, 0), other_player.quilt)
					self.model.place_patch(other_player, Patch(100, [[1]], 0, 0, 0), row, col)

				#if game is over, exit running loop and update p1_win counter
				if self.model.game_over():
					if self.model.p1_win() == 1:
						p1_win += 1
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


