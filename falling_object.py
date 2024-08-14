import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 20
OBJECT_RADIUS = 15
PLAYER_SPEED = 10
OBJECT_SPEED = 7
WINNING_SCORE = 10
FPS = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Catch the Falling Objects')


player_rect = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
objects = []


score = 0
object_timer = 0

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 36)  

def reset_game():
    """Reset the game state."""
    global player_rect, objects, object_timer, score
    player_rect = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    objects = []
    object_timer = 0
    score = 0

def draw_player():
    pygame.draw.rect(screen, GREEN, player_rect)

def draw_objects():
    for obj in objects:
        pygame.draw.circle(screen, RED, obj, OBJECT_RADIUS)

def update_objects():
    global objects, score
    for obj in objects[:]:
        obj[1] += OBJECT_SPEED
        
        if obj[1] > HEIGHT:
            objects.remove(obj)
        elif player_rect.collidepoint(obj[0], obj[1]):
            objects.remove(obj)
            score += 1
def draw_score():
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_win_message():
    screen.fill(BLACK)
    win_text = font.render("You Win!", True, WHITE)
    restart_text = small_font.render("Press R to Restart", True, WHITE)
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + win_text.get_height() // 2))
    pygame.display.flip()

def main():
    global player_rect, objects, object_timer, score

    def create_object():
        """Create a new falling object."""
        object_x = random.randint(OBJECT_RADIUS, WIDTH - OBJECT_RADIUS)
        return [object_x, -OBJECT_RADIUS] 
    def restart_game():
        """Restart the game."""
        reset_game()

    game_over = False
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0 and not game_over:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH and not game_over:
            player_rect.x += PLAYER_SPEED
        if keys[pygame.K_r] and game_over:
            restart_game()
            game_over = False

        if not game_over:
           
            object_timer += 1
            if object_timer > 30:
                objects.append(create_object())
                object_timer = 0

          
            update_objects()

           
            screen.fill(BLACK)
            draw_objects()
            draw_player()
            draw_score()

       
            if score >= WINNING_SCORE:
                game_over = True
        else:
            draw_win_message()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
