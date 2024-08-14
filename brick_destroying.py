import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_RADIUS = 15
BRICK_WIDTH, BRICK_HEIGHT = 75, 30
PADDLE_SPEED = 10
BALL_SPEED_X, BALL_SPEED_Y = 5, -5
BRICK_ROWS, BRICK_COLS = 5, 8


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Brick Destroying')


paddle_rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
ball_rect = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)


def create_bricks():
    bricks = []
    start_x = 30
    start_y = 30
    spacing_x = 10
    spacing_y = 10
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick_rect = pygame.Rect(start_x + col * (BRICK_WIDTH + spacing_x),
                                     start_y + row * (BRICK_HEIGHT + spacing_y),
                                     BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append(brick_rect)
    return bricks


bricks = create_bricks()


ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y
game_over = False
win = False


font = pygame.font.Font(None, 74)
score_font = pygame.font.Font(None, 36)
score = 0

def draw_paddle():
    pygame.draw.rect(screen, WHITE, paddle_rect)

def draw_ball():
    pygame.draw.ellipse(screen, WHITE, ball_rect)

def draw_bricks():
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

def update_ball():
    global ball_dx, ball_dy, score, game_over, win

    ball_rect.x += ball_dx
    ball_rect.y += ball_dy


    if ball_rect.left <= 0 or ball_rect.right >= WIDTH:
        ball_dx = -ball_dx
    if ball_rect.top <= 0:
        ball_dy = -ball_dy


    if ball_rect.colliderect(paddle_rect):
        ball_dy = -ball_dy

    for brick in bricks[:]:
        if ball_rect.colliderect(brick):
            bricks.remove(brick)
            ball_dy = -ball_dy
            score += 1

    if ball_rect.bottom >= HEIGHT:
        game_over = True

    if not bricks:
        win = True

def draw_score():
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_win_message():
    screen.fill(BLACK)
    win_text = font.render("You Win!", True, WHITE)
    restart_text = score_font.render("Press R to Restart", True, WHITE)
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + win_text.get_height() // 2 + 20))
    pygame.display.flip()

def draw_game_over_message():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    restart_text = score_font.render("Press R to Restart", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2 + 20))
    pygame.display.flip()

def main():
    global ball_dx, ball_dy, game_over, win, bricks, score

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_rect.left > 0 and not game_over and not win:
            paddle_rect.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle_rect.right < WIDTH and not game_over and not win:
            paddle_rect.x += PADDLE_SPEED
        if keys[pygame.K_r] and (game_over or win):
       
            paddle_rect.x = WIDTH // 2 - PADDLE_WIDTH // 2
            ball_rect.x = WIDTH // 2 - BALL_RADIUS
            ball_rect.y = HEIGHT // 2 - BALL_RADIUS
            ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y
            bricks = create_bricks() 
            score = 0
            game_over = False
            win = False

        if not game_over and not win:
            update_ball()


            screen.fill(BLACK)
            draw_bricks()
            draw_ball()
            draw_paddle()
            draw_score()
        elif win:
            draw_win_message()
        else:
            draw_game_over_message()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
