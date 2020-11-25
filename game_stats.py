
class Game_stats:

	'''initialize all game statistics'''
	def __init__(self, ai_settings):

		#initialize the game statistics
		self.ai_settings = ai_settings
		self.reset_stats()
		self.game_active = False
		self.high_score = 0
		self.high_text = "High Score"
		self.score_text = "Score"
		self.level_text = "Level"


	def reset_stats(self):
		"""initialize statistics that can change during game runtime"""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1


	

	
