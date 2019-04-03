import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from collections import deque

from model.TimeTrack import TimeTrack
from model.TrackTile import TrackTile
from model.QuiltBoard import QuiltBoard
from model.Patch import Patch
from model.Player import Player
from model.PatchworkModel import PatchworkModel
from model.Turn import BuyTurn
from model.Turn import JumpTurn

class TestTimeTrackMethods(unittest.TestCase):

	#TODO: THIS TEST IS DUMB
	def test_removepatch_patchremoved(self):
		new_track = TimeTrack()

		self.assertEqual(new_track.trackToString(), "00000$00000$00000$00P00$00P00$00P00$00000$00P00$00P00E")

		new_track.removePatch(20)

		self.assertEqual(new_track.trackToString(), "00000$00000$00000$00000$00P00$00P00$00000$00P00$00P00E")

class TestQuiltBoardMethods(unittest.TestCase):

	def test_valid_placement(self):
		tetris_array_top = [1, 0, 0] 
		tetris_array_mid = [1, 1, 0]
		tetris_array_bot = [1, 0 ,0]

		tetris_array = [tetris_array_top, tetris_array_mid, tetris_array_bot]
		tetris = Patch(tetris_array, 2, 3, 0)

		new_board = QuiltBoard()

		self.assertEqual(new_board.valid_placement(tetris, 0, 0), True)
		self.assertEqual(new_board.valid_placement(tetris, 0, 7), True)
		self.assertEqual(new_board.valid_placement(tetris, 0, 8), False)
		self.assertEqual(new_board.valid_placement(tetris, 6, 0), True)
		self.assertEqual(new_board.valid_placement(tetris, 7, 0), False)

		new_board.place_patch(tetris, 0, 0)

		self.assertEqual(new_board.valid_placement(tetris, 0, 0), False)
		self.assertEqual(new_board.valid_placement(tetris, 0, 1), False)

	def test_place_patch(self):
		tetris_array_top = [1, 0, 0] 
		tetris_array_mid = [1, 1, 0]
		tetris_array_bot = [1, 0 ,0]

		test_board_array = [[0 for row in range(9)] for col in range(9)]

		tetris_array = [tetris_array_top, tetris_array_mid, tetris_array_bot]
		tetris = Patch(tetris_array, 2, 3, 0)

		new_board = QuiltBoard()

		self.assertEqual(new_board.board_array, test_board_array)

		new_board.place_patch(tetris, 0, 0)

		test_board_array[0][0] = 1
		test_board_array[1][0] = 1
		test_board_array[2][0] = 1
		test_board_array[1][1] = 1

		self.assertEqual(new_board.board_array, test_board_array)

	def test_calculate_quilt_score(self):
		new_board = QuiltBoard()

		self.assertEqual(new_board.calculate_board_coverage(), 81*-2)

		new_board.board_array = [[1 for row in range(9)] for col in range(9)]

		self.assertEqual(new_board.calculate_board_coverage(), 0)

	def test_copy_quilt(self):
		test_board_array = [[0 for row in range(9)] for col in range(9)]
		new_board = QuiltBoard()

		for i in range (5):
			test_board_array[i][i] = 1
			new_board.board_array[i][i] = 1

		self.assertEqual(test_board_array, new_board.board_array)

		copy = new_board.copy()

		self.assertEqual(test_board_array, new_board.board_array)
		self.assertEqual(test_board_array, copy.board_array)

		test_board_array2 = [[0 for row in range(9)] for col in range(9)]
		for i in range(9):
			new_board.board_array[i][i] = 1
			test_board_array2[i][i] = 1

		self.assertEqual(test_board_array2, new_board.board_array)
		self.assertEqual(test_board_array, copy.board_array)

class TestPatchMethods(unittest.TestCase):

	def test_patch_rotate(self):
		tetris_array_top = [1, 0] 
		tetris_array_mid = [1, 1]
		tetris_array_bot = [1, 0]

		tetris_array = [tetris_array_top, tetris_array_mid, tetris_array_bot]
		tetris = Patch(tetris_array, 2, 3, 0)

		tetris_array_cw_top = [1, 1, 1]
		tetris_array_cw_mid = [0, 1, 0]

		tetris_array_rotated = [tetris_array_cw_top, tetris_array_cw_mid]

		self.assertEqual(tetris.shape, tetris_array)
		self.assertEqual(tetris.orientation, tetris_array)

		tetris.rotate_cw()

		self.assertEqual(tetris.shape, tetris_array)
		self.assertEqual(tetris.orientation, tetris_array_rotated)

	def test_patch_flip(self):
		tetris_array_top = [1, 0] 
		tetris_array_mid = [1, 1]
		tetris_array_bot = [1, 0]

		tetris_array = [tetris_array_top, tetris_array_mid, tetris_array_bot]
		tetris = Patch(tetris_array, 2, 3, 0)

		tetris_array_flip_top = [0, 1] 
		tetris_array_flip_mid = [1, 1]
		tetris_array_flip_bot = [0, 1]

		tetris_array_flipped = [tetris_array_flip_top, tetris_array_flip_mid, tetris_array_flip_bot]

		self.assertEqual(tetris.shape, tetris_array)
		self.assertEqual(tetris.orientation, tetris_array)

		tetris.flip()

		self.assertEqual(tetris.shape, tetris_array)
		self.assertEqual(tetris.orientation, tetris_array_flipped)

		l_array_top = [1, 0] 
		l_array_mid = [1, 0]
		l_array_bot = [1, 1]

		l_array = [l_array_top, l_array_mid, l_array_bot]
		l_patch = Patch(l_array, 2, 3, 0)

		l_array_flip_top = [0, 1] 
		l_array_flip_mid = [0, 1]
		l_array_flip_bot = [1, 1]

		l_array_flipped = [l_array_flip_top, l_array_flip_mid, l_array_flip_bot]

		self.assertEqual(l_patch.shape, l_array)
		self.assertEqual(l_patch.orientation, l_array)

		l_patch.flip()

		self.assertEqual(l_patch.shape, l_array)
		self.assertEqual(l_patch.orientation, l_array_flipped)

	def test_copy_patch(self):
		tetris_array_top = [1, 0] 
		tetris_array_mid = [1, 1]
		tetris_array_bot = [1, 0]

		tetris_array = [tetris_array_top, tetris_array_mid, tetris_array_bot]
		tetris = Patch(tetris_array, 2, 3, 0)

		self.assertEqual(tetris.shape, tetris_array)
		self.assertEqual(tetris.orientation, tetris_array)
		self.assertEqual(tetris.cost, 2)
		self.assertEqual(tetris.time_cost, 3)
		self.assertEqual(tetris.button_gen, 0)

		copy = tetris.copy()

		self.assertEqual(copy.shape, tetris_array)
		self.assertEqual(copy.orientation, tetris_array)
		self.assertEqual(copy.cost, 2)
		self.assertEqual(copy.time_cost, 3)
		self.assertEqual(copy.button_gen, 0)

		tetris.rotate_cw()

		tetris_array_cw_top = [1, 1, 1]
		tetris_array_cw_mid = [0, 1, 0]

		tetris_array_rotated = [tetris_array_cw_top, tetris_array_cw_mid]

		self.assertEqual(tetris.shape, tetris_array)
		self.assertEqual(tetris.orientation, tetris_array_rotated)
		self.assertEqual(tetris.cost, 2)
		self.assertEqual(tetris.time_cost, 3)
		self.assertEqual(tetris.button_gen, 0)

		self.assertEqual(copy.shape, tetris_array)
		self.assertEqual(copy.orientation, tetris_array)
		self.assertEqual(copy.cost, 2)
		self.assertEqual(copy.time_cost, 3)
		self.assertEqual(copy.button_gen, 0)

		copy.rotate_cw()

		self.assertEqual(tetris.shape, tetris_array)
		self.assertEqual(tetris.orientation, tetris_array_rotated)
		self.assertEqual(tetris.cost, 2)
		self.assertEqual(tetris.time_cost, 3)
		self.assertEqual(tetris.button_gen, 0)

		self.assertEqual(copy.shape, tetris_array)
		self.assertEqual(copy.orientation, tetris_array_rotated)
		self.assertEqual(copy.cost, 2)
		self.assertEqual(copy.time_cost, 3)
		self.assertEqual(copy.button_gen, 0)




class TestPlayerMethods(unittest.TestCase):

	def test_player_move_simple(self):
		p1 = Player(1)
		p2 = Player(2)

		tetris_array_top = [1, 0, 0] 
		tetris_array_mid = [1, 1, 0]
		tetris_array_bot = [1, 0 ,0]
		tetris_array = [tetris_array_top, tetris_array_mid, tetris_array_bot]
		tetris = Patch(tetris_array, 2, 3, 3)

		p1.quilt.place_patch(tetris, 0, 0)


		track = TimeTrack()

		self.assertEqual(p1.position, 0)

		p1.move(4, track, p2)

		self.assertEqual(p1.position, 4)
		self.assertEqual(p1.buttons, 5)

		p1.move(1, track, p2)

		self.assertEqual(p1.position, 5)
		self.assertEqual(p1.buttons, 8)

		no_tile = p1.move(14, track, p2)

		self.assertEqual(p1.position, 19)
		self.assertEqual(p1.buttons, 14)
		self.assertEqual(no_tile, False)

		tile = p1.move(1, track, p2)

		self.assertEqual(p1.position, 20)
		self.assertEqual(p1.buttons, 14)
		self.assertEqual(tile, True)

		p1.move(32, track, p2)

		self.assertEqual(p1.position, 52)
		self.assertEqual(p1.buttons, 29)

		p1.move(1, track, p2)

		self.assertEqual(p1.position, 53)
		self.assertEqual(p1.buttons, 32)

		p1.move(2, track, p2)

		self.assertEqual(p1.position, 53)
		self.assertEqual(p1.buttons, 32)


	def test_player_move_overshoot(self):
		p1 = Player(1)
		p2 = Player(2)
		track = TimeTrack()

		self.assertEqual(p1.position, 0)

		p1.move(30, track, p2)

		self.assertEqual(p1.position, 30)

		p1.move(30, track, p2)

		self.assertEqual(p1.position, 53)

		p1.move(10, track, p2)

		self.assertEqual(p1.position, 53)

	def test_player_move_player_interaction(self):
		p1 = Player(1)
		p2 = Player(2)


		track = TimeTrack()

		self.assertEqual(p1.on_top, True)
		self.assertEqual(p2.on_top, False)

		p1.move(3, track, p2)

		self.assertEqual(p1.on_top, True)
		self.assertEqual(p2.on_top, True)

		p2.move(3, track, p1)

		self.assertEqual(p1.on_top, False)
		self.assertEqual(p2.on_top, True)

	def test_player_move_consume_patch(self):
		p1 = Player(1)
		p2 = Player(2)

		track = TimeTrack()

		self.assertEqual(track.track[20], TrackTile.PATCH)

		self.assertEqual(p1.move(20, track, p2), True)

		self.assertEqual(track.track[20], TrackTile.BLANK)

	def test_player_buy_patch(self):
		p1 = Player(1)
		p2 = Player(2)

		p1.buttons = 5

		track = TimeTrack()

		tetris_array_top = [1, 0, 0] 
		tetris_array_mid = [1, 1, 0]
		tetris_array_bot = [1, 0 ,0]
		tetris_array = [tetris_array_top, tetris_array_mid, tetris_array_bot]
		tetris = Patch(tetris_array, 2, 3, 3)

		p1.buy_patch(tetris, track, p2)

		self.assertEqual(p1.position, 3)
		self.assertEqual(p1.buttons, 3)

	def test_player_jump_simple(self):
		p1 = Player(1)
		p2 = Player(2)

		track = TimeTrack()

		#placing piece to kick off button generation
		tetris_array_top = [1, 0, 0] 
		tetris_array_mid = [1, 1, 0]
		tetris_array_bot = [1, 0 ,0]
		tetris_array = [tetris_array_top, tetris_array_mid, tetris_array_bot]
		tetris = Patch(tetris_array, 2, 3, 3)
		p1.quilt.place_patch(tetris, 0, 0)

		p2.position = 3

		p1.jump(track, p2)

		self.assertEqual(p1.position, 4)
		self.assertEqual(p1.buttons, 9)

		p2.position = 5

		self.assertEqual(p1.jump(track, p2), False)

		self.assertEqual(p1.position, 6)
		self.assertEqual(p1.buttons, 14)

		p2.position = 19

		self.assertEqual(p1.jump(track, p2), True)



	def test_player_calc_score(self):
		p1 = Player(1)

		p1.buttons = 10

		self.assertEqual(p1.get_score(), -152)

		p1.quilt.board_array = [[1 for row in range(9)] for col in range(9)]

		self.assertEqual(p1.get_score(), 10)



class TestModelMethods(unittest.TestCase):

	def test_p1_win_over(self):
		model = PatchworkModel()

		self.assertEqual(model.game_over(), False)

		model.p1.move(53, model.time_track, model.p2)

		self.assertEqual(model.game_over(), False)

		model.p2.move(53, model.time_track, model.p1)

		self.assertEqual(model.game_over(), True)

	def test_get_winner(self):
		model = PatchworkModel()

		self.assertEqual(model.p1_win(), 0)

		model.p1.buttons = 30

		self.assertEqual(model.p1_win(), 1)

		model.p2.buttons = 60

		self.assertEqual(model.p1_win(), -1)

		model.p1.buttons = 60

		self.assertEqual(model.p1_win(), 0)

	def test_p1_turn(self):
		model = PatchworkModel()
		self.assertEqual(model.p1_turn(), True)

		model.p1.position = 10
		self.assertEqual(model.p1_turn(), False)

		model.p2.position = 10
		self.assertEqual(model.p1_turn(), True)

		model.p1.on_top = False
		model.p2.on_top = True
		self.assertEqual(model.p1_turn(), False)

	def test_get_moves(self):
		model = PatchworkModel()
		model.patch_list = deque(model.build_patch_list())
		self.assertIsInstance(model.get_turns()[0], BuyTurn)
		self.assertEqual(model.get_turns()[0].patch_idx, 1)
		self.assertIsInstance(model.get_turns()[1], BuyTurn)
		self.assertEqual(model.get_turns()[1].patch_idx, 2)
		self.assertIsInstance(model.get_turns()[2], JumpTurn)


if __name__ == '__main__':
	unittest.main()