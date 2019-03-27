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
from ai.PatchworkAI import PatchworkAI
from model.Turn import BuyTurn
from model.Turn import JumpTurn

class PatchworkControllerPvAI():
	FLAGS = 0
	WIDTH = 1500
	HEIGHT = 900
	FPS = 30

	def __init__(self):
		pygame.init()
		pygame.font.init()
		
		self.view = PatchworkView()
		self.model = PatchworkModel()
		self.ai = PatchworkAI()

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

		#current phase of a turn 
		phase = MovePhase.BUYPHASE


		while self.running:
			#Don't do any more processing if the game is over
			#if self.model.game_over():
			#	self.view.render(self.model, phase, track_scroll_y, piece_scroll_y, highlighted_patch_idx, selected_patch, selected_patch_row, selected_patch_col)

			#else:
			mouse_x, mouse_y = pygame.mouse.get_pos()

			#EVENT HANDLING
			#p1 is the human player
			if self.model.p1_turn():
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
								#check for 1x1 placement
								self.model.jump()
								#if self.model.jump():
								#	phase = MovePhase.SPECIAL_PLACEPHASE
								#	selected_patch = Patch([[1]], 0, 0, 0)

						#if phase == MovePhase.PLACEPHASE or phase == MovePhase.SPECIAL_PLACEPHASE:
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
									#if in placephase, buy the patch to advance to next phase
									#if phase == MovePhase.PLACEPHASE:
									self.model.place_patch(selected_patch, selected_patch_row, selected_patch_col)
									self.model.buy_patch(highlighted_patch_idx)
									phase = MovePhase.BUYPHASE
										#check for 1x1 placement
										#passed_patch = self.model.buy_patch(highlighted_patch_idx)
										#print(passed_patch)
										#if passed_patch:
										#	phase = MovePhase.SPECIAL_PLACEPHASE
										#	selected_patch = Patch([[1]], 0, 0, 0)
										#else:
										#	phase = MovePhase.BUYPHASE
									#else in special place phase, phase ends when piece is placed (dont need to buy)
									#else:
									#	self.model.place_patch(selected_patch, selected_patch_row, selected_patch_col)
									#	phase = MovePhase.BUYPHASE

					if event.type == pygame.QUIT:
						self.running = False

			#AI turn
			else:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.running = False

				turn = self.ai.choose_turn(self.model)
				if isinstance(turn, BuyTurn):

					#TEMPORARY HANDLING FOR IF THE PIECE CANT BE PLACED, NEED NEW SOLUTION FOR THIS
					if self.ai.choose_placement(self.model.patch_list[turn.patch_idx], self.model.p2.quilt) == False:
						turn = JumpTurn()
					else:
						row, col = self.ai.choose_placement(self.model.patch_list[turn.patch_idx], self.model.p2.quilt)
						self.model.place_patch(self.model.patch_list[turn.patch_idx], row, col)
				turn.run(self.model)

				#RENDERING

			self.view.render(self.model, phase, track_scroll_y, piece_scroll_y, highlighted_patch_idx, selected_patch, selected_patch_row, selected_patch_col)
			
		pygame.quit()