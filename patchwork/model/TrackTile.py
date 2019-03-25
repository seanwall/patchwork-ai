import enum
import pygame

class TrackTile(enum.Enum):
	BLANK = 1
	INCOME = 2
	PATCH = 3
	END = 4

	def render(self, surface, x, y):
		square_width = int(surface.get_width()/2.25)

		pygame.draw.rect(surface, (255, 255, 255), [x, y, square_width, square_width])

		pygame.font.init()
		f = pygame.font.SysFont("", 25)

		if self == TrackTile.INCOME:
			income_text = f.render("INCOME", False, (0, 0, 0))
			text_width = income_text.get_width()
			text_height = income_text.get_height()
			surface.blit(income_text, (x + square_width/2 - (text_width/2), y + square_width/2 - (text_height/2)))
		if self == TrackTile.PATCH:
			patch_text = f.render("PATCH", False, (0, 0, 0))
			text_width = patch_text.get_width()
			text_height = patch_text.get_height()
			surface.blit(patch_text, (x + square_width/2 - (text_width/2), y + square_width/2 - (text_height/2)))
		if self == TrackTile.END:
			end_text = f.render("END", False, (0, 0, 0))
			text_width = end_text.get_width()
			text_height = end_text.get_height()
			surface.blit(end_text, (x + square_width/2 - (text_width/2), y + square_width/2 - (text_height/2)))