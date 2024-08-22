import pygame as pg
import random
import spaceships
import math
import copy

# Resolution of school laptops
RESOLUTION = (1366, 768)

# Initializing pygame
pg.init()

# Initializing screen and clock
screen = pg.display.set_mode(RESOLUTION)
clock = pg.time.Clock()

# Initializing sounds
ready_sound = pg.mixer.Sound('ready.mp3')
click_sound = pg.mixer.Sound('click.mp3')

# Custom font template using coordingates. Must be in a 8x16 box
LETTERS = {'a':[[0, 16], [4, 0], [8, 16], [6, 8], [2, 8]],
           'b':[[0, 16], [0, 0], [6, 4], [0, 8], [6, 12], [0, 16]],
           'c':[[8, 0], [0, 6], [0, 10], [8, 16]],
           'd':[[0, 16], [8, 8], [0, 0], [0, 16]],
           'e':[[8, 0], [0, 0], [0, 8], [8, 8], [0, 8], [0, 16], [8, 16]],
           'f':[[8, 0], [0, 0], [0, 8], [4, 8], [0, 8], [0, 16]],
           'g':[[8, 0], [0, 8], [8, 16], [8, 8], [4, 8]],
           'h':[[0, 0], [0, 16], [0, 8], [8, 8], [8, 0], [8, 16]],
           'i':[[0, 0], [8, 0], [4, 0], [4, 16], [0, 16], [8, 16]],
           'j':[[0, 0], [8, 0], [6, 0], [6, 12], [3, 16], [0, 12]],
           'k':[[0, 0], [0, 8], [8, 0], [0, 8], [8, 16], [0, 8], [0, 16]],
           'l':[[0, 0], [0, 16], [8, 16]],
           'm':[[0, 16], [0, 0], [4, 8], [8, 0], [8, 16]],
           'n':[[0, 16], [0, 0], [8, 16], [8, 0]],
           'o':[[0, 16], [8, 16], [8, 0], [0, 0], [0, 8], [0, 16]],
           'p':[[0, 16], [0, 0], [8, 4], [0, 8], [0, 16]],
           'q':[[4, 0], [0, 8], [4, 16], [6, 12], [8, 16], [6, 12], [8, 8], [4, 0]],
           'r':[[0, 16], [0, 0], [8, 4], [4, 6], [8, 16], [4, 6], [0, 8]],
           's':[[8, 0], [0, 6], [8, 12], [0, 16]],
           't':[[0, 0], [8, 0], [4, 0], [4, 16]],
           'u':[[0, 0], [2, 16], [6, 16], [8, 0]],
           'v':[[0, 0], [4, 16], [8, 0]],
           'w':[[0, 0], [2, 16], [4, 10], [6, 16], [8, 0]],
           'x':[[0, 0], [8, 16], [4, 8], [8, 0], [0, 16]],
           'y':[[0, 0], [4, 8], [8, 0], [4, 8], [4, 16]],
           'z':[[0, 0], [8, 0], [0, 16], [8, 16]],
           '0':[[0, 16], [8, 16], [8, 0], [0, 0], [0, 8], [0, 16], [8, 0]],
           '1':[[0, 4], [4, 0], [4, 16], [0, 16], [8, 16]],
           '2':[[0, 4], [4, 0], [8, 4], [0, 16], [8, 16]],
           '3':[[0, 0], [8, 3], [8, 8], [0, 8], [8, 8], [8, 13], [0, 16]],
           '4':[[8, 16], [8, 0], [0, 8], [8, 8]],
           '5':[[8, 0], [0, 0], [0, 6], [6, 6], [8, 8], [8, 14], [6, 16], [0, 16]],
           '6':[[8, 0], [0, 2], [0, 16], [8, 16], [8, 8], [0, 8]],
           '7':[[0, 0], [8, 0], [0, 16]],
           '8':[[8, 8], [0, 8], [0, 16], [8, 16], [8, 0], [0, 0], [0, 8]],
           '9':[[0, 16], [8, 14], [8, 0], [0, 0], [0, 8], [8, 8]],
           '.':[[2, 16], [2, 14]],
           '?':[[0, 0], [8, 3], [4, 8], [4, 12]],
           '(':[[6, 0], [2, 4], [2, 12], [6, 16]],
           ')':[[2, 0], [6, 4], [6, 12], [2, 16]],
           '-':[[0, 8], [8, 8]],
           }

def generate_font(size):
    '''
    Customizes font template to specific size and returns new font.
    '''
    l = copy.deepcopy(LETTERS)
    for coords in l.values():
        for coord in coords:
            coord[0] *= size
            coord[1] *= size
    return l

def generate_text(text, font, size, topleft, color, screen, boldness=4):
    h = 0
    v = 0
    if topleft[0] == 'centered':
        topleft[0] = RESOLUTION[0]/2 - (len(text.split("\\")[0])*size*1.4)/2
    for letter in text:
        if letter == '\\': 
            v += 1
            h = 0
        if letter == ' ':
            h += 1
        if letter.lower() in font.keys():
            pts = [[topleft[0] + p[0] + h*size*1.4, topleft[1] + p[1] + v*size*2.4] for p in font[letter.lower()]]
            pg.draw.lines(screen, color, False, pts, boldness)
            h += 1

def generate_stars(num):
    '''
    Creates list of stars with random position & velocity
    '''
    stars = []
    for i in range(100):
        stars.append([random.randint(0, RESOLUTION[0]), random.randint(0, RESOLUTION[1]), random.randint(1, 5)/10])
    return stars
    
def draw_stars(stars, screen):
    '''
    Displays the stars to the screen
    '''
    for star in stars:
        pg.draw.circle(screen, '#aaaaaa', (star[0], star[1]), random.randint(20, 30)/10) # Random size for twinkle effect
        star[0] = star[0]%RESOLUTION[0] + star[2]
        star[1] = star[1]%RESOLUTION[1] - star[2]
    return stars

# Generating stars and fonts before game starts
stars = generate_stars(100)
fontsize = 16
font = generate_font(fontsize/8)
title_font_size = 64
title_font = generate_font(title_font_size/8)
score = [0, 0]

'''
START = Main menu
SELECT = Select ship menu
GAME = Main game loop
PLAYAGAIN = "Play Again?" prompt screen
QUIT = Closes the game
'''
running = 'START'
while running != 'QUIT':
    match running:
        case 'GAME':
            # Game Loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = 'QUIT'
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN and ship2.shooting_type == 'tap':
                        ship2.shoot()
                    if event.key == pg.K_s and ship1.shooting_type == 'tap':
                        ship1.shoot()

            # Right ship controls
            if pg.key.get_pressed()[pg.K_UP]:
                ship2.fly_forward()
            if pg.key.get_pressed()[pg.K_LEFT]:
                ship2.fly_turn(-1)
            if pg.key.get_pressed()[pg.K_RIGHT]:
                ship2.fly_turn(1)
            if pg.key.get_pressed()[pg.K_s]:
                if ship1.shooting_type == 'hold':
                    ship1.shoot()
            elif type(ship1) == spaceships.Gamma: ship1.bullets = []
            if pg.key.get_pressed()[pg.K_DOWN]:
                if ship2.shooting_type == 'hold':
                    ship2.shoot()
            elif type(ship2) == spaceships.Gamma: ship2.bullets = []
            
            # Left ship controls
            if pg.key.get_pressed()[pg.K_w]:
                ship1.fly_forward()
            if pg.key.get_pressed()[pg.K_a]:
                ship1.fly_turn(-1)
            if pg.key.get_pressed()[pg.K_d]:
                ship1.fly_turn(1)

            # Check for game over   
            if ship1.health <= 0:
                running = "PLAYAGAIN"
                score[1] += 1
            elif ship2.health <= 0:
                running  = "PLAYAGAIN"
                score[0] += 1
            
            # Drawing to screen
            screen.fill("black")

            stars = draw_stars(stars, screen)

            ship1.update() # Updates ship1 position
            ship1.draw()

            ship2.update() # Updates ship2 position
            ship2.draw()

            
            cd = spaceships.checkdamage(ship1, ship2)
            cooldown = [max(0, c - 1) for c in cooldown]
            if cd[1] > 0:
                damage_accumulator[cd[0]] += cd[1]
                if cd[1] > 0: cooldown[cd[0]] = 30
            for i in range(len(damage_accumulator)):
                if cooldown[i] > 0:
                    generate_text(str(round(damage_accumulator[i])), font, fontsize, (ship2 if i else ship1).position+pg.Vector2(40, -40), 'red', screen)
                else: damage_accumulator[i] = 0


            generate_text(f'{score[0]} - {score[1]}', font, fontsize, ['centered', 5], 'yellow', screen)
        case 'PLAYAGAIN':
            # Prompt to play again
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = 'QUIT'
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_y:
                        click_sound.play()
                        running = 'SELECT'
                        ship_choices = [spaceships.Alpha, spaceships.Beta, spaceships.Gamma]
                        ready = [0, 0]
                    if event.key == pg.K_n:
                        running = 'QUIT'

            # Draw sky
            screen.fill('black')
            stars = draw_stars(stars, screen)
            
            # Draws play again text
            generate_text(f'{score[0]} - {score[1]}', title_font, title_font_size, ['centered', 50], 'RED', screen, boldness=12)
            generate_text(f'WOULD YOU LIKE TO PLAY AGAIN?\\\\\\   yes (y)         no (n)', font, fontsize, ['centered', 300], 'yellow', screen)
        
        case 'START':
            # Main menu
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = 'QUIT'
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        click_sound.play()
                        running = 'SELECT'
                        ship_choices = [spaceships.Alpha, spaceships.Beta, spaceships.Gamma]
                        chosen = [0, 0]
                        ready = [0, 0]
                    if event.key == pg.K_q:
                        running = 'QUIT'

            # Draw sky
            screen.fill('black')
            stars = draw_stars(stars, screen)

            # Draw main menu text
            generate_text('SPACESHIPS', title_font, title_font_size, [250, 50], 'RED', screen, boldness=12)
            generate_text('\\(SPACE) TO PLAY\\\\  (Q) TO QUIT', font, fontsize, [520, 200], 'yellow', screen)
        case 'SELECT':
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = 'QUIT'
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE and ready[0] and ready[1]:
                        click_sound.play()
                        running = 'GAME'
                        ship1 = ship_choices[chosen[0]]((200, 359), 0, 'red', screen)
                        ship2 = ship_choices[chosen[1]]((1366-200, 359), -math.pi, 'blue', screen)
                        damage_accumulator = [0, 0]
                        cooldown = [0, 0]
                    if not ready[0]:
                        if event.key == pg.K_a:
                            chosen[0] = (chosen[0]-1)%len(ship_choices)
                            click_sound.play()
                        if event.key == pg.K_d:
                            chosen[0] = (chosen[0]+1)%len(ship_choices)
                            click_sound.play()
                    if not ready[1]:
                        if event.key == pg.K_LEFT:
                            chosen[1] = (chosen[1]-1)%len(ship_choices)
                            click_sound.play()
                        if event.key == pg.K_RIGHT:
                            chosen[1] = (chosen[1]+1)%len(ship_choices)
                            click_sound.play()
                    if event.key == pg.K_s:
                        ready[0] = 1
                        ready_sound.play()
                    if event.key == pg.K_DOWN:
                        ready[1] = 1
                        ready_sound.play()

            # Draw sky
            screen.fill('black')
            stars = draw_stars(stars, screen)
            
            generate_text('CHOOSE YOUR SHIP', font, fontsize, ['centered', 50], 'yellow', screen)
            if not(ready[0] and ready[1]):
                generate_text('PRESS [DOWN] TO READY', font, fontsize, ['centered', 150], 'green', screen)
            else:
                generate_text('[SPACE] TO START', font, fontsize, ['centered', 150], 'green', screen)

            if ready[0]:
                pg.draw.lines(screen, 'green', False, [((RESOLUTION[0]/4-20, RESOLUTION[1]/2+80)), (RESOLUTION[0]/4, RESOLUTION[1]/2+100), (RESOLUTION[0]/4+50, RESOLUTION[1]/2+50)], 10)
            if ready[1]:
                pg.draw.lines(screen, 'green', False, [((RESOLUTION[0]/4*3-20, RESOLUTION[1]/2+80)), (RESOLUTION[0]/4*3, RESOLUTION[1]/2+100), (RESOLUTION[0]/4*3+50, RESOLUTION[1]/2+50)], 10)

            display_left = ship_choices[chosen[0]](pg.Vector2(RESOLUTION[0]/4, RESOLUTION[1]/2), -math.pi/2, 'red', screen)
            display_left.fire = True
            display_right = ship_choices[chosen[1]](pg.Vector2(RESOLUTION[0]/4*3, RESOLUTION[1]/2), -math.pi/2, 'blue', screen)
            display_right.fire = True

            display_left.draw()
            display_right.draw()

            pg.draw.polygon(screen, 'yellow', [[RESOLUTION[0]/4-75, RESOLUTION[1]/2], [RESOLUTION[0]/4-60, RESOLUTION[1]/2+15], [RESOLUTION[0]/4-60, RESOLUTION[1]/2-15]])
            pg.draw.polygon(screen, 'yellow', [[RESOLUTION[0]/4+75, RESOLUTION[1]/2], [RESOLUTION[0]/4+60, RESOLUTION[1]/2+15], [RESOLUTION[0]/4+60, RESOLUTION[1]/2-15]])

            pg.draw.polygon(screen, 'yellow', [[RESOLUTION[0]/4*3-75, RESOLUTION[1]/2], [RESOLUTION[0]/4*3-60, RESOLUTION[1]/2+15], [RESOLUTION[0]/4*3-60, RESOLUTION[1]/2-15]])
            pg.draw.polygon(screen, 'yellow', [[RESOLUTION[0]/4*3+75, RESOLUTION[1]/2], [RESOLUTION[0]/4*3+60, RESOLUTION[1]/2+15], [RESOLUTION[0]/4*3+60, RESOLUTION[1]/2-15]])



    # 60 FPS
    clock.tick(60)
    pg.display.update()