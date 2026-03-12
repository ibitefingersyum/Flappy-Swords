# Alex Zheng
# inspired by flappy bird and dino swords

import pygame
import sys
import random

# display
display_width = 600
display_height = 800
backgroundcolor = (70, 100, 225)
groundcolor = (54, 117, 77)

# ground
ground_height = 250

# pipes
pipe_width = 50
pipe_speed = 2
pipe_part = 20
pipe_part_height = 20
pipe_color = (0, 180, 0)
pipe_part_color = (0, 150, 0)
pipe_gap = 125

# pipe list
pipes = [
    [
        display_width,
        random.randint(50, display_height - ground_height - pipe_gap - 20),
        False,
    ]
]

# player
player_size = 20
player_x = 50
player_y = display_height // 3
player_velocity = 0
gravity = 0.2
jump_force = -4.5
player_color = (255, 0, 0)

# score
score = 0


def draw_pipe(surface, x, height):
    # top pipe
    top_height = max(0, height)
    pygame.draw.rect(surface, pipe_color, (x, 0, pipe_width, top_height))

    # top pipe part
    part_y = height - pipe_part
    part_x = x - pipe_part // 2
    if part_y + pipe_part_height > 0:
        part_y_clamped = max(0, part_y)
        part_height_visible = pipe_part_height - max(0, -part_y)
        if part_height_visible > 0:
            pygame.draw.rect(
                surface,
                pipe_part_color,
                (part_x, part_y_clamped, pipe_width + pipe_part, part_height_visible),
            )

    # bottom pipe
    bottom_y = height + pipe_gap
    bottom_y_clamped = max(bottom_y, 0)
    bottom_height = display_height - ground_height - bottom_y_clamped
    if bottom_height > 0:
        pygame.draw.rect(
            surface, pipe_color, (x, bottom_y_clamped, pipe_width, bottom_height)
        )

        # bottom pipe part
        bottom_part_y = bottom_y - pipe_part
        pygame.draw.rect(
            surface,
            pipe_part_color,
            (part_x, bottom_part_y, pipe_width + pipe_part, pipe_part_height),
        )


def check_collision(player_rect, pipes, ground_y):
    # ground
    if player_rect.bottom >= ground_y:
        return True

    # ceiling
    if player_rect.top <= 0:
        return True

    # pipes
    for pipe in pipes:
        # top pipe
        top_pipe_rect = pygame.Rect(pipe[0], 0, pipe_width, pipe[1])
        if player_rect.colliderect(top_pipe_rect):
            return True

        # top pipe part
        top_part_y = pipe[1] - pipe_part
        if top_part_y + pipe_part_height > 0:
            top_part_y_clamped = max(0, top_part_y)
            top_part_height_visible = pipe_part_height - max(0, -top_part_y)
            if top_part_height_visible > 0:
                top_part_x = pipe[0] - pipe_part // 2
                top_part_rect = pygame.Rect(
                    top_part_x,
                    top_part_y_clamped,
                    pipe_width + pipe_part,
                    top_part_height_visible,
                )
                if player_rect.colliderect(top_part_rect):
                    return True

        # bottom pipe
        bottom_y = pipe[1] + pipe_gap
        bottom_height = display_height - ground_height - bottom_y
        if bottom_height > 0:
            bottom_pipe_rect = pygame.Rect(pipe[0], bottom_y, pipe_width, bottom_height)
            if player_rect.colliderect(bottom_pipe_rect):
                return True

        # bottom pipe part
        bottom_part_y = bottom_y - pipe_part
        bottom_part_x = pipe[0] - pipe_part // 2
        bottom_part_rect = pygame.Rect(
            bottom_part_x, bottom_part_y, pipe_width + pipe_part, pipe_part_height
        )
        if player_rect.colliderect(bottom_part_rect):
            return True

    return False


def draw_score(surface, score):
    # score
    font = pygame.font.Font(None, 74)
    score_text = font.render(str(score), True, (255, 255, 255))
    surface.blit(score_text, (10, 10))


def main():
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("FlappySwords")
    clock = pygame.time.Clock()
    global pipes, player_y, player_velocity
    pipe_x_threshold = display_width // 2
    ground_rect = pygame.Rect(
        0, display_height - ground_height, display_width, ground_height
    )

    running = True
    paused = False
    global score

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # jump
                    if not paused:
                        player_velocity = jump_force

        if not paused:
            # pipe movement
            for pipe in pipes:
                pipe[0] -= pipe_speed

            # new pipe
            if pipes[-1][0] < pipe_x_threshold:
                pipes.append(
                    [
                        display_width,
                        random.randint(
                            50, display_height - ground_height - pipe_gap - 20
                        ),
                        False,
                    ]
                )

            # remove old pipes
            pipes = [pipe for pipe in pipes if pipe[0] + pipe_width > 0]

            # gravity
            player_velocity += gravity
            player_y += player_velocity

            # collision
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            ground_y = display_height - ground_height
            if check_collision(player_rect, pipes, ground_y):
                paused = True

            # scoring
            for pipe in pipes:
                if pipe[0] + pipe_width < player_x and not pipe[2]:
                    score += 1
                    pipe[2] = True

        # background
        screen.fill(backgroundcolor)

        # pipes
        for pipe in pipes:
            draw_pipe(screen, pipe[0], pipe[1])

        # player
        pygame.draw.rect(
            screen, player_color, (player_x, player_y, player_size, player_size)
        )

        # ground
        pygame.draw.rect(screen, groundcolor, ground_rect)

        # score
        draw_score(screen, score)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
