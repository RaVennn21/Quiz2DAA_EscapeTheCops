import pygame
import os

# Helper to load and slice sprites
def load_sprites(path, width, height, is_player=True):
    if not os.path.exists(path):
        print(f"Sprite not found: {path}")
        return []
    
    sheet = pygame.image.load(path).convert_alpha()
    sheet_w, sheet_h = sheet.get_size()
    
    frame_width = sheet_w // 4
    frame_height = sheet_h // 2
    
    sprites = []
   
    row = 0 if is_player else 1
    
    for col in range(4):
        rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
      
        image = sheet.subsurface(rect)
        
        image = pygame.transform.scale(image, (width, height))
        sprites.append(image)
        
    return sprites

class Player(pygame.sprite.Sprite):
    def __init__(self, maze, cell_size, image_path="criminal_police.png"):
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

        
        # 0: Front/Down, 1: Right, 2: Back/Up, 3: Left
        self.sprites = load_sprites(image_path, self.player_size, self.player_size, is_player=True)
        
        # Default fallback if image fails
        if not self.sprites:
            surf = pygame.Surface((self.player_size, self.player_size))
            surf.fill((50, 120, 200))
            self.sprites = [surf] * 4

        self.current_image = self.sprites[0] # Default front
        self.rect = self.current_image.get_rect()
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
            new_x, new_y = self.player_x, self.player_y
            moved = False 
            
            # --- DIRECTIONAL MOVEMENT AND SPRITE SWAPPING ---
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                new_y -= 1
                moved = True
                self.current_image = self.sprites[2] # Back 
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                new_y += 1
                moved = True
                self.current_image = self.sprites[0] # Front 
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                new_x -= 1
                moved = True
                self.current_image = self.sprites[3] # Left 
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                new_x += 1
                moved = True
                self.current_image = self.sprites[1] # Right 
            
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
        surface.blit(self.current_image, self.rect)

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, cell_size, image_path="cake.png"):
        super().__init__()
        self.x = x
        self.y = y
        self.cell_size = cell_size
        
        self.rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        self.image = None

       
        if os.path.exists(image_path):
            try:
                raw_image = pygame.image.load(image_path).convert_alpha()
                icon_size = int(cell_size * 0.8)
                scaled_image = pygame.transform.scale(raw_image, (icon_size, icon_size))
                
                self.image = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                offset = (cell_size - icon_size) // 2
                self.image.blit(scaled_image, (offset, offset))
                print(f"Loaded coin image: {image_path}")
            except Exception as e:
                print(f"Error loading coin: {e}")

        if self.image is None:
            self.image = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            radius = int(cell_size * 0.3)
            pygame.draw.circle(self.image, (255, 215, 0), (cell_size//2, cell_size//2), radius)

class Police(pygame.sprite.Sprite):
    sprites = []

    def __init__(self, maze, start_x, start_y, mode="Easy"): 
        super().__init__()
        self.maze = maze
        self.policex = start_x
        self.policey = start_y
        self.mode = mode 
        self.cell_size = 40 
        
        if not Police.sprites:
            
            police_size = int(40 * 0.8)
            Police.sprites = load_sprites("criminal_police.png", police_size, police_size, is_player=False)

        # Default to front facing
        self.image = Police.sprites[0] if Police.sprites else None

    def move_towards_player(self, target_x, target_y):
        old_x, old_y = self.policex, self.policey

        if self.mode == "Hard":
            from maze_generator import astar
            path = astar(self.maze, (self.policex, self.policey), (target_x, target_y))
        else:
            from maze_generator import bfs
            path = bfs(self.maze, (self.policex, self.policey), (target_x, target_y))
            
        if len(path) > 1:
            self.policex, self.policey = path[1]
        
        # Update sprite facing
        if self.image:
            if self.policex > old_x:   self.image = Police.sprites[1] # Right
            elif self.policex < old_x: self.image = Police.sprites[3] # Left
            elif self.policey > old_y: self.image = Police.sprites[0] # Down
            elif self.policey < old_y: self.image = Police.sprites[2] # Up
    
    def update(self, player):
        self.move_towards_player(player.player_x, player.player_y)
        if (self.policex, self.policey) == (player.player_x, player.player_y):
            player.game_lost = True  
    
    def draw(self, surface, cell_size):
        police_size = int(cell_size * 0.8)
        padding = (cell_size - police_size) // 2
        
        if self.image:
            pos = (self.policex * cell_size + padding, self.policey * cell_size + padding)
            surface.blit(self.image, pos)
        else:
            rect = pygame.Rect(
                self.policex * cell_size + padding,
                self.policey * cell_size + padding,
                police_size,
                police_size
            )
            color = (200, 50, 50) if self.mode == "Easy" else (200, 0, 0) 
            pygame.draw.rect(surface, color, rect, border_radius=5)