import pygame
import sys
import os

import tkinter as tk
from tkinter import filedialog

import game
from game import start_game, SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()
pygame.mixer.init() 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Escape The Police!")
clock = pygame.time.Clock()

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (217, 13, 13) # Biru
GRAY = (100, 100, 100)
BLUE = (11, 47, 212)
GREEN = (50, 200, 50)

# Font
title_font = pygame.font.Font(None, 70)
menu_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

def draw_text_centered(text, font, color, y_offset):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)

def draw_text(text, font, color,x_offset, y_offset):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x_offset,SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)

def select_image_file():
    root = tk.Tk()
    root.withdraw() 
    
    root.attributes('-topmost', True)
    
    file_path = filedialog.askopenfilename(
        title="Select Player Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")] 
    )
    
    root.destroy() 
    
    if file_path:
        game.PLAYER_IMAGE_PATH = file_path
        print(f"Selected image: {game.PLAYER_IMAGE_PATH}")
        return True 
    return False 

def main_menu():
    global screen
    
    options = ["Easy", "Hard", "Endless","Custom Image", "Quit"]
    selected_index = 0

    image_status_text = ""
    
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
        
        draw_text("ESCAPE THE POLICE", title_font, WHITE, 500, -270)
        # draw_text("Pick diff", menu_font, GRAY, 700, -170)
        # draw_text("Can you escape?", menu_font , BLUE, 500, -200)
        
        for i, option in enumerate(options):
            color = HIGHLIGHT if i == selected_index else WHITE
            text = f"> {option} <" if i == selected_index else option
            draw_text(text, menu_font, color, 720, -150 + (i * 60))

        if game.PLAYER_IMAGE_PATH:
            filename = os.path.basename(game.PLAYER_IMAGE_PATH)
            status_msg = f"Using custom image: {filename}"
            draw_text(status_msg, small_font, GREEN, 500, 250) 

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
                    
                    if selected_index == 3:
                        if select_image_file():
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    
                    elif selected_index == 4:
                        pygame.quit()
                        sys.exit()
                        
                    else:
                        pygame.mixer.music.stop()
                        
                        if selected_index == 0: start_game("Easy")
                        elif selected_index == 1: start_game("Hard")
                        elif selected_index == 2: start_game("Endless")
                        
                        # Balik ke Menu
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        pygame.display.set_caption("Maze Game - Main Menu")
                        try: pygame.mixer.music.play(-1)
                        except: pass
        
        clock.tick(60)

if __name__ == "__main__":
    main_menu()