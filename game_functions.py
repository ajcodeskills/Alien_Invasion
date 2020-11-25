import sys
import pygame
from bullets import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb):

	#cheching any mouse event while pressing the key
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				#click position
				mouse_x, mouse_y = pygame.mouse.get_pos()
				check_play_botton(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb)


			elif event.type == pygame.KEYDOWN:
				check_keydown_events(event, ai_settings, screen, ship, bullets)

			elif event.type == pygame.KEYUP:
				check_keyup_events(ship, event)

def check_play_botton(ai_settings, screen, stats, play_button,ship, aliens, bullets, mouse_x, mouse_y, sb):

	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)

		stats.reset_stats()
		stats.game_active = True

		#reseting the score screen
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()


		#empty the bullets and aliens fleet
		aliens.empty()
		bullets.empty()

		#create new fleet
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()




def check_keydown_events(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:
					#move the ship to right
		ship.moving_right = True

	elif event.key == pygame.K_LEFT:
		ship.moving_left = True

	elif event.key == pygame.K_SPACE:
		
		fire_bullet(ai_settings, screen, ship, bullets)

def check_keyup_events(ship,event):
	if event.key == pygame.K_RIGHT:
					#move the ship to right
		ship.moving_right = False

	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

	#exit the game
	elif event.key ==pygame.K_q:
		sys.exit()





def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb):
	#fill the after each pass of for loop	
	screen.fill(ai_settings.bg_color)

	#redraw all bullets that are behind the ship
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	#draw a ship
	ship.blitme()	

	#draw aliens on the screen
	aliens.draw(screen)
	sb.show_score()


	if not stats.game_active:
		play_button.draw_button()

	#make the most recent screen 
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, ship, aliens, bullets, sb):
	#update bullet position
	bullets.update()
	# Get rid of bullets that have disappeared.
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
		 	bullets.remove(bullet)  

	#check foe bullets collissions
	check_bullet_alien_collision(ai_settings, screen, stats, ship, aliens, bullets, sb)

def fire_bullet(ai_settings, screen, ship, bullets):
	'''fire bullets if the limit not gets reached'''
	if len(bullets) < ai_settings.bullets_allowed:
		#create new bullet
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
	'''creating a fleet of aliens'''

	#finding the available space for aliens
	#finding the number of aliens that can be placed
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	number_aliens_x = get_number_alien(ai_settings,alien_width)
	number_rows= get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):

			#creating a new alien
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_alien(ai_settings, alien_width):

	available_space_x = ai_settings.screen_width -(2 * alien_width)
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):

	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + (2 * alien_width * alien_number)
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):

	#determine the number of rows
	available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
	number_aliens_y = int(available_space_y / (2 * alien_height))
	return number_aliens_y

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
	#update the position of aliens
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	#look for alien ship collision
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
	#look for aliens hitting the bottom of the screen
	check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def check_fleet_edges(ai_settings, aliens):
	'''check the appropiate direction'''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):

	'''change the direction'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	
	ai_settings.fleet_direction *= -1	

def check_bullet_alien_collision(ai_settings, screen, stats, ship, aliens, bullets, sb):
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	#update the point whenever a bullet collide with aliens or hits the alien
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)	


	if len(aliens) == 0:
		bullets.empty()

		#speeding up the speed
		ai_settings.increase_speed()

		#updating the level
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
	if stats.ships_left > 0:
		'''Decrement the ship_left'''
		stats.ships_left -= 1
		sb.prep_ships()


		#Empty the aliens and bullets
		aliens.empty()
		bullets.empty()

		#create new fleet on the screen
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		#pause
		sleep(0.5)

	else:
			stats.game_active = False
			pygame.mouse.set_visible(True)

def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
	'''check if aliens hits the bottom of the screen'''
	for alien in aliens.sprites():
		screen_rect = screen.get_rect()
		if alien.rect.bottom >= screen_rect.bottom:
			#treat aliens as if ship hit
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
			break
def check_high_score(stats, sb):

	"""checking the high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score




 


