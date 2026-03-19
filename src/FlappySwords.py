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

pipes = [
    [display_width, random.randint(50, display_height - ground_height - pipe_gap - 20), False, False]
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

# weapon system
current_weapon = None
next_weapon_score = random.choice([3, 5, 7])

# sword (melee)
sword_width = 35
sword_height = 12
sword_color = (255, 165, 0)
sword_duration = 20

# special (gravity invert)
gravity_inverted = False


def draw_pipe(surface, x, height, disabled):
    alpha = 80 if disabled else 255
    pipe_surface = pygame.Surface((display_width, display_height), pygame.SRCALPHA)

    pygame.draw.rect(pipe_surface, (*pipe_color, alpha), (x, 0, pipe_width, height))

    part_x = x - pipe_part // 2
    pygame.draw.rect(
        pipe_surface,
        (*pipe_part_color, alpha),
        (part_x, height - pipe_part, pipe_width + pipe_part, pipe_part_height),
    )

    bottom_y = height + pipe_gap
    pygame.draw.rect(
        pipe_surface,
        (*pipe_color, alpha),
        (x, bottom_y, pipe_width, display_height - ground_height - bottom_y),
    )

    pygame.draw.rect(
        pipe_surface,
        (*pipe_part_color, alpha),
        (part_x, bottom_y - pipe_part, pipe_width + pipe_part, pipe_part_height),
    )

    surface.blit(pipe_surface, (0, 0))


def check_collision(player_rect, pipes, ground_y):
    if player_rect.bottom >= ground_y or player_rect.top <= 0:
        return True

    for pipe in pipes:
        if pipe[3]:
            continue

        x, h = pipe[0], pipe[1]
        bottom_y = h + pipe_gap

        if (
            player_rect.colliderect(pygame.Rect(x, 0, pipe_width, h)) or
            player_rect.colliderect(pygame.Rect(x - pipe_part//2, h - pipe_part, pipe_width + pipe_part, pipe_part_height)) or
            player_rect.colliderect(pygame.Rect(x, bottom_y, pipe_width, display_height - ground_height - bottom_y)) or
            player_rect.colliderect(pygame.Rect(x - pipe_part//2, bottom_y - pipe_part, pipe_width + pipe_part, pipe_part_height))
        ):
            return True

    return False


def draw_score(surface, score):
    font = pygame.font.Font(None, 74)
    surface.blit(font.render(str(score), True, (255, 255, 255)), (10, 10))


def draw_ammo(surface, weapon):
    if not weapon:
        return
    font = pygame.font.Font(None, 36)
    surface.blit(font.render(f"{weapon['type']} Ammo: {weapon['ammo']}", True, (255,255,255)), (10, 80))


def main():
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()

    global pipes, player_y, player_velocity, score
    global current_weapon, next_weapon_score, gravity_inverted

    pipe_x_threshold = display_width // 2
    ground_rect = pygame.Rect(0, display_height - ground_height, display_width, ground_height)

    paused = False

    while True:
        current_gravity = -gravity if gravity_inverted else gravity
        current_jump = -jump_force if gravity_inverted else jump_force

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not paused:
                    player_velocity = current_jump

                if event.key == pygame.K_s:
                    if current_weapon and current_weapon["type"] == "melee" and current_weapon["ammo"] > 0:
                        current_weapon["active"] = True
                        current_weapon["timer"] = sword_duration
                        current_weapon["ammo"] -= 1

                if event.key == pygame.K_q:
                    if current_weapon and current_weapon["type"] == "special" and current_weapon["ammo"] > 0:
                        gravity_inverted = True
                        current_weapon["ammo"] -= 1
                        current_weapon["start_score"] = score

        if not paused:
            for pipe in pipes:
                pipe[0] -= pipe_speed

            if pipes[-1][0] < pipe_x_threshold:
                pipes.append([
                    display_width,
                    random.randint(50, display_height - ground_height - pipe_gap - 20),
                    False,
                    False,
                ])

            pipes = [p for p in pipes if p[0] + pipe_width > 0]

            player_velocity += current_gravity
            player_y += player_velocity

            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            ground_y = display_height - ground_height

            if check_collision(player_rect, pipes, ground_y):
                paused = True

            for pipe in pipes:
                if pipe[0] + pipe_width < player_x and not pipe[2]:
                    score += 1
                    pipe[2] = True

                    if score >= next_weapon_score:
                        # RANDOM weapon
                        if random.choice(["melee", "special"]) == "melee":
                            current_weapon = {"type": "melee", "ammo": random.randint(2, 4), "active": False, "timer": 0}
                        else:
                            current_weapon = {"type": "special", "ammo": 1}

                        next_weapon_score += random.randint(5, 10)

            # sword logic
            if current_weapon and current_weapon.get("type") == "melee" and current_weapon.get("active"):
                current_weapon["timer"] -= 1

                sword_rect = pygame.Rect(
                    player_x + player_size,
                    player_y + player_size // 2 - sword_height // 2,
                    sword_width,
                    sword_height,
                )

                for pipe in pipes:
                    if pipe[3]:
                        continue

                    x, h = pipe[0], pipe[1]
                    bottom_y = h + pipe_gap

                    if (
                        sword_rect.colliderect(pygame.Rect(x, 0, pipe_width, h)) or
                        sword_rect.colliderect(pygame.Rect(x - pipe_part//2, h - pipe_part, pipe_width + pipe_part, pipe_part_height)) or
                        sword_rect.colliderect(pygame.Rect(x, bottom_y, pipe_width, display_height - ground_height - bottom_y)) or
                        sword_rect.colliderect(pygame.Rect(x - pipe_part//2, bottom_y - pipe_part, pipe_width + pipe_part, pipe_part_height))
                    ):
                        pipe[3] = True

                if current_weapon["timer"] <= 0:
                    current_weapon["active"] = False

            # special logic duration
            if gravity_inverted and current_weapon and current_weapon.get("type") == "special":
                if score - current_weapon.get("start_score", 0) >= 5:
                    gravity_inverted = False
                    current_weapon = None

        screen.fill(backgroundcolor)

        for pipe in pipes:
            draw_pipe(screen, pipe[0], pipe[1], pipe[3])

        if current_weapon and current_weapon.get("type") == "melee" and current_weapon.get("active"):
            pygame.draw.rect(
                screen,
                sword_color,
                (
                    player_x + player_size,
                    player_y + player_size // 2 - sword_height // 2,
                    sword_width,
                    sword_height,
                ),
            )

        pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))
        pygame.draw.rect(screen, groundcolor, ground_rect)

        draw_score(screen, score)
        draw_ammo(screen, current_weapon)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
