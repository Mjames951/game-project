import pygame
from sys import exit
import random

#PYGAME INITIALIZING
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Nathan\'s Hungry Adventure')
clock = pygame.time.Clock()

#GAME LOGIC VARIABLES
instructions = False
player_lives = 3
game_active = False
score = 0
first_game = True
highscore = 20
bad_food_in = False

#CHARACTER MOVEMENT NUMBERS
movement_speed = 0
movement_acceleration = 1
movement_decceleration = 2

#FOOD MOVEMENT VARIABLES
food_starter_speed = 9
food_speedup_threshold = 3
food_speed_increment = 2
food_max_speed = 23
food_speed = food_starter_speed

#CHARACTER MOVEMENT VARIABLES
mouth_move_down = False
mouth_down_button = False
mouth_move_up = False
mouth_up_button = False

#BACKGROUND STUFF
background_surf = pygame.Surface((800, 400))
background_surf.fill('White')
background_rect = background_surf.get_rect(midtop = (400, 0))
top_background_surf = pygame.Surface((800, 30))
top_background_surf.fill('Black')
top_background_rect = top_background_surf.get_rect(midtop = (400, 0))

#STARTING/LOST SCREEN
game_font = pygame.font.Font(None, 50)
start_surf = game_font.render('PRESS ENTER KEY TO START', True, 'Black')
start_rect = start_surf.get_rect(midtop = (400, 200))
controls_surf = game_font.render('PRESS \'X\' FOR INSTRUCTIONS', True, 'Black')
controls_rect = controls_surf.get_rect(midtop = (400, 100))
lost_surf = game_font.render('YOU LOST', True, 'Red')
lost_rect = lost_surf.get_rect(midtop = (400, 20))
won_surf = game_font.render('YOU WON', True, 'Green')
won_rect = won_surf.get_rect(midtop = (400, 20))
won_backsurf = pygame.Surface((200, 30))
won_backrect = won_backsurf.get_rect(midtop = (400, 20))
highscore_surf = game_font.render(f'HIGH SCORE IS: {highscore}', True, 'Black')
highscore_rect = highscore_surf.get_rect(midtop = (400, 40))

#INSTRUCTIONS SCREEN
instructions_text_surf_pt1 = game_font.render('USE ARROW KEYS TO MOVE UP AND DOWN', True, 'Black')
insructions_text_rect_pt1 = instructions_text_surf_pt1.get_rect(midtop = (400, 100))
instructions_text_surf_pt2 = game_font.render('TOUCH PURPLE CUBES', True, 'Black')
insructions_text_rect_pt2 = instructions_text_surf_pt2.get_rect(midtop = (400, 130))
instructions_text_surf_pt3 = game_font.render('AVOID RED ONES', True, 'Black')
insructions_text_rect_pt3 = instructions_text_surf_pt3.get_rect(midtop = (400, 160))
return_text_surf = game_font.render('PRESS \'X\' TO RETURN TO HOME SCREEN', True, 'Black')
return_text_rect = return_text_surf.get_rect(midtop = (400, 300))

#CHARACTER SIZE AND LOOKS
mouth_surf = pygame.Surface((50, 50))
mouth_surf.fill('DarkOrange')
mouth_rect = mouth_surf.get_rect(midright = (100, 200))

#FOOD SIZE AND LOOKS
food_surf = pygame.Surface((20, 20))
food_surf.fill('Purple')
food_rect = food_surf.get_rect(midleft = (800, 200))

#BAD FOOD SIZE AND LOOKS
bad_surf = pygame.Surface((30, 30))
bad_surf.fill('Red')
bad_rect = bad_surf.get_rect(midleft = (800, 200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #CHARACTER CONTROLS
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    mouth_move_down = True
                    mouth_down_button = True
                    mouth_move_up = False
                if event.key == pygame.K_UP:
                    mouth_move_up = True
                    mouth_move_down = False
                    mouth_up_button = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    mouth_move_down = False
                    mouth_down_button = False
                    if mouth_up_button == True:
                        mouth_move_up = True
                if event.key == pygame.K_UP:
                    mouth_move_up = False
                    mouth_up_button = False
                    if mouth_down_button == True:
                        mouth_move_down = True

        #START SCREEN AND RESET MECHANICS
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_active = True
                    first_game = False
                    player_lives = 3

                    mouth_rect.right = 100
                    food_speed = food_starter_speed

                    if score > highscore:
                        highscore = score

                    score = 0
                    insructions = False

                #CHANGING TO AND FROM INSTRUCTION SCREEN
                if event.key == pygame.K_x:
                    if instructions == False:
                        instructions = True
                    else:
                        instructions = False

    if game_active:

        # putting in the background
        screen.blit(background_surf, background_rect)
        screen.blit(top_background_surf, top_background_rect)

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
        if mouth_rect.top < 30:
            mouth_rect.top = 30
            movement_speed = 0
        if mouth_rect.bottom > 400:
            mouth_rect.bottom = 400
            movement_speed = 0

        screen.blit(mouth_surf, mouth_rect)

        #FOOD LOGIC
        food_rect.x -= food_speed
        if food_rect.colliderect(mouth_rect):
            score += 1
            food_rect.x = 800
            food_rect.y = random.randint(40, 380)
            food_speedup_threshold -= 1
            if food_speedup_threshold <= 0:
                if food_speed <= food_max_speed:
                    food_speed += food_speed_increment
                    food_speedup_threshold = 3
        if food_rect.x <= -20:
            food_rect.x = 800
            player_lives -= 1
            if player_lives <= 0:
                game_active = False

        screen.blit(food_surf, food_rect)

        #BAD FOOD LOGIC
        if score >= 10:
            if 350 <= food_rect.x <= 450 and bad_food_in == False:
                bad_food_in = True
            if bad_food_in == True:
                bad_rect.x -= food_speed
                if bad_rect.colliderect(mouth_rect):
                    player_lives -= 1
                    bad_rect.x = 800
                    bad_rect.y = random.randint(40, 380)
                    bad_food_in = False
                    if player_lives <= 0:
                        game_active = False
                if bad_rect.x <= -20:
                    bad_rect.x = 800
                    bad_food_in = False
        else:
            bad_rect.x = 800

        screen.blit(bad_surf, bad_rect)

        #INGAME TEXT
        game_score_surf = game_font.render(f'SCORE: {score}', True, 'White')
        game_score_rect = game_score_surf.get_rect(topright = (800, 0))
        game_lives_surf = game_font.render(f'LIVES: {player_lives}', True, 'Red')
        game_lives_rect = game_lives_surf.get_rect(topleft = (0,0))
        screen.blit(game_lives_surf, game_lives_rect)
        screen.blit(game_score_surf, game_score_rect)
    else:

        if instructions == False:
            #start screen
            screen.blit(background_surf, background_rect)
            screen.blit(start_surf, start_rect)
            if first_game == False:

                highscore_surf = game_font.render(f'SCORE TO BEAT IS: {highscore}', True, 'Black')
                highscore_rect = highscore_surf.get_rect(midtop=(400, 70))
                if score > highscore:
                    screen.blit(won_backsurf, won_backrect)
                    screen.blit(won_surf, won_rect)
                    score_surf = game_font.render(f'NEW HIGH SCORE IS {score} POINTS', True, 'Black')
                    score_rect = score_surf.get_rect(midbottom=(400, 380))
                else:
                    screen.blit(lost_surf, lost_rect)
                    screen.blit(highscore_surf, highscore_rect)
                    score_surf = game_font.render(f'YOU SCORED {score} POINTS', True, 'Black')
                    score_rect = score_surf.get_rect(midbottom=(400, 380))
                screen.blit(score_surf, score_rect)
            else:
                screen.blit(controls_surf, controls_rect)
                screen.blit(highscore_surf, highscore_rect)
        else:
            #INSTRUCTIONS SCREEN
            screen.blit(background_surf, background_rect)
            screen.blit(instructions_text_surf_pt1, insructions_text_rect_pt1)
            screen.blit(instructions_text_surf_pt2, insructions_text_rect_pt2)
            screen.blit(instructions_text_surf_pt3, insructions_text_rect_pt3)

            screen.blit(return_text_surf, return_text_rect)

    pygame.display.update()
    clock.tick(30)
