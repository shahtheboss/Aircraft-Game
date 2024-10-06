import pygame, sys
import random
import math
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Menu")

BG = pygame.image.load(r"C:\Users\bigno\OneDrive\Python\SASE Hack\assets\Background-1.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(r"C:\Users\bigno\OneDrive\Python\SASE Hack\assets\font.ttf", size)

def play():
    while True:

        PLAY_MOUSE_POS = pygame.mouse.get_pos()  

        SCREEN.fill("black")
    
        Width = 1600
        Height = 900
        bw = 100
        bh = 100

        display_surface = pygame.display.set_mode((Width, Height))
        pygame.display.set_caption('Design Your Plane!')

        back = pygame.image.load(r"C:\Users\bigno\OneDrive\Python\SASE Hack\design_board.png")
        back = pygame.transform.scale(back, (Width, Height))

        g_size = 25
        snap_dist = 25
        active_box = None

        # Initialize box colors
        colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta']  # 8 colors total

        boxes = []
        starting_x_left = 75  # Starting x position for the first set of boxes
        starting_x_right = Width - 75 - bw  # Starting x position for the second set of boxes
        starting_y = 200  # Starting y position for all boxes
        vertical_spacing = 100/3  # Define vertical spacing between boxes

        # Create and position the boxes on the left
        for i in range(4):
            x = starting_x_left  # X position remains the same
            y = starting_y + (bh + vertical_spacing) * i  # Position boxes with vertical spacing
            box = pygame.Rect(x, y, bw, bh)
            boxes.append(box)

        # Create and position the boxes on the right
        for i in range(4):
            x = starting_x_right  # X position remains the same
            y = starting_y + (bh + vertical_spacing) * i  # Position boxes with vertical spacing
            box = pygame.Rect(x, y, bw, bh)
            boxes.append(box)

        # Store original positions for resetting
        original_positions = [box.topleft for box in boxes]

        def collision(moving_box, all_boxes):
            for box in all_boxes:
                if box != moving_box and box.colliderect(moving_box):
                    return True
            return False

        def grid(box):
            snap_x = round(box.x / g_size) * g_size
            snap_y = round(box.y / g_size) * g_size
            if abs(box.x - snap_x) <= snap_dist:
                box.x = snap_x
            if abs(box.y - snap_y) <= snap_dist:
                box.y = snap_y

        def reset_boxes():
            for i, box in enumerate(boxes):
                box.topleft = original_positions[i]

        run = True
        while run:
            display_surface.blit(back, (0, 0))
            
            for i, box in enumerate(boxes):
                pygame.draw.rect(display_surface, colors[i], box)  # Draw each box with its color

            # Draw reset button
            reset_button = pygame.Rect(Width - 150, 20, 130, 50)  # Define button position and size
            pygame.draw.rect(display_surface, 'gray', reset_button)  # Draw the button
            font = pygame.font.Font(None, 36)
            text_surface = font.render('Reset', True, 'white')
            text_rect = text_surface.get_rect(center=reset_button.center)
            display_surface.blit(text_surface, text_rect)  # Draw the text

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Check if reset button is clicked
                        if reset_button.collidepoint(event.pos):
                            reset_boxes()
                        else:
                            for num, box in enumerate(boxes):
                                if box.collidepoint(event.pos):
                                    active_box = num
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and active_box is not None:
                        grid(boxes[active_box])
                        active_box = None
                
                if event.type == pygame.MOUSEMOTION:
                    if active_box is not None:
                        original_position = boxes[active_box].topleft
                        boxes[active_box].move_ip(event.rel)

                        if collision(boxes[active_box], boxes):
                            boxes[active_box].topleft = original_position
                
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.flip()

        pygame.quit()

#def test():
#    while True:

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(800, 240))

        PLAY_BUTTON = Button(image=pygame.image.load(r"C:\Users\bigno\OneDrive\Python\SASE Hack\assets\Play Rect.png"), pos=(800, 490), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(r"C:\Users\bigno\OneDrive\Python\SASE Hack\assets\Quit Rect.png"), pos=(800, 690), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
