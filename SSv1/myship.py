import pyglet
from pyglet.window import key
import ship
import math
import utils
import bullet
import monster
import random
import alien
import item

pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent',) 

my_attrs = ['x', 'y', 'dx', 'dy', 'rotation', 'thrust', 
					'rot_spd', 'rot_left', 'rot_right', 'engines']

player_name	= ""

while len(player_name) == 0:
	player_name = raw_input("Player Name: ")
	player_name = player_name	[:12]

#Things that change at levels
max_aliens = [3 + i for i in range(100)]
alien_brains = [1 - 0.85 ** n for n in range(100)]
bullet_freq = [2 + 2 * (0.5 ** n) for n in range(100)]
kill_advance = [3 + 1 * i for i in range(100)]
#kill_advance = [2000 + 1 * i for i in range(100)]

window = pyglet.window.Window(fullscreen=True)
pyglet.resource.path.append('./images')
pyglet.resource.path.append('./audio')
pyglet.resource.reindex()


planet_image = pyglet.resource.image('earth.jpg')
utils.center_anchor(planet_image)
ship_image = pyglet.resource.image('ship1_pur.png')
utils.center_anchor(ship_image)
ship_image_on = pyglet.resource.image('ship_on_pur.png')
utils.center_anchor(ship_image_on)
alien_image = pyglet.resource.image('monster1.png')
utils.center_anchor(alien_image)
eliot_image = pyglet.resource.image('bullet_eliot.jpg')
utils.center_anchor(eliot_image)
#bullet_sound = pyglet.resource.media('bullet_long.wav', streaming=False)
high_score_file = 'high_score.csv'


class Planet(pyglet.sprite.Sprite, key.KeyStateHandler):
	def __init__(self, image, x=0, y=0, batch=None):
		super(Planet, self).__init__(
			image, x, y, batch=batch)
		self.x = x
		self.y = y
		self.mass = 500000
		self.radius = (self.image.height + self.image.width) / 4
		self.score = 0
		self.aliens = []
		self.level = 0
		self.no_aliens = -1.0
		self.init_life = 30
		self.max_life = 3
		self.total_kills = 0
		self.level_kills = 0
		self.items = []
		self.new_level()
		self.new_level_time = 0.0
		self.lyla_mode = False
		self.cheat_mode = False
		self.game_state	= 1
		self.pause = False
		self.eliot_mode = False
		self.new_bullet = False
		

	def new_level(self):
		self.max_aliens = max_aliens[self.level]
		self.alien_brains = alien_brains[self.level]
		self.bullet_freq = bullet_freq[self.level]
		
		self.no_aliens = -1.0
		self.new_level_time = 5.0
		self.level_kills = 0
		self.eliot_mode = False
		
		if self.level > 0:
			for a_bullet in ship.bullets:
				ship.bullets.remove(a_bullet)
			for an_alien in self.aliens:
				for a_bullet in an_alien.bullets:
					an_alien.bullets.remove(a_bullet)
				self.aliens.remove(an_alien)
			ship.reset()
			ship.life_timer = 0.0
			for a_bullet in ship.bullets:
				ship.bullets.remove(a_bullet)

		for an_item in self.items:
			self.items.remove(an_item)


	def update(self, dt):
		if not self.pause:
			force, angle, distance = self.force_on(ship)
			force_x = force * math.cos(angle) * dt
			force_y = force * math.sin(angle) * dt
			ship.dx += force_x
			ship.dy += force_y

			if distance < self.radius + ship.radius:
				ship.reset()
				ship.alive = False
				return

			self.score = ship.score
			score.text = "Score: %d" % self.score
			game_over.text = "Game Over! \n" +  "Score: %d" % ship.score
			game_over.text += " \n" + "Total Kills: %d" % planet.total_kills
			game_over.text += "\n" + "Space to continue"

			if len([an_alien for an_alien in self.aliens if an_alien.alive]) == 0:
				if self.no_aliens == -1.0:
					self.no_aliens = 1.0
				else:
					self.no_aliens -= dt
					if self.no_aliens < 0:
						print "Auto-spawn"
						self.spawn_alien()
						self.no_aliens = -1.0

			if len([an_alien for an_alien in self.aliens if an_alien.alive]) < self.max_aliens:
				if random.random() < 1 / (dt * 2000):
					self.spawn_alien()
					print "Random spawn"

			if self[key.R]:
				self.max_life = self.init_life
				self.cheat_mode = True

			if self[key._3]:
				self.lyla_mode = True
				self.cheat_mode = True
			if self[key._4]:
				self.lyla_mode = False

			if self.level_kills >= kill_advance[self.level] and not self.lyla_mode:
				self.level += 1
				print "New Level: " + str(self.level)
				self.new_level()

			if self.new_level_time > 0:
				self.new_level_time -= dt
				temp = math.ceil(self.new_level_time)
				level_screen.text = "Level: %d" % (self.level + 1)
				level_screen.text += " \n"
				level_screen.text += "Starts in: %d" % temp
				if self[key.ENTER]:
					self.new_level_time = 0

			if planet.max_life <= 0 and planet.game_state == 1:
				planet.game_state = 2

			if planet.game_state == 1:
				for an_item in item.item_list:
					temp_num = sum([1 for the_item in planet.items if the_item.type == an_item])
					if temp_num < item.item_max[an_item]:
						temp = random.random()
						if temp < 1 / (dt * item.item_freq[an_item]):
							new_item = item.Item(an_item, ship=ship)
							#print "new item, random: " + str(temp)
						#else:
							#print "no item, random: " +  str(temp)



	def force_on(self, target):
		if not self.lyla_mode:
			G = 0.5
		else:
			G = 0.0000001
		distance, angle = utils.dist_vec_to(self, target)
		return ((G * self.mass) / (distance ** 2), angle, distance)

	def spawn_alien(self):
		new_alien = alien.Alien(alien_image, window.width, window.height, ship, planet, brains=self.alien_brains, 
			bullet_freq=self.bullet_freq)
		new_alien.reset()
		self.aliens.append(new_alien)

class ShowLife(pyglet.sprite.Sprite):
	def __init__(self, image, x=0, y=0, batch=None):
		super(ShowLife, self).__init__(
			image, x, y, batch=batch)
		self.x = x
		self.y = y

def calc_highscore():
	#read in high scores
	#print "Calc HighScore"
	
	MAX_SHOW = 10
	high_score_names = []
	high_score_scores = []
	high_scores = utils.read_high_scores(high_score_file)
	#print "1" 
	#print high_scores.items()
	if high_scores == False or len(high_scores) == 0:
		hs_loc = 0
		#is_high_score = True

	else:
		score_list = high_scores.keys()
		while score_list:
			my_key = max(score_list)
			for an_item in range(len(high_scores[my_key])):
				high_score_names.append(high_scores[my_key][an_item])
				high_score_scores.append(my_key)
			score_list.remove(my_key)
		
		if planet.cheat_mode:
			hs_loc = 20000000

		elif planet.score < min(high_score_scores):
			hs_loc = len(high_score_scores) + 1
			
		else:
			hs_loc	= min([j for j in range(len(high_score_scores)) if high_score_scores[j] <= planet.score])

	NUM_SHOW = min(10, len(high_score_names))

	is_high_score = False

	#print "2", hs_loc, NUM_SHOW	
	#add notated score to list and sort
	if hs_loc <= max(MAX_SHOW,NUM_SHOW):
		#is_high_score = True
		#NUM_SHOW = min(MAX_SHOW, NUM_SHOW + 1)
		names_out = high_score_names[:hs_loc]
		scores_out = high_score_scores[:hs_loc]
		names_out.append("**YOU**")
		scores_out.append(planet.score)
		NUM_SHOW += 1
		for i in range(hs_loc, min(NUM_SHOW, len(high_score_names))):
			names_out.append(high_score_names[i])
			scores_out.append(high_score_scores[i])

	else:
		names_out = high_score_names[:NUM_SHOW]
		scores_out = high_score_scores[:NUM_SHOW]

	#print "3", len(names_out), NUM_SHOW	

	#amend text; add you didn't get in!
	for i in range(NUM_SHOW):
		my_str = names_out[i] + " " * (15 - len(names_out[i])) + str(scores_out[i])
		high_score_screen.text += names_out[i] + "\n"
		high_score_screen_2.text += str(scores_out[i]) + "\n"
		print my_str
		if names_out[i] == "**YOU**":
			is_high_score = True
	
	if not is_high_score:
		if planet.cheat_mode: 
			high_score_screen.text += "No high scores in Cheat Mode!"
		else:
			high_score_screen.text += "You didn't get a high score!"
	else:
		high_score_screen.text += "Good work!"

	#print "4"

	#write new line to file
	utils.write_high_score(high_score_file, player_name, planet.score)


center_x = int(window.width/2)
center_y = int(window.height/2)
planet = Planet(planet_image, center_x, center_y, None)

ship_lives = []
for i in range(max(0,planet.init_life)):
	my_y = ship_image.height / 2 + 10
	my_x = window.width - 20 - (i + 1/2) * ship_image.width
	ship_lives.append(ShowLife(ship_image, my_x, my_y))

ship = ship.Ship(ship_image, window.height, window.width, x=center_x+500, y=center_y, dx=0, dy=0, rotv=-90, planet=planet)

planet.spawn_alien()

score = pyglet.text.Label('Speed: 0',
	font_name = 'Arial',
	font_size = 36, 
	x = 10,
	y = 10,
	anchor_x = 'left', anchor_y = 'bottom')
score.color = (255,255,255,255)

lyla_status = pyglet.text.Label('Speed: 0',
	font_name = 'Arial',
	font_size = 36, 
	x = window.width / 2,
	y = 10,
	anchor_x = 'center', anchor_y = 'bottom')
lyla_status.color = (255,255,255,255)
lyla_status.text = "LYLA MODE"

pause_status = pyglet.text.Label('Speed: 0',
	font_name = 'Arial',
	font_size = 72, 
	x = window.width / 2,
	y = window.height / 2,
	anchor_x = 'center', anchor_y = 'bottom')
pause_status.color = (0,0,255,255)
pause_status.text = "PAUSED"

game_over = pyglet.text.Label('Speed: 0',
	font_name = 'Arial',
	font_size = 48,
	x = window.width / 2,
	y = window.height / 2, 
	anchor_x = 'center', anchor_y = 'center',
	multiline=True,
	width=1000)
game_over.color = (255, 255, 255, 255)

level_screen = pyglet.text.Label('Speed: 0',
	font_name = 'Arial', 
	font_size = 72,
	x = window.width / 2,
	y = window.height / 2, 
	anchor_x = 'center', anchor_y = 'center',
	multiline=True,
	width=500)
level_screen.color = (255, 255, 255, 255)

high_score_screen = pyglet.text.Label('Speed: 0',
	font_name = 'Arial', 
	font_size = 18,
	x = window.width / 2,
	y = window.height / 2, 
	anchor_x = 'center', anchor_y = 'center',
	multiline=True,
	width=500, )
high_score_screen.color = (255, 255, 255, 255)
high_score_screen.text = "HIGH SCORES: \n"

high_score_screen_2 = pyglet.text.Label('Speed: 0',
	font_name = 'Arial', 
	font_size = 18,
	x = window.width / 2 + 200,
	y = window.height / 2, 
	anchor_x = 'center', anchor_y = 'center',
	multiline=True,
	width=500, )
high_score_screen_2.color = (255, 255, 255, 255)
high_score_screen_2.text = "\n"

@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.P:
		if planet.pause:
			planet.pause = False
			print "unpause"
		else:
			planet.pause = True
			print "pause"
	if symbol == key.SPACE and planet.game_state == 2:
		#print "Into State 3"
		calc_highscore()
		planet.game_state = 3
	if symbol == key.E:
		planet.eliot_mode = True

@window.event
def on_draw():
	
	if planet.game_state == 1:
		if planet.new_level_time > 0:
			window.clear()
			level_screen.draw()

		else:
			window.clear()
			planet.draw()
			ship.bullets_batch.draw()
			if ship.alive:
				ship.draw()
			for an_alien in planet.aliens:
				if an_alien.alive == True:
					an_alien.draw()
				an_alien.bullets_batch.draw()
			score.draw()
			for i in range(planet.max_life-1):
				ship_lives[i].draw()
			if planet.lyla_mode:
				lyla_status.draw()
			for an_item in planet.items:
				an_item.draw()
			if planet.new_bullet:
				#bullet_sound.play()
				planet.new_bullet = False

		if planet.pause:
			pause_status.draw()

	elif planet.game_state == 2:
		window.clear()
		game_over.draw()
	elif planet.game_state == 3:
		window.clear()
		high_score_screen.draw()
		high_score_screen_2.draw()
	else:
		window.clear()
		pyglet.app.exit()


def update(dt):
	
	planet.update(dt)

	if not planet.pause:
		ship.update(dt)
		for bullet in ship.bullets:
			bullet.update(dt)
		for an_alien in planet.aliens:
			an_alien.update(dt)
			for bullet in an_alien.bullets:
				bullet.update(dt)
		for an_item in planet.items:
			an_item.update(dt)
		for an_item in ship.items:
			an_item.update(dt)

window.push_handlers(ship)
window.push_handlers(planet)
window.push_handlers(bullet)

pyglet.clock.schedule_interval(update, 1/25.0)

pyglet.app.run()



