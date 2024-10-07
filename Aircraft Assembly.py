import pygame, sys
import math
import random
import tkinter as tk
from tkinter import messagebox
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1600, 900))

BG = pygame.image.load(r"File Path For Background-1.png") # INSERT FILE HERE

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(r"File Path For font.ttf", size) # INSERT FILE HERE

def play():
    Width = 1600 # sets the design space to width of 1600
    Height = 900 # sets the design space to height of 900
    bw = 100 # size of each box
    bh = 100

    display_surface = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption('Design Your Plane!')

    back = pygame.image.load(r"File Path For design_board.png") # INSERT FILE HERE
    back = pygame.transform.scale(back, (Width, Height))

    # Load images for the boxes (replace these paths with your image files)
    image_paths = [
        r"File Path For part1.png",
        r"File Path For part2.png",
        r"File Path For part-3.png",
        r"File Path For part4.png",
        r"File Path For part-5.png",
        r"File Path For part6.png",
        r"File Path For part7.png",
        r"File Path For part8.png"]
    
    images = [pygame.image.load(path) for path in image_paths]
    resized_images = [pygame.transform.scale(image, (bw, bh)) for image in images]  # Resize images to fit the box size

    boxes = []
    starting_x_left = 75
    starting_x_right = Width - 75 - bw
    starting_y = 200
    vertical_spacing = 25

    # Left-hand side inventory
    for i in range(4):  # This will make 4 boxes with spacing of 25
        x = starting_x_left
        y = starting_y + (bh + vertical_spacing) * i
        box = pygame.Rect(x, y, bw, bh)
        boxes.append(box)

    # Right-hand side inventory
    for i in range(4):
        x = starting_x_right
        y = starting_y + (bh + vertical_spacing) * i
        box = pygame.Rect(x, y, bw, bh)
        boxes.append(box)

    original_positions = [box.topleft for box in boxes]

    # checks if box controlled by cursor comes in contact with a stationary block
    def collision(moving_box, all_boxes):
        for box in all_boxes:
            if box != moving_box and box.colliderect(moving_box):
                return True
        return False

    g_size = 25 # this defines the grid size
    snap_dist = 25 # how close the block is to the edge of grid before "snapping"
    active_box = None

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

    def show_popup():
        # 50-50 chance of success or failure
        if random.choice([True, False]):  # True = success, False = failure
            # Success popup
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Flight Status", "Congrats, your aircraft flies!")
            root.destroy()
        else:
            # Failure popup
            root = tk.Tk()
            root.withdraw()
            messagebox.showwarning("Flight Status", "Oops, the aircraft did not fly. Try again!")
            root.destroy()

    # Define the green button
    button_radius = 35  # Radius of the circle
    button_x, button_y = (19 * 50), (16 * 50)  # Position of the center of the circle

    def is_point_in_circle(point, circle_center, radius):
        # Check if a point (mouse click) is inside the circle using the distance formula
        return math.sqrt((point[0] - circle_center[0]) ** 2 + (point[1] - circle_center[1]) ** 2) <= radius

    run = True
    while run:
        display_surface.blit(back, (0, 0))

        # Display each image in its corresponding box
        for i, box in enumerate(boxes):
            display_surface.blit(resized_images[i], box)  # Draw the image inside the box

        # Draw reset button
        reset_button = pygame.Rect(Width - 150, 20, 130, 50)  # Define button position and size
        pygame.draw.rect(display_surface, 'gray', reset_button)  # Draw the button
        font = pygame.font.Font(None, 36)
        text_surface = font.render('Reset', True, 'white')
        text_rect = text_surface.get_rect(center=reset_button.center)
        display_surface.blit(text_surface, text_rect)  # Draw the text

        # Draw back button
        back_button = pygame.Rect(Width - 1580, 20, 130, 50)  # Define button position and size
        pygame.draw.rect(display_surface, 'red', back_button)  # Draw the button
        font = pygame.font.Font(None, 36)
        text_surface = font.render('Back', True, 'white')
        text_rect = text_surface.get_rect(center=back_button.center)
        display_surface.blit(text_surface, text_rect)  # Draw the text

        # Draw the green circular button
        pygame.draw.circle(display_surface, 'green', (button_x, button_y), button_radius)  # Draw the green button
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render('Click', True, 'white')
        button_text_rect = button_text.get_rect(center=(button_x, button_y))
        display_surface.blit(button_text, button_text_rect)  # Draw text in the circle

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left-click
                    # Check if reset button is clicked
                    if reset_button.collidepoint(event.pos):
                        reset_boxes()
                    # Check if back button is clicked
                    elif back_button.collidepoint(event.pos):
                        return  # Go back to the main menu
                    # Check if the green circular button is clicked
                    elif is_point_in_circle(event.pos, (button_x, button_y), button_radius):
                        show_popup()  # Show the popup when the green button is clicked
                    else:
                        for num, box in enumerate(boxes):
                            if box.collidepoint(event.pos):
                                active_box = num
            # allow to select the airplane piece by pressing mouse down
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and active_box is not None:
                    grid(boxes[active_box])
                    active_box = None

            # allow to drag the airplane piece around
            if event.type == pygame.MOUSEMOTION:
                if active_box is not None:
                    original_position = boxes[active_box].topleft
                    boxes[active_box].move_ip(event.rel)

                    if collision(boxes[active_box], boxes):
                        boxes[active_box].topleft = original_position

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos() # track mouse position in main menu

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b56e18")
        MENU_RECT = MENU_TEXT.get_rect(center=(800, 170))

        PLAY_BUTTON = Button(image=pygame.image.load(r"File Path For Play Rect.png"), pos=(800, 350), # INSERT FILE HERE
                            text_input="PLAY", font=get_font(75), base_color="White", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(r"File Path For Quit Rect.png"), pos=(800, 690), # INSERT FILE HERE
                            text_input="QUIT", font=get_font(75), base_color="White", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS): # play() is called if button is clicked - move to the game screen
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS): # quit button closes program
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
