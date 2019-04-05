from patchwork.model.QuiltBoard import QuiltBoard
from patchwork.model.TrackTile import TrackTile

import pygame

class Player():

	def __init__(self, player_num):
		self.buttons = 5
		self.position = 0 #this is a bad name
		self.player_num = player_num
		self.quilt = QuiltBoard()

		if self.player_num == 1:
			self.on_top = True
		else:
			self.on_top = False

	#returns false if the player did not pass a 1x1 patch tile, true if they did
	#boolean used so controller can initiate a patch placement for the player based
	#on the boolean
	#Also does all checking for passing income generation tiles and patch tiles

	#TODO might want to pass controller here so can dynamic dispatch back to player
	#placement if patch tile is landed on?

	def move(self, distance, time_track, other_player):
		#check if player is entering final tile on this move and cap distance accordingly
		if(self.position + distance >= len(time_track.track)):
			distance = (len(time_track.track) - 1) - self.position 


		#if the other_player was beneath this player before the move, update that player's
		#'on_top' value to true now that they are no longer covered
		if other_player.position == self.position:
			other_player.update_order(True)

		passed_patch = False

		#check if the player passes an income or 1x1 patch tile
		for tile in range(distance):
			#dont want 0 indexed
			tile += 1
			#update current player button count if it ever passes an income tile
			if time_track.track[tile + self.position] == TrackTile.INCOME or time_track.track[tile + self.position] == TrackTile.END:
				self.buttons += self.quilt.button_gen

			#update passed_patch value and remove the tile from the time_track 
			if time_track.track[tile + self.position] == TrackTile.PATCH:
				passed_patch = True
				time_track.removePatch(tile + self.position)

		if(self.position + distance >= len(time_track.track)):
			self.position = len(time_track) - 1
		else:
			self.position = self.position + distance

		#if this player lands on the other player, update on_top values
		if other_player.position == self.position:
			other_player.update_order(False)
			self.on_top = True

		return passed_patch

	#TODO: algorithm to check if the patch will fit on the board anywhere
	def can_buy(self, patch):
		return patch.cost <= self.buttons


	#returns value of move to see if a 1x1 patch was passed
	def buy_patch(self, patch, time_track, other_player):
		if patch.cost > self.buttons:
			#raise Exception("Not enough buttons")
			return None
		else:
			self.buttons -= patch.cost
			return self.move(patch.time_cost, time_track, other_player)

	def place_patch(self, patch, row, col):
		if not self.quilt.valid_placement(patch, row, col):
			return None
		else:
			self.quilt.place_patch(patch, row, col)

	def can_place(self, patch, row, col):
		return self.quilt.valid_placement(patch, row, col)

	#jump to other player (move one past that player and gain the distance moved as income)
	#returns value of move to be used to check if patch placement is needed
	def jump(self, time_track, other_player):
		distance = other_player.position - self.position + 1

		#if other player is at end cap distance
		if other_player.position == len(time_track.track) - 1:
			distance -= 1

		self.buttons += distance

		return self.move(distance, time_track, other_player)

	def update_order(self, on_top):
		self.on_top = on_top

	def get_score(self):
		return self.buttons + self.quilt.calculate_board_coverage()

	#TODO: THIS IS BAD, NEED BETTER VIEW HANDLING
	def render_piece(self, surface, x, y):
		if self.player_num == 1:
			color = (0, 0, 255)
		else:
			color = (255, 0, 0)

		pygame.draw.circle(surface, color, (x, y), int(surface.get_width()/10))

	#render board when it is the focused board (current player)
	def render_board_primary(self, surface, x, y):
		self.quilt.render_primary(surface, x, y, self.buttons, self.player_num)

	#render board when it is the unfocused board (not the current player)
	def render_board_secondary(self, surface, x, y):
		self.quilt.render_secondary(surface, x, y, self.buttons)






