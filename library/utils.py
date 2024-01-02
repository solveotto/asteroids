import os
import pygame
import math

from library import player

pygame.init()


### CONSTANTS ###
# Fysikk
FD_FRIC = 0.5
BD_FRIC = 0.1
PLAYER_MAX_SPEED = 20.0
PLAYER_MAX_RTSPEED = 10

# Skjerm
DISPLAY_WIDTH  = 800
DISPLAY_HEIGHT = 600

# Color
WHITE = (255, 255, 255)
YELLOW = (231, 245, 39)
BLACK = (0, 0, 0)

# Fonts
FONT_PATH = 'fonts/Hyperspace-JvEM.ttf' 
FONT_SIZE = 36 
CUSTOM_FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)

# SOUNDS
SOUND_PATH = os.path.join('.', 'sounds/')
SND_CHANNEL_FIRE = pygame.mixer.Channel(0)
SND_CHANNEL_UFO = pygame.mixer.Channel(1)
SND_CHANNEL_THRUST = pygame.mixer.Channel(2)
SND_CHANNEL_OTHER = pygame.mixer.Channel(3)

# Volume
SND_CHANNEL_UFO.set_volume(0.1)

# SndFX
SND_FIRE = pygame.mixer.Sound(SOUND_PATH+"fire.wav")
SND_THRUST = pygame.mixer.Sound(SOUND_PATH+"thrust.wav")
SND_UFO_SMALL = pygame.mixer.Sound(SOUND_PATH+"saucerSmall.wav")
SND_UFO_LARGE = pygame.mixer.Sound(SOUND_PATH+"saucerBig.wav")
SND_BANG_SMALL = pygame.mixer.Sound(SOUND_PATH+"bangSmall.wav")
SND_BANG_MEDIUM = pygame.mixer.Sound(SOUND_PATH+"bangMedium.wav")
SND_BANG_LARGE = pygame.mixer.Sound(SOUND_PATH+"bangLarge.wav")
SND_EXTRA_SHIP = pygame.mixer.Sound(SOUND_PATH+"extraShip.wav")


CLOCK = pygame.time.Clock()

ICON = pygame.image.load('images/icon.png')
pygame.display.set_caption("Asteroids")
pygame.display.set_icon(ICON)
SCREEN = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))


def collision(x, y, x2, y2, size):
    if x > x2 - size and x < x2 + size and y > y2 - size and y < y2 + size:
        return True
    return False

def drawText(msg, x, y, size, color, orient="centered"):
    text = pygame.font.Font(FONT_PATH, size).render(msg, True, color)
    if orient == "centered":
        # lager et rektangel med koordinatene til texten
        rect = text.get_rect()
        rect.center = (x, y)
    elif orient == "right":
        rect = text.get_rect()
        rect.right = x
        rect.y = y
    elif orient == "left":
        rect = text.get_rect()
        rect.left = x
        rect.y = y
    else:
        rect = (x,y)
    SCREEN.blit(text, rect)



def check_warp(input_x, input_y):
    
    x = input_x
    y = input_y

    if input_y < 0:
        y = DISPLAY_HEIGHT
    elif input_y > DISPLAY_HEIGHT:
        y = 0
    elif input_x < 0:
        x = DISPLAY_WIDTH
    elif input_x > DISPLAY_WIDTH:
        x = 0

    return x, y 



def killPlayer(plyr, debr):
    plyr.player_pieces.append(player.DeadPlayer(plyr.x, plyr.y, 5 * plyr.size / (2 * math.cos(math.atan(1 / 3)))))
    plyr.player_pieces.append(player.DeadPlayer(plyr.x, plyr.y, plyr.size))
    plyr.player_pieces.append(player.DeadPlayer(plyr.x, plyr.y, plyr.size / 2))

    debr.create_debris(plyr.x, plyr.y, 10)
    SND_CHANNEL_OTHER.play(SND_BANG_LARGE)

    # Spiller dør
    plyr.state = "dead"
    plyr.invisible_dur  = 120
    plyr.spawn_dur = 60
    plyr.lives -= 1
    plyr.resetPlayer()

