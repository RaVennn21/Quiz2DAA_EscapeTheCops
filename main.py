import pygame
import sys
import random
from maze_generator import Maze, bfs
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
RED = (200, 50, 50)
DARK_GRAY = (60, 60, 60)
YELLOW = (255, 215, 0)
GRAY = (150, 150, 150)

# Global variables
screen = None
clock = None
font = None
large_font = None # Font baru untuk judul besar
maze = None
player = None
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
    status_text = f"Moves: {player.moves} | Coins: {player.coins_collected}/3"
    text = font.render(status_text, True, WHITE)
    screen.blit(text, (10, ui_y + 20))

# --- FUNGSI BARU: GAMBAR LAYAR AKHIR ---
def draw_end_screen(title, color, sub_text_str):
    # 1. Fill layar hitam penuh
    screen.fill(BLACK)
    
    # 2. Gambar Judul Besar (Tengah)
    title_surf = large_font.render(title, True, color)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(title_surf, title_rect)
    
    # 3. Gambar Info Tambahan
    info_surf = font.render(f"Moves: {player.moves} | Coins Collected: {player.coins_collected}", True, WHITE)
    info_rect = info_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
    screen.blit(info_surf, info_rect)

    # 4. Gambar Instruksi (Retry/Quit)
    sub_surf = font.render(sub_text_str, True, GRAY)
    sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(sub_surf, sub_rect)

def initialize_game():
    global maze, player, coins_group, policelist, police_group
    
    maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
    maze.create_maze(1, 1)
    maze.set_random_exit()
    Maze.add_loops(maze, loop_count=10)
    
    player = Player(maze, CELL_SIZE)
    
    # --- SPAWN COINS ---
    coins_group = pygame.sprite.Group()
    placed_coins = 0
    while placed_coins < 3:
        cx = random.randint(1, MAZE_WIDTH - 2)
        cy = random.randint(1, MAZE_HEIGHT - 2)
        if not maze.is_wall(cx, cy) and (cx, cy) != (1, 1) and (cx, cy) != maze.exit:
             is_stack = False
             for c in coins_group:
                 if c.x == cx and c.y == cy:
                     is_stack = True
             if not is_stack:
                coin = Coin(cx, cy, CELL_SIZE)
                coins_group.add(coin)
                placed_coins += 1

    # --- SPAWN POLICE ---
    policelist = [] 
    numpolice = 2 
    police_group = pygame.sprite.Group() 
    candidate_cells = []
    min_safe_dist = (MAZE_WIDTH + MAZE_HEIGHT) // 2 
    
    for y in range(maze.height):
        for x in range(maze.width):
            if not maze.is_wall(x, y):
                path = bfs(maze, (1, 1), (x, y))
                if path and len(path) > min_safe_dist:
                    candidate_cells.append((x, y))

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
    global screen, clock, font, large_font
    
    pygame.init()
    try:
        pygame.mixer.init()
    except:
        pass
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game - Collect 3 Coins!")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    large_font = pygame.font.Font(None, 80) # Font besar untuk Game Over

    # Music Play
    try:
        pygame.mixer.music.load("bgm.mp3")
        pygame.mixer.music.set_volume(0.4) 
        pygame.mixer.music.play(-1) 
    except pygame.error:
        pass

    initialize_game()
    
    running = True
    police_timer = 0 
    
    # Variabel status warna teks
    warning_timer = 0 

    while running:
        dt = clock.tick(60)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # ==========================================
        # LOGIKA PERCABANGAN (STATE MACHINE SIMPEL)
        # ==========================================
        
        # KONDISI 1: KALAH (GAME OVER)
        if player.game_lost:
            # Gambar layar hitam penuh
            draw_end_screen("GAME OVER", RED, "Press R to Retry, ESC to Menu")
            
            # Input hanya untuk R atau ESC
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                initialize_game()
            if keys[pygame.K_ESCAPE]:
                running = False

        # KONDISI 2: MENANG (VICTORY)
        # Cek menang hanya jika koin cukup.
        elif player.game_won and player.coins_collected >= 3:
            # Gambar layar hitam penuh
            draw_end_screen("VICTORY!", GREEN, "Press R to Replay, ESC to Menu")
            
            # Input hanya untuk R atau ESC
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                initialize_game()
            if keys[pygame.K_ESCAPE]:
                running = False

        # KONDISI 3: GAME MASIH JALAN
        else:
            # --- UPDATE ---
            police_timer += dt
            
            # Player hanya diupdate di sini (jadi kalau menang/kalah, dia ga gerak)
            player.update()
            
            # Cek Koin
            collected = pygame.sprite.spritecollide(player, coins_group, True)
            if collected:
                player.coins_collected += len(collected)

            # Cek Polisi
            if police_timer >= 250:
                for police in policelist:
                    police.update(player)
                police_timer = 0

            # Cek Exit tapi Koin Kurang
            # Jika player nyentuh exit (game_won True) tapi koin kurang
            if player.game_won and player.coins_collected < 3:
                player.game_won = False # Reset biar ga stuck dan ga trigger win screen
                warning_timer = 60 # Set timer untuk tulisan peringatan (60 frame / 1 detik)

            # --- DRAWING (GAMEPLAY) ---
            screen.fill(WHITE)
            draw_maze()
            coins_group.draw(screen)
            player.draw(screen)
            for police in policelist:
                police.draw(screen, CELL_SIZE)
            draw_ui()

            # Gambar tulisan peringatan jika ada
            if warning_timer > 0:
                warn_text = font.render("Collect all coins first!", True, RED)
                # Tampilkan di atas kepala player
                screen.blit(warn_text, (player.rect.x - 40, player.rect.y - 30))
                warning_timer -= 1
            
            # Tombol ESC saat main (Pause/Back)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False

        pygame.display.flip()

    pygame.mixer.music.stop()
    return

if __name__ == "__main__":
    start_game()