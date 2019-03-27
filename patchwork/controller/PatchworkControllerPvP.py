import os
import sys
import string
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time 
import pygame
import enum

from model.PatchworkModel import PatchworkModel
from view.PatchworkView import PatchworkView
from controller.MovePhase import MovePhase

class PatchworkControllerPvP():
	FLAGS = 0
	WIDTH = 1500
	HEIGHT = 900
	FPS = 30

	def __init__(self):
		pygame.init()
		pygame.font.init()
		
		self.view = PatchworkView()
		self.model = PatchworkModel()

		self.clock = pygame.time.Clock()
		pygame.display.set_caption("TEST TEST TEST")

		self.running = True

	def mainloop(self):

		time_track_x = (self.WIDTH - (self.WIDTH/3) - 1)
		piece_list_x = (self.WIDTH - (self.WIDTH/6))

		track_scroll_y = 0
		piece_scroll_y = 0

		highlighted_patch_idx = 0
		selected_patch = None
		selected_patch_row = 0
		selected_patch_col = 0

		#current player 
		#TODO: should be a better way to do this than just if statements on this variable 
		p1_turn = self.model.p1_turn()

		#current phase of a turn 
		phase = MovePhase.BUYPHASE


		while self.running:
			#Don't do any more processing if the game is over
			#if self.model.game_over():
			#	self.view.render(self.model, phase, track_scroll_y, piece_scroll_y, highlighted_patch_idx, selected_patch, selected_patch_row, selected_patch_col)

			#else:
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
				if event.type == pygame.KEYUP:
					#if in the buy phase up/down arrows should change the selected pice
					if phase == MovePhase.BUYPHASE:
						if event.key == pygame.K_DOWN:
							if highlighted_patch_idx < 2:
								highlighted_patch_idx += 1
						if event.key == pygame.K_UP:
							if highlighted_patch_idx > 0:
								highlighted_patch_idx -= 1
						if event.key == pygame.K_RETURN:
							#if self.model.buy_patch(curr_player, highlighted_patch_idx) is not None:
							#if the patch is purchasable by the current player, enter placement mode
							if self.model.can_buy(highlighted_patch_idx) :
								selected_patch = self.model.patch_list[highlighted_patch_idx]
								phase = MovePhase.PLACEPHASE
						if event.key == pygame.K_TAB:
							self.model.jump()
							p1_turn = self.model.p1_turn()

					if phase == MovePhase.PLACEPHASE:
						if event.key == pygame.K_UP:
							if selected_patch_row > 0:
								selected_patch_row -= 1
						if event.key == pygame.K_DOWN:
							if selected_patch_row < 8:
								selected_patch_row += 1
						if event.key == pygame.K_LEFT:
							if selected_patch_col > 0:
								selected_patch_col -= 1
						if event.key == pygame.K_RIGHT:
							if selected_patch_col < 8:
								selected_patch_col += 1
						if event.key == pygame.K_SPACE:
							selected_patch.rotate_cw()
						if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
							if self.model.can_place(selected_patch, selected_patch_row, selected_patch_col):

								self.model.place_patch(selected_patch, selected_patch_row, selected_patch_col)
								self.model.buy_patch(highlighted_patch_idx)

								phase = MovePhase.BUYPHASE
								p1_turn = self.model.p1_turn()

				if event.type == pygame.QUIT:
					self.running = False

				#RENDERING

			self.view.render(self.model, phase, track_scroll_y, piece_scroll_y, highlighted_patch_idx, selected_patch, selected_patch_row, selected_patch_col)
			
		pygame.quit()