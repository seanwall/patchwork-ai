class PatchworkAI():
	def choose_turn(self, model):
		return model.get_turns()[0]

	def choose_placement(self, patch, quilt):
		for row in range(len(patch.orientation)):
			for col in range(len(patch.orientation[row])):
				print (patch.orientation[row][col], end="")
			print()
		print()

		for row in range(9):
			for col in range(9):
				if quilt.valid_placement(patch, row, col):
					return row, col
		return False