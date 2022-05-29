import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, KEYUP, K_SPACE
pygame.init()
pygame.display.set_caption("game")

WINDOW_SIZE = (600, 400)
FPS = 60

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))

doux_image = pygame.image.load("assets/sprites/doux.png")
bg_image = pygame.transform.scale(pygame.image.load("assets/sprites/bg.png"), WINDOW_SIZE)

def load_map(file):
	map_file = open(file, 'r')
	data = map_file.read()
	map_file.close()
	data = data.split('\n')
	map = []
	for row in data:
		map.append(list(row))
	return map

map = load_map("assets/sprites/map.txt")

moving_right = False
moving_left = False
vertical_momentum = 0
air_time = 0

doux_rect = pygame.Rect(100, 100, *doux_image.get_size()) 
dirt_image = pygame.image.load("assets/sprites/dirt.png")
grass_image = pygame.image.load("assets/sprites/grass.png")

def collision_test(rect, tiles):
	return [tile for tile in tiles if rect.colliderect(tile)]

def move(rect, movement, tiles):
	collision_types = {'top': False, 'right': False, 'bottom': False, 'left': False}
	rect.x += movement[0]
	hit_list = collision_test(rect, tiles)
	for tile in hit_list:
		if movement[0] > 0:
			rect.right = tile.left
			collision_types['right'] = True
		elif movement[0] < 0:
			rect.left = tile.right
			collision_types['left'] = True
	
	rect.y += movement[1]
	hit_list = collision_test(rect, tiles)
	for tile in hit_list:
		if movement[1] > 0:
			rect.bottom = tile.top
			collision_types['bottom'] = True
		elif movement[1] < 0:
			rect.top = tile.bottom
			collision_types['top'] = True
		
	return rect, collision_types

while True:

	display.blit(bg_image, (0, 0))
	
	tile_rects = []

	for y, row in enumerate(map):
		for x, col in enumerate(row):
			if col == '1':
				display.blit(dirt_image, (x * dirt_image.get_width(), y * dirt_image.get_height()))
			if col == '2':
				display.blit(grass_image, (x * dirt_image.get_width(), y * dirt_image.get_height()))
			if col != '0':
				tile_rects.append(pygame.Rect(x*16, y*16, 16, 16))
	

	doux_movement = [0, 0]
	if moving_left == True:
		doux_movement[0] -= 2
	if moving_right == True:
		doux_movement[0] += 2
	doux_movement[1] += vertical_momentum
	vertical_momentum += 0.2
	if vertical_momentum > 3: vertical_momentum = 3
	
	doux_rect, collision = move(doux_rect, doux_movement, tile_rects)

	if collision['bottom']:
		vertical_momentum = 0
		air_time = 0
	if collision['top']:
		vertical_momentum = 0
		air_time = 0
	else: air_time += 1

	display.blit(
		pygame.transform.flip(doux_image, moving_left, False), 
		(doux_rect.x, doux_rect.y)
	)
	pygame.draw.rect(display, (255, 0, 0), doux_rect, 1)

	for event in pygame.event.get(): 
		if event.type == QUIT: 
			pygame.quit() 
			sys.exit() 
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				moving_right = True
			if event.key == K_LEFT:
				moving_left = True
			if event.key == K_SPACE:
				if air_time < 6:
					vertical_momentum = -5
		if event.type == KEYUP:
			if event.key == K_RIGHT:
				moving_right = False
			if event.key == K_LEFT:
				moving_left = False

	screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
	pygame.display.update()
	clock.tick(60)

