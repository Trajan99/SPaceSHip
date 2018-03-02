

import pyglet
import utils
import random
from pyglet.window import key

pyglet.resource.path.append('./images')
pyglet.resource.reindex()

item_list = ['life']
item_image_files = {'life' : 'ship1_mini.png'}
item_freq = {'life' : 4000}
item_max = {'life' : 1}
lose_on_reset = []
item_images = {}

give_life = ['life']

for an_item in item_list:
	item_images[an_item] = pyglet.resource.image(item_image_files[an_item])
	utils.center_anchor(item_images[an_item])

class Item(pyglet.sprite.Sprite, key.KeyStateHandler):
	def __init__(self, item_type, x=0, y=0, ship=None, batch=None, timer=20):
		super(Item, self).__init__(item_images[item_type], x, y, batch=batch)

		self.dx = 0
		self.dy = 0
		self.timer = timer #how long it lasts after spawn
		self.ship = ship
		self.image = item_images[item_type]
		self.radius = max(self.image.height, self.image.width) / 2
		self.location = self.ship.planet
		self.location.items.append(self)
		self.type = item_type
		self.on_ship = False

		self.x = random.random() * self.ship.window_width
		self.y = random.random() * self.ship.window_height

		my_dist, my_ang = utils.dist_vec_to(self, self.ship)

		while my_dist < self.radius * 1.25:
			self.x = random.random() * self.ship.window_width
			self.y = random.random() * self.ship.window_height

			my_dist, my_ang = utils.dist_vec_to(self, self.ship)


	def update(self, dt):
		temp_dist, temp_ang = utils.dist_vec_to(self, self.ship)
		if temp_dist <  self.radius and self.on_ship == False:
			self.location.items.remove(self)
			self.ship.items.append(self)
			self.on_ship = True
			return
			
		self.timer -= dt

		if self.timer <= 0:
			self.location.items.remove(self)



