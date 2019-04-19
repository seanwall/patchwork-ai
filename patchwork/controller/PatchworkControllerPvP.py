import time 
import pygame
import enum

from patchwork.model.PatchworkModel import PatchworkModel
from patchwork.model.Patch import Patch
from patchwork.view.PatchworkView import PatchworkView
from patchwork.controller.MovePhase import MovePhase

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

		#TESTING
		#self.model.p1.position = 19
		#self.model.p2.position = 19

		self.clock = pygame.time.Clock()
		pygame.display.set_caption("P v P")

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
			if self.model.p1_turn():
				player = self.model.p1
				other_player = self.model.p2
			else:
				player = self.model.p2
				other_player = self.model.p1
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
							#if the patch is purchasable by the current player, enter placement mode
							if self.model.can_buy(highlighted_patch_idx) :
								selected_patch = self.model.patch_list[highlighted_patch_idx]
								phase = MovePhase.PLACEPHASE
						if event.key == pygame.K_TAB:
							#check for 1x1 placement
							if self.model.jump():
								phase = MovePhase.SPECIAL_PLACEPHASE
								selected_patch = Patch([[1]], 0, 0, 0)

					if phase == MovePhase.PLACEPHASE or phase == MovePhase.SPECIAL_PLACEPHASE:
					#if phase == MovePhase.PLACEPHASE:
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
								#if in placephase, buy the patch to advance to next phase
								if phase == MovePhase.PLACEPHASE:
									#check for 1x1 placement
									self.model.place_patch(player, self.model.patch_list[highlighted_patch_idx], selected_patch_row, selected_patch_col)
									passed_patch, passed_button_gen = self.model.buy_patch(highlighted_patch_idx)
									if passed_patch:
										phase = MovePhase.SPECIAL_PLACEPHASE
										selected_patch = Patch(34,[[1]], 0, 0, 0)
									else:
										phase = MovePhase.BUYPHASE
								#else in special place phase, phase ends when piece is placed (dont need to buy)
								else:
									self.model.place_patch(other_player, selected_patch, selected_patch_row, selected_patch_col)
									phase = MovePhase.BUYPHASE

				if event.type == pygame.QUIT:
					self.running = False

			#RENDERING
			self.view.render(self.model, phase, track_scroll_y, piece_scroll_y, highlighted_patch_idx, selected_patch, selected_patch_row, selected_patch_col)
			
		pygame.quit()