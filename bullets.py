import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

	'''class for firing bullets'''
	def __init__(self, ai_settings, screen, ship):

		'''managing the bullets screen'''
		super(Bullet, self).__init__()
		self.screen = screen

		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		#storing decimal values
		self.y = float(self.rect.y)

		#color and speed of bullet
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor

	def update(self):
		'''move the bullet up the screen'''
		#update the decimal position of bullet
		self.y -= self.speed_factor

		#update the position
		self.rect.y = self.y

	def draw_bullet(self):
		'''draw the bullet to the screen'''
		pygame.draw.rect(self.screen, self.color, self.rect)	

	

	



