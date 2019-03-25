import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from model.TimeTrack import TimeTrack
from model.TrackTile import TrackTile
from model.QuiltBoard import QuiltBoard
from model.Patch import Patch
from model.Player import Player
from model.PatchworkModel import PatchworkModel

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
		self.assertEqual(p1.buttons, 0)

		p1.move(1, track, p2)

		self.assertEqual(p1.position, 5)
		self.assertEqual(p1.buttons, 3)

		no_tile = p1.move(14, track, p2)

		self.assertEqual(p1.position, 19)
		self.assertEqual(p1.buttons, 9)
		self.assertEqual(no_tile, False)

		tile = p1.move(1, track, p2)

		self.assertEqual(p1.position, 20)
		self.assertEqual(p1.buttons, 9)
		self.assertEqual(tile, True)

		p1.move(32, track, p2)

		self.assertEqual(p1.position, 52)
		self.assertEqual(p1.buttons, 24)

		p1.move(1, track, p2)

		self.assertEqual(p1.position, 53)
		self.assertEqual(p1.buttons, 27)

		p1.move(2, track, p2)

		self.assertEqual(p1.position, 53)
		self.assertEqual(p1.buttons, 27)


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
		self.assertEqual(p1.buttons, 4)

		p2.position = 5

		self.assertEqual(p1.jump(track, p2), False)

		self.assertEqual(p1.position, 6)
		self.assertEqual(p1.buttons, 9)

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


if __name__ == '__main__':
	unittest.main()