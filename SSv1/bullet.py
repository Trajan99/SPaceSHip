import pyglet
import utils
from pyglet.window import key

pyglet.resource.path.append('./images')
pyglet.resource.reindex()
#bullet_image = pyglet.resource.image('bullet2.png')
bullet_image = pyglet.resource.image('bullet2.png')
utils.center_anchor(bullet_image)
eliot_image = pyglet.resource.image('bullet_eliot.jpg')
utils.center_anchor(eliot_image)

class Bullet(pyglet.sprite.Sprite, key.KeyStateHandler):
	def __init__(self, window_width, window_height, x=0, y=0, dx=0, dy=0, ship=None, batch=None, image=bullet_image, timer=5):
		super(Bullet, self).__init__(image, x, y, batch=batch)
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.radius = self.image.width / 2
		self.timer = timer #change to disappear if goes off screen
		self.window_width = window_width
		self.window_height = window_height
		self.ship = ship
		self.rotation = self.ship.rotation
		self.ship.planet.new_bullet = True

	def update(self, dt):
		self.x += self.dx * dt
		self.y += self.dy * dt
		self.x = utils.wrap(self.x, self.window_width)
		self.y = utils.wrap(self.y, self.window_height)
		self.radius = self.image.width / 2

		self.timer -= dt
		distance, angle = utils.dist_vec_to(self, self.ship.planet)
		if distance <= self.ship.planet.radius or self.timer <= 0:
			self.ship.bullets.remove(self)

		if type(self.ship).__name__ == "Ship":
			if self.ship.planet.eliot_mode:
				self.image = eliot_image
				self.rotation = 0

			for an_alien in self.ship.planet.aliens:
				dist, angle = utils.dist_vec_to(self, an_alien)
				if dist < an_alien.radius:
					an_alien.reset()
					an_alien.alive = False
					self.ship.planet.aliens.remove(an_alien)
					print len(self.ship.planet.aliens)
					if self in self.ship.bullets:
						self.ship.bullets.remove(self)
					self.ship.score += 50
					self.ship.planet.level_kills += 1
					self.ship.planet.total_kills += 1
					return

		if type(self.ship).__name__ == "Alien":
			dist, angle = utils.dist_vec_to(self, self.ship.ship)
			if dist < (self.radius + self.ship.ship.radius) * 0.75:
				self.ship.ship.reset()
				self.ship.ship.alive = False
				self.ship.bullets.remove(self)
			for an_alien in self.ship.planet.aliens:
				dist, angle = utils.dist_vec_to(self, an_alien)
				if dist < an_alien.radius and self not in an_alien.bullets:
					an_alien.reset()
					an_alien.alive = False
					self.ship.planet.aliens.remove(an_alien)
					if self in self.ship.bullets:
							self.ship.bullets.remove(self)





