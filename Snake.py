import pygame, sys, random

pygame.init()

# Modern color palette
BG_COLOR = (44, 62, 80)         # Dark background (#2C3E50)
TEXT_COLOR = (236, 240, 241)    # Light text (#ECF0F1)
HIGHLIGHT_COLOR = (236, 240, 241)
OUTLINE_COLOR = (236, 240, 241)
ERROR_COLOR = (231, 76, 60)     # Modern red

# Window configuration
window_size = (640, 480)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Options for colors (for snake and apple)
color_options = {
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Orange": (255, 165, 0),
    "Purple": (128, 0, 128),
    "Red": (255, 0, 0)
}

# Default colors
snake_color = color_options["Green"]
apple_color = color_options["Red"]

# Speed options
speed_options = {"Slow": 10, "Normal": 15, "Fast": 20}
game_speed = 15

# Grid cell size
snake_size = 20

def spawn_food():
    """Generates a food position aligned to the grid."""
    return [
        random.randrange(0, window_size[0] // snake_size) * snake_size,
        random.randrange(0, window_size[1] // snake_size) * snake_size
    ]

def game_over():
    """Displays the Game Over screen for 750ms then returns to the main menu."""
    font = pygame.font.SysFont('Arial', 50)
    game_over_surface = font.render("Game Over", True, ERROR_COLOR)
    game_over_rect = game_over_surface.get_rect(center=(window_size[0] / 2, window_size[1] / 4))
    screen.fill(BG_COLOR)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.update()
    pygame.time.delay(750)
    main_menu()

def draw_snake(snake_body):
    """Draws the snake as circles. The head is drawn with eyes."""
    # Draw head with eyes
    head_x, head_y = snake_body[0]
    center = (head_x + snake_size//2, head_y + snake_size//2)
    pygame.draw.circle(screen, snake_color, center, snake_size//2)
    # Draw eyes (simple small white circles)
    eye_radius = 2
    offset = snake_size // 5
    # For simplicity, draw two eyes on the upper half
    pygame.draw.circle(screen, TEXT_COLOR, (center[0] - offset, center[1] - offset), eye_radius)
    pygame.draw.circle(screen, TEXT_COLOR, (center[0] + offset, center[1] - offset), eye_radius)
    # Draw the rest of the body
    for pos in snake_body[1:]:
        body_center = (pos[0] + snake_size//2, pos[1] + snake_size//2)
        pygame.draw.circle(screen, snake_color, body_center, snake_size//2)

def draw_apple(food_pos):
    """Draws the apple as a red circle with a small green leaf."""
    center = (food_pos[0] + snake_size//2, food_pos[1] + snake_size//2)
    pygame.draw.circle(screen, apple_color, center, snake_size//2)
    # Draw a simple leaf on top of the apple
    leaf_width = snake_size // 3
    leaf_height = snake_size // 2
    leaf_rect = pygame.Rect(center[0] - leaf_width//2, food_pos[1] - leaf_height//2, leaf_width, leaf_height)
    pygame.draw.ellipse(screen, (34, 139, 34), leaf_rect)

def game():
    """
    Main game function.
    The snake and apple are drawn using circles for a more natural look.
    Pressing ESC toggles pause.
    """
    global snake_color, apple_color, game_speed

    snake_pos = [100, 100]
    snake_body = [[100, 100], [80, 100], [60, 100]]
    food_pos = spawn_food()
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    change_to = 'UP'
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    change_to = 'DOWN'
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    change_to = 'LEFT'
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    change_to = 'RIGHT'
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused

        if paused:
            pause_font = pygame.font.SysFont('Arial', 50)
            pause_text = pause_font.render("Paused", True, TEXT_COLOR)
            pause_rect = pause_text.get_rect(center=(window_size[0] / 2, window_size[1] / 2))
            screen.fill(BG_COLOR)
            screen.blit(pause_text, pause_rect)
            pygame.display.update()
            clock.tick(game_speed)
            continue

        # Validate direction (avoid immediate reversal)
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Update snake head position
        if direction == 'UP':
            snake_pos[1] -= snake_size
        elif direction == 'DOWN':
            snake_pos[1] += snake_size
        elif direction == 'LEFT':
            snake_pos[0] -= snake_size
        elif direction == 'RIGHT':
            snake_pos[0] += snake_size

        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = spawn_food()
            food_spawn = True

        screen.fill(BG_COLOR)
        draw_snake(snake_body)
        draw_apple(food_pos)

        # Check for collisions with boundaries
        if snake_pos[0] < 0 or snake_pos[0] >= window_size[0] or snake_pos[1] < 0 or snake_pos[1] >= window_size[1]:
            game_over()
        # Check for collisions with itself
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()

        # Display score
        font_score = pygame.font.SysFont('Arial', 25)
        score_surface = font_score.render("Score: " + str(score), True, TEXT_COLOR)
        score_rect = score_surface.get_rect(topleft=(window_size[0] / 10, 15))
        screen.blit(score_surface, score_rect)

        pygame.display.update()
        clock.tick(game_speed)

def options_menu():
    """
    Options menu to choose snake color, apple color, and game speed.
    Navigation is done with arrow keys; the current selection remains highlighted.
    """
    global snake_color, apple_color, game_speed

    # Option lists
    snake_colors_list = list(color_options.items())
    apple_colors_list = list(color_options.items())
    speed_options_list = list(speed_options.items())

    # Initial indices corresponding to current choices
    snake_index = next(i for i, item in enumerate(snake_colors_list) if item[1] == snake_color)
    apple_index = next(i for i, item in enumerate(apple_colors_list) if item[1] == apple_color)
    speed_index = next(i for i, item in enumerate(speed_options_list) if item[1] == game_speed)

    # Navigation sections:
    # 0 - Snake Color, 1 - Apple Color, 2 - Game Speed, 3 - Back
    selected_section = 0
    font_title = pygame.font.SysFont('Arial', 40)
    font_small = pygame.font.SysFont('Arial', 25)
    btn_width = 80
    gap = 20

    while True:
        screen.fill(BG_COLOR)
        title_text = font_title.render("Options", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(window_size[0] / 2, 30))
        screen.blit(title_text, title_rect)

        # --- Section 0: Snake Color ---
        snake_section_y = 60
        snake_instr = font_small.render("Select Snake Color:", True, TEXT_COLOR)
        snake_instr_rect = snake_instr.get_rect(center=(window_size[0] / 2, snake_section_y + 20))
        screen.blit(snake_instr, snake_instr_rect)
        n = len(snake_colors_list)
        total_width = n * btn_width + (n - 1) * gap
        start_x = (window_size[0] - total_width) / 2
        for i, (name, color_val) in enumerate(snake_colors_list):
            btn_rect = pygame.Rect(start_x + i * (btn_width + gap), snake_section_y + 50, btn_width, 40)
            if i == snake_index:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, btn_rect, border_radius=8)
                label_color = BG_COLOR
            else:
                pygame.draw.rect(screen, OUTLINE_COLOR, btn_rect, width=2, border_radius=8)
                label_color = TEXT_COLOR
            label = font_small.render(name, True, label_color)
            label_rect = label.get_rect(center=btn_rect.center)
            screen.blit(label, label_rect)

        # --- Section 1: Apple Color ---
        apple_section_y = snake_section_y + 120
        apple_instr = font_small.render("Select Apple Color:", True, TEXT_COLOR)
        apple_instr_rect = apple_instr.get_rect(center=(window_size[0] / 2, apple_section_y + 20))
        screen.blit(apple_instr, apple_instr_rect)
        n = len(apple_colors_list)
        total_width = n * btn_width + (n - 1) * gap
        start_x = (window_size[0] - total_width) / 2
        for i, (name, color_val) in enumerate(apple_colors_list):
            btn_rect = pygame.Rect(start_x + i * (btn_width + gap), apple_section_y + 50, btn_width, 40)
            if i == apple_index:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, btn_rect, border_radius=8)
                label_color = BG_COLOR
            else:
                pygame.draw.rect(screen, OUTLINE_COLOR, btn_rect, width=2, border_radius=8)
                label_color = TEXT_COLOR
            label = font_small.render(name, True, label_color)
            label_rect = label.get_rect(center=btn_rect.center)
            screen.blit(label, label_rect)

        # --- Section 2: Game Speed ---
        speed_section_y = apple_section_y + 120
        speed_instr = font_small.render("Select Game Speed:", True, TEXT_COLOR)
        speed_instr_rect = speed_instr.get_rect(center=(window_size[0] / 2, speed_section_y + 20))
        screen.blit(speed_instr, speed_instr_rect)
        n = len(speed_options_list)
        total_width = n * btn_width + (n - 1) * gap
        start_x = (window_size[0] - total_width) / 2
        for i, (name, speed_val) in enumerate(speed_options_list):
            btn_rect = pygame.Rect(start_x + i * (btn_width + gap), speed_section_y + 50, btn_width, 40)
            if i == speed_index:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, btn_rect, border_radius=8)
                label_color = BG_COLOR
            else:
                pygame.draw.rect(screen, OUTLINE_COLOR, btn_rect, width=2, border_radius=8)
                label_color = TEXT_COLOR
            label = font_small.render(name, True, label_color)
            label_rect = label.get_rect(center=btn_rect.center)
            screen.blit(label, label_rect)

        # --- Section 3: Back Button ---
        back_y = speed_section_y + 120
        back_text = font_small.render("Back", True, TEXT_COLOR)
        back_rect = back_text.get_rect(center=(window_size[0] / 2, back_y))
        if selected_section == 3:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, back_rect.inflate(20, 10), border_radius=8)
            back_text = font_small.render("Back", True, BG_COLOR)
        else:
            pygame.draw.rect(screen, OUTLINE_COLOR, back_rect.inflate(20, 10), width=2, border_radius=8)
        screen.blit(back_text, back_rect)

        # Error message if snake and apple colors are identical
        if snake_colors_list[snake_index][1] == apple_colors_list[apple_index][1]:
            error_message = "Snake and apple colors must be different!"
            error_text = font_small.render(error_message, True, ERROR_COLOR)
            error_rect = error_text.get_rect(center=(window_size[0] / 2, back_y + 40))
            screen.blit(error_text, error_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_section = (selected_section - 1) % 4
                elif event.key == pygame.K_DOWN:
                    selected_section = (selected_section + 1) % 4
                elif event.key == pygame.K_LEFT:
                    if selected_section == 0:
                        snake_index = (snake_index - 1) % len(snake_colors_list)
                    elif selected_section == 1:
                        apple_index = (apple_index - 1) % len(apple_colors_list)
                    elif selected_section == 2:
                        speed_index = (speed_index - 1) % len(speed_options_list)
                elif event.key == pygame.K_RIGHT:
                    if selected_section == 0:
                        snake_index = (snake_index + 1) % len(snake_colors_list)
                    elif selected_section == 1:
                        apple_index = (apple_index + 1) % len(apple_colors_list)
                    elif selected_section == 2:
                        speed_index = (speed_index + 1) % len(speed_options_list)
                elif event.key == pygame.K_RETURN:
                    if selected_section == 3:
                        if snake_colors_list[snake_index][1] == apple_colors_list[apple_index][1]:
                            pass
                        else:
                            snake_color = snake_colors_list[snake_index][1]
                            apple_color = apple_colors_list[apple_index][1]
                            game_speed = speed_options_list[speed_index][1]
                            return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # Section 0
                for i, (name, color_val) in enumerate(snake_colors_list):
                    btn_rect = pygame.Rect((window_size[0] - (len(snake_colors_list) * btn_width + (len(snake_colors_list)-1)*gap)) / 2 + i * (btn_width+gap),
                                             snake_section_y + 50, btn_width, 40)
                    if btn_rect.collidepoint(pos):
                        snake_index = i
                        selected_section = 0
                # Section 1
                for i, (name, color_val) in enumerate(apple_colors_list):
                    btn_rect = pygame.Rect((window_size[0] - (len(apple_colors_list) * btn_width + (len(apple_colors_list)-1)*gap)) / 2 + i * (btn_width+gap),
                                             apple_section_y + 50, btn_width, 40)
                    if btn_rect.collidepoint(pos):
                        apple_index = i
                        selected_section = 1
                # Section 2
                for i, (name, speed_val) in enumerate(speed_options_list):
                    btn_rect = pygame.Rect((window_size[0] - (len(speed_options_list) * btn_width + (len(speed_options_list)-1)*gap)) / 2 + i * (btn_width+gap),
                                             speed_section_y + 50, btn_width, 40)
                    if btn_rect.collidepoint(pos):
                        speed_index = i
                        selected_section = 2
                # Section 3
                if back_rect.collidepoint(pos):
                    selected_section = 3
                    if snake_colors_list[snake_index][1] != apple_colors_list[apple_index][1]:
                        snake_color = snake_colors_list[snake_index][1]
                        apple_color = apple_colors_list[apple_index][1]
                        game_speed = speed_options_list[speed_index][1]
                        return

        pygame.display.update()
        clock.tick(game_speed)

def main_menu():
    """Main menu with arrow-key navigation and modern highlighting."""
    selected = 0
    menu_items = ["Start", "Options", "Exit"]
    font_small = pygame.font.SysFont('Arial', 30)

    while True:
        screen.fill(BG_COLOR)
        title_font = pygame.font.SysFont('Arial', 50)
        title_text = title_font.render("Snake Game", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(window_size[0] / 2, window_size[1] / 4))
        screen.blit(title_text, title_rect)

        for i, item in enumerate(menu_items):
            text = font_small.render(item, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(window_size[0] / 2, window_size[1] / 2 + i * 50))
            if i == selected:
                highlight_rect = text_rect.inflate(20, 10)
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect, border_radius=8)
                text = font_small.render(item, True, BG_COLOR)
            else:
                pygame.draw.rect(screen, OUTLINE_COLOR, text_rect.inflate(20, 10), width=2, border_radius=8)
            screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        game()
                    elif selected == 1:
                        options_menu()
                    elif selected == 2:
                        pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, item in enumerate(menu_items):
                    text = font_small.render(item, True, TEXT_COLOR)
                    text_rect = text.get_rect(center=(window_size[0] / 2, window_size[1] / 2 + i * 50))
                    if text_rect.inflate(20, 10).collidepoint(event.pos):
                        selected = i
                        if i == 0:
                            game()
                        elif i == 1:
                            options_menu()
                        elif i == 2:
                            pygame.quit(); sys.exit()

        pygame.display.update()
        clock.tick(game_speed)

if __name__ == '__main__':
    main_menu()