import pygame

from model.PatchworkModel import PatchworkModel
from controller.MovePhase import MovePhase

class PatchworkView():
	WIDTH = 1500
	HEIGHT = 900

	def __init__(self):
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		self.track_surface = pygame.surface.Surface((self.WIDTH/6, self.HEIGHT*8))
		self.piece_surface = pygame.surface.Surface((self.WIDTH/6, self.HEIGHT*4))

		self.primary_board_surface = pygame.surface.Surface((self.WIDTH/2.5, self.WIDTH/2))
		self.secondary_board_surface = pygame.surface.Surface((self.WIDTH/6.5, self.WIDTH/5))
	
	def render(self, model, phase, track_scroll_y, piece_scroll_y, highlighted_patch_idx, selected_patch, selected_patch_row, selected_patch_col):
		time_track_x = (self.WIDTH - (self.WIDTH/3) - 1)
		piece_list_x = (self.WIDTH - (self.WIDTH/6))

		#fill screens and menus with base color
		self.screen.fill((0, 200, 255))
		self.piece_surface.fill((0, 0, 0))
		self.track_surface.fill((0, 0, 0))
		self.primary_board_surface.fill((0, 200, 255))
		self.secondary_board_surface.fill((0, 200, 255))

		#highlight selected piece
		pygame.draw.rect(self.piece_surface, (0,200,255),[0, highlighted_patch_idx * 100, self.WIDTH/6, 100])

		#draw patches on patch scroll bar
		for patch in range(len(model.patch_list)):
			model.patch_list[patch].render_buy_list(self.piece_surface, 20, 20 + (100*patch))

		#draw time track tiles on time track scroll bar
		for tile in range(len(model.time_track.track)):
			model.time_track.track[tile].render(self.track_surface, self.track_surface.get_width()/4, (tile * self.track_surface.get_width()/2))

		#draw players on time track
		model.p1.render_piece(self.track_surface, int(self.track_surface.get_width()/3), int(model.p1.position * self.track_surface.get_width()/2 + self.track_surface.get_width()/3))
		model.p2.render_piece(self.track_surface, int(self.track_surface.get_width() - self.track_surface.get_width()/2.5), int(model.p2.position * self.track_surface.get_width()/2 + self.track_surface.get_width()/3))

		#draw player quilt boards
		if model.p1_turn():
			curr_player = model.p1
			other_player = model.p2
		else:
			curr_player = model.p2
			other_player = model.p1

		#Text
		pygame.font.init()
		f = pygame.font.SysFont("", 30)
		player_text = f.render("Player: " + str(curr_player.player_num), False, (255, 255, 255))
		other_player_text = f.render("Player: " + str(other_player.player_num), False, (255, 255, 255))

		#rendering for a 1x1 tile placement (other player is primary board in this case)
		if phase == MovePhase.SPECIAL_PLACEPHASE:
			self.screen.blit(other_player_text, (self.WIDTH/4.5, self.HEIGHT/8 - 20))
			self.screen.blit(player_text, (self.WIDTH/30, self.HEIGHT/6 - 20))
			other_player.render_board_primary(self.primary_board_surface, 0, 0)
			curr_player.render_board_primary(self.secondary_board_surface, 0, 0)
		#rendering for all other phases, where current player is primary board and other player is secondary
		else:
			self.screen.blit(player_text, (self.WIDTH/4.5, self.HEIGHT/8 - 20))
			self.screen.blit(other_player_text, (self.WIDTH/30, self.HEIGHT/6 - 20))
			curr_player.render_board_primary(self.primary_board_surface, 0, 0)
			other_player.render_board_primary(self.secondary_board_surface, 0, 0)

		#curr_player.render_board_primary(self.primary_board_surface, 0, 0)
		#other_player.render_board_primary(self.secondary_board_surface, 0, 0)

		#draw selected patch if in the placement phase
		if phase == MovePhase.PLACEPHASE or phase == MovePhase.SPECIAL_PLACEPHASE:
		#if phase == MovePhase.PLACEPHASE:
			if selected_patch is not None:
				selected_patch.render_placement(self.primary_board_surface, selected_patch_col, selected_patch_row, (0, 255, 0))

		#render time track, patch scroll bar, primary board, and secondary board surfaces onto the window
		self.screen.blit(self.track_surface, (time_track_x, track_scroll_y))
		self.screen.blit(self.piece_surface, (piece_list_x, piece_scroll_y))
		self.screen.blit(self.primary_board_surface, (self.WIDTH/4.5, self.HEIGHT/8))
		self.screen.blit(self.secondary_board_surface, (self.WIDTH/30, self.HEIGHT/6))

		#rules text based on phase
		rules_text = f.render("Hover over the time track or patch list to scroll through them.", False, (0, 0, 0))
		rules_text_2 = f.render("^ This might only work with a track pad idk", False, (0, 0, 0))
		if phase == MovePhase.SPECIAL_PLACEPHASE or phase == MovePhase.PLACEPHASE:
			specific_text = f.render("ARROW KEYS to move piece, SPACE to rotate piece, SHIFT to place piece ", False, (255, 255, 255))
		else:
			specific_text = f.render("ARROW KEYS to highlight piece, ENTER to select piece", False, (255, 255, 255))

		self.screen.blit(rules_text, (50, 30))
		self.screen.blit(rules_text_2, (50, 50))
		self.screen.blit(specific_text, (50, 70))




		pygame.display.flip()