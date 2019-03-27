import pygame

class Patch():
	#TODO, would be nice if patches had their buttons on them
	def __init__(self, shape, cost, time_cost, button_gen): #these names suck
		self.shape = shape
		self.orientation = shape
		self.cost = cost
		self.time_cost = time_cost
		self.button_gen = button_gen

	def rotate_cw(self):
		rotated_shape = [[0 for height in range(len(self.orientation))] for width in range(len(self.orientation[0]))]

		transform_height = len(rotated_shape)
		transform_width = len(rotated_shape[0])

		for row in range(len(self.orientation)):
			for col in range(len(self.orientation[row])):
				rotated_shape[col][transform_width - row - 1] = self.orientation[row][col]

		self.orientation = rotated_shape

	#renders patch onto the given surface with the upper left hand corner starting at x,y
	def render_buy_list(self, surface, x, y):
		
		pygame.font.init()

		f = pygame.font.SysFont("", 25)

		cost_text = f.render("Cost: " + str(self.cost), False, (255, 255, 255))
		time_text = f.render("Time Cost: " + str(self.time_cost), False, (255, 255, 255))
		button_gen_text = f.render("Button Gen: " + str(self.button_gen), False, (255, 255, 255))

		surface.blit(cost_text, (x + surface.get_width()/3, y))
		surface.blit(time_text, (x + surface.get_width()/3, y + 25))
		surface.blit(button_gen_text, (x + surface.get_width()/3, y + 50))

		square_width = int(surface.get_width()/20)

		for row in range(len(self.shape)):
			for col in range(len(self.shape[row])):
				if self.shape[row][col] == 1:
					pygame.draw.rect(surface, (255, 255, 255), [x + (square_width*col), y + (square_width*row), square_width - 1, square_width - 1])

	#renders patch onto the given surface with the upper left hand corner starting at x,y
	def render_placement(self, surface, x, y, color):
		square_width = int(surface.get_width()/9)

		for row in range(len(self.orientation)):
			for col in range(len(self.orientation[row])):
				if self.orientation[row][col] == 1:
					pygame.draw.rect(surface, color, [(x*square_width) + (square_width*col), (y*square_width) + (square_width*row), square_width - 1, square_width - 1])

