import pygame.font

class Button():

	def __init__(self, ai_settings, screen, msg):

		'''initialize the button attributes'''
		self.screen = screen
		self.screen_rect = screen.get_rect()

		#set the button properties
		self.width, self.height = 200, 5
		self.button_color = (192, 0, 192)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		#Build the rect of the button
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		#prepped the message only once
		self.prep_msg(msg)

	def prep_msg(self, msg):

		#rendering the image on the botton
		self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)

		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):

		'''draw the blank botton on the screen'''
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
	

	
