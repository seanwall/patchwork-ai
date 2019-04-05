import unittest

from ai.PatchworkAI import PatchworkAI
from patchwork.model.QuiltBoard import QuiltBoard
from patchwork.model.Patch import Patch

class PlacementMethods(unittest.TestCase):
	def test_get_quilt_utility(self):
		board = QuiltBoard()

		self.assertEqual(PatchworkAI().get_quilt_utility(board), 288)

		board.board_array[0][0] = 1

		self.assertEqual(PatchworkAI().get_quilt_utility(board), 284)

		board.board_array[0][1] = 1
		board.board_array[1][0] = 1
		board.board_array[1][1] = 1

		self.assertEqual(PatchworkAI().get_quilt_utility(board), 272)

	def test_placement(self):
		board = QuiltBoard()

		board.board_array[0][1] = 1
		board.board_array[1][0] = 1
		board.board_array[1][1] = 1

		row, col, patch_orientation = PatchworkAI().choose_placement(Patch([[1]], 0, 0, 0), board)

		self.assertEqual(row, 0)
		self.assertEqual(col, 0)





if __name__ == '__main__':
	unittest.main()
