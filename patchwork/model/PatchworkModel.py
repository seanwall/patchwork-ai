from collections import deque
import random

from patchwork.model.Patch import Patch
from patchwork.model.Player import Player
from patchwork.model.QuiltBoard import QuiltBoard
from patchwork.model.TimeTrack import TimeTrack
from patchwork.model.TrackTile import TrackTile
from patchwork.model.Turn import BuyTurn
from patchwork.model.Turn import JumpTurn

class PatchworkModel():
	PATCH_LIST_CONST = []
	#initialize model for a new patchwork game
	def __init__(self):
		self.p1 = Player(1)
		self.p2 = Player(2)
		self.time_track = TimeTrack()
		PatchworkModel.PATCH_LIST_CONST = self.build_patch_list()
		#store patch list as a deque, so that it can be rotated to track the current available pieces
		self.patch_list = deque(self.randomize_pieces())


	def randomize_pieces(self):
		temp_list = PatchworkModel.PATCH_LIST_CONST.copy()
		#remove the 1x2 patch before shuffling array, as it should always be last in the list
		temp_list.pop(32)
		random.shuffle(temp_list)
		#add the 1x2 patch back onto the end of the list
		temp_list.append(PatchworkModel.PATCH_LIST_CONST[32])

		return temp_list

	#check if the game represented by this model is over
	def game_over(self):
		return self.time_track.track[self.p1.position] == TrackTile.END and self.time_track.track[self.p2.position] == TrackTile.END

	#returns 1 if p1 won, -1 if p2 won, 0 if there is a tie
	def p1_win(self):
		if self.p1.get_score() > self.p2.get_score():
			return 1
		elif self.p1.get_score() < self.p2.get_score():
			return -1
		else:
			return 0

	#return player.buy_patch to see if a patch was passed in the move
	def buy_patch(self, patch_idx):
		if self.p1_turn():
			player = self.p1
			other_player = self.p2
		else:
			player = self.p2
			other_player = self.p1

		if player.can_buy(self.patch_list[patch_idx]):
			patch = self.patch_list[patch_idx]
			#remove patch from patch list if it is purchased
			#temp_list = PatchworkModel.patch_list.copy()
			del self.patch_list[patch_idx]
			self.patch_list.rotate(-patch_idx)

			return player.buy_patch(patch, self.time_track, other_player)

	def place_patch(self, player, patch, row, col):
		player.place_patch(patch, row, col)

	def can_buy(self, patch_idx):
		if self.p1_turn():
			player = self.p1
		else:
			player = self.p2

		return player.can_buy(self.patch_list[patch_idx])

	def can_place(self, patch, row, col):
		if self.p1_turn():
			player = self.p1
		else:
			player = self.p2

		return player.can_place(patch, row, col)

	#return player.jump value to see if a patch was passed
	def jump(self):
		if self.p1_turn():
			player = self.p1
			other_player = self.p2
		else:
			player = self.p2
			other_player = self.p1

		return player.jump(self.time_track, other_player)

	#returns True if p1 turn, False if p2 turn
	def p1_turn(self):
		return (self.p1.position < self.p2.position) or ((self.p1.position == self.p2.position) and self.p1.on_top == True)

	#return valid turns for the current model
	def get_turns(self):
		if self.p1_turn():
			player = self.p1
			other_player = self.p2
		else:
			player = self.p2
			other_player = self.p1

		turns = []

		for i in range(3):
			if self.can_buy(i):
				turns.append(BuyTurn(i))

		turns.append(JumpTurn())

		return turns

	#builds a list of the patches in patchwork
	def build_patch_list(self):
		p1_r1 = [0, 1, 1] 
		p1_r2 = [0, 1, 1]
		p1_r3 = [1, 1, 0]
		p1_array = [p1_r1, p1_r2, p1_r3]
		p1 = Patch(1, p1_array, 8, 6, 3)

		p2_r1 = [0, 1, 0]
		p2_r2 = [0, 1, 0]
		p2_r3 = [1, 1, 1]
		p2_r4 = [0, 1, 0]
		p2_array = [p2_r1, p2_r2, p2_r3, p2_r4]
		p2 = Patch(2, p2_array, 0, 3, 1)

		p3_r1 = [1, 1, 0]
		p3_r2 = [0, 1, 0]
		p3_r3 = [0, 1, 0]
		p3_r4 = [0, 1, 1]
		p3_array = [p3_r1, p3_r2, p3_r3, p3_r4]
		p3 = Patch(3, p3_array, 1, 2, 0)

		p4_r1 = [1, 1]
		p4_r2 = [1, 0]
		p4_r3 = [1, 1]
		p4_array = [p4_r1, p4_r2, p4_r3]
		p4 = Patch(4, p4_array, 1, 2, 0)

		p5_r1 = [0, 1]
		p5_r2 = [0, 1]
		p5_r3 = [1, 1]
		p5_r4 = [0, 1]
		p5_array = [p5_r1, p5_r2, p5_r3, p5_r4]
		p5 = Patch(5, p5_array, 3, 4, 1)

		p6_r1 = [1, 0]
		p6_r2 = [1, 1]
		p6_r3 = [1, 1]
		p6_r4 = [0, 1]
		p6_array = [p6_r1, p6_r2, p6_r3, p6_r4]
		p6 = Patch(6, p6_array, 4, 2, 0)

		p7_r1 = [1, 0]
		p7_r2 = [1, 0]
		p7_r3 = [1, 1]
		p7_array = [p7_r1, p7_r2, p7_r3]
		p7 = Patch(7, p7_array, 4, 2, 1)

		p8_r1 = [0, 1, 0]
		p8_r2 = [1, 1, 1]
		p8_r3 = [1, 0, 1]
		p8_array = [p8_r1, p8_r2, p8_r3]
		p8 = Patch(8, p8_array, 3, 6, 2)

		p9_r1 = [0, 1]
		p9_r2 = [1, 1]
		p9_r3 = [0, 1]
		p9_array = [p9_r1, p9_r2, p9_r3]
		p9 = Patch(9, p9_array, 2, 2, 0)

		p10_r1 = [0, 1, 1, 0]
		p10_r2 = [1, 1, 1, 1]
		p10_array = [p10_r1, p10_r2]
		p10 = Patch(10, p10_array, 7, 4, 2)

		p11_r1 = [0, 1]
		p11_r2 = [1, 1]
		p11_r3 = [1, 0]
		p11_array = [p11_r1, p11_r2, p11_r3]
		p11 = Patch(11, p11_array, 3, 2, 1)

		p12_r1 = [0, 1]
		p12_r2 = [1, 1]
		p12_array = [p12_r1, p12_r2]
		p12 = Patch(12, p12_array, 1, 3, 0)

		p13_r1 = [0, 0, 1]
		p13_r2 = [0, 1, 1]
		p13_r3 = [1, 1, 0]
		p13_array = [p13_r1, p13_r2, p13_r3]
		p13 = Patch(13, p13_array, 10, 4, 3)

		p14_r1 = [1, 1, 1]
		p14_r2 = [0, 1, 0]
		p14_r3 = [1, 1, 1]
		p14_array = [p14_r1, p14_r2, p14_r3]
		p14 = Patch(14, p14_array, 2, 3, 0)

		p15_r1 = [0, 1, 0]
		p15_r2 = [0, 1, 0]
		p15_r3 = [1, 1, 1]
		p15_r4 = [0, 1, 0]
		p15_r5 = [0, 1, 0]
		p15_array = [p15_r1, p15_r2, p15_r3, p15_r4, p15_r5]
		p15 = Patch(15, p15_array, 1, 4, 1)

		p16_r1 = [1, 1, 1]
		p16_array = [p16_r1]
		p16 = Patch(16, p16_array, 2, 2, 0)

		p17_r1 = [1, 1, 1, 1]
		p17_array = [p17_r1]
		p17 = Patch(17, p17_array, 3, 3, 1)

		p18_r1 = [0, 1, 0]
		p18_r2 = [1, 1, 1]
		p18_r3 = [1, 1, 1]
		p18_r4 = [0, 1, 0]
		p18_array = [p18_r1, p18_r2, p18_r3, p18_r4]
		p18 = Patch(18, p18_array, 5, 3, 1)

		p19_r1 = [0, 1]
		p19_r2 = [0, 1]
		p19_r3 = [1, 1]
		p19_r4 = [1, 1]
		p19_array = [p19_r1, p19_r2, p19_r3, p19_r4]
		p19 = Patch(19, p19_array, 10, 5, 3)

		p20_r1 = [0, 1, 1, 1]
		p20_r2 = [1, 1, 0, 0]
		p20_array = [p20_r1, p20_r2]
		p20 = Patch(20, p20_array, 2, 3, 1)

		p21_r1 = [1, 0, 0, 1]
		p21_r2 = [1, 1, 1, 1]
		p21_array = [p21_r1, p21_r2]
		p21 = Patch(21, p21_array, 1, 5, 1)

		p22_r1 = [0, 0, 1, 0]
		p22_r2 = [1, 1, 1, 1]
		p22_r3 = [0, 1, 0, 0]
		p22_array = [p22_r1, p22_r2, p22_r3]
		p22 = Patch(22, p22_array, 2, 1, 0)

		p23_r1 = [0, 0, 0, 1]
		p23_r2 = [1, 1, 1, 1]
		p23_array = [p23_r1, p23_r2]
		p23 = Patch(23, p23_array, 10, 3, 2)

		p24_r1 = [1, 0, 0, 0]
		p24_r2 = [1, 1, 1, 1]
		p24_r3 = [1, 0, 0, 0]
		p24_array = [p24_r1, p24_r2, p24_r3]
		p24 = Patch(24, p24_array, 7, 2, 2)

		p25_r1 = [0, 1, 0]
		p25_r2 = [1, 1, 1]
		p25_r3 = [0, 1, 0]
		p25_array = [p25_r1, p25_r2, p25_r3]
		p25 = Patch(25, p25_array, 5, 4, 2)

		p26_r1 = [1, 1] 
		p26_r2 = [0, 1] 
		p26_r3 = [0, 1] 
		p26_array = [p26_r1, p26_r2, p26_r3]
		p26 = Patch(26, p26_array, 4, 6, 2)

		p27_r1 = [0, 1]
		p27_r2 = [1, 1]
		p27_r3 = [1, 1]
		p27_array = [p27_r1, p27_r2, p27_r3]
		p27 = Patch(27, p27_array, 2, 2, 0)

		p28_r1 = [0, 1, 1]
		p28_r2 = [1, 1, 0]
		p28_array = [p28_r1, p28_r2]
		p28 = Patch(28, p28_array, 7, 6, 3)

		p29_r1 = [0, 1]
		p29_r2 = [1, 1]
		p29_array = [p29_r1, p29_r2]
		p29 = Patch(29, p29_array, 3, 1, 0)

		p30_r1 = [0, 1, 0]
		p30_r2 = [0, 1, 0]
		p30_r3 = [1, 1, 1]
		p30_array = [p30_r1, p30_r2, p30_r3]
		p30 = Patch(30, p30_array, 5, 5, 2)

		p31_r1 = [1, 1]
		p31_r2 = [1, 1]
		p31_array = [p31_r1, p31_r2]
		p31 = Patch(31, p31_array, 6, 5, 2)

		p32_r1 = [1, 1, 1, 1, 1]
		p32_array = [p32_r1]
		p32 = Patch(32, p32_array, 7, 1, 1)

		p33_r1 = [1, 1]
		p33_array = [p33_r1]
		p33 = Patch(33, p33_array, 2, 1, 0)


		#TODO: There's gotta be a better way
		PATCH_LIST_CONST = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30, p31, p32, p33]

		return PATCH_LIST_CONST

#new_model = PatchworkModel()
#for patch in new_model.PATCH_LIST_CONST:
#	for row in patch.shape:
#		for i in row:
#			print(i, end="")
#		print()
#	print()
#print("----------------------------------------------------------")
#print()
#
#for patch in new_model.patch_list:
#	for row in patch.shape:
#		for i in row:
#			print(i, end="")
#		print()
#	print()
