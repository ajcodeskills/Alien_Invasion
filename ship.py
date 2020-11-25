import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

	def __init__(self, ai_settings, screen):
		"""initialize the screen with ship"""
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		#set the ship image on screen
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		#start each new ship at buttom center of the screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		#set for decimal values
		self.center = float(self.rect.centerx)

		#Moving flag
		self.moving_right = False
		self.moving_left = False

	def blitme(self):

		#draw the ship at its current location
		self.screen.blit(self.image, self.rect)

	def update(self):

		'''update the ship position according to the movement flag'''
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor

		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor

		self.rect.centerx = self.center	
	
	def center_ship(self):
		#adjusting ship at center
		self.center = self.screen_rect.centerx



	



	   	

 	
		