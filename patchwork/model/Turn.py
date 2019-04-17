#Represents turns, constructed with all the info they need to execute the turn. Run method is given all objects that the turn will affect,
#right now just the model and state model
class BuyTurn():
	def __init__(self, patch_idx, patch, passes_patch, passes_econ, passes_player):
		self.patch_idx = patch_idx
		self.patch = patch
		self.passes_patch = passes_patch
		self.passes_econ = passes_econ
		self.passes_player = passes_player

	def run(self, model, state_model):
		if state_model is not None:
			state_model.passed_patch = self.passes_patch
			state_model.passed_econ = self.passes_econ
			#state_model.add_patch(self.patch_id)
		return model.buy_patch(self.patch_idx)

class JumpTurn():
	def __init__(self, passes_patch, passes_econ, passes_player):
		self.passes_patch = passes_patch
		self.passes_econ = passes_econ
		self.passes_player = True

	def run(self, model, state_model):
		if state_model is not None:
			state_model.passed_patch = self.passes_patch
			state_model.passed_econ = self.passes_econ
		return model.jump()