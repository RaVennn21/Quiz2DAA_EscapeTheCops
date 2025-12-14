import pygame
import sys
from main import start_game, SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()
pygame.mixer.init() 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game - Main Menu")
clock = pygame.time.Clock()

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (217, 13, 13) # Biru
GRAY = (100, 100, 100)
BLUE = (11, 47, 212)

# Font
title_font = pygame.font.Font(None, 70)
menu_font = pygame.font.Font(None, 50)

def draw_text_centered(text, font, color, y_offset):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)

def draw_text(text, font, color,x_offset, y_offset):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x_offset,SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)

def main_menu():
    global screen
    
    options = ["Easy Mode", "Hard Mode", "Quit"]
    selected_index = 0
    
    bg_image = None
    try:
        original_image = pygame.image.load("menu4.png")
        bg_image = pygame.transform.scale(original_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error:
        print("Gambar background tidak ditemukan.")
    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(50)

    try:
        pygame.mixer.music.load("menu_bgm.mp3")
        pygame.mixer.music.set_volume(0.5) 
        pygame.mixer.music.play(-1) 
    except pygame.error: pass

    while True:
        if bg_image:
            screen.blit(bg_image, (0, 0)) 
            screen.blit(overlay, (0, 0))  
        else:
            screen.fill(BLACK)
        
        draw_text("ESCAPE THE POLICE", title_font, WHITE, 700, -220)
        draw_text("Can you escape?", menu_font, GRAY, 700, -170)
        # draw_text("Can you escape?", menu_font , BLUE, 500, -200)
        
        for i, option in enumerate(options):
            color = HIGHLIGHT if i == selected_index else WHITE
            text = f"> {option} <" if i == selected_index else option
            draw_text(text, menu_font, color, 720, -80 + (i * 60))

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:

                    if selected_index == 0:
                        # EASY MODE
                        pygame.mixer.music.stop()
                        start_game("Easy") # Panggil dengan parameter Easy
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        pygame.display.set_caption("Maze Game - Main Menu")
                        try: pygame.mixer.music.play(-1)
                        except: pass
                        
                    elif selected_index == 1:
                        # HARD MODE
                        pygame.mixer.music.stop()
                        start_game("Hard") # Panggil dengan parameter Hard
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        pygame.display.set_caption("Maze Game - Main Menu")
                        try: pygame.mixer.music.play(-1)
                        except: pass
                        
                    elif selected_index == 2:
                        pygame.quit()
                        sys.exit()
        
        clock.tick(60)

if __name__ == "__main__":
    main_menu()