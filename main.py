import pygame
import sys
import random
import math
import time
from queue import deque
from queue import PriorityQueue

DISPLAY_WIDTH = 1270
DISPLAY_HEIGHT = 780
MAZE_SIZE = 71

def gen_maze():
    maze = [[1] * MAZE_SIZE for _ in range(MAZE_SIZE)]
    
    for i in range(1, MAZE_SIZE, 2):
        for j in range(1, MAZE_SIZE, 2):
            maze[i][j] = 0

    walls = []
    for i in range(1, MAZE_SIZE, 2):
        for j in range(1, MAZE_SIZE, 2):
            if j + 2 < MAZE_SIZE:
                walls.append(((i, j + 1), (i, j), (i, j + 2)))
            if i + 2 < MAZE_SIZE:
                walls.append(((i + 1, j), (i, j), (i + 2, j)))

    parent = {(i, j): (i, j) for i in range(1, MAZE_SIZE, 2) for j in range(1, MAZE_SIZE, 2)}

    def find(cell):
        if parent[cell] != cell:
            parent[cell] = find(parent[cell])
        return parent[cell]

    def union(c1, c2):
        r1, r2 = find(c1), find(c2)
        parent[r2] = r1

    random.shuffle(walls)
    for wall, c1, c2 in walls:
        if find(c1) != find(c2):
            union(c1, c2)
            maze[wall[0]][wall[1]] = 0

    return maze

def calculate_offsets(cell_size):
    maze_width = MAZE_SIZE * cell_size
    maze_height = MAZE_SIZE * cell_size
    offset_x = (DISPLAY_WIDTH - maze_width) // 2
    offset_y = (DISPLAY_HEIGHT - maze_height) // 2
    return offset_x, offset_y

def bfs(screen, maze, start, end, cell_size, offset_x, offset_y):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}
  
    visual_maze = [row[:] for row in maze]

    while queue:
        current = queue.popleft()
        if current == end:
            break

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and
                    maze[nx][ny] == 0 and neighbor not in visited):
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

                visual_maze[nx][ny] = 2
                draw_maze(screen, visual_maze, cell_size, offset_x, offset_y)
                pygame.display.update()
                pygame.time.delay(10)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    if end not in parent:
        return

    path = []
    step = end
    while step is not None:
        path.append(step)
        step = parent.get(step)

    path.reverse()
    for step in path:
        x, y = step
        visual_maze[x][y] = 3
        draw_maze(screen, visual_maze, cell_size, offset_x, offset_y)
        pygame.display.update()
        pygame.time.delay(30)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def dfs(screen, maze, start, end, cell_size, offset_x, offset_y):
    stck = [start]
    visited = set()
    visited.add(start)
    parent = {start: None}

    visual_maze = [row[:] for row in maze]

    while stck:
        current = stck.pop()
        if current == end:
            break

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and
                    maze[nx][ny] == 0 and neighbor not in visited):
                stck.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

                visual_maze[nx][ny] = 2
                draw_maze(screen, visual_maze, cell_size, offset_x, offset_y)
                pygame.display.update()
                pygame.time.delay(10)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    if end not in parent:
        return
    
    path = []
    step = end
    while step is not None:
        path.append(step)
        step = parent.get(step)

    path.reverse()
    for step in path:
        x, y = step
        visual_maze[x][y] = 3
        draw_maze(screen, visual_maze, cell_size, offset_x, offset_y)
        pygame.display.update()
        pygame.time.delay(30)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(screen, maze, start, end, cell_size, offset_x, offset_y):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    open_set_hash = {start} 
    
    visual_maze = [row[:] for row in maze]
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        current = open_set.get()[1]
        open_set_hash.remove(current)
        
        if current == end:
           
            path = []
            while current in came_from:
                current = came_from[current]
                path.append(current)
            
            for step in reversed(path):
                x, y = step
                visual_maze[x][y] = 3
                draw_maze(screen, visual_maze, cell_size, offset_x, offset_y)
                pygame.display.update()
                pygame.time.delay(30)
            
            visual_maze[end[0]][end[1]] = 3  
            draw_maze(screen, visual_maze, cell_size, offset_x, offset_y)
            return
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if (0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and 
                maze[neighbor[0]][neighbor[1]] == 0):
          
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                    
                    if neighbor not in open_set_hash:
                        open_set.put((f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)

                        visual_maze[neighbor[0]][neighbor[1]] = 2
                        draw_maze(screen, visual_maze, cell_size, offset_x, offset_y)
                        pygame.display.update()
                        pygame.time.delay(10)

def greedy(screen, maze, start, end, cell_size, offset_x, offset_y):

    open_set = PriorityQueue()
    open_set.put((heuristic(start, end), start))
    came_from = {start: None}
    visited = {start}
    
    visual_maze = [row[:] for row in maze]
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        _, current = open_set.get()
        
        if current == end:
            path = []
            step = end
            while step is not None:
                path.append(step)
                step = came_from.get(step)
            
            path.reverse()
            for step in path:
                x, y = step
                visual_maze[x][y] = 3
                draw_maze(screen, visual_maze, cell_size, offset_x, offset_y)
                pygame.display.update()
                pygame.time.delay(30)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            return

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            
            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and 
                maze[nx][ny] == 0 and neighbor not in visited):

                open_set.put((heuristic(neighbor, end), neighbor))
                visited.add(neighbor)
                came_from[neighbor] = current

                visual_maze[nx][ny] = 2
                draw_maze(screen, visual_maze, cell_size, offset_x, offset_y)
                pygame.display.update()
                pygame.time.delay(10)


def draw_maze(screen, maze, cell_size, offset_x, offset_y):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            color = (255, 255, 255) 
            if cell == 1:
                color = (0, 0, 0)  
            elif cell == 2:
                color = (0, 255, 0)  
            elif cell == 3:
                color = (255, 0, 0) 
            pygame.draw.rect(screen, color, (offset_x + j * cell_size, offset_y + i * cell_size, cell_size, cell_size))

def main():
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()

    m = gen_maze()
    p = [1, 1]  
    e = [MAZE_SIZE - 2, MAZE_SIZE - 2]

    csf = min(DISPLAY_WIDTH / MAZE_SIZE, DISPLAY_HEIGHT / MAZE_SIZE) * 0.8
    cell_size = int(math.floor(csf))

    offset_x, offset_y = calculate_offsets(cell_size)

    font = pygame.font.Font(None, 24) 
    header = font.render("Find your way out of this maze!", True, (0, 0, 0))
    textrect = header.get_rect()
    textrect.midtop = (DISPLAY_WIDTH // 2, 10)

    bfs_button_width, bfs_button_height = 100, 50
    bfs_button_x, bfs_button_y = 100, 220
    bfs_button_rect = pygame.Rect(bfs_button_x, bfs_button_y, bfs_button_width, bfs_button_height)

    dfs_button_width, dfs_button_height = 100, 50
    dfs_button_x, dfs_button_y = 100, 320
    dfs_button_rect = pygame.Rect(dfs_button_x, dfs_button_y, dfs_button_width, dfs_button_height)

    astar_button_width, astar_button_height = 100, 50
    astar_button_x, astar_button_y = 100, 420
    astar_button_rect = pygame.Rect(astar_button_x, astar_button_y, astar_button_width, astar_button_height)

    greedy_button_width, greedy_button_height = 100, 50
    greedy_button_x, greedy_button_y = 100, 520
    greedy_button_rect = pygame.Rect(greedy_button_x, greedy_button_y, greedy_button_width, greedy_button_height)

    running = True
    solving = False
    won = False

    while running:
        screen.fill((200, 200, 200))  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN and not solving:
                np = p.copy()
                if event.key in (pygame.K_UP, pygame.K_w): np[0] -= 1
                elif event.key in (pygame.K_DOWN, pygame.K_s): np[0] += 1
                elif event.key in (pygame.K_LEFT, pygame.K_a): np[1] -= 1
                elif event.key in (pygame.K_RIGHT, pygame.K_d): np[1] += 1
               

                if 0 <= np[0] < MAZE_SIZE and 0 <= np[1] < MAZE_SIZE and m[np[0]][np[1]] == 0:
                    p = np
       
                    if p == e:
                        won = True
      
                if event.key == pygame.K_r:
                    m = gen_maze()
                    p = [1, 1]
                    won = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN and not solving:
                if bfs_button_rect.collidepoint(event.pos):
                    solving = True
                    bfs(screen, m, tuple(p), tuple(e), cell_size, offset_x, offset_y)
                    solving = False
                if dfs_button_rect.collidepoint(event.pos):
                    solving = True
                    dfs(screen, m, tuple(p), tuple(e), cell_size, offset_x, offset_y)
                    solving = False
                if astar_button_rect.collidepoint(event.pos):
                    solving = True
                    astar(screen, m, tuple(p), tuple(e), cell_size, offset_x, offset_y)
                    solving = False
                if greedy_button_rect.collidepoint(event.pos):
                    solving = True
                    greedy(screen, m, tuple(p), tuple(e), cell_size, offset_x, offset_y)
                    solving = False

        draw_maze(screen, m, cell_size, offset_x, offset_y)

        pr = pygame.Rect(offset_x + p[1] * cell_size, offset_y + p[0] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (0, 0, 255), pr)  
        
        er = pygame.Rect(offset_x + e[1] * cell_size, offset_y + e[0] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (255, 165, 0), er)
      
        pygame.draw.rect(screen, (0, 0, 0), bfs_button_rect)
        text = font.render("BFS", True, (255, 255, 255))
        text_rect = text.get_rect(center=bfs_button_rect.center)
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, (0, 0, 0), dfs_button_rect)
        text = font.render("DFS", True, (255, 255, 255))
        text_rect = text.get_rect(center=dfs_button_rect.center)
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, (0, 0, 0), astar_button_rect)
        text = font.render("Astar", True, (255, 255, 255))
        text_rect = text.get_rect(center=astar_button_rect.center)
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, (0, 0, 0), greedy_button_rect)
        text = font.render("Greedy", True, (255, 255, 255))
        text_rect = text.get_rect(center=greedy_button_rect.center)
        screen.blit(text, text_rect)

        screen.blit(header, textrect)
        
        if won:
            win_text = font.render("Congratulations! You escaped the maze!", True, (255, 0, 0))
            win_rect = win_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 50))
            screen.blit(win_text, win_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()