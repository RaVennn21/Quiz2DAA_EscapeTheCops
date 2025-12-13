import random
from collections import deque

class Maze:
    def __init__(self, width, height):
        self.width = width // 2 * 2 + 1
        self.height = height // 2 * 2 + 1
        self.cells = [[True for x in range(self.width)] for y in range(self.height)]  
        self.exit = None
    
    def set_path(self, x, y):
        self.cells[y][x] = False
    
    def is_wall(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return False
    
    def create_maze(self, x, y):
        self.set_path(x, y)
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + 2*dx, y + 2*dy
            if self.is_wall(nx, ny):
                self.set_path(x + dx, y + dy)  
                self.create_maze(nx, ny)  

    def set_random_exit(self):
        border_cells = []
        
        for x in range(1, self.width - 1, 2):
            if not self.is_wall(x, 1): 
                border_cells.append((x, 1))
            if not self.is_wall(x, self.height - 2): 
                border_cells.append((x, self.height - 2))
        
        for y in range(1, self.height - 1, 2):
            if not self.is_wall(1, y): 
                border_cells.append((1, y))
            if not self.is_wall(self.width - 2, y): 
                border_cells.append((self.width - 2, y))
        
        start_pos = (1, 1)
        best_exit = None
        max_dist = -1

        for candidate in border_cells:
            path = bfs(self, start_pos, candidate)
            if path:
                dist = len(path)
                if dist > max_dist:
                    max_dist = dist
                    best_exit = candidate
        
        if best_exit:
            self.exit = best_exit
        else:
            self.exit = border_cells[-1] if border_cells else (self.width-2, self.height-2)
        
        self.set_path(*self.exit)
    
    def __str__(self):
        conv = {True: "██", False: "  "}
        rows = []
        for y, row in enumerate(self.cells):
            cells = []
            for x, c in enumerate(row):
                if self.exit and (x, y) == self.exit:
                    cells.append("EX")
                else:
                    cells.append(conv[c])
            rows.append("".join(cells))
        return "\n".join(rows)
    
    @staticmethod
    def add_loops(maze, loop_count):
        tries = 0
        added = 0
        max_tries = loop_count * 10  # Avoid infinite loop
        
        while added < loop_count and tries < max_tries:
            x = random.randrange(2, maze.width - 2, 2)
            y = random.randrange(2, maze.height - 2, 2)
            
            if maze.is_wall(x, y):
                if (not maze.is_wall(x-1, y) and not maze.is_wall(x+1, y) and maze.is_wall(x, y-1) and maze.is_wall(x, y+1)) or \
                   (not maze.is_wall(x, y-1) and not maze.is_wall(x, y+1) and maze.is_wall(x-1, y) and maze.is_wall(x+1, y)):
                    maze.set_path(x, y)
                    added += 1
            
            tries += 1

def bfs(maze, start, goal):
    queue = deque()
    queue.append((start, [start]))
    visited = set([start])
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == goal:
            return path
        
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze.width and 0 <= ny < maze.height and not maze.is_wall(nx, ny) and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
    
    return [start]
