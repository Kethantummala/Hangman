#Hangman Game

#Requirements
"""
pip install pygame
pip install screeninfo
"""

import os
import pygame
import screeninfo
from screeninfo import get_monitors

m=get_monitors()[0]
sc_width=m.width
sc_height=m.height

os.environ['SDL_VIDEO_CENTERED'] = '1'#Centering window before init.
#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
pygame.init()

White=(255,255,255)
Black=(0,0,0)
Red=(255,0,0)
Green=(0,255,0)
Blue=(0,0,255)

gdd=(int(sc_width),int(sc_height-40))
gameDisplay=pygame.display.set_mode(gdd,pygame.RESIZABLE)
pygame.display.set_caption('Let\'s play Hangman')
#Setup Done

gameExit=False

while not gameExit:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            gameExit=True
    
    gameDisplay.fill(White)
    #Shape1
    s1_s=(gdd[0]*.15,gdd[1]*.85)#shape1_start
    s1_e=(s1_s[0],s1_s[1]-gdd[1]*.4)
    pygame.draw.line(gameDisplay,Black,s1_s,s1_e,5)
    #Shape2
    s2_s=s1_e
    s2_e=(s2_s[0]+gdd[0]*.15,s2_s[1])
    pygame.draw.line(gameDisplay,Black,s2_s,s2_e,5)
    #Shape3
    s3_s=(s1_s[0],s1_e[1]+gdd[1]*.06)
    s3_e=(s2_s[0]+gdd[0]*.03,s2_s[1])
    pygame.draw.line(gameDisplay,Black,s3_s,s3_e,5)
    #Shape4
    s4_s=(s2_e[0]-gdd[0]*.02,s2_e[1])
    s4_e=(s4_s[0],s4_s[1]+gdd[1]*.15)
    pygame.draw.line(gameDisplay,Black,s4_s,s4_e,5)
    pygame.display.update()





pygame.quit()
#quit()
