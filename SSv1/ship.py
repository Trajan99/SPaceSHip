import pyglet
import utils
import math
import bullet
from pyglet.window import key

pyglet.resource.path.append('./images')
pyglet.resource.reindex()
ship_image = pyglet.resource.image('ship1_pur.png')
utils.center_anchor(ship_image)
ship_image_on = pyglet.resource.image('ship_on_pur.png')
utils.center_anchor(ship_image_on)
lyla_image = pyglet.resource.image('lyla.jpg')
utils.center_anchor(lyla_image)

class Ship(pyglet.sprite.Sprite, 
					key.KeyStateHandler):
	def __init__(self, image, window_height, window_width, x=0, y=0, dx=0, dy=0, rotv=0, planet=None, batch=None):
		super(Ship, self).__init__(
			image, x, y, batch=batch)
		self.x=x
		self.y=y
		self.dx=dx
		self.dy=dy
		self.rotation = rotv
		self.thrust = 50.0
		self.rot_spd = 75.0
		self.window_width = window_width
		self.window_height = window_height
		self.radius = (self.image.height + self.image.width) / 4
		self.alive = True
		self.life_timer = 0.0
		self.init_x = x
		self.init_y = y
		self.init_rot = rotv
		self.shot_timer = 0.25
		self.reload_timer = 0
		self.bullets = []
		self.planet = planet
		self.bullets_batch = pyglet.graphics.Batch()
		self.max_spd = 250.0
		self.score = 0


	def update(self, dt):

		if self.planet.new_level_time > 0:
			return

		self.image = ship_image
		#if self.rot_left:
		if self[key.LEFT]:
			self.rotation -= self.rot_spd * dt
		if self[key.RIGHT]:
			self.rotation += self.rot_spd * dt
		self.rotation = utils.wrap(self.rotation, 360.)

		rotation_x = math.sin(
				utils.to_radians(self.rotation))
		rotation_y = math.cos(
				utils.to_radians(self.rotation))

		if self[key.UP]:
			self.image = ship_image_on
			self.dx += self.thrust * rotation_x * dt
			self.dy += self.thrust * rotation_y * dt

		if self[key.L]:
			self.image = lyla_image
			for an_alien in self.planet.aliens:
				an_alien.reset()
				an_alien.alive = False
			for a_bullet in self.bullets:
				self.bullets.remove(a_bullet)
			self.planet.cheat_mode = True

		if self.reload_timer > 0:
			self.reload_timer -= dt
		elif self[key.SPACE] and self.alive:
			self.bullets.append(
				bullet.Bullet(self.window_width, self.window_height, self.x, self.y, rotation_x*self.thrust*4+self.dx, 
					rotation_y*self.thrust*4+self.dy, ship=self, batch=self.bullets_batch)
				)
			self.reload_timer = self.shot_timer

		speed_toto = (self.dx ** 2 + self.dy ** 2) ** 0.5
		if speed_toto > self.max_spd:
			self.dx = self.dx * self.max_spd / speed_toto 
			self.dy = self.dy * self.max_spd / speed_toto

		self.x += self.dx * dt
		self.y += self.dy * dt

		self.x = utils.wrap(self.x, self.window_width)
		self.y = utils.wrap(self.y, self.window_height)

		if not self.alive:
			print ("Dead! Respawn in %s" %
				self.life_timer)
			self.life_timer -= dt
			if self.life_timer > 0:
				return
			else:
				self.planet.max_life -= 1
				self.score -= 100
				self.reset()
				self.alive = True
					
	def reset(self):
		self.life_timer = 2.0
		self.x = self.init_x
		self.y = self.init_y
		self.dx = 0
		self.dy = 0
		self.rotation = self.init_rot



