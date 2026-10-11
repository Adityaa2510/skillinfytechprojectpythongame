import sys
import pygame
from game_logic import move_snake, has_collision, spawn_food

CELL = 20
COLS = 30
ROWS = 30
WIDTH = CELL * COLS
HEIGHT = CELL * ROWS

BG = (17, 24, 35)
GRID = (31, 43, 54)
GREEN = (65, 230, 125)
DARK_GREEN = (35, 155, 85)
RED = (255, 85, 95)
WHITE = (245, 245, 245)
YELLOW = (255, 210, 75)

DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def new_game():
    snake = [(15, 15), (14, 15), (13, 15)]
    return snake, (1, 0), spawn_food(snake, COLS, ROWS), 0


def draw_cell(screen, position, color):
    x, y = position
    rect = pygame.Rect(x * CELL + 2, y * CELL + 2, CELL - 4, CELL - 4)
    pygame.draw.rect(screen, color, rect, border_radius=5)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Arena | Python DevSecOps")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    title_font = pygame.font.Font(None, 56)

    snake, direction, food, score = new_game()
    paused = False
    game_over = False
    won = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE and not game_over:
                paused = not paused
                continue
            if event.key == pygame.K_r and game_over:
                snake, direction, food, score = new_game()
                paused = False
                game_over = False
                won = False
                continue
            if not paused and not game_over:
                candidate = DIRECTIONS.get(event.key)
                if candidate:
                    reverse = (
                        candidate[0] == -direction[0]
                        and candidate[1] == -direction[1]
                    )
                    if not reverse:
                        direction = candidate

        if not paused and not game_over:
            next_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            eating = next_head == food
            updated = move_snake(snake, direction, grow=eating)
            if has_collision(updated, COLS, ROWS):
                game_over = True
            else:
                snake = updated
                if eating:
                    score += 1
                    food = spawn_food(snake, COLS, ROWS)
                    if food is None:
                        game_over = True
                        won = True

        speed = min(20, 8 + score // 3)
        screen.fill(BG)
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))
        if food is not None:
            draw_cell(screen, food, RED)
        for i, segment in enumerate(snake):
            draw_cell(screen, segment, GREEN if i == 0 else DARK_GREEN)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

        if paused or game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(190)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            if game_over:
                message = "YOU WIN!" if won else "GAME OVER"
                color = GREEN if won else RED
                hint = "Press R to restart"
            else:
                message, color, hint = "PAUSED", YELLOW, "Press SPACE to resume"
            title = title_font.render(message, True, color)
            subtitle = font.render(hint, True, WHITE)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25)))
            screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))

        pygame.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    main()
