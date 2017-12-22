import pyglet
import utils
import math
from pyglet.window import key

pyglet.resource.path.append('./images')
pyglet.resource.reindex()
monster_image = pyglet.resource.image('monster1.png')
utils.center_anchor(monster_image)

class Monster(pyglet.sprite.Sprite):
	def __init__(self, x=0, y=0, dx=0, dy=0, batch=None):
		super(Monster, self).__init__(monster_image, x, y, batch=batch)
		self.x = x
		self.y = y
		self.radius = self.image.width / 2