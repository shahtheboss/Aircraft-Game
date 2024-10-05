import pygame
import random
import math

pygame.init()

Width = 1600
Height = 900

display_surface = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Design Your Plane!')

back = pygame.image.load("c:/Users/mlego/Desktop/THE GAME YEAHHHHHHH/design_board.png")
back = pygame.transform.scale(back, (Width, Height))

g_size = 50
snap_dist = 50

active_box = None
boxes = []
for i in range(7):
    x = random.randint(250, 1150)
    y = random.randint(250, 550)
    w = 100
    h = 100
    box = pygame.Rect(x, y, w, h)
    boxes.append(box)

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

run = True
while run:
    display_surface.blit(back, (0, 0))
    
    for box in boxes:
        pygame.draw.rect(display_surface, 'red', box)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
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
