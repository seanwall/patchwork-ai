from model.Patch import Patch
import pygame

class QuiltBoard():
	
	def __init__(self):
		self.board_array = [[0 for row in range(9)] for col in range(9)]
		self.pieces = []
		self.button_gen = 0

	def valid_placement(self, patch, row, col):
		board_row = row
		for patch_row in range(len(patch.orientation)):
			board_col = col
			for patch_col in range(len(patch.orientation[patch_row])):

				if patch.orientation[patch_row][patch_col] == 1 :
					if board_row >= 9:
						return False
					if board_col >= 9:
						return False
					if self.board_array[board_row][board_col] == 1 :
						return False

				board_col += 1

			board_row += 1

		return True

	def place_patch(self, patch, row, col):
		if not self.valid_placement(patch, row, col):
			#raise Exception("invalid placement")
			print('Patch cannot be placed at those coordinates')
			return
		else:
			board_row = row
			for patch_row in range(len(patch.orientation)):
				board_col = col
				for patch_col in range(len(patch.orientation[patch_row])):
					if patch.orientation[patch_row][patch_col] == 1:
						self.board_array[board_row][board_col] = 1

					board_col += 1
				board_row += 1

			#update button gen for the board and the pieces list
			self.button_gen += patch.button_gen
			self.pieces.append(patch)

	#-2 for each open tile
	def calculate_board_coverage(self):
		sum = 0
		for row in range(len(self.board_array)):
			for col in range(len(self.board_array[row])):
				if self.board_array[row][col] == 0:
					sum -= 2

		return sum

	#TODO: THIS IS BAD, NEED BETTER VIEW HANDLING PASSING EVERYTHING AROUND IS MESSY
	def render_primary(self, surface, x, y, button_count):
		square_width = int(surface.get_width()/9)

		pygame.font.init()
		f = pygame.font.SysFont("", 30)
		buttons_text = f.render("Buttons: " + str(button_count), False, (255, 255, 255))
		button_gen_text = f.render("Button Gen: " + str(self.button_gen), False, (255, 255, 255))

		surface.blit(buttons_text, (x, y + square_width * 9 + 20))
		surface.blit(button_gen_text, (x, y + square_width * 9 + 40))

		for row in range(len(self.board_array)):
			for col in range(len(self.board_array[row])):
				if self.board_array[row][col] == 1:
					pygame.draw.rect(surface, (0, 0, 0), [x + (square_width*col), y + (square_width*row), square_width - 1, square_width - 1])
				else:
					pygame.draw.rect(surface, (255, 255, 255), [x + (square_width*col), y + (square_width*row), square_width - 1, square_width - 1])

	def render_secondary(self, surface, x, y, button_count):
		square_width = int(surface.get_width()/60)

		pygame.font.init()
		f = pygame.font.SysFont("", 30)
		buttons_text = f.render("Buttons: " + str(button_count), False, (255, 255, 255))
		button_gen_text = f.render("Button Gen: " + str(self.button_gen), False, (255, 255, 255))

		surface.blit(buttons_text, (x, y + square_width * 9 + 20))
		surface.blit(button_gen_text, (x, y + square_width * 9 + 45))

		for row in range(len(self.board_array)):
			for col in range(len(self.board_array[row])):
				if self.board_array[row][col] == 1:
					pygame.draw.rect(surface, (0, 0, 0), [x + (square_width*col), y + (square_width*row), square_width - 1, square_width - 1])
				else:
					pygame.draw.rect(surface, (255, 255, 255), [x + (square_width*col), y + (square_width*row), square_width - 1, square_width - 1])

