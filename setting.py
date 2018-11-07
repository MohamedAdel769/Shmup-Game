import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'Images')
font_dir = path.join(path.dirname(__file__), 'Fonts')
snd_dir = path.join(path.dirname(__file__), 'Sounds')

font_name = 'Hokjesgeest.ttf'
Title = "ShmupGame"
WIDTH = 480
HEIGHT = 600
FPS = 60
HEALTH = 100
BAR_LENGTH = 100
BAR_HEIGHT = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
