import pygame

CELL_SIZE = 20

class Player(pygame.sprite.Sprite):
    def __init__(self, maze, cell_size=20):
        super().__init__()
        self.maze = maze
        self.cell_size = cell_size
        

        self.player_x = 1
        self.player_y = 1
        self.player_size = cell_size - 6
        

        self.moves = 0
        self.game_won = False
        self.game_lost = False

        self.image = pygame.Surface((self.player_size, self.player_size))
        self.image.fill((50, 120, 200))
        self.rect = self.image.get_rect(
            x=self.player_x * cell_size + 3,
            y=self.player_y * cell_size + 3
        )
    
    def can_move(self, x, y):
        """Check if can move to position"""
        if 0 <= x < self.maze.width and 0 <= y < self.maze.height:
            return not self.maze.is_wall(x, y)
        return False
    
    def update(self):
        """Update player position based on keyboard input"""
        keys = pygame.key.get_pressed()
        new_x = self.player_x
        new_y = self.player_y
        
        # Handle movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= 1
            self.moves += 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += 1
            self.moves += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= 1
            self.moves += 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += 1
            self.moves += 1
        

        if self.can_move(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y
            

            self.rect.x = self.player_x * self.cell_size + 3
            self.rect.y = self.player_y * self.cell_size + 3
        

        if self.maze.exit and (self.player_x, self.player_y) == self.maze.exit:
            self.game_won = True
    
    def draw(self, surface):
        """Draw player on surface"""
        rect = pygame.Rect(
            self.player_x * self.cell_size + 3,
            self.player_y * self.cell_size + 3,
            self.player_size,
            self.player_size
        )
        pygame.draw.rect(surface, (50, 120, 200), rect, border_radius=5)

class Police(pygame.sprite.Sprite):
    def __init__(self, maze, start_x, start_y):
        super().__init__()
        self.maze = maze
        self.policex = start_x
        self.policey = start_y
    
    def move_towards_player(self, target_x, target_y):
        from maze_generator import bfs
        path = bfs(self.maze, (self.policex, self.policey), (target_x, target_y))
        if len(path) > 1:
            self.policex, self.policey = path[1]
    
    def update(self, player):
        self.move_towards_player(player.player_x, player.player_y)
        if (self.policex, self.policey) == (player.player_x, player.player_y):
            player.game_lost = True  
    
    def draw(self, surface, cell_size):
        police_size = cell_size - 6
        rect = pygame.Rect(
            self.policex * cell_size + 3,
            self.policey * cell_size + 3,
            police_size,
            police_size
        )
        pygame.draw.rect(surface, (200, 50, 50), rect, border_radius=5)
