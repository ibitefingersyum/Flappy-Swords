#alex zheng

# inspired by the games flappy bird and dino swords

import pygame
import sys
import random


display_width = 600
display_height = 800
backgroundcolor = (70, 100, 225)
groundcolor = (50, 200, 50)

# ground
ground_height = 120

# ---------------------------------------------------------------------- pipes
pipe_width = 50
pipe_speed = 3
pipe_x = display_width
pipe_height = random.randint(50, display_height - 200)
pipe_part= 20
pipe_part_width = 10
pipe_part_height = 20
pipe_color = (0, 180, 0)
pipe_part_color = (0, 150, 0)
pipe_gap = 100


def draw_pipe(surface, x, height):
	# main top pipe
	pygame.draw.rect(surface, pipe_color, (x, 0, pipe_width, height))
	# lower part pipe
	part_y = height - pipe_part
	part_width = pipe_width + pipe_part_width
	part_x = x - (pipe_part_width // 2)
	pygame.draw.rect(surface, pipe_part_color, (part_x, part_y, part_width, pipe_part_height))
	# makes it so bottom pipe don't draw into the ground
	bottom_y = height + pipe_gap
	bottom_height = display_height - ground_height - bottom_y
	if bottom_height > 0:
		pygame.draw.rect(surface, pipe_color, (x, bottom_y, pipe_width, bottom_height))

# ---------------------------------------------------------------------- player



# ---------------------------------------------------------------------- foundation
def main():
	pygame.init()
	screen = pygame.display.set_mode((display_width, display_height))
	pygame.display.set_caption('flappyswords')

	clock = pygame.time.clock()
	global pipe_x

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.quit:
				running = False

		pipe_x -= pipe_speed

		pygame.draw.rect(screen, backgroundcolor, (0, 0, display_width, display_height))

		# delete pipe when leaves screen
		if pipe_x + pipe_width > 0:
			draw_pipe(screen, pipe_x, pipe_height)
		pygame.draw.rect(screen, groundcolor, (0, display_height - ground_height, display_width, ground_height))

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	main()
