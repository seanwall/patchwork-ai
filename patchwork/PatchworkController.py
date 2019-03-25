import os
import sys
import string
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time 
import pygame
import enum

from model.PatchworkModel import PatchworkModel

class MovePhase(enum.Enum):
	BUYPHASE = 1
	PLACEPHASE = 2

class PatchworkController():
	FLAGS = 0
	WIDTH = 1500
	HEIGHT = 900
	FPS = 30

	def __init__(self):
		pygame.init()
		pygame.font.init()
		
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		self.track_surface = pygame.surface.Surface((self.WIDTH/6, self.HEIGHT*8))
		self.piece_surface = pygame.surface.Surface((self.WIDTH/6, self.HEIGHT*4))

		self.clock = pygame.time.Clock()
		pygame.display.set_caption("TEST TEST TEST")

		self.running = True

		self.model = PatchworkModel()


	def mainloop(self):
		time_track_x = (self.WIDTH - (self.WIDTH/3) - 1)
		piece_list_x = (self.WIDTH - (self.WIDTH/6))

		track_scroll_y = 0
		piece_scroll_y = 0

		highlighted_patch_idx = 0

		#current player 
		#TODO: should be a better way to do this than just if statements on this variable 
		curr_player = 1

		#current phase of a turn 
		phase = MovePhase.BUYPHASE


		while self.running:
			mouse_x, mouse_y = pygame.mouse.get_pos()

			#EVENT HANDLING
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					#if mouse is hovering the time track, scroll the time track
					if(mouse_x >= time_track_x and mouse_x < piece_list_x):
						if event.button == 4: track_scroll_y = min(track_scroll_y + 30, 0)
						if event.button == 5: track_scroll_y = max(track_scroll_y - 30, -self.HEIGHT*8)
					#if mouse is hovering the patch list, scroll the patch list
					if(mouse_x >= piece_list_x):
						if event.button == 4: piece_scroll_y = min(piece_scroll_y + 30, 0)
						if event.button == 5: piece_scroll_y = max(piece_scroll_y - 30, -self.HEIGHT*4)
				if event.type == pygame.KEYDOWN:
					#if in the buy phase up/down arrows should change the selected pice
					if phase == MovePhase.BUYPHASE:
						if event.key == pygame.K_DOWN:
							if highlighted_patch_idx < 2:
								highlighted_patch_idx += 1
						if event.key == pygame.K_UP:
							if highlighted_patch_idx > 0:
								highlighted_patch_idx -= 1
				if event.type == pygame.QUIT:
					self.running = False

			#RENDERING

			#fill screens and menus with base color
			self.screen.fill((0, 200, 255))
			self.piece_surface.fill((0, 0, 0))
			self.track_surface.fill((0, 0, 0))

			#highlight selected piece
			pygame.draw.rect(self.piece_surface, (0,200,255),[0, highlighted_patch_idx * 100, self.WIDTH/6, 100])

			#draw patches on patch scroll bar
			for patch in range(len(self.model.patch_list)):
				self.model.patch_list[patch].render(self.piece_surface, 20, 20 + (100*patch))

			#draw time track tiles on time track scroll bar
			for tile in range(len(self.model.time_track.track)):
				self.model.time_track.track[tile].render(self.track_surface, self.track_surface.get_width()/4, (tile * self.track_surface.get_width()/2))

			#draw players on time track
			self.model.p1.render_piece(self.track_surface, int(self.track_surface.get_width()/3), int(self.model.p1.position * self.track_surface.get_width()/2 + self.track_surface.get_width()/3))
			self.model.p2.render_piece(self.track_surface, int(self.track_surface.get_width() - self.track_surface.get_width()/2.5), int(self.model.p1.position * self.track_surface.get_width()/2 + self.track_surface.get_width()/3))

			#render time track and patch scroll bar surfaces onto the window
			self.screen.blit(self.track_surface, (time_track_x, track_scroll_y))
			self.screen.blit(self.piece_surface, (piece_list_x, piece_scroll_y))

			#draw p1 quilt board
			#TODO: SWAP THIS BASED ON CURRENT PLAYER
			self.model.p1.render_board_primary(self.screen, self.WIDTH/5, self.HEIGHT/15)
			self.model.p2.render_board_secondary(self.screen, self.WIDTH/30, self.HEIGHT/6)


			pygame.display.flip()
			
		pygame.quit()

PatchworkController().mainloop()