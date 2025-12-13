import pygame
import sys
import random
from maze_generator import Maze, bfs
# Jangan lupa import Coin
from core import Player, Police, Coin

# --- CONSTANTS ---
CELL_SIZE = 40
MAZE_WIDTH = 25
MAZE_HEIGHT = 15
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE + 60

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 120, 200)
GREEN = (50, 200, 50)
DARK_GRAY = (60, 60, 60)
YELLOW = (255, 215, 0) # Warna teks koin

# Global variables
screen = None
clock = None
font = None
maze = None
player = None
# Group untuk Koin
coins_group = None 
policelist = []
police_group = None

def draw_maze():
    for y in range(maze.height):
        for x in range(maze.width):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze.is_wall(x, y):
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            if maze.exit and (x, y) == maze.exit:
                pygame.draw.rect(screen, GREEN, rect)

def draw_ui():
    ui_y = MAZE_HEIGHT * CELL_SIZE
    pygame.draw.rect(screen, DARK_GRAY, (0, ui_y, SCREEN_WIDTH, 60))
    
    # UI Text diperbarui ada info Coin
    status_text = f"Moves: {player.moves} | Coins: {player.coins_collected}/3"
    text = font.render(status_text, True, WHITE)
    screen.blit(text, (10, ui_y + 20))

def initialize_game():
    global maze, player, coins_group, policelist, police_group
    
    maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
    maze.create_maze(1, 1)
    
    # 1. Exit sekarang otomatis cari yang terjauh
    maze.set_random_exit()
    Maze.add_loops(maze, loop_count=10)
    
    player = Player(maze, CELL_SIZE)
    
    # --- SPAWN COINS (3 Biji) ---
    coins_group = pygame.sprite.Group()
    placed_coins = 0
    while placed_coins < 3:
        cx = random.randint(1, MAZE_WIDTH - 2)
        cy = random.randint(1, MAZE_HEIGHT - 2)
        
        # Syarat spawn koin:
        # 1. Bukan tembok
        # 2. Bukan posisi player (1,1)
        # 3. Bukan posisi exit
        # 4. Belum ada koin disitu (cek manual sederhana atau collision nanti)
        if not maze.is_wall(cx, cy) and (cx, cy) != (1, 1) and (cx, cy) != maze.exit:
             # Cek biar ga numpuk sama koin lain
             is_stack = False
             for c in coins_group:
                 if c.x == cx and c.y == cy:
                     is_stack = True
             
             if not is_stack:
                coin = Coin(cx, cy, CELL_SIZE)
                coins_group.add(coin)
                placed_coins += 1

    # --- SPAWN POLICE (Lebih Jauh) ---
    policelist = [] 
    numpolice = 2 
    police_group = pygame.sprite.Group() 

    candidate_cells = []
    # Kita cari kandidat yang jaraknya > setengah lebar map + setengah tinggi map (Jauh banget)
    min_safe_dist = (MAZE_WIDTH + MAZE_HEIGHT) // 2 
    
    for y in range(maze.height):
        for x in range(maze.width):
            if not maze.is_wall(x, y):
                path = bfs(maze, (1, 1), (x, y))
                # Spawn polisi harus jauh dari player, tapi jangan di dalam tembok
                if path and len(path) > min_safe_dist:
                    candidate_cells.append((x, y))

    # Kalau map kekecilan dan ga nemu tempat jauh, kurangi syarat jarak
    if len(candidate_cells) < numpolice:
        candidate_cells = []
        fallback_dist = 10
        for y in range(maze.height):
            for x in range(maze.width):
                if not maze.is_wall(x, y):
                    path = bfs(maze, (1, 1), (x, y))
                    if path and len(path) > fallback_dist:
                        candidate_cells.append((x, y))

    random.shuffle(candidate_cells)
    for i in range(numpolice):
        if i < len(candidate_cells):
            px, py = candidate_cells[i]
            police = Police(maze, px, py)
            policelist.append(police)
            police_group.add(police)

def start_game():
    global screen, clock, font
    
    pygame.init()
    try:
        pygame.mixer.init()
    except:
        pass
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game - Collect 3 Coins!")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    try:
        pygame.mixer.music.load("bgm.mp3")
        pygame.mixer.music.set_volume(0.4) 
        pygame.mixer.music.play(-1) 
    except pygame.error:
        pass

    initialize_game()
    
    running = True
    police_timer = 0 

    while running:
        dt = clock.tick(60) 
        police_timer += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        player.update()
        
        # --- LOGIC MAKAN KOIN ---
        # Cek tabrakan player dengan grup koin
        # Dokum: spritecollide(sprite, group, dokill) -> dokill=True artinya koin dihapus
        collected = pygame.sprite.spritecollide(player, coins_group, True)
        if collected:
            player.coins_collected += len(collected)
            # Opsional: Bisa tambah sfx coin disini
        # ------------------------

        if police_timer >= 250 and not player.game_won and not player.game_lost:
            for police in policelist:
                police.update(player)
            police_timer = 0
        
        screen.fill(WHITE)
        draw_maze()
        
        # Gambar Koin
        coins_group.draw(screen)
        
        player.draw(screen)
        
        for police in policelist:
            police.draw(screen, CELL_SIZE)
        
        draw_ui()
        
        # LOGIKA MENANG (Harus exit DAN koin 3)
        # Kalau kamu mau "Boleh exit asal 3 koin", pakai logika di bawah:
        if player.game_won:
            # Cek Koin dulu
            if player.coins_collected < 3:
                # Kalau koin belum cukup, jangan menang dulu! (Batalkan menang)
                player.game_won = False
                # Tampilkan pesan "Need more coins" (bisa di UI atau popup simpel)
                need_text = font.render("Collect all coins first!", True, (255, 0, 0))
                screen.blit(need_text, (player.rect.x - 20, player.rect.y - 20))
            else:
                # Menang beneran
                victory_text = font.render(f"VICTORY! Moves: {player.moves}", True, GREEN)
                sub_text = font.render("Press R to Replay, ESC to Menu", True, GREEN)
                
                center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                pygame.draw.rect(screen, BLACK, (center_x - 200, center_y - 60, 400, 120))
                
                screen.blit(victory_text, (center_x - 100, center_y - 30))
                screen.blit(sub_text, (center_x - 150, center_y + 10))
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    running = False 
                if keys[pygame.K_r]:
                    initialize_game()
        
        if player.game_lost:
            lost_text = font.render("CAUGHT! You lost!", True, (255, 0, 0))
            sub_text = font.render("Press R to Retry, ESC to Menu", True, (255, 0, 0))
            
            center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            pygame.draw.rect(screen, BLACK, (center_x - 200, center_y - 60, 400, 120))
            
            screen.blit(lost_text, (center_x - 130, center_y - 30))
            screen.blit(sub_text, (center_x - 150, center_y + 10))
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
            if keys[pygame.K_r]:
                initialize_game()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and not player.game_won and not player.game_lost:
            running = False

        pygame.display.flip()

    pygame.mixer.music.stop()
    return

if __name__ == "__main__":
    start_game()