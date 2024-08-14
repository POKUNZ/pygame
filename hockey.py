import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PUCK_SIZE = 20
PADDLE_SPEED = 5
PUCK_SPEED = 4
INITIAL_WINNING_SCORE = 5
FINAL_WINNING_SCORE = 10


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Hockey')


left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
puck = pygame.Rect(WIDTH // 2 - PUCK_SIZE // 2, HEIGHT // 2 - PUCK_SIZE // 2, PUCK_SIZE, PUCK_SIZE)


puck_dx, puck_dy = PUCK_SPEED, PUCK_SPEED


left_score = 0
right_score = 0


font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)


winning_score = INITIAL_WINNING_SCORE

def reset_game():
    """Reset the puck to the center and randomize its direction."""
    global puck_dx, puck_dy, puck
    puck.center = (WIDTH // 2, HEIGHT // 2)
    puck_dx = PUCK_SPEED * (-1 if puck_dx > 0 else 1)
    puck_dy = PUCK_SPEED * (-1 if puck_dy > 0 else 1)

def display_message(message, color, size, position):
    """Display a message on the screen."""
    font = pygame.font.Font(None, size)
    text = font.render(message, True, color)
    screen.blit(text, position)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if left_score >= winning_score or right_score >= winning_score:
        if left_score >= winning_score and right_score >= winning_score:
            winning_score = FINAL_WINNING_SCORE 
            left_score = 0
            right_score = 0
            reset_game()
        elif left_score >= winning_score:
            screen.fill(BLACK)
            display_message("Left Player Wins!", WHITE, 74, (WIDTH // 4, HEIGHT // 2 - 37))
            display_message("Press R to Restart", WHITE, 36, (WIDTH // 4, HEIGHT // 2 + 50))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        left_score = 0
                        right_score = 0
                        winning_score = INITIAL_WINNING_SCORE
                        reset_game()
                        break
                else:
                    continue
                break
        elif right_score >= winning_score:
            screen.fill(BLACK)
            display_message("Right Player Wins!", WHITE, 74, (WIDTH // 4, HEIGHT // 2 - 37))
            display_message("Press R to Restart", WHITE, 36, (WIDTH // 4, HEIGHT // 2 + 50))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        left_score = 0
                        right_score = 0
                        winning_score = INITIAL_WINNING_SCORE
                        reset_game()
                        break
                else:
                    continue
                break


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

    puck.x += puck_dx
    puck.y += puck_dy

    if puck.top <= 0 or puck.bottom >= HEIGHT:
        puck_dy = -puck_dy

    if puck.left <= 0:
        right_score += 1
        reset_game()
    elif puck.right >= WIDTH:
        left_score += 1
        reset_game()

    if puck.colliderect(left_paddle) or puck.colliderect(right_paddle):
        puck_dx = -puck_dx


    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, puck)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    

    left_text = font.render(f"{left_score}", True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 20))
    right_text = font.render(f"{right_score}", True, WHITE)
    screen.blit(right_text, (WIDTH * 3 // 4 - right_text.get_width(), 20))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
