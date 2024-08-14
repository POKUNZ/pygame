import pygame
import random
import heapq


pygame.init()


WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Generator and Solver')

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def draw_grid(grid, path=[]):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = WHITE
            if (x, y) in path:
                color = BLUE
            elif grid[y][x] == 1:
                color = BLACK
            pygame.draw.rect(screen, color, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_character(pos):
    pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_exit(exit_pos):
    pygame.draw.rect(screen, RED, pygame.Rect(exit_pos[0] * CELL_SIZE, exit_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_win_message():
    font = pygame.font.Font(None, 74)
    restart_font = pygame.font.Font(None, 36)
    screen.fill(WHITE)
    win_text = font.render("You Win!", True, GREEN)
    restart_text = restart_font.render("Press R to Restart", True, BLACK)
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + win_text.get_height() // 2 + 20))
    pygame.display.flip()

def generate_maze():
    grid = [[1] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    stack = [(0, 0)]
    grid[0][0] = 0

    while stack:
        x, y = stack[-1]
        neighbors = []

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] == 1:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            grid[ny][nx] = 0
            grid[y + (ny - y) // 2][x + (nx - x) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return grid

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in DIRECTIONS:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] == 0:
                next = (nx, ny)
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    heapq.heappush(open_set, (priority, next))
                    came_from[next] = current

    return []

def is_adjacent(pos1, pos2):
    return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1

def find_reachable_exit(start, grid):
    for _ in range(100):  
        exit_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if grid[exit_pos[1]][exit_pos[0]] == 0 and exit_pos != start and not is_adjacent(start, exit_pos):
            path = a_star_search(start, exit_pos, grid)
            if path:
                return exit_pos
    return None

def main():
    clock = pygame.time.Clock()
    grid = generate_maze()
    start = (0, 0)
    exit_pos = find_reachable_exit(start, grid)
    if exit_pos is None:
        raise RuntimeError("No reachable exit found")
    path = []
    char_pos = list(start)
    win = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and char_pos[0] > 0 and grid[char_pos[1]][char_pos[0] - 1] == 0:
            char_pos[0] -= 1
        if keys[pygame.K_RIGHT] and char_pos[0] < GRID_WIDTH - 1 and grid[char_pos[1]][char_pos[0] + 1] == 0:
            char_pos[0] += 1
        if keys[pygame.K_UP] and char_pos[1] > 0 and grid[char_pos[1] - 1][char_pos[0]] == 0:
            char_pos[1] -= 1
        if keys[pygame.K_DOWN] and char_pos[1] < GRID_HEIGHT - 1 and grid[char_pos[1] + 1][char_pos[0]] == 0:
            char_pos[1] += 1

        if keys[pygame.K_s] and not win:  
            path = a_star_search(start, exit_pos, grid)

        if keys[pygame.K_r]:  
            grid = generate_maze()
            exit_pos = find_reachable_exit(start, grid)
            if exit_pos is None:
                raise RuntimeError("No reachable exit found")
            path = []
            char_pos = list(start)
            win = False

        if char_pos == list(exit_pos):
            win = True

        screen.fill(WHITE)
        draw_grid(grid, path)
        draw_character(char_pos)
        draw_exit(exit_pos)
        if win:
            draw_win_message()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
