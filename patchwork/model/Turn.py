class BuyTurn():
	def __init__(self, patch_idx, patch_id):
		self.patch_idx = patch_idx
		self.patch_id = patch_id

	def run(self, model):
		return model.buy_patch(self.patch_idx)

class JumpTurn():
	def run(self, model):
		return model.jump()