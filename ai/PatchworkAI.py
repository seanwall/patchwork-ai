import math

class PatchworkAI():
	def choose_turn(self, model):
		return model.get_turns()[0]


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

