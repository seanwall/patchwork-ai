from model.TrackTile import TrackTile

class TimeTrack():

	def __init__(self):
		self.track = []
		#initializing time track
		for idx in range(5):
			self.track.append(TrackTile.BLANK)
		for section in range(8):
			for idx in range(6):
				if idx == 0:
					self.track.append(TrackTile.INCOME)
				else:
					if section > 1 and section != 5:
						if idx == 3:
							self.track.append(TrackTile.PATCH)
						else:
							self.track.append(TrackTile.BLANK)
					else:
						self.track.append(TrackTile.BLANK)
		self.track.append(TrackTile.END)

	def removePatch(self, index):
		self.track[index] = TrackTile.BLANK

	def trackToString(self):
		trackString = ""
		for tile in self.track:
			if(tile == TrackTile.BLANK):
				trackString += "0"
			elif(tile == TrackTile.INCOME):
				trackString += "$"
			elif(tile == TrackTile.PATCH):
				trackString += "P"
			elif(tile == TrackTile.END):
				trackString += "E"
		return trackString



