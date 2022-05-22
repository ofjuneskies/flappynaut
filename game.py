import pygame
import sys
import math
import random

SURFACE_W = 800
SURFACE_H = 600
gravity = 0.03
CLOCK = pygame.time.Clock()
FPS = 60
font_name = "inkfree"

def format_images(img): 
    created_img = pygame.image.load(img).convert_alpha()
    return created_img

def check_game_over(astroX, astroY, astroWidth, astroHeight, planets, speech):
    game_over = False
    astroX = astroX + astroWidth
    astroY = astroY + astroHeight

    if astroY > SURFACE_H or astroY <= 0:
        game_over = True

    for planet in planets:
        if (astroX > planet['x'] and astroX < planet['x'] + planet['width'] and astroY > planet['y'] and astroY < planet['y'] + planet['height']):
            game_over = True

    for words in speech:
        if (astroX > words['x'] and astroX < words['x'] + words['width'] and ((astroY > words['y'] and astroY < words['y'] + words['height']) or (astroY - astro.get_height() > words['y'] and astroY - astro.get_height() < words['y'] + words['height']))):
            game_over = True

    return game_over

def add_planet(planets):
    planet_choose = random.randint(1, 2)
    if planet_choose == 1:
        img = format_images('pink.png')
        img = pygame.transform.scale(img, (img.get_width()/10, img.get_height()/10))
    else:
        img = format_images('periwinkle.png')
        img = pygame.transform.scale(img, (img.get_width()/25, img.get_height()/25))
    y = random.randrange(-(img.get_height()), SURFACE_H - 30)
    planets.append({'img' : img, 'x' : SURFACE_W, 'y' : y, 'width' : img.get_width(), 'height' : img.get_height()})

def run_planets(surface, planets):
    if planets[-1]['x'] < surface.get_width()/2 + 3 and planets[-1]['x'] > surface.get_width()/2 - 3:
        add_planet(planets)
    for planet in planets:
        planet['x'] -= 3
        surface.blit(planet['img'], (planet['x'], planet['y']))
        if planet['x'] + planet['width'] < 0:
            planets.remove(planet)

def add_laptop(laptops, planets):
    laptop = format_images('laptop.png')
    laptop = pygame.transform.scale(laptop, (laptop.get_width()/25, laptop.get_height()/25))
    y = random.randrange(0, SURFACE_H - laptop.get_height())
    while True:
        for planet in planets:
            if planet['x'] > SURFACE_W + laptop.get_width() and planet['x'] + planet['width'] < SURFACE_W and y + laptop.get_height() > planet['y'] and y < planet['y'] + planet['height']:
                y = random.randrange(0, SURFACE_H - laptop.get_height())
        else:
            break
    laptops.append({'img' : laptop, 'x' : SURFACE_W, 'y' : y, 'width' : laptop.get_width(), 'height' : laptop.get_height()})

def draw_laptop(surface, laptops, planets, laptopPresent, astro, astroX, astroY, score):
    if not laptopPresent:
        add_laptop(laptops, planets)
        laptopPresent = True
    for laptop in laptops:
        laptop['x'] -= 3
        surface.blit(laptop['img'], (laptop['x'], laptop['y']))
        if laptop['x'] + laptop['width'] < 0:
            laptops.remove(laptop)
            laptopPresent = False

        if (astroX + astro.get_width() < laptop['x'] + laptop['width'] and astroX + astro.get_width() > laptop['x'] and ((astroY > laptop['y'] and astroY < laptop['y'] + laptop['height']) or (astroY + astro.get_height() < laptop['y'] + laptop['height'] and astroY + astro.get_height() > laptop['y']))):
            laptops.remove(laptop)
            laptopPresent = False
            score += 1
    return laptopPresent, score

def display_counter(surface, score):
    font = pygame.font.SysFont(font_name, 40)
    text = font.render('Score: ' + str(score), True, (255, 255, 255))
    surface.blit(text, (0, 0))

def display_health(surface, health):
    font = pygame.font.SysFont(font_name, 40)
    text = font.render('Health: ' + str(health), True, (255, 255, 255))
    surface.blit(text, (0, 0))

def final_boss():
    bossImg = format_images('alien.png')
    bossImg = pygame.transform.scale(bossImg, (bossImg.get_width()/2, bossImg.get_height()/2))
    bossX = SURFACE_W - bossImg.get_width() - 50
    bossY = 100
    boss = {'img' : bossImg, 'x' : bossX, 'y' : bossY, 'width' : bossImg.get_width(), 'height' : bossImg.get_height(), 'health' : 10}
    return boss

def move_boss(boss):
    chance = random.randint(1, 100)
    if chance <= 4:
        if chance <= 2:
            y = random.randint(-50, -20)
        else:
            y = random.randint(20, 50)
        if boss['y'] + y + boss['height'] < SURFACE_H and boss['y'] + y > 0:
            boss['y'] += y
    surface.blit(boss['img'], (boss['x'], boss['y']))

def add_stars(stars, astro, astroX, astroY):
    choose_stars = random.randint(1,3)
    if choose_stars == 1:
        star_img = format_images('cassiopeia.png')
    elif choose_stars == 2:
        star_img = format_images('dipper.png')
    else:
        star_img = format_images('pegasus.png')
    star_img = pygame.transform.scale(star_img, (star_img.get_width()/50, star_img.get_height()/50))
    stars.append({'img' : star_img, 'x' : astroX + astro.get_width(), 'y' : astroY + astro.get_height()/2, 'width' : star_img.get_width(), 'height' : star_img.get_height()})

def draw_stars(surface, stars, boss):
    for star in stars:
        star['x'] += 7
        surface.blit(star['img'], (star['x'], star['y']))
        if star['x'] + star['width'] > SURFACE_W:
            stars.remove(star)
        if star['x'] + star['width'] > boss['x'] + 50 and star['x'] < boss['x'] + boss['width'] and star['y'] + star['height'] > boss['y'] and star['y'] < boss['y'] + boss['height']:
            stars.remove(star)
            boss['health'] -= 1
            if boss['health'] <= 0:
                return True
    return False

def add_boss_speech(speech):
    words_choose = random.randint(1, 2)
    font = pygame.font.SysFont(font_name, 40)
    if words_choose == 1:
        text = font.render("Women's brains aren't wired for the tech field", True, (255, 255, 255))
    else:
        text = font.render('You should go into an easier major', True, (255, 255, 255))
    y = random.randrange(-(text.get_height()), SURFACE_H - 30)
    speech.append({'txt' : text, 'x' : 800, 'y' : y, 'width' : text.get_width(), 'height' : text.get_height()})

def run_boss_speech(surface, speech):
    if speech[-1]['x'] < surface.get_width()/2 + 3 and speech[-1]['x'] > surface.get_width()/2 - 3:
        add_boss_speech(speech)
    for words in speech:
        words['x'] -= 3
        surface.blit(words['txt'], (words['x'], words['y']))
        if words['x'] + words['width'] < 0:
            speech.remove(words)

if __name__ == "__main__":
    running = True
    game_over = False
    astroX = 100
    astroY = 100
    velocity = 3
    score = 0
    show_text = True
    white = (255, 255, 255)
    boss_screen = True

    pygame.init()

    #Creates Screen
    surface = pygame.display.set_mode((SURFACE_W, SURFACE_H))
    pygame.display.set_caption('Flappynaut')

    #Images
    bg = format_images('space_bg.jpg')
    astro = format_images('astronaut.png')
    astro = pygame.transform.scale(
        astro, (astro.get_width()/60, astro.get_height()/60))
    font = pygame.font.SysFont(font_name, 100)
    text = font.render('Game Over', True, white)

    planets = []
    add_planet(planets)

    laptops = []
    laptopPresent = True
    add_laptop(laptops, planets)

    stars = []
    boss_dead = False
    boss = final_boss()
    speech = []
    add_boss_speech(speech)

    #Game Variables
    bg_width = bg.get_width()
    bg_scroll = 0
    bg_tiles_maker = math.ceil(SURFACE_W/bg_width) + 1
    start = False

    #Game Loop
    while running:
        CLOCK.tick(FPS)

        #Draw Scrolling BG
        for i in range(0, bg_tiles_maker): 
            surface.blit(bg, (i * bg_width + bg_scroll ,0))
        bg_scroll -= 2
        if abs(bg_scroll) > bg_width:
            bg_scroll = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and game_over == True:
                if event.key == pygame.K_SPACE:
                    running = True
                    start = False
                    game_over = False
                    planets = []
                    add_planet(planets)
                    laptops = []
                    laptopPresent = True
                    add_laptop(laptops, planets)
                    stars = []
                    boss_dead = False
                    boss = final_boss()
                    speech = []
                    add_boss_speech(speech)
                    astroX = 100
                    astroY = 100
                    velocity = 3
                    score = 0


        if not game_over:
            pygame.time.wait(5)
            keys = pygame.key.get_pressed()
            if start == False:
                start_message = font.render('Hold Up to Start', True, white)
                surface.blit(start_message, (SURFACE_W/2 - (start_message.get_width()/2),
                        SURFACE_H/2 - (start_message.get_height()/2)))
            if keys[pygame.K_UP]:
                start = True
                velocity -= 0.07
            if start == True:
                velocity += gravity
                astroY += velocity
                if score < 5:
                    run_planets(surface, planets)
                    laptopPresent, score = draw_laptop(surface, laptops, planets, laptopPresent, astro, astroX, astroY, score)
                    display_counter(surface, score)
                else:
                    if boss_screen:
                        surface.blit(bg, (0, 0))
                        font = pygame.font.SysFont(font_name, 50)
                        text = font.render('Defeat the Alien of the Patriarchy!', True, white)
                        surface.blit(text, (SURFACE_W/2 - (text.get_width()/2),
                                        SURFACE_H/2 - (text.get_height()/2)))
                        pygame.display.update()
                        pygame.time.wait(2000)
                        surface.blit(bg, (0, 0))
                        boss_screen = False
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RIGHT:
                                add_stars(stars, astro, astroX, astroY)
                    if not boss_dead:
                        move_boss(boss)
                        run_boss_speech(surface, speech)
                    else:
                        game_over = True
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                    pygame.quit()
                                    sys.exit()
                            if show_text:
                                text_array = []
                                font1 = pygame.font.SysFont(font_name, 100)
                                text1 = font.render('You Win!', True, white)
                                text_array.append(text1)
                                
                                font2 = pygame.font.SysFont(font_name, 30)
                                text2 = font2.render("Women face many challenges in the tech field", True, white)
                                text3 = font2.render("From double standards to stereotypes to blatant sexism", True, white)
                                text7 = font2.render("But if you can defeat the Alien of the Patriarchy", True, white)
                                text8 = font2.render("You can defeat anything", True, white)
                                text4 = font2.render("Don't let the difficulties hold you back", True, white)
                                text5 = font2.render("Don't let the world tell you you can't", True, white)
                                font1 = pygame.font.SysFont(font_name, 80)
                                text6 = font1.render("Thanks for playing :)", True, white)

                                text_array.append(text2)
                                text_array.append(text3)
                                text_array.append(text7)
                                text_array.append(text8)
                                text_array.append(text4)
                                text_array.append(text5)
                                text_array.append(text6)
                                for txt in text_array:
                                    surface.blit(txt, (SURFACE_W/2 - (txt.get_width()/2),
                                                    SURFACE_H/2 - (txt.get_height()/2)))
                                    pygame.display.update()
                                    pygame.time.wait(2500)
                                    surface.blit(bg, (0, 0))
                                show_text = False
                    boss_dead = draw_stars(surface, stars, boss)
                    display_health(surface, boss['health'])
                    planets = []
                    laptops = []
                
                surface.blit(astro, (astroX, astroY))

                game_over = check_game_over(astroX, astroY, astro.get_width(), astro.get_height(), planets, speech)
                
        else:
            surface.blit(text, (SURFACE_W/2 - (text.get_width()/2),
                         SURFACE_H/2 - (text.get_height()/2)))
        
        
        pygame.display.update()

    
