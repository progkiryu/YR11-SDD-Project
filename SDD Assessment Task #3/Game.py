#Imported modules
import pygame as pg
from pygame import mixer as mx
import os, sys, random

#Screen Setup
pg.init()
#Music Setup
mx.init()
#Dimensions of the resolution
window_w, window_h = (1080, 720)
#Sets the size of the window with resolution measurements.
window = pg.display.set_mode((window_w, window_h))
#Sets the caption of the window.
pg.display.set_caption("RESOLVE")

#RGB Setup
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#Main menu setup
class Menu:
    def __init__(self, window):
        self.window = window
        self.bd = 0
        self.pause = 0
        self.song_number = 1
        self.playlist = []
        self.playlist.append(os.path.join("Music", "Champions League Theme 8-bit with Super Soccer.mp3"))
        self.playlist.append(os.path.join("Music", "GOT menu theme.mp3"))
        self.playlist.append(os.path.join("Music", "GOT menu theme2.mp3"))
        self.enter_sound = mx.Sound(os.path.join("Sound Effects", "button_enter se.mp3"))
        self.return_sound = mx.Sound(os.path.join("Sound Effects", "button_return se.mp3"))
        self.font = pg.font.Font((os.path.join("Sprites", "8bit font.ttf")), 80)
    def title(self, window, x, y):
        self.x = x
        self.y = y
        text_obj = self.font.render("RESOLVE", True, white)
        if self.bd >= 0:
            window.blit(text_obj, (self.x, self.y))
    def text(self, window, x, y):
        self.text_x = x
        self.text_y = y
        text_font = pg.font.Font((os.path.join("Sprites", "8bit font.ttf")), 60)
        if self.bd == 1:
            text_obj = text_font.render("OPTIONS", True, white)
        elif self.bd == 2:
            text_obj = text_font.render("MUSIC", True, white)
        elif self.bd == 3:
            text_obj = text_font.render("CONTROLS", True, white)
        if self.bd >= 1:
            window.blit(text_obj, (self.text_x, self.text_y))
    def music(self):
        random.shuffle(self.playlist)
        mx.music.load(self.playlist[self.song_number])
        mx.music.play(-1)
        for num, song in enumerate(self.playlist):
            if num == self.song_number:
                continue
            else:
                mx.music.queue(song)
    def controls(self):
        text_font = pg.font.Font((os.path.join("Sprites", "8bit font.ttf")), 30)
        movement_text_obj = text_font.render("MOVEMENT: W Jump A Left D Right", True, red)
        attack_text_obj = text_font.render("ATTACK: SPACE Kunai O Light Attack P Heavy Attack", True, green)
        action_text_obj = text_font.render("ACTION: E Unsheathe or Sheathe L Block", True, blue)
        tips_text_obj = text_font.render("TIPS:", True, white)
        tip1_text_obj = text_font.render("Remember to stagger by heavy attacking or using kunai.", True, white)
        tip2_text_obj = text_font.render("Jumping or attacking uses stamina.", True, white)
        if self.bd == 3:
            window.blit(movement_text_obj, (24, 210))
            window.blit(attack_text_obj, (24, 260))
            window.blit(action_text_obj, (24, 310))
            window.blit(tips_text_obj, (24, 410))
            window.blit(tip1_text_obj, (24, 460))
            window.blit(tip2_text_obj, (24, 510))
    def fade(self):
        fade = pg.Surface((window_w, window_h))
        fade.fill(white)
        for colour_change in range(0, 300):
            fade.set_alpha(colour_change)
            window.fill(black)
            window.blit(fade, (0, 0))
            pg.display.flip()
            pg.time.delay(10)
    def display(self, window):
        self.controls()
        window.fill(black)
        self.title(window, 20, 20)
        self.text(window, 20, 100)

#Sets Menu functions as a variable.
menu = Menu(window)

#Game setup
class Game:
    def __init__(self, window):
        self.window = window
        self.bd = 0
        self.sky = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "game GUI (sky).png")).convert_alpha()), (window_w, 550))
        self.sky2 = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "game GUI (sky).png")).convert_alpha()), (window_w, 550))
        self.sky_x = 0
        self.sky2_x = 1080
        self.grass = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "game GUI (grass).png")).convert_alpha()), (window_w, 170))
        self.pause = 0
        self.exit = False
        self.font = pg.font.Font((os.path.join("Sprites", "8bit font.ttf")), 80)
        self.start = True
        self.wave = 1
        self.dh = False
        self.dh2 = False
        self.aa = False
        self.wave_displaytime = 0
        self.wave_displaytime2 = 0
        self.wave_hiddentime = 0
        self.wave_hiddentime2 = 0
        self.end = False
        self.score = 0
    def pathway(self, window, x, y):
        text_x = x
        text_y = y
        if self.bd == 0:
            text_obj = self.font.render("Tutorial?", True, black)
        elif self.exit == True:
            text_obj = self.font.render("Exit to menu?", True, black)
        window.blit(text_obj, (text_x, text_y)) 
    def r_fade(self):
        fade = pg.Surface((window_w, window_h))
        fade.fill(black)
        for colour_change in range(0, 300):
            fade.set_alpha(colour_change)
            window.fill(white)
            window.blit(fade, (0, 0))
            pg.display.flip()
            pg.time.delay(10)  
    def s_display(self, window):
        font = pg.font.Font(os.path.join("Sprites", "8bit font.ttf"), 60)
        text_obj = font.render("Score:" + str(self.score), True, white)
        if self.start == False:
            window.blit(text_obj, (780, 0))
    def o_display(self, window):
        text_obj = self.font.render("Press ENTER to begin.", True, white)
        text_obj2 = self.font.render("Press ENTER to restart.", True, white)
        if samurai.enter_pressed == False and self.start == True:
            window.blit(text_obj, (60, 150))
        elif self.end == True:
            window.blit(text_obj2, (25, 150))
    def wave_timer(self, window):
        text_obj = self.font.render("WAVE 1", True, white)
        if self.dh == False:
            self.wave_hiddentime += 1
            if self.wave_hiddentime >= 50:
                self.dh = True
                self.aa = True
        elif self.wave_displaytime < 100 and self.dh == True:
            self.wave_displaytime += 1
            self.wave_hiddentime = 0
            window.blit(text_obj, (400, 200))
    def wave2_timer(self, window):
        text_obj = self.font.render("WAVE 2", True, white)
        if self.dh2 == False:
            self.wave_hiddentime2 += 1
            if self.wave_hiddentime2 >= 50:
                self.dh2 = True
                self.asp = True
        elif self.wave_displaytime2 < 100 and self.dh2 == True:
            self.wave_displaytime2 += 1
            self.wave_hiddentime2 = 0
            window.blit(text_obj, (400, 200))
    def reset(self):
        self.score = 0
        self.exit = False
        self.start = True
        self.pause = 0
        self.wave = 1
        self.dh = False
        self.dh2 = False
        self.aa = False
        self.wave_displaytime = 0
        self.wave_displaytime2 = 0
        self.wave_hiddentime = 0
        self.wave_hiddentime2 = 0
        self.end = False
    def display(self, window):
        if self.bd == 0 or self.exit == True:   
            window.fill(white)
        else:
            if not self.sky_x <= -1080:
                self.sky_x -= 0.5
            else:
                self.sky_x = 0
            if not self.sky2_x <= 0:
                self.sky2_x -= 0.5
            else:
                self.sky2_x = 1080
            window.blit(self.sky, (self.sky_x, 0))
            window.blit(self.sky2, (self.sky2_x, 0))
            window.blit(self.grass, (0, 550))
        self.s_display(window)
        self.o_display(window)

#Sets Game functions as a variable.
game = Game(window)

#Loads all sprite sheets.
class Spritesheets:
    def __init__(self):

        #Loads the spritesheet by following the pygame.image.load function, with convert_alpha to make sure the image loads properly
        self.spritesheet_start = pg.image.load(os.path.join("Sprites", "Samurai", "8bit samurai (start).png")).convert_alpha()

        self.spritesheet_us = pg.image.load(os.path.join("Sprites", "Samurai", "8bit samurai (unsheathed).png")).convert_alpha()
        self.spritesheet_thrown = pg.image.load(os.path.join("Sprites", "Samurai", "8bit samurai (thrown).png")).convert_alpha()
        self.spritesheet_movement = pg.image.load(os.path.join("Sprites", "Samurai", "8bit samurai (movement).png")).convert_alpha()
        self.spritesheet_health_stamina = pg.image.load(os.path.join("Sprites", "Samurai", "healthstamina.png")).convert_alpha()
        self.spritesheet_jump = pg.image.load(os.path.join("Sprites", "Samurai", "8bit samurai (jump).png")).convert_alpha()
        self.spritesheet_light_attack = pg.image.load(os.path.join("Sprites", "Samurai", "8bit samurai (light attack).png")).convert_alpha()
        self.spritesheet_heavy_attack = pg.image.load(os.path.join("Sprites", "Samurai", "8bit samurai (heavy attack).png")).convert_alpha()
        self.spritesheet_archer = pg.image.load(os.path.join("Sprites", "Enemies", "8bit archer.png")).convert_alpha()
        self.spritesheet_Ahealthstagger = pg.image.load(os.path.join("Sprites", "Enemies", "Ahealthstagger.png")).convert_alpha()
        self.spritesheet_Amovement = pg.image.load(os.path.join("Sprites", "Enemies", "8bit archer (movement).png")).convert_alpha()
        self.spritesheet_death = pg.image.load(os.path.join("Sprites", "Samurai", "8bit samurai (death).png")).convert_alpha()
    def get_spritesheet_start(self, x, y, width, height):
        
        #Sets a variable for both width and height, 
        #then the image object is formed with the pygame.Surface function and blits the loaded spritesheet image
        #and is then scaled by integer dividing. Once each spritesheet function is called, return image will
        #generate it by setting the x, y, width, height arguments.
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_start, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image

    def get_spritesheet_us(self, x, y, width, height):
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_us, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
    def get_spritesheet_thrown(self, x, y, width, height):
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_thrown, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
    def get_spritesheet_movement(self, x, y, width, height):
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_movement, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, ((width // 2) - 30, (height // 2) - 30))
        return image
    def get_spritesheet_jump(self, x, y, width, height):
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_jump, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, ((width // 2, height // 2)))
        return image
    def get_spritesheet_health_stamina(self, x, y, width, height):
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_health_stamina, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * 2, height * 2))
        return image
    def get_spritesheet_light_attack(self, x, y, width, height):
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_light_attack, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
    def get_spritesheet_heavy_attack(self, x, y, width, height):
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_heavy_attack, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
    def get_spritesheet_archer(self, x, y, width, height):
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_archer, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
    def get_spritesheet_Ahealthstagger(self, x, y, width, height):
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_Ahealthstagger, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * 2, height * 2))
        return image
    def get_spritesheet_Amovement(self, x, y, width, height):
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_Amovement, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
    def get_spritesheet_death(self, x, y, width, height):
        image_width = width
        image_height = height
        image = pg.Surface((image_width, image_height))
        image.blit(self.spritesheet_death, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image

#Sets a variable for the Samurai sheathing/unsheathing sprite sheet.
spritesheets = Spritesheets()

#Loads up the sprite for the Samurai, records movement, jump mechanics, health and damage.
class Samurai:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        #Velocity
        self.x_vel = 15
        self.y_vel = 12

        #Starting variables
        self.image = spritesheets.get_spritesheet_start(0, 0, 324, 280)
        self.image_rect = self.image.get_rect()
        self.enter_pressed = False
        self.start_index = 0

        #Starting frames
        self.start_images = []
        self.start_images.append(spritesheets.get_spritesheet_start(324, 0, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(648, 0, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(972, 0, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1296, 0, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1620, 0, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(0, 280, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(324, 280, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(648, 280, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(972, 280, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1296, 280, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1620, 280, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(0, 560, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(324, 560, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(648, 560, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(972, 560, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1296, 560, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1620, 560, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(0, 840, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(324, 840, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(648, 840, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(972, 840, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1296, 840, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1620, 840, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(0, 1120, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(324, 1120, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(648, 1120, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(972, 1120, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1296, 1120, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1620, 1120, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(0, 1400, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(324, 1400, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(648, 1400, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(972, 1400, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1296, 1400, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(1620, 1400, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(0, 1680, 324, 280))
        self.start_images.append(spritesheets.get_spritesheet_start(324, 1680, 324, 280))
        
        #Health and its variables
        self.health_value = 10
        self.l_h = []
        self.h_index = 0
        self.h2_index = 0

        #Stamina and its variables
        self.stamina_value = 6
        self.l_s = []
        self.s_index = 0
        self.s2_index = 0

        #Samurai's stagger and health damage
        self.stagger_damage = 20
        self.health_damage = 10

        #Samurai's movement arguments
        self.left_pressed = False
        self.right_pressed = False
        self.left_facing = False
        self.right_facing = True

        #Samurai's jump variables
        self.up_pressed = False
        self.jump_count = 10
        self.negative = 0
        self.space_pressed = False

        #Kunai counter and score font
        self.font = pg.font.Font(os.path.join("Sprites", "8bit font.ttf"), 60)

        #Kunai variables
        self.k_value = 6
        self.kunais = []
        self.pn = 0

        #Unsheathing and sheathing variables
        self.u_change = 2
        self.u_display = False
        self.s_display = False

        #Unsheathing and sheathing frames
        self.u_index = 0
        self.u_images = []
        self.u_images.append(spritesheets.get_spritesheet_us(280, 0, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(560, 0, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(840, 0, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(0, 280, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(280, 280, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(560, 280, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(840, 280, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(0, 560, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(280, 560, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(560, 560, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(840, 560, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(0, 840, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(280, 840, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(560, 840, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(840, 840, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(0, 1120, 280, 280))
        self.u_images.append(spritesheets.get_spritesheet_us(280, 1120, 280, 280))
        self.s_images = []
        self.s_images.append(spritesheets.get_spritesheet_us(280, 1120, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(0, 1120, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(840, 840, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(560, 840, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(280, 840, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(0, 840, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(840, 560, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(560, 560, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(280, 560, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(0, 560, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(840, 280, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(560, 280, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(280, 280, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(0, 280, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(840, 0, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(560, 0, 280, 280))
        self.s_images.append(spritesheets.get_spritesheet_us(280, 0, 280, 280))

        #Unsheathing and sheathing sfx
        self.u_sound = mx.Sound(os.path.join("Sound Effects", "Samurai SFX", "samurai_unsheathing se.mp3"))
        self.s_sound = mx.Sound(os.path.join("Sound Effects", "Samurai SFX", "samurai_sheathing se.mp3"))

        #Samurai throwing frames
        self.k_display = False
        self.k_images_index = 0
        self.k_images = []
        self.k_images.append(spritesheets.get_spritesheet_thrown(0, 0, 280, 280))
        self.k_images.append(spritesheets.get_spritesheet_thrown(280, 0, 280, 280))
        self.k_images.append(spritesheets.get_spritesheet_thrown(560, 0, 280, 280))
        self.k_images.append(spritesheets.get_spritesheet_thrown(0, 280, 280, 280))
        self.k_images.append(spritesheets.get_spritesheet_thrown(280, 280, 280, 280))
        self.k_images.append(spritesheets.get_spritesheet_thrown(560, 280, 280, 280))
        self.k2_images = []
        self.k2_images.append(spritesheets.get_spritesheet_thrown(0, 560, 280, 280))
        self.k2_images.append(spritesheets.get_spritesheet_thrown(280, 560, 280, 280))
        self.k2_images.append(spritesheets.get_spritesheet_thrown(560, 560, 280, 280))
        self.k2_images.append(spritesheets.get_spritesheet_thrown(0, 840, 280, 280))
        self.k2_images.append(spritesheets.get_spritesheet_thrown(280, 840, 280, 280))
        self.k2_images.append(spritesheets.get_spritesheet_thrown(560, 840, 280, 280))

        #Throwing sfx
        self.k_sound = mx.Sound(os.path.join("Sound Effects", "Samurai SFX", "kunai_throw se.mp3"))

        #Samurai's movement frames
        self.m_images_index = 0
        self.m_images = []
        self.m_images.append(spritesheets.get_spritesheet_movement(0, 0, 279, 335))
        self.m_images.append(spritesheets.get_spritesheet_movement(0, 0, 279, 335))
        self.m_images.append(spritesheets.get_spritesheet_movement(0, 0, 279, 335))
        self.m_images.append(spritesheets.get_spritesheet_movement(279, 0, 279, 335))
        self.m_images.append(spritesheets.get_spritesheet_movement(279, 0, 279, 335))
        self.m_images.append(spritesheets.get_spritesheet_movement(279, 0, 279, 335))
        self.m_images.append(spritesheets.get_spritesheet_movement(558, 0, 279, 335))
        self.m_images.append(spritesheets.get_spritesheet_movement(558, 0, 279, 335))
        self.m_images.append(spritesheets.get_spritesheet_movement(558, 0, 279, 335))
        self.m_images.append(spritesheets.get_spritesheet_movement(0, 335, 279, 335))
        self.m_images.append(spritesheets.get_spritesheet_movement(0, 335, 279, 335))
        self.m_images.append(spritesheets.get_spritesheet_movement(0, 335, 279, 335))
        self.m2_images = []
        self.m2_images.append(spritesheets.get_spritesheet_movement(279, 335, 279, 335))
        self.m2_images.append(spritesheets.get_spritesheet_movement(279, 335, 279, 335))
        self.m2_images.append(spritesheets.get_spritesheet_movement(279, 335, 279, 335))
        self.m2_images.append(spritesheets.get_spritesheet_movement(558, 335, 279, 335))
        self.m2_images.append(spritesheets.get_spritesheet_movement(558, 335, 279, 335))
        self.m2_images.append(spritesheets.get_spritesheet_movement(558, 335, 279, 335))
        self.m2_images.append(spritesheets.get_spritesheet_movement(0, 669, 279, 335))
        self.m2_images.append(spritesheets.get_spritesheet_movement(0, 669, 279, 335))
        self.m2_images.append(spritesheets.get_spritesheet_movement(0, 669, 279, 335))
        self.m2_images.append(spritesheets.get_spritesheet_movement(279, 669, 279, 335))
        self.m2_images.append(spritesheets.get_spritesheet_movement(279, 669, 279, 335))
        self.m2_images.append(spritesheets.get_spritesheet_movement(279, 669, 279, 335))

        #Movement on grass sfx
        self.m_sound = mx.Sound(os.path.join("Sound Effects", "Samurai SFX", "movement sfx.mp3"))

        #Blocking argument
        self.l_pressed = False

        #Light attack variables
        self.l_a_display = False
        self.l_a2_display = False
        self.l_a3_display = False
        self.l_a_change = 1
        self.o_change = 1
        self.o_index = 0

        #Light attack variation frames
        self.l_a_images = []
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(0, 0, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(0, 0, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(324, 0, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(324, 0, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(648, 0, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(648, 0, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(972, 0, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(972, 0, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(1296, 0, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(1296, 0, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(0, 280, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(0, 280, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(324, 280, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(324, 280, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(648, 280, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(648, 280, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(972, 280, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(972, 280, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(1296, 280, 324, 280))
        self.l_a_images.append(spritesheets.get_spritesheet_light_attack(1296, 280, 324, 280))
        self.l_a2_images = []
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(0, 560, 324, 280))
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(0, 560, 324, 280))
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(324, 560, 324, 280))
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(324, 560, 324, 280))
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(648, 560, 324, 280))
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(648, 560, 324, 280))
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(972, 560, 324, 280))
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(972, 560, 324, 280))
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(1296, 560, 324, 280))
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(1296, 560, 324, 280))
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(0, 840, 324, 280))
        self.l_a2_images.append(spritesheets.get_spritesheet_light_attack(0, 840, 324, 280))
        self.l_a3_images = []
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(324, 840, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(324, 840, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(648, 840, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(648, 840, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(972, 840, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(972, 840, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(1296, 840, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(1296, 840, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(0, 1120, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(0, 1120, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(324, 1120, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(324, 1120, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(648, 1120, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(648, 1120, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(972, 1120, 324, 280))
        self.l_a3_images.append(spritesheets.get_spritesheet_light_attack(972, 1120, 324, 280))

        #Heavy attack variables
        self.h_a_display = False
        self.h_a2_display = False
        self.h_a_change = 1
        self.p_change = 1
        self.p_index = 0

        #Heavy attack variation frames (in progress)
        self.h_a_images = []
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(0, 0, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(0, 0, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(354, 0, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(354, 0, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(708, 0, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(708, 0, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(1062, 0, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(1062, 0, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(0, 280, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(0, 280, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(354, 280, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(354, 280, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(708, 280, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(708, 280, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(1062, 280, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(1062, 280, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(0, 560, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(0, 560, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(354, 560, 354, 280))
        self.h_a_images.append(spritesheets.get_spritesheet_heavy_attack(354, 560, 354, 280))
        self.h_a2_images = []
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(708, 560, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(708, 560, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(1062, 560, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(1062, 560, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(0, 840, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(0, 840, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(354, 840, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(354, 840, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(708, 840, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(708, 840, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(1062, 840, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(1062, 840, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(0, 1120, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(0, 1120, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(354, 1120, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(354, 1120, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(708, 1120, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(708, 1120, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(1062, 1120, 354, 280))
        self.h_a2_images.append(spritesheets.get_spritesheet_heavy_attack(1062, 1120, 354, 280))

        #Attack sfx
        self.a1_sound = mx.Sound(os.path.join("Sound Effects", "Samurai SFX", "sword swing 1.mp3"))
        self.a2_sound = mx.Sound(os.path.join("Sound Effects", "Samurai SFX", "sword swing 2.mp3"))
        self.a3_sound = mx.Sound(os.path.join("Sound Effects", "Samurai SFX", "sword swing 3.mp3"))

        #Death animation frames
        self.death_index = 0
        self.death_images = []
        self.death = False
        self.death_images.append(spritesheets.get_spritesheet_death(0, 0, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(0, 0, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(420, 0, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(420, 0, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(840, 0, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(840, 0, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(1260, 0, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(1260, 0, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(0, 280, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(0, 280, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(420, 280, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(420, 280, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(840, 280, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(840, 280, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(1260, 280, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(1260, 280, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(0, 560, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(0, 560, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(420, 560, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(420, 560, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(840, 560, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(840, 560, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(1260, 560, 420, 280))
        self.death_images.append(spritesheets.get_spritesheet_death(1260, 560, 420, 280))
        self.death2_images = []
        self.death2_images.append(spritesheets.get_spritesheet_death(0, 840, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(0, 840, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(420, 840, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(420, 840, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(840, 840, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(840, 840, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(1260, 840, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(1260, 840, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(0, 1120, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(0, 1120, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(420, 1120, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(420, 1120, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(840, 1120, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(840, 1120, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(1260, 1120, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(1260, 1120, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(0, 1400, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(0, 1400, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(420, 1400, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(420, 1400, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(840, 1400, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(840, 1400, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(1260, 1400, 420, 280))
        self.death2_images.append(spritesheets.get_spritesheet_death(1260, 1400, 420, 280))

    def start(self): 
        if game.start == True:
            if self.enter_pressed == True:
                self.start_index += 1
                if self.start_index >= len(self.start_images):
                    self.start_index = 0
                    self.enter_pressed = False
                    game.start = False
                elif self.start_index > 0:
                    self.image = self.start_images[self.start_index]
    def health(self, window):

        #If health value is 10, then the health image would display full bars.
        #If lower than 9 then lower than decreasing value, the health image changes.
        if self.health_value == 10:
            self.health_image = spritesheets.get_spritesheet_health_stamina(0, 0, 280, 40)
        elif self.health_value == 9:
            self.health_image = spritesheets.get_spritesheet_health_stamina(280, 0, 280, 40)
        elif self.health_value == 8:
            self.health_image = spritesheets.get_spritesheet_health_stamina(0, 40, 280, 40)
        elif self.health_value == 7:
            self.health_image = spritesheets.get_spritesheet_health_stamina(280, 40, 280, 40)
        elif self.health_value == 6:
            self.health_image = spritesheets.get_spritesheet_health_stamina(0, 80, 280, 40)
        elif self.health_value == 5:
            self.health_image = spritesheets.get_spritesheet_health_stamina(280, 80, 280, 40)
        elif self.health_value == 4:
            self.health_image = spritesheets.get_spritesheet_health_stamina(0, 120, 280, 40)
        elif self.health_value == 3:
            self.health_image = spritesheets.get_spritesheet_health_stamina(280, 120, 280, 40)
        elif self.health_value == 2:
            self.health_image = spritesheets.get_spritesheet_health_stamina(0, 160, 280, 40)
        elif self.health_value == 1:
            self.health_image = spritesheets.get_spritesheet_health_stamina(280, 160, 280, 40)
        elif self.health_value <= 0:
            self.death = True
        #set_colorkey function gets clears out the specified color.
        self.health_image.set_colorkey(black)

        if game.start == False and self.death == False:
            window.blit(self.health_image, (0, 0))
        elif self.death == True and game.end == False:
            if self.u_change == 2:
                self.death_index += 1
                if self.death_index >= len(self.death_images):
                    self.death_index = 0
                    game.end = True
                    self.u_change = 3
                elif self.death_index > 0:
                    self.image = self.death_images[self.death_index]
            elif self.u_change == 1:
                self.death_index += 1
                if self.death_index >= len(self.death2_images):
                    self.death_index = 0
                    game.end = True
                    self.u_change = 4
                elif self.death_index > 0:
                    self.image = self.death2_images[self.death_index]
        if self.u_change == 3:
            self.image = spritesheets.get_spritesheet_death(1260, 560, 420, 280)
        elif self.u_change == 4:
            self.image = spritesheets.get_spritesheet_death(1260, 1400, 420, 280)
    def stamina(self, window):
        
        #Same system as health.
        if self.stamina_value == 6:
            self.stamina_image = spritesheets.get_spritesheet_health_stamina(280, 200, 280, 40)
        elif self.stamina_value == 5:
            self.stamina_image = spritesheets.get_spritesheet_health_stamina(0, 240, 280, 40)
        elif self.stamina_value == 4:
            self.stamina_image = spritesheets.get_spritesheet_health_stamina(280, 240, 280, 40)
        elif self.stamina_value == 3:
            self.stamina_image = spritesheets.get_spritesheet_health_stamina(0, 280, 280, 40)
        elif self.stamina_value == 2:
            self.stamina_image = spritesheets.get_spritesheet_health_stamina(280, 280, 280, 40)
        elif self.stamina_value == 1:
            self.stamina_image = spritesheets.get_spritesheet_health_stamina(0, 320, 280, 40)
        elif self.stamina_value == 0:
            self.stamina_image = spritesheets.get_spritesheet_health_stamina(280, 320, 280, 40)
        if self.stamina_value < 6:
            self.s_index += 1
            if self.s_index >= 25:
                self.s_index = 0
                self.stamina_value += 1

        #If the samurai performs a jump, attack or gets hit while blocking, they will append in the l_s list
        #a "loss" which activates this pathway. While a stamina bar gets depleted, a time/increment system plays until it
        #reaches its max to clear the list and regenerates until all stamina bars are fully restored. (Inspired by the projectile system)
        if "loss" in self.l_s:
            self.s2_index += 1
            if self.s2_index > 20:
                self.s2_index = 0
                self.l_s.clear()
        self.stamina_image.set_colorkey(black)
        if game.start == False:
            window.blit(self.stamina_image, (0, 80))
    def display(self, window):
        self.start()
        self.health(window)
        if self.death == False:
            self.stamina(window)
            self.us()
            self.movement()
            self.jump()
            self.throw(window)
            self.block()
            self.light_attack()
            self.heavy_attack()
        if self.left_facing == True and not self.right_facing:
            self.image = pg.transform.flip(self.image, True, False)
        elif self.right_facing == True and not self.left_facing:
            self.image = pg.transform.flip(self.image, False, False)
        self.image.set_colorkey(black)
        self.image_rect.topleft = (self.x, self.y)
        window.blit(self.image, self.image_rect)
    def us(self):
        if self.u_display == True:
            self.u_change = 0
            self.u_index += 1
            if self.u_index >= len(self.u_images):
                self.u_index = 0
                self.u_change = 1
                self.u_display = False
            self.image = self.u_images[self.u_index]
        elif self.s_display == True:
            self.u_change = 0
            self.u_index += 1
            if self.u_index >= len(self.s_images):
                self.u_index = 0
                self.u_change = 2
                self.s_display = False
            self.image = self.s_images[self.u_index] 
        if game.start == False:
            if self.u_change == 1:
                self.image = spritesheets.get_spritesheet_us(560, 1120, 200, 280)
            elif self.u_change == 2:
                self.image = spritesheets.get_spritesheet_us(0, 0, 200, 280)
    def movement(self):
        if self.left_pressed == True and not self.right_pressed: 
            if self.x > -30:
                if self.up_pressed == False:
                    if self.u_change == 2:
                        self.m_images_index += 1
                        if self.m_images_index >= len(self.m_images):
                            self.m_images_index = 0
                        self.image = self.m_images[self.m_images_index]
                    elif self.u_change == 1:
                        self.m_images_index += 1
                        if self.m_images_index >= len(self.m2_images):
                            self.m_images_index = 0
                        self.image = self.m2_images[self.m_images_index]
                self.x -= self.x_vel
            else:
                self.m_images_index = 0
                self.x = -30
        elif self.right_pressed == True and not self.left_pressed:
            if self.x < 1000:
                if self.up_pressed == False:
                    if self.u_change == 2:
                        self.m_images_index += 1
                        if self.m_images_index >= len(self.m_images):
                            self.m_images_index = 0
                        self.image = self.m_images[self.m_images_index]
                    elif self.u_change == 1:
                        self.m_images_index += 1
                        if self.m_images_index >= len(self.m2_images):
                            self.m_images_index = 0
                        self.image = self.m2_images[self.m_images_index]
                self.x += self.x_vel
            else:
                self.m_images_index = 0
                self.x = 1000
    def jump(self):
        if self.up_pressed == True and self.jump_count >= -10:
            if self.u_change == 2:
                self.image = spritesheets.get_spritesheet_jump(0, 0, 280, 280)
            elif self.u_change == 1:
                self.image = spritesheets.get_spritesheet_jump(0, 280, 280, 280)
            self.negative = 1
            if self.jump_count < 0:
                self.negative = -1
            self.y -= (self.jump_count ** 2) * 0.5 * self.negative
            self.jump_count -= 1
        else:
            self.up_pressed = False
            self.jump_count = 10
    def throw(self, window):
        kunai_text = self.font.render(str(self.k_value), True, white)
        kunai_counter = pg.transform.smoothscale(pg.image.load(os.path.join("Sprites", "Samurai", "kunaicounter.png")).convert_alpha(), (150, 80))
        for kunai in self.kunais:
            self.space_pressed = False
            if kunai.x > -45 and kunai.x < 1100:
                if self.k_display == True and self.u_change == 2:
                    self.k_images_index += 1
                    if self.k_images_index >= len(self.k_images):
                        self.k_images_index = 0
                        self.k_display = False
                    self.image = self.k_images[self.k_images_index]
                elif self.k_display == True and self.u_change == 1:
                    self.k_images_index += 1
                    if self.k_images_index >= len(self.k2_images):
                        self.k_images_index = 0
                        self.k_display = False
                    self.image = self.k2_images[self.k_images_index]
                kunai.display(window)
                kunai.movement()
            else:
                self.kunais.pop(self.kunais.index(kunai))
        if game.start == False:
            window.blit(kunai_counter, (0, 160))
            window.blit(kunai_text, (100, 170))
    def block(self):
        if self.l_pressed == True:
            self.image = pg.transform.smoothscale(pg.image.load(os.path.join("Sprites", "Samurai", "8bit samurai (block).png")).convert_alpha(), (230 // 2, 280 // 2))
    def light_attack(self):
        if game.start == False:
            if self.l_a_display == True:
                self.o_change = 0
                self.o_index += 1
                self.x += 5 * -self.l_a_change
                if self.o_index >= len(self.l_a_images):
                    self.o_change = 2
                    self.o_index = 0
                    self.l_a_display = False
                elif self.o_index > 0:
                    self.image = self.l_a_images[self.o_index]
            elif self.l_a2_display == True:
                self.o_change = 0
                self.o_index += 1
                self.x += 4 * -self.l_a_change
                if self.o_index >= len(self.l_a2_images):
                    self.o_change = 3
                    self.o_index = 0
                    self.l_a2_display = False
                elif self.o_index > 0:
                    self.image = self.l_a2_images[self.o_index]
            elif self.l_a3_display == True:
                self.o_change = 0
                self.o_index += 1
                self.x += 4 * -self.l_a_change
                if self.o_index >= len(self.l_a3_images):
                    self.o_change = 1
                    self.o_index = 0
                    self.l_a3_display = False
                elif self.o_index > 0:
                    self.image = self.l_a3_images[self.o_index]
    def heavy_attack(self):
        if game.start == False:
            if self.h_a_display == True:
                self.p_change = 0
                self.p_index += 1
                self.x += 5 * -self.h_a_change
                if self.p_index >= len(self.h_a_images):
                    self.p_change = 2
                    self.p_index = 0
                    self.h_a_display = False
                elif self.p_index > 0:
                    self.image = self.h_a_images[self.p_index]
            elif self.h_a2_display == True:
                self.p_change = 0
                self.p_index += 1
                self.x += 4 * -self.h_a_change
                if self.p_index >= len(self.h_a2_images):
                    self.p_change = 1
                    self.p_index = 0
                    self.h_a2_display = False
                elif self.p_index > 0:
                    self.image = self.h_a2_images[self.p_index]
    def reset(self):
        self.x = 490
        self.y = 438
        self.image = spritesheets.get_spritesheet_start(0, 0, 324, 280)
        self.health_value = 10
        self.l_h.clear()
        self.stamina_value = 6
        self.s_index = 0
        self.s2_index = 0
        self.l_s.clear()
        self.left_pressed = False
        self.right_pressed = False
        self.left_facing = False
        self.right_facing = True
        self.up_pressed = False
        self.jump_count = 8
        self.negative = 0
        self.space_pressed = False
        self.k_value = 6
        self.kunais.clear()
        self.pn = 0
        self.u_change = 2
        self.u_display = False
        self.s_display = False
        self.l_a_change = 1
        self.o_index = 0
        self.h_a_change = 1
        self.p_index = 0
        self.l_a_display = False
        self.l_a2_display = False
        self.l_a3_display = False
        self.h_a_display = False
        self.h_a2_display = False
        self.l_pressed = False
        self.death_index = 0
        self.death = False
    
#Sets a variable for the player to use.
samurai = Samurai(490, 438)

#Loads up the sprite for kunais, for the player to throw.
class Kunai:
    def __init__(self, x, y):
        self.x = x
        self.y = y + 60
        self.vel = 60
        scale = pg.transform.smoothscale(pg.image.load(os.path.join("Sprites", "Samurai", "kunai.png")).convert_alpha(), (22, 7))
        self.left = pg.transform.flip(scale, True, False)
        self.right = pg.transform.flip(scale, False, False)
        self.image = self.right
    def movement(self):
        self.x += self.vel * samurai.pn
    def display(self, window):
        if samurai.pn == -1:
            self.image = self.left
        elif samurai.pn == 1:
            self.image = self.right
        window.blit(self.image, (self.x, self.y))

#Enemies
#Archers show up only in the first wave.
class Archers:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        #Health and stagger value
        self.health = 6
        self.aa_h_index = 0
        self.stagger = 3
        self.s_regenerate = 0
        self.aa_s_index = 0
        self.aa_h = []
        self.aa_s = []
        self.death = 0

        #Normal stance
        self.image = spritesheets.get_spritesheet_archer(0, 0, 354, 280)
        self.image_rect = self.image.get_rect()
        self.s = True

        #Archer's shooting variables
        self.a_change = 1
        self.pn = 1
        self.reload_time = 20
        self.arrows = []
        self.arming_time = 40

        #Archer arming animation
        self.a_display = False
        self.arming_index = 0
        self.arming_images = []
        self.arming_images.append(spritesheets.get_spritesheet_archer(354, 0, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(708, 0, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(1062, 0, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(1416, 0, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(0, 280, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(354, 280, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(708, 280, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(1062, 280, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(1416, 280, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(0, 560, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(354, 560, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(708, 560, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(1062, 560, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(1416, 560, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(0, 840, 354, 280))
        self.arming_images.append(spritesheets.get_spritesheet_archer(354, 840, 354, 280))

        #Archer movement animation
        self.m_index = 0
        self.m_images = []
        self.m_images.append(spritesheets.get_spritesheet_Amovement(0, 0, 280, 280))
        self.m_images.append(spritesheets.get_spritesheet_Amovement(0, 0, 280, 280))
        self.m_images.append(spritesheets.get_spritesheet_Amovement(280, 0, 280, 280))
        self.m_images.append(spritesheets.get_spritesheet_Amovement(280, 0, 280, 280))
        self.m_images.append(spritesheets.get_spritesheet_Amovement(0, 280, 280, 280))
        self.m_images.append(spritesheets.get_spritesheet_Amovement(0, 280, 280, 280))
        self.m_images.append(spritesheets.get_spritesheet_Amovement(280, 280, 280, 280))
        self.m_images.append(spritesheets.get_spritesheet_Amovement(280, 280, 280, 280))
        
        #Archer releasing animation
        self.r_display = False
        self.r_index = 0
        self.releasing_images = []
        self.releasing_images.append(spritesheets.get_spritesheet_archer(1062, 840, 354, 280))
        self.releasing_images.append(spritesheets.get_spritesheet_archer(1416, 840, 354, 280))
        self.releasing_images.append(spritesheets.get_spritesheet_archer(0, 1120, 354, 280))
        self.releasing_images.append(spritesheets.get_spritesheet_archer(354, 1120, 354, 280))
        self.releasing_images.append(spritesheets.get_spritesheet_archer(708, 1120, 354, 280))

        #Archer death animation
        self.d_index = 0
        self.death_images = []
        self.death_images.append(spritesheets.get_spritesheet_archer(1062, 1120, 354, 280))
        self.death_images.append(spritesheets.get_spritesheet_archer(1062, 1120, 354, 280))
        self.death_images.append(spritesheets.get_spritesheet_archer(1416, 1120, 354, 280))
        self.death_images.append(spritesheets.get_spritesheet_archer(1416, 1120, 354, 280))
        self.death_images.append(spritesheets.get_spritesheet_archer(0, 1400, 354, 280))
        self.death_images.append(spritesheets.get_spritesheet_archer(0, 1400, 354, 280))
        self.death_images.append(spritesheets.get_spritesheet_archer(354, 1400, 354, 280))
        self.death_images.append(spritesheets.get_spritesheet_archer(354, 1400, 354, 280))
        self.death_images.append(spritesheets.get_spritesheet_archer(708, 1400, 354, 280))
        self.death_images.append(spritesheets.get_spritesheet_archer(708, 1400, 354, 280))
    def display(self, window):
        if game.aa == True:
            self.start()
        if self.s == False:
            self.hit()
            self.healthstagger(window)
            self.arrow()
            if self.stagger > 0:
                if samurai.x < (self.x + 25):
                    self.pn = -1
                    self.image = pg.transform.flip(self.image, True, False)
                elif samurai.x > (self.x + 25):
                    self.pn = 1
                    self.image = pg.transform.flip(self.image, False, False)
        self.image.set_colorkey(black)
        self.image_rect.topleft = (self.x, self.y)
        if self.death == False:
            window.blit(self.image, self.image_rect)
    def start(self):
        if self.s == True:
            self.m_index += 1
            if self.m_index >= len(self.m_images):
                self.m_index = 0
            elif self.m_index > 0:
                self.image = self.m_images[self.m_index]
            if self.x < 200:
                self.x += 10
                if self.x >= 200:
                    self.m_index = 0
                    self.x = 200
                    self.s = False
            if self.x > 650 and self.x < 1600:
                self.x -= 10
                if self.x <= 650:
                    self.m_index = 0
                    self.x = 650
                    self.s = False
            if self.x > 880:
                self.image = pg.transform.flip(self.image, True, False)
                self.x -= 10
                if self.x <= 880:
                    self.m_index = 0
                    self.x = 880
                    self.s = False   
    def healthstagger(self, window):
        if self.stagger > 0:
            if self.stagger == 3:
                status_image = spritesheets.get_spritesheet_Ahealthstagger(0, 30, 40, 10)
            elif self.stagger == 2:
                status_image = spritesheets.get_spritesheet_Ahealthstagger(40, 30, 40, 10)
            elif self.stagger == 1:
                status_image = spritesheets.get_spritesheet_Ahealthstagger(0, 40, 40, 10)
        elif self.health > 0:
            if self.health == 6:
                status_image = spritesheets.get_spritesheet_Ahealthstagger(0, 0, 40, 10)
            elif self.health == 5:
                status_image = spritesheets.get_spritesheet_Ahealthstagger(40, 0, 40, 10)
            elif self.health == 4:
                status_image = spritesheets.get_spritesheet_Ahealthstagger(0, 10, 40, 10)
            elif self.health == 3:
                status_image = spritesheets.get_spritesheet_Ahealthstagger(40, 10, 40, 10)
            elif self.health == 2:
                status_image = spritesheets.get_spritesheet_Ahealthstagger(0, 20, 40, 10)
            elif self.health == 1:
                status_image = spritesheets.get_spritesheet_Ahealthstagger(40, 20, 40, 10)
        if self.stagger > 0 or self.health > 0:
            status_image.set_colorkey(black)
            window.blit(status_image, (self.x + 50, self.y - 30))
        if "loss" in self.aa_h:
            self.aa_h_index += 1
            if self.aa_h_index >= 20:
                self.aa_h.clear()
                self.aa_h_index = 0
        if "loss" in self.aa_s:
            self.aa_s_index += 1
            if self.aa_s_index >= 20:
                self.aa_s.clear()
                self.aa_s_index = 0
    def arrow(self):
        if not self.stagger == 0:

            #Initiates an reload and arming system to indicate the player
            #that the archers is about to shoot.
            if self.arming_time > 0:
                self.arming_time -= 1
                self.a_display = True
            elif self.a_display == True:
                self.a_change = 0
                self.arming_index += 1
                if self.arming_index >= len(self.arming_images):
                    self.arming_index = 0
                    self.a_change = 2
                    self.a_display = False
                elif self.arming_index > 0:
                    self.image = self.arming_images[self.arming_index]
            
            #Once the arming time is up and the arrow list is empty,
            #the archer will shoot depending on which side the
            #player is at.
            elif len(self.arrows) < 1:
                self.reload_time -= 1
                if self.reload_time <= 0:
                    self.r_display = True
                    self.arrows.append(Arrows(self.x, self.y))
            for arrow in self.arrows:
                if arrow.x > -45 and arrow.x < 1200:
                    if self.r_display == True:
                        self.a_change = 0
                        self.r_index += 1
                        if self.r_index >= len(self.releasing_images):
                            self.r_index = 0
                            self.a_change = 3
                            self.r_display = False
                        elif self.r_index > 0:
                            self.image = self.releasing_images[self.r_index]
                    if samurai.death == False:
                        if self.pn == -1 and samurai.image_rect.collidepoint(arrow.x, arrow.y):
                            if samurai.l_pressed == True and samurai.right_facing == True:
                                self.a_change = 3
                                self.reload_time = 20
                                self.arming_time = 40
                                self.arrows.pop(self.arrows.index(arrow))
                            else:
                                self.a_change = 3
                                samurai.health_value -= 1
                                self.reload_time = 20
                                self.arming_time = 40
                                self.arrows.pop(self.arrows.index(arrow))
                        if self.pn == 1 and samurai.image_rect.collidepoint(arrow.x, arrow.y):
                            if samurai.l_pressed == True and samurai.left_facing == True:
                                self.a_change = 3
                                self.reload_time = 20
                                self.arming_time = 40
                                self.arrows.pop(self.arrows.index(arrow))
                            else:
                                self.a_change = 3
                                samurai.health_value -= 1
                                self.reload_time = 20
                                self.arming_time = 40
                                self.arrows.pop(self.arrows.index(arrow))
                    arrow.display(window)

                    #Arrow movement dependent on the samurai's position.
                    arrow.x += arrow.vel * self.pn   

                else:
                    self.reload_time = 20
                    self.arming_time = 40
                    self.arrows.pop(self.arrows.index(arrow))
        elif self.health > 3:
            self.a_change = 4
        elif self.health < 3:
            self.a_change = 5      
        if self.health > 0:      
            if self.a_change == 1:
                self.image = spritesheets.get_spritesheet_archer(0, 0, 354, 280)
            elif self.a_change == 2:
                self.image = spritesheets.get_spritesheet_archer(708, 840, 354, 280)
            elif self.a_change == 3:
                self.image = spritesheets.get_spritesheet_archer(708, 1120, 354, 280)
            elif self.a_change == 4:
                self.image = spritesheets.get_spritesheet_archer(1062, 1400, 354, 280)
            elif self.a_change == 5:
                self.image = spritesheets.get_spritesheet_archer(1416, 1400, 354, 280)
        
        #Initation of death.
        else:
            self.d_index += 1
            if self.d_index >= len(self.death_images):
                self.d_index = 0
                self.death = True
            elif self.d_index > 0:
                self.image = self.death_images[self.d_index]

    def hit(self):
        if samurai.image_rect.collidepoint(self.x + 110, self.y + 40):
            if samurai.o_change == 0:
                if self.stagger == 0:
                    if len(self.aa_h) < 1:
                        self.health -= 1
                        self.aa_h.append("loss")
            elif samurai.p_change == 0:
                if not self.stagger == 0:
                    if len(self.aa_s) < 1:
                        self.stagger -= 1
                        self.aa_s.append("loss")
                elif len(self.aa_h) < 1:
                    self.health -= 2
                    self.aa_h.append("loss")
        for kunai in samurai.kunais:
            if self.image_rect.collidepoint(kunai.x, kunai.y):
                if not self.stagger == 0:
                    if len(self.aa_s) < 1:
                        self.stagger = 0
                        self.aa_s.append("loss")
                elif len(self.aa_h) < 1:
                    self.health -= 1
                    self.aa_h.append("loss")
                samurai.kunais.pop(samurai.kunais.index(kunai))
    def reset(self):
        self.image = spritesheets.get_spritesheet_archer(0, 0, 354, 280)
        self.health = 6
        self.stagger = 3
        self.aa_h_index = 0
        self.aa_s_index = 0
        self.a_change = 1
        self.aa_h.clear()
        self.aa_s.clear() 
        self.d_index = 0  
        self.r_index = 0
        self.reload_time = 20
        self.arming_time = 40
        self.arming_index = 0
        self.a_display = False
        self.pn = 1
        self.arrows.clear()
        archers.death = False
        archers2.death = False
        archers3.death = False
        archers4.death = False
        archers5.death = False
        archers.s = True
        archers2.s = True
        archers3.s = True
        archers4.s = True
        archers5.s = True
        archers.x = -240
        archers2.x = 1300
        archers3.x = 1650
        archers4.x = 1300
        archers5.x = -240

#Sets all archers as a variable.
archers = Archers(-240, 438)
archers2 = Archers(1300, 438)
archers3 = Archers(1650, 438)
archers4 = Archers(1300, 438)
archers5 = Archers(-240, 438)

#Arrows that the archer uses.
class Arrows:
    def __init__(self, x, y):
        self.x = x + 100
        self.y = y + 60
        self.vel = 80
        scale = pg.transform.smoothscale(pg.image.load(os.path.join("Sprites", "Enemies", "arrow.png")).convert_alpha(), (22, 7))
        self.left = pg.transform.flip(scale, True, False)
        self.right = pg.transform.flip(scale, False, False)
        self.image = self.right
    def display(self, window):
        if archers.pn == -1:
            self.image = self.left
        elif archers.pn == 1:
            self.image = self.right
        window.blit(self.image, (self.x, self.y))

#Creates a button for the first row.
class Button_1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "Buttons", "button colour.png")).convert_alpha()), (400, 150))
        self.image.set_colorkey(black)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (self.x, self.y)
        self.font_elr = 0
        self.collide = False
    def text(self, window, x, y):
        text_x = x
        text_y = y
        text_font = pg.font.Font((os.path.join("Sprites", "8bit font.ttf")), 50)
        if menu.bd == 0:
            self.text_obj = text_font.render("READY UP...", True, red)
        elif menu.bd == 1:
            self.text_obj = text_font.render("EDIT TRACK", True, red)
        elif menu.bd == 2:
            if menu.pause == 0:
                self.text_obj = text_font.render("PAUSE TRACK", True, red)
            elif menu.pause == 1:
                self.text_obj = text_font.render("PLAY TRACK", True, red)
        window.blit(self.text_obj, (text_x, text_y))
    def hovering(self):
        if self.collide == True:
            self.font_elr = 20
            window.blit(self.image, (self.image_rect.x - 10, self.image_rect.y - 40))
            window.blit(self.text_obj, self.image_rect)
            if menu.bd >= 0:
                self.text(window, 430, 270)
        else:
            self.font_elr = 0
            window.blit(self.text_obj, self.image_rect)
    def display(self, window):
        text_font = pg.font.Font((os.path.join("Sprites", "8bit font.ttf")), (50 + self.font_elr))
        if menu.bd == 0:
            self.image_rect.center = (230, 330)
            self.text_obj = text_font.render("START", True, white)
        elif menu.bd == 1:
            self.image_rect.center = (230, 330)
            self.text_obj = text_font.render("MUSIC", True, white)
        elif menu.bd == 2:
            if menu.pause == 0:
                self.text_obj = text_font.render("PAUSE", True, white)
            elif menu.pause == 1:
                self.text_obj = text_font.render("PLAY", True, white)
        elif game.bd == 0 or game.exit == True:
            self.image_rect.center = (550, 420)
            self.text_obj = text_font.render("YES", True, black)
        window.blit(self.text_obj, self.image_rect)
        self.hovering()

#Sets a variable for each button that sits on the first row of the Main Menu text.
button_1 = Button_1(230, 330)

#Creates a button for the second row.
class Button_2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "Buttons", "button colour.png")).convert_alpha()),
        (400, 150))
        self.image.set_colorkey(black)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (self.x, self.y)
        self.font_elr = 0
        self.collide = False
    def text(self, window, x, y):
        text_x = x
        text_y = y
        text_font = pg.font.Font((os.path.join("Sprites", "8bit font.ttf")), 50)
        if menu.bd == 0:
            self.text_obj = text_font.render("EDIT FEATURES", True, red)
        elif menu.bd == 1:
            self.text_obj = text_font.render("VIEW CONTROLS", True, red)
        elif menu.bd == 2 or game.pause_bd == 1:
            self.text_obj = text_font.render("SHUFFLE TRACK", True, red)
        window.blit(self.text_obj, (text_x, text_y))
    def hovering(self):
        if self.collide == True:
            self.font_elr = 20
            window.blit(self.image, (self.image_rect.x - 10, self.image_rect.y - 40))
            window.blit(self.text_obj, self.image_rect)
            if menu.bd >= 0:
                self.text(window, 430, 430)
        else:
            self.font_elr = 0
            window.blit(self.text_obj, self.image_rect)
    def display(self, window):
        text_font = pg.font.Font((os.path.join("Sprites", "8bit font.ttf")), (50 + self.font_elr))
        if menu.bd == 0:
            self.image_rect.center = (230, 490)
            self.text_obj = text_font.render("OPTIONS", True, white)
        elif menu.bd == 1:
            self.image_rect.center = (230, 490)
            self.text_obj = text_font.render("CONTROLS", True, white)
        elif menu.bd == 2:
            self.text_obj = text_font.render("SHUFFLE", True, white)
        elif game.bd == 0 or game.exit == True:
            self.image_rect.center = (550, 580)
            self.text_obj = text_font.render("NO", True, black)
        window.blit(self.text_obj, self.image_rect)
        self.hovering()

#Sets a variable for each button that sits on the second row of the Main Menu text.
button_2 = Button_2(230, 490)

#Creates a button for the third row.
class Button_3:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "Buttons", "button colour.png")).convert_alpha()), (400, 150))
        self.image.set_colorkey(black)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (self.x, self.y)
        self.font_elr = 0
        self.collide = False
    def text(self, window, x, y):
        text_x = x
        text_y = y
        text_font = pg.font.Font((os.path.join("Sprites", "8bit font.ttf")), 50)
        if menu.bd == 0:
            text_obj = text_font.render("QUIT PROGRAM", True, red)
        elif menu.bd == 1:
            if game.pause == 1:
                text_obj = text_font.render("BACK TO GAME", True, red)
            else:
                text_obj = text_font.render("BACK TO MENU", True, red)
        elif menu.bd == 2 or menu.bd == 3:
            text_obj = text_font.render("BACK TO OPTIONS", True, red)
        window.blit(text_obj, (text_x, text_y))
    def hovering(self):
        if self.collide == True:
            self.font_elr = 20
            window.blit(self.image, (self.image_rect.x - 10, self.image_rect.y - 40))
            window.blit(self.text_obj, self.image_rect)
            self.text(window, 430, 610)
        else:
            self.font_elr = 0
            window.blit(self.text_obj, self.image_rect)
    def display(self, window):
        text_font = pg.font.Font((os.path.join("Sprites", "8bit font.ttf")), (50 + self.font_elr))
        if menu.bd == 0:
            self.text_obj = text_font.render("EXIT", True, white)
        elif menu.bd == 1:
            if game.pause == 1:
                self.text_obj = text_font.render("RESUME", True, white)
            else:
                self.text_obj = text_font.render("RETURN", True, white)
        elif menu.bd == 2 or menu.bd == 3:
            self.text_obj = text_font.render("RETURN", True, white)
        window.blit(self.text_obj, self.image_rect)
        self.hovering()

#Sets a variable for each button that sits on the third row of the Main Menu text.
button_3 = Button_3(230, 670)

#Creates a in-game settings button.
class Button_4:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "Buttons", "settings1.png")).convert_alpha()), (80, 80))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (self.x, self.y)
        self.collide = False
    def hovering(self):
        if self.collide == True:
            self.image = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "Buttons", "settings2.png")).convert_alpha()), (80, 80))
        else:
            self.image = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "Buttons", "settings1.png")).convert_alpha()), (80, 80))
    def display(self, window):
        window.blit(self.image, self.image_rect)
        self.hovering()

#Sets a variable for the in-game settings button.
game_options_button = Button_4(50, 670)

#Creates a in-game exit button.
class Button_5:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "Buttons", "exit1.png")).convert_alpha()), (80, 80))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (self.x, self.y)
        self.collide = False
    def hovering(self):
        if self.collide == True:
            self.image = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "Buttons", "exit2.png")).convert_alpha()), (80, 80))
        else:
            self.image = pg.transform.smoothscale((pg.image.load(os.path.join("Sprites", "Buttons", "exit1.png")).convert_alpha()), (80, 80))
    def display(self, window):
        window.blit(self.image, self.image_rect)
        self.hovering()

#Sets a variable for the in-game exit button.
game_exit_button = Button_5(1030, 670)

#Main Menu GUI
def main_menu():
    run_pg = True
    while run_pg == True:

        #In the while loop, the computer always tracks the position of the mouse, used for the button mechanics.
        mouse_x, mouse_y = pg.mouse.get_pos()
        
        #Displays the menu background colour and title.
        menu.display(window)
        button_3.display(window)

        #Main Menu backdrop
        if menu.bd == 0:
            button_1.display(window)
            button_2.display(window)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run_pg = False
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEMOTION:
                    if button_1.image_rect.collidepoint(mouse_x, mouse_y):
                        button_1.collide = True
                    else:
                        button_1.collide = False
                    if button_2.image_rect.collidepoint(mouse_x, mouse_y):
                        button_2.collide = True
                    else:
                        button_2.collide = False
                    if button_3.image_rect.collidepoint(mouse_x, mouse_y):
                        button_3.collide = True
                    else:
                        button_3.collide = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if button_1.image_rect.collidepoint(mouse_x, mouse_y):
                        menu.enter_sound.play()
                        button_1.collide = True
                        run_pg = False
                        menu.bd = -1
                        menu.fade()
                        game.bd = 0
                        game_screen()
                    elif button_2.image_rect.collidepoint(mouse_x, mouse_y):
                        menu.enter_sound.play()
                        button_2.collide = False
                        menu.bd = 1
                    elif button_3.image_rect.collidepoint(mouse_x, mouse_y):
                        run_pg = False
                        pg.quit()
                        sys.exit()
        
        #Options backdrop
        elif menu.bd == 1:
            button_1.display(window)
            button_2.display(window)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run_pg = False
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEMOTION:
                    if button_1.image_rect.collidepoint(mouse_x, mouse_y):
                        button_1.collide = True
                    else:
                        button_1.collide = False
                    if button_2.image_rect.collidepoint(mouse_x, mouse_y):
                        button_2.collide = True
                    else:
                        button_2.collide = False
                    if button_3.image_rect.collidepoint(mouse_x, mouse_y):
                        button_3.collide = True
                    else:
                        button_3.collide = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if button_1.image_rect.collidepoint(mouse_x, mouse_y):
                        menu.enter_sound.play()
                        button_1.collide = False
                        menu.bd = 2
                    elif button_2.image_rect.collidepoint(mouse_x, mouse_y):
                        menu.enter_sound.play()
                        button_2.collide = False
                        menu.bd = 3
                    elif button_3.image_rect.collidepoint(mouse_x, mouse_y):
                        menu.return_sound.play()
                        button_3.collide = False
                        menu.bd = 0
        
        #Music backdrop
        elif menu.bd == 2:
            button_1.display(window)
            button_2.display(window)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run_pg = False
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEMOTION:
                    if button_1.image_rect.collidepoint(mouse_x, mouse_y):
                        button_1.collide = True
                    else:
                        button_1.collide = False
                    if button_2.image_rect.collidepoint(mouse_x, mouse_y):
                        button_2.collide = True
                    else:
                        button_2.collide = False
                    if button_3.image_rect.collidepoint(mouse_x, mouse_y):
                        button_3.collide = True
                    else:
                        button_3.collide = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if button_1.image_rect.collidepoint(mouse_x, mouse_y) and menu.pause == 0:
                        button_1.collide = False
                        menu.pause = 1
                        mx.music.pause()
                    elif button_1.image_rect.collidepoint(mouse_x, mouse_y) and menu.pause == 1:
                        button_1.collide = False
                        menu.pause = 0
                        mx.music.unpause()
                    elif button_2.image_rect.collidepoint(mouse_x, mouse_y):
                        button_2.collide = False
                        menu.pause = 0
                        menu.music()
                    elif button_3.image_rect.collidepoint(mouse_x, mouse_y):
                        menu.return_sound.play()
                        button_3.collide = False
                        menu.bd = 1     
        
        #Controls backdrop
        elif menu.bd == 3:
            menu.controls()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run_pg = False
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEMOTION:
                    if button_3.image_rect.collidepoint(mouse_x, mouse_y):
                        button_3.collide = True
                    else:
                        button_3.collide = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if button_3.image_rect.collidepoint(mouse_x, mouse_y):
                        menu.return_sound.play()
                        button_3.collide = False
                        menu.bd = 1

        #Updates the screen
        pg.display.flip()

#Game GUI
def game_screen():
    run_pg = True
    while run_pg == True:
        mouse_x, mouse_y = pg.mouse.get_pos()
        if game.bd == 0:
            game.display(window)
            game.pathway(window, 340, 240)
            button_1.display(window)
            button_2.display(window)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run_pg = False
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEMOTION:
                    if button_1.image_rect.collidepoint(mouse_x, mouse_y):
                        button_1.collide = True
                    else:
                        button_1.collide = False
                    if button_2.image_rect.collidepoint(mouse_x, mouse_y):
                        button_2.collide = True
                    else:
                        button_2.collide = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if button_1.image_rect.collidepoint(mouse_x, mouse_y): 
                        menu.enter_sound.play()
                        button_1.collide = False
                    elif button_2.image_rect.collidepoint(mouse_x, mouse_y):
                        menu.enter_sound.play()
                        button_2.collide = False
                        game.bd = 2
        elif game.bd == 2:

            #Takes individual key inputs outside of the pygame.event loop.
            key = pg.key.get_pressed()

            #Introduces the game by an animation when RETURN is pressed.
            if game.start == True:
                game.display(window)
                samurai.display(window)
                pg.time.delay(40)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run_pg = False
                        pg.quit()
                        sys.exit()
                if key[pg.K_RETURN]:
                    samurai.enter_pressed = True

            #When current game is unpaused, the keys can be used.
            elif game.pause == 0:
                game.display(window)
                game.wave_timer(window)
                samurai.display(window)
                game_exit_button.display(window)
                if game.wave == 1:
                    archers.display(window)
                    if archers.death == True:
                        archers.x = -240
                        archers2.display(window)
                        archers3.display(window)
                    if archers2.death == True and archers3.death == True:
                        archers4.display(window)
                        archers5.display(window)
                    if archers4.death == True and archers5.death == True:
                        game.wave2_timer(window)

                    #Resets the archer's x location so the player's kunai does not
                    #randomly hit an invisible target
                    if archers2.death == True:
                        archers2.x = 1300
                    if archers3.death == True:
                        archers3.x = 1650
                    if archers4.death == True:
                        archers4.x = 1300
                    if archers5.death == True:
                        archers5.x = -240
                pg.time.delay(25)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run_pg = False
                        pg.quit()
                        sys.exit()
                    
                    #As long as the player lives, the player can use option and move in the for event loop.
                    if samurai.death == False:
                        if event.type == pg.MOUSEMOTION:
                            if game_options_button.image_rect.collidepoint(mouse_x, mouse_y):
                                game_options_button.collide = True
                            else:
                                game_options_button.collide = False
                            if game_exit_button.image_rect.collidepoint(mouse_x, mouse_y):
                                game_exit_button.collide = True
                            else:
                                game_exit_button.collide = False
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            if game_options_button.image_rect.collidepoint(mouse_x, mouse_y):
                                menu.enter_sound.play()
                                game_options_button.collide = False
                                menu.bd = 1
                                game.pause = 1
                            elif game_exit_button.image_rect.collidepoint(mouse_x, mouse_y):
                                menu.enter_sound.play()
                                game_exit_button.collide = False
                                game.exit = True
                                game.pause = 1


                        #If the sword is being sheathed or unsheathed, the player cannot move.
                        if samurai.u_change >= 1 and samurai.o_change >= 1 and samurai.p_change >= 1:

                            #If a kunai is being thrown, the player cannot move.
                            if samurai.space_pressed == False:

                                #Basic player movement
                                if event.type == pg.KEYDOWN:
                                    if samurai.l_pressed == False:
                                        if event.key == pg.K_a:
                                            samurai.m_sound.play()
                                            samurai.left_pressed = True
                                            samurai.left_facing = True
                                            samurai.right_facing = False
                                        elif event.key == pg.K_d:
                                            samurai.m_sound.play()
                                            samurai.right_pressed = True
                                            samurai.right_facing = True
                                            samurai.left_facing = False
                                    if samurai.up_pressed == False and samurai.u_change == 1:
                                        if event.key == pg.K_l:
                                            samurai.l_pressed = True
                                            samurai.left_pressed = False
                                            samurai.right_pressed = False
                                elif event.type == pg.KEYUP:
                                    if event.key == pg.K_a:
                                        samurai.m_sound.stop()
                                        samurai.left_pressed = False
                                    elif event.key == pg.K_d:
                                        samurai.m_sound.stop()
                                        samurai.right_pressed = False
                                    elif event.key == pg.K_l:
                                        samurai.l_pressed = False     
                            else:
                                samurai.left_pressed = False
                                samurai.right_pressed = False
                        else:
                            samurai.left_pressed = False
                            samurai.right_pressed = False

                #As long as the player is alive, action and attacks will be allowed.
                if samurai.death == False:
                    game_options_button.display(window)

                    #Key input for sheathing/unsheathing the sword.
                    if key[pg.K_e]:
                        if samurai.l_pressed == False and samurai.o_change >= 1 and samurai.p_change >= 1:
                            if samurai.up_pressed == False and samurai.space_pressed == False:

                                #If the sword is sheathed, the sword will unsheathe with an unsheathing sound effect.
                                if samurai.u_change == 2:
                                    samurai.u_sound.play()
                                    samurai.u_display = True

                                #If the sword is unsheathed, the sword will sheathe with a sheathing sound effect.
                                elif samurai.u_change == 1:
                                    samurai.s_sound.play()
                                    samurai.s_display = True
                    
                    #Key input for throwing kunai. If the sword is unsheathing/sheathing, the player cannot use kunai.
                    elif key[pg.K_SPACE]:
                        if samurai.u_change >= 1 and samurai.o_change >= 1 and samurai.p_change >= 1:
                            if samurai.l_pressed == False and samurai.space_pressed == False and samurai.up_pressed == False:
                                if samurai.k_value > 0:
                                    if len(samurai.kunais) < 1:
                                        game.score += 10
                                        samurai.space_pressed = True
                                        samurai.k_value -= 1
                                        if samurai.left_facing == True:
                                            samurai.pn = -1
                                        elif samurai.right_facing == True:
                                            samurai.pn = 1
                                            
                                        #Displays the kunai from the player's position.
                                        samurai.k_sound.play()
                                        samurai.k_display = True
                                        samurai.kunais.append(Kunai(samurai.x, samurai.y))
                                else:
                                    samurai.space_pressed = False
                            else:
                                samurai.space_pressed = False
                        else:
                            samurai.space_pressed = False

                    #Key input for jumping. If the sword is unsheathing/sheathing, the player cannot jump.
                    elif key[pg.K_w]:
                        if samurai.u_change >= 1:
                            if samurai.l_pressed == False and samurai.o_change >= 1 and samurai.p_change >= 1:
                                if not samurai.stamina_value <= 0:
                                    if len(samurai.l_s) < 1:
                                        samurai.m_sound.stop()
                                        samurai.stamina_value -= 1
                                        samurai.s_index = 0
                                        samurai.l_s.append("loss")
                                    samurai.up_pressed = True
                            else:
                                samurai.up_pressed = False
                        else:
                            samurai.up_pressed = False
                    
                    #Key input for light attacking. If the sword is not unsheathed, samurai is in a jumping motion,
                    #throwing a kunai or empty on stamina, the player cannot use light attacks.
                    elif key[pg.K_o]:
                        if samurai.u_change == 1 and samurai.p_change >= 1:
                            if samurai.l_pressed == False and samurai.space_pressed == False and samurai.up_pressed == False:
                                if not samurai.stamina_value <= 1:
                                    if samurai.left_facing == True:
                                        samurai.l_a_change = 1
                                    elif samurai.right_facing == True:
                                        samurai.l_a_change = -1
                                    if samurai.o_change == 1:
                                        if len(samurai.l_s) < 1:    
                                            samurai.x += 100 * samurai.l_a_change
                                            samurai.m_sound.stop()
                                            samurai.a1_sound.play()
                                            samurai.stamina_value -= 2
                                            samurai.s_index = 0
                                            samurai.l_s.append("loss")
                                        samurai.l_a_display = True
                                    elif samurai.o_change == 2:
                                        if len(samurai.l_s) < 1:
                                            samurai.x += 30 * samurai.l_a_change
                                            samurai.m_sound.stop()
                                            samurai.a2_sound.play()
                                            samurai.stamina_value -= 2
                                            samurai.s_index = 0
                                            samurai.l_s.append("loss")
                                        samurai.l_a2_display = True
                                    elif samurai.o_change == 3:
                                        if len(samurai.l_s) < 1:
                                            samurai.x += 50 * samurai.l_a_change
                                            samurai.m_sound.stop()
                                            samurai.a3_sound.play()
                                            samurai.stamina_value -= 2
                                            samurai.s_index = 0
                                            samurai.l_s.append("loss")
                                        samurai.l_a3_display = True

                    #Key input for heavy attacking.
                    elif key[pg.K_p]:
                        if samurai.u_change == 1 and samurai.o_change >= 1:
                            if samurai.l_pressed == False and samurai.space_pressed == False and samurai.up_pressed == False:
                                if not samurai.stamina_value <= 2:
                                    if samurai.left_facing == True:
                                        samurai.h_a_change = 1
                                    elif samurai.right_facing == True:
                                        samurai.h_a_change = -1
                                    if samurai.p_change == 1:
                                        if len(samurai.l_s) < 1:
                                            samurai.x += 80 * samurai.h_a_change
                                            samurai.m_sound.stop()
                                            samurai.a3_sound.play()
                                            samurai.stamina_value -= 3
                                            samurai.s_index = 0
                                            samurai.l_s.append("loss")
                                        samurai.h_a_display = True
                                    elif samurai.p_change == 2:
                                        if len(samurai.l_s) < 1:
                                            samurai.x += 70 * samurai.h_a_change
                                            samurai.m_sound.stop()
                                            samurai.a1_sound.play()
                                            samurai.stamina_value -= 3
                                            samurai.s_index = 0
                                            samurai.l_s.append("loss")
                                        samurai.h_a2_display = True  

                #Once the player has lost, the RETURN button will reset everything
                #for the player to retry.
                elif game.end == True:
                    if key[pg.K_RETURN]:
                        samurai.reset()
                        archers.reset()
                        game.reset() 
                        samurai.enter_pressed = True

            #Displays the menu when paused, resets the A and D keys to stop the player from moving.
            if game.pause == 1:
                samurai.left_pressed = False
                samurai.right_pressed = False

                #Options backdrop
                if menu.bd == 1:
                    menu.display(window)

                    #A pause icon to indicate that the game is paused
                    pg.draw.rect(window, white, (1000, 42, 8, 45))
                    pg.draw.rect(window, white, (1020, 42, 8, 45))

                    button_1.display(window)
                    button_2.display(window)
                    button_3.display(window)
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            run_pg = False
                            pg.quit()
                            sys.exit()
                        elif event.type == pg.MOUSEMOTION:
                            if button_1.image_rect.collidepoint(mouse_x, mouse_y):
                                button_1.collide = True
                            else:
                                button_1.collide = False
                            if button_2.image_rect.collidepoint(mouse_x, mouse_y):
                                button_2.collide = True
                            else:
                                button_2.collide = False
                            if button_3.image_rect.collidepoint(mouse_x, mouse_y):
                                button_3.collide = True
                            else:
                                button_3.collide = False
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            if button_1.image_rect.collidepoint(mouse_x, mouse_y):
                                menu.enter_sound.play()
                                button_1.collide = False
                                menu.bd = 2
                            elif button_2.image_rect.collidepoint(mouse_x, mouse_y):
                                menu.enter_sound.play()
                                button_2.collide = False
                                menu.bd = 3
                            elif button_3.image_rect.collidepoint(mouse_x, mouse_y):
                                menu.return_sound.play()
                                button_3.collide = False
                                menu.bd = -1
                                game.pause = 0

                #Music backdrop
                elif menu.bd == 2:
                    menu.display(window)
                    menu.title(window, 20, 20)
                    pg.draw.rect(window, white, (1000, 42, 8, 45))
                    pg.draw.rect(window, white, (1020, 42, 8, 45))
                    menu.text(window, 20, 100)
                    button_1.display(window)
                    button_2.display(window)
                    button_3.display(window)
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            run_pg = False
                            pg.quit()
                            sys.exit()
                        elif event.type == pg.MOUSEMOTION:
                            if button_1.image_rect.collidepoint(mouse_x, mouse_y):
                                button_1.collide = True
                            else:
                                button_1.collide = False
                            if button_2.image_rect.collidepoint(mouse_x, mouse_y):
                                button_2.collide = True
                            else:
                                button_2.collide = False
                            if button_3.image_rect.collidepoint(mouse_x, mouse_y):
                                button_3.collide = True
                            else:
                                button_3.collide = False
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            if button_1.image_rect.collidepoint(mouse_x, mouse_y) and menu.pause == 0:
                                button_1.collide = False
                                menu.pause = 1
                                mx.music.pause()
                            elif button_1.image_rect.collidepoint(mouse_x, mouse_y) and menu.pause == 1:
                                button_1.collide = False
                                menu.pause = 0
                                mx.music.unpause()
                            elif button_2.image_rect.collidepoint(mouse_x, mouse_y):
                                button_2.collide = False
                                menu.pause = 0
                                menu.music()
                            elif button_3.image_rect.collidepoint(mouse_x, mouse_y):
                                menu.return_sound.play()
                                button_3.collide = False
                                menu.bd = 1     
                    pg.display.flip()
                
                #Controls backdrop
                elif menu.bd == 3:
                    menu.display(window)
                    menu.title(window, 20, 20)
                    pg.draw.rect(window, white, (1000, 42, 8, 45))
                    pg.draw.rect(window, white, (1020, 42, 8, 45))
                    menu.text(window, 20, 100)
                    menu.controls()
                    button_3.display(window)
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            run_pg = False
                            pg.quit()
                            sys.exit()
                        elif event.type == pg.MOUSEMOTION:
                            if button_3.image_rect.collidepoint(mouse_x, mouse_y):
                                button_3.collide = True
                            else:
                                button_3.collide = False
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            if button_3.image_rect.collidepoint(mouse_x, mouse_y):
                                menu.return_sound.play()
                                button_3.collide = False
                                menu.bd = 1
            
                #Exit pathway
                elif game.exit == True:
                    game.display(window)
                    game.pathway(window, 240, 240)
                    button_1.display(window)
                    button_2.display(window)
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            run_pg = False
                            pg.quit()
                            sys.exit()
                        elif event.type == pg.MOUSEMOTION:
                            if button_1.image_rect.collidepoint(mouse_x, mouse_y):
                                button_1.collide = True
                            else:
                                button_1.collide = False
                            if button_2.image_rect.collidepoint(mouse_x, mouse_y):
                                button_2.collide = True
                            else:
                                button_2.collide = False
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            if button_1.image_rect.collidepoint(mouse_x, mouse_y): 
                                menu.enter_sound.play()
                                button_1.collide = False
                                samurai.reset()
                                archers.reset()
                                game.reset()
                                run_pg = False
                                menu.bd = 0
                                game.r_fade()
                                samurai.enter_pressed = False
                                main_menu()                    
                            elif button_2.image_rect.collidepoint(mouse_x, mouse_y):
                                menu.return_sound.play()
                                button_2.collide = False
                                game.pause = 0
                                game.exit = False
        pg.display.flip()

#Initiates  music
mx.music.load(os.path.join("Music", "GOT menu theme.mp3"))

#Setting the loop to -1 makes it infinite.
mx.music.play(-1)

#Program starts...
main_menu()