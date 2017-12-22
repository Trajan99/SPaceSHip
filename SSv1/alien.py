import pyglet
import utils
import random
import math
import bullet

pyglet.resource.path.append('./images')
pyglet.resource.reindex()

alien_image = pyglet.resource.image('monster1.png')
utils.center_anchor(alien_image)
bullet_image = pyglet.resource.image('bullet3.png')
utils.center_anchor(bullet_image)

class Alien(pyglet.sprite.Sprite):
	def __init__(self, image, window_width, window_height, ship, planet, x=0, y=0, dx=0, dy=0, batch=None, brains=0.5, bullet_freq=2):
		super(Alien, self).__init__(alien_image, x, y, batch=batch)

		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.radius = self.image.width / 2
		self.life_timer = 200000.0 #REDACTED
		self.accel_spd = 50.0
		self.max_spd = 100.0
		self.alive = True
		self.window_width = window_width
		self.window_height = window_height
		self.ship = ship
		self.brains = brains
		self.bullets = []
		self.bullets_batch = pyglet.graphics.Batch()
		self.shot_freq = bullet_freq
		self.planet = planet

	def reset(self):
		self.alive = True
		self.life_timer = 200000.0 #REDACTED
		
		ship_distance = 0
		while ship_distance < self.radius * 8:
			self.x = random.random() * self.window_width
			self.y = random.random() * self.window_height
			self.dx = random.random() * self.max_spd / 4
			self.dy = random.random() * self.max_spd / 4

			ship_distance, temp = utils.dist_vec_to(self, self.ship)


	def update(self,dt):
		if not self.alive:
			self.life_timer -= dt
			if self.life_timer > 0:
				return
			else:
				self.reset()

		if random.random() < 0.2:
			dist, ang = utils.dist_vec_to(self, self.ship)
			accel_dir = self.brains * (ang - math.pi) + (1 - self.brains) * random.random() * math.pi * 2
			while accel_dir > math.pi * 2:
				accel_dir -= math.pi * 2
			while accel_dir < 0:
				accel_dir += math.pi * 2


			accel_amt = random.random() * self.accel_spd
			accel_x, accel_y = utils.vec_to_xy(accel_amt, accel_dir)
			self.dx += accel_x
			self.dy += accel_y

		speed_toto = (self.dx ** 2 + self.dy ** 2) ** 0.5
		if speed_toto > self.max_spd:
			self.dx = self.dx * self.max_spd / speed_toto 
			self.dy = self.dy * self.max_spd / speed_toto

		self.x += self.dx * dt
		self.y += self.dy * dt

		self.x = utils.wrap(self.x, self.window_width)
		self.y = utils.wrap(self.y, self.window_height)

		player_dist, player_angle = utils.dist_vec_to(self, self.ship)
		if player_dist < (self.ship.radius + self.radius) * 0.75:
			self.reset()
			self.alive = False
			self.ship.planet.aliens.remove(self)
			self.ship.reset()
			self.ship.alive = False

		planet_dist, temp = utils.dist_vec_to(self, self.ship.planet)

		if planet_dist < self.ship.planet.radius:
			self.reset()
			self.alive = False

		if random.random() < 1 / (self.shot_freq / dt) and player_dist > 150:
			myrand = random.random() * 2 * math.pi
			my_dx, my_dy = utils.vec_to_xy(self.max_spd, myrand)

			self.bullets.append(
				bullet.Bullet(self.window_width, self.window_height, self.x, self.y, my_dx, 
					my_dy, ship=self, batch=self.bullets_batch, image=bullet_image, timer=2)
				)
			






