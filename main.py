import pygame
from sys import exit
import random

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Nathan\'s Hungry Adventure')
clock = pygame.time.Clock()

background_surf = pygame.Surface((800, 400))
background_surf.fill('black')

movement_speed = 0
movement_acceleration = 1
movement_decceleration = 2
mouth_surf = pygame.Surface((50, 50))
mouth_surf.fill('Pink')
mouth_rect = mouth_surf.get_rect(midright = (100, 100))

mouth_move_down = False
mouth_down_button = False
mouth_move_up = False
mouth_up_button = False

food_surf = pygame.Surface((20, 20))
food_surf.fill('Brown')
food_rect = food_surf.get_rect(midleft = (800, 200))
food_speed = 8
food_speedup_threshold = 3
food_speed_increment = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                mouth_move_down = True
                mouth_down_button = True
                mouth_move_up = False
            if event.key == pygame.K_EQUALS:
                mouth_move_up = True
                mouth_move_down = False
                mouth_up_button = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_MINUS:
                mouth_move_down = False
                mouth_down_button = False
                if mouth_up_button == True:
                    mouth_move_up = True
            if event.key == pygame.K_EQUALS:
                mouth_move_up = False
                mouth_up_button = False
                if mouth_down_button == True:
                    mouth_move_down = True

    screen.blit(background_surf, (0,0))

    #MOUTH MOVEMENT LOGIC
    if mouth_move_down:
        if movement_speed < 0: movement_speed += movement_decceleration
        if movement_speed >= 0: movement_speed += movement_acceleration
        mouth_rect.y += movement_speed
    elif mouth_move_up:
        if movement_speed > 0: movement_speed -= movement_decceleration
        if movement_speed <= 0: movement_speed -= movement_acceleration
        mouth_rect.y += movement_speed
    else:
        if -2 < movement_speed < 2:
            movement_speed = 0
        if movement_speed > 0:
            movement_speed -= movement_decceleration
            mouth_rect.y += movement_speed
        if movement_speed < 0:
            movement_speed += movement_decceleration
            mouth_rect.y += movement_speed
    if mouth_rect.top < 0:
        mouth_rect.top = 0
        movement_speed = 0
    if mouth_rect.bottom > 400:
        mouth_rect.bottom = 400
        movement_speed = 0




    #FOOD LOGIC
    food_rect.x -= food_speed
    if food_rect.colliderect(mouth_rect):
        food_rect.x = 800
        food_rect.y = random.randint(10, 390)
        food_speedup_threshold -= 1
        if food_speedup_threshold == 0:
            food_speed += food_speed_increment
            food_speedup_threshold = 3
    if food_rect.x <= 0:
        food_rect.x = 800

    screen.blit(food_surf, food_rect)
    screen.blit(mouth_surf, mouth_rect)


    pygame.display.update()
    clock.tick(30)
