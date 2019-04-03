from model.PatchworkModel import PatchworkModel
from model.Patch import Patch
from ai.PatchworkAI import PatchworkAI
from model.Turn import BuyTurn
from model.Turn import JumpTurn

class PatchworkControllerAIvAI():
	def __init__(self):
		self.model = PatchworkModel()
		self.ai = PatchworkAI()
		self.running = True

	def mainloop(self):
		while self.running:
			if self.model.p1_turn():
				player = self.model.p1
				other_player = self.model.p2
			else:
				player = self.model.p2
				other_player = self.model.p1

			turn = self.ai.choose_turn(self.model)
			if isinstance(turn, BuyTurn):
				#TEMPORARY HANDLING FOR IF THE PIECE CANT BE PLACED, NEED NEW SOLUTION FOR THIS
				if not self.ai.can_place(self.model.patch_list[turn.patch_idx], player.quilt):
					turn = JumpTurn()
				else:
					row, col, patch_orientation = self.ai.choose_placement(self.model.patch_list[turn.patch_idx], player.quilt)
					self.model.place_patch(player, patch_orientation, row, col)
			#run the turn (buy piece for buy, jump for jump), and check if patch is passed on time track
			if turn.run(self.model):
				row, col, patch_orientation = self.ai.choose_placement(Patch([[1]], 0, 0, 0), other_player.quilt)
				self.model.place_patch(other_player, Patch([[1]], 0, 0, 0), row, col)

			if self.model.game_over():
				self.running = False

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


