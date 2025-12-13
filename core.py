import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, maze, cell_size):
        super().__init__()
        self.maze = maze
        self.cell_size = cell_size
        
        self.player_x = 1
        self.player_y = 1
        
        self.player_size = int(cell_size * 0.8) 
        self.padding = (cell_size - self.player_size) // 2
        
        self.moves = 0
        self.game_won = False
        self.game_lost = False
        
        self.coins_collected = 0

        self.last_move_time = 0
        self.move_delay = 100 

        self.image = pygame.Surface((self.player_size, self.player_size))
        self.image.fill((50, 120, 200)) 
        
        self.rect = self.image.get_rect()
        self.update_rect_position()
    
    def update_rect_position(self):
        self.rect.x = self.player_x * self.cell_size + self.padding
        self.rect.y = self.player_y * self.cell_size + self.padding

    def can_move(self, x, y):
        if 0 <= x < self.maze.width and 0 <= y < self.maze.height:
            return not self.maze.is_wall(x, y)
        return False
    
    def update(self):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_move_time > self.move_delay:
            keys = pygame.key.get_pressed()
            new_x = self.player_x
            new_y = self.player_y
            moved = False 

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                new_y -= 1
                moved = True
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                new_y += 1
                moved = True
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                new_x -= 1
                moved = True
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                new_x += 1
                moved = True
            
            if moved:
                if self.can_move(new_x, new_y):
                    self.player_x = new_x
                    self.player_y = new_y
                    self.moves += 1
                    self.update_rect_position()
                    self.last_move_time = current_time 
                
            if self.maze.exit and (self.player_x, self.player_y) == self.maze.exit:
                self.game_won = True
    
    def draw(self, surface):
        pygame.draw.rect(surface, (50, 120, 200), self.rect, border_radius=5)

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, cell_size):
        super().__init__()
        self.x = x
        self.y = y
        self.cell_size = cell_size
        
        # make coin
        self.radius = int(cell_size * 0.3)
        self.image = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (cell_size//2, cell_size//2), self.radius)  
        
        self.rect = self.image.get_rect()
        self.rect.x = x * cell_size
        self.rect.y = y * cell_size

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
        police_size = int(cell_size * 0.8)
        padding = (cell_size - police_size) // 2
        
        rect = pygame.Rect(
            self.policex * cell_size + padding,
            self.policey * cell_size + padding,
            police_size,
            police_size
        )
        pygame.draw.rect(surface, (200, 50, 50), rect, border_radius=5)