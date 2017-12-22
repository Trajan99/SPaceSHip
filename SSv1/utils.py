import pyglet
import math
import os
import csv

HS_Fields = {'name' : 'Name',
				'score' : 'Score'}
field_order = ['name', 'score']

def center_anchor(img):
	img.anchor_x = img.width // 2
	img.anchor_y = img.height // 2

def wrap(value, width):
	if width == 0:
		return 0
	if value > width:
		value -= width
	if value < 0:
		value += width
	return value

def to_radians(degrees):
	return math.pi * degrees / 180.0

def dist_vec_to_old(me, target):
		dx = target.x - me.x
		dy = target.y - me.y
		sqr_distance = dx**2 + dy**2
		distance = sqr_distance ** 0.5

		angle = math.acos(float(dx) / max(distance, 0.0001))
		if dy < 0:
			angle = 2 * math.pi - angle
		return distance, angle

def vec_to_xy(distance, angle):
	x = distance * math.cos(angle)
	y = distance * math.sin(angle)
	return (x,y)

def make_vec((x1, y1), (x2, y2)):
	dx = x1-x2
	dy = y1-y2
	distance = (dx**2 + dy**2) ** 0.5
	if distance == 0:
		return (0,0)
	angle = math.acos(float(dx)/distance)
	if dy < 0:
		angle = 2*math.pi - angle
	return (distance, angle)

def dist_vec_to(source, target):
	return make_vec(
		(source.x, source.y), (target.x, target.y)
		)

def checkfile(filename):
	if os.access(filename, os.F_OK):
		return True
	else:
		return False

def read_high_scores(filename):
	
	if not checkfile(filename):
		print "File Not Found - 1"
		return False

	file = open(filename, 'r')
	high_scores = {}
	temp, temp = file.readline().split(",")
	while True:
		try:
			name, score = file.readline().split(",")
			if int(score) in high_scores.keys():
				high_scores[int(score)].append(name)
			else:
				high_scores[int(score)] = [name]
		except:
			break

	return high_scores

def write_high_score(filename, name, score):

    if os.access(filename, os.F_OK):
        file_mode = "ab"
    else:
        file_mode = "wb"

    csv_writer = csv.DictWriter(
        open(filename, file_mode),
        fieldnames=field_order,
        extrasaction="ignore")

    if file_mode == "wb":
        csv_writer.writerow(HS_Fields)

    my_score = {}
    my_score['name'] = name
    my_score['score'] = score
    csv_writer.writerow(my_score)



	





