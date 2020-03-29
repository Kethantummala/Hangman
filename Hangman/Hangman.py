#Hangman Game

#Requirements
"""
pip install pygame
pip install screeninfo
"""

import os
import time
import random
import screeninfo
from screeninfo import get_monitors
import pygame

m=get_monitors()[0]
sc_width=m.width
sc_height=m.height

os.environ['SDL_VIDEO_CENTERED'] = '1'#Centering window before init.
#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
pygame.init()

White=(255,255,255)
Black=(0,0,0)
Blue=(0,0,255)
Yellow=(255,255,0)
Red=(255,0,0)
Green=(0,255,0)
Subtle_Green=(71, 129, 65)
Deepish_Light_Blue=(0, 217, 225)

gdd=[int(sc_width),int(sc_height-40)]
gameDisplay=pygame.display.set_mode(gdd,pygame.RESIZABLE)
pygame.display.set_caption('Let\'s play Hangman')
#Setup Done

clock=pygame.time.Clock()

font_multiple=10
font_Huge = pygame.font.SysFont(None,font_multiple*24)
font_Title = pygame.font.SysFont(None,font_multiple*12)
font_Caption = pygame.font.SysFont(None,font_multiple*6)
font_SubHeading = pygame.font.SysFont(None,font_multiple*10)
font_General_Text = pygame.font.SysFont(None,font_multiple*4)
font_Letters = pygame.font.SysFont(None,font_multiple*4)
font_Answer_Letters = pygame.font.SysFont(None,font_multiple*12)

size_scale=1.4
Shapes=["1","2","3","4","Man"]

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.notclicked=True
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.isOver()

    def draw(self,win):
        #Call this method to draw the button on the screen
        pygame.draw.ellipse(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            text = font_Letters.render(self.text, True, Black)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self):
        pos=pygame.mouse.get_pos()
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def show_shape(shape_name):
    #Shape1
    s1_s=(gdd[0]*.1,gdd[1]*.95)#shape1_start
    s1_e=(s1_s[0],s1_s[1]-((gdd[1]*.4)*size_scale))
    #Shape2
    s2_s=s1_e
    s2_e=(s2_s[0]+((gdd[0]*.175)*size_scale),s2_s[1])
    #Shape3
    s3_s=(s1_s[0],s1_e[1]+((gdd[1]*.06)*size_scale))
    s3_e=(s2_s[0]+((gdd[0]*.03)*size_scale),s2_s[1])
    #Shape4
    s4_s=(s2_e[0]-((gdd[0]*.02)*size_scale),s2_e[1])
    s4_e=(s4_s[0],s4_s[1]+((gdd[1]*.1)*size_scale))
    #man_head
    head_radius=int((gdd[1]*.02)*size_scale)
    #man_body
    body_s=(s4_e[0],s4_e[1]+head_radius*2)
    body_e=(s4_e[0],body_s[1]+((gdd[1]*.07)*size_scale))
    #man_leftarm
    mla_s=(body_s[0],body_s[1]+((gdd[1]*.015)*size_scale))
    mla_e=(body_s[0]-((gdd[0]*.015)*size_scale),body_s[1]+((gdd[1]*.04)*size_scale))
    #man_rightarm
    mra_s=(body_s[0],body_s[1]+((gdd[1]*.015)*size_scale))
    mra_e=(body_s[0]+((gdd[0]*.015)*size_scale),body_s[1]+((gdd[1]*.04)*size_scale))
    #man_leftleg
    mll_s=(body_e[0],body_e[1]-((gdd[1]*.01)*size_scale))
    mll_e=(body_e[0]-((gdd[0]*.015)*size_scale),body_e[1]+((gdd[1]*.025)*size_scale))
    #man_rightleg
    mrl_s=(body_e[0],body_e[1]-((gdd[1]*.01)*size_scale))
    mrl_e=(body_e[0]+((gdd[0]*.015)*size_scale),body_e[1]+((gdd[1]*.025)*size_scale))

    if shape_name=="1":
        pygame.draw.line(gameDisplay,Black,s1_s,s1_e,5)
    
    elif shape_name=="2":
        pygame.draw.line(gameDisplay,Black,s2_s,s2_e,5)
    
    elif shape_name=="3":
        pygame.draw.line(gameDisplay,Black,s3_s,s3_e,5)
    
    elif shape_name=="4":
        pygame.draw.line(gameDisplay,Black,s4_s,s4_e,5)

    elif shape_name=="Man":
        pygame.draw.circle(gameDisplay,Black,(int(s4_e[0]),int(s4_e[1]+head_radius)),head_radius,2)
        pygame.draw.line(gameDisplay,Black,body_s,body_e,7)
        pygame.draw.line(gameDisplay,Black,mla_s,mla_e,2)
        pygame.draw.line(gameDisplay,Black,mra_s,mra_e,2)
        pygame.draw.line(gameDisplay,Black,mll_s,mll_e,2)
        pygame.draw.line(gameDisplay,Black,mrl_s,mrl_e,2)

def gameExit():
    pygame.quit()
    exit()

def gameWon():

    GWButts=[]
    gameW=True
    print("Game Won")
    while gameW:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit()
            if event.type==pygame.MOUSEMOTION:
                for B in GWButts:
                    if B.isOver():
                        B.color=Yellow
                    else:
                        B.color=Deepish_Light_Blue
            if event.type==pygame.MOUSEBUTTONDOWN:
                if GWButts[0].isOver():
                    print(GWButts[0].text+" is clicked!")
                    Play()
                if GWButts[1].isOver():
                    print(GWButts[1].text+" is clicked!")
                    gameExit()
                if GWButts[2].isOver():
                    print(GWButts[2].text+" is clicked!")
                    startPage()
        
        #Clean Background
        gameDisplay.fill(White)

        #Title
        Title=font_Huge.render("YOU WON!",True,Red)
        gameDisplay.blit(Title,[gdd[0]*.3,gdd[1]*.2])

        #PlayGame Button
        B_PlayGame=button(Deepish_Light_Blue, gdd[0]*.23, gdd[1]*.6, gdd[0]*.15, gdd[1]*.15,"Play!")
        B_PlayGame.draw(gameDisplay)
        if B_PlayGame not in GWButts:
            GWButts.append(B_PlayGame)

        #ExitGame Button
        B_ExitGame=button(Deepish_Light_Blue, gdd[0]*.43, gdd[1]*.6, gdd[0]*.15, gdd[1]*.15,"Exit")
        B_ExitGame.draw(gameDisplay)
        if B_ExitGame not in GWButts:
            GWButts.append(B_ExitGame)

        #Instructions Button
        B_Instructions=button(Deepish_Light_Blue, gdd[0]*.63, gdd[1]*.6, gdd[0]*.15, gdd[1]*.15,"Instructions")
        B_Instructions.draw(gameDisplay)
        if B_Instructions not in GWButts:
            GWButts.append(B_Instructions)

        clock.tick(60)
        pygame.display.update()

def gameOver():

    GOButts=[]
    gameO=True
    print("Game Over")
    
    while gameO:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit()
            if event.type==pygame.MOUSEMOTION:
                for B in GOButts:
                    if B.isOver():
                        B.color=Yellow
                    else:
                        B.color=Deepish_Light_Blue
            if event.type==pygame.MOUSEBUTTONDOWN:
                if GOButts[0].isOver():
                    print(GOButts[0].text+" is clicked!")
                    Play()
                if GOButts[1].isOver():
                    print(GOButts[1].text+" is clicked!")
                    gameExit()
                if GOButts[2].isOver():
                    print(GOButts[2].text+" is clicked!")
                    startPage()
        
        #Clean Background
        gameDisplay.fill(White)

        #Title
        Title=font_Huge.render("GAME OVER!",True,Red)
        gameDisplay.blit(Title,[gdd[0]*.22,gdd[1]*.2])

        #PlayGame Button
        B_PlayGame=button(Deepish_Light_Blue, gdd[0]*.2, gdd[1]*.6, gdd[0]*.15, gdd[1]*.15,"Play!")
        B_PlayGame.draw(gameDisplay)
        if B_PlayGame not in GOButts:
            GOButts.append(B_PlayGame)

        #ExitGame Button
        B_ExitGame=button(Deepish_Light_Blue, gdd[0]*.4, gdd[1]*.6, gdd[0]*.15, gdd[1]*.15,"Exit")
        B_ExitGame.draw(gameDisplay)
        if B_ExitGame not in GOButts:
            GOButts.append(B_ExitGame)

        #Instructions Button
        B_Instructions=button(Deepish_Light_Blue, gdd[0]*.6, gdd[1]*.6, gdd[0]*.15, gdd[1]*.15,"Instructions")
        B_Instructions.draw(gameDisplay)
        if B_Instructions not in GOButts:
            GOButts.append(B_Instructions)

        clock.tick(60)
        pygame.display.update()
    
def Play():
    words=["ABANDON","BOUNDARY","CENTURY","DAY","EDGE"]
    answer=random.choice(words)
    Filled=[False]*8
    la=len(answer)
    no_hints=la//3
    Correct=no_hints
    while no_hints:
        x=random.randint(0,la-1)
        if not Filled[x]:
            Filled[x]=True
            no_hints-=1
    Butts=[]
    Blanks=[]
    Wrongs=0
    Playing=True

    a_n=1#Alphabet_Number
        
    while a_n<11:
        B_Created=button(Deepish_Light_Blue, gdd[0]*(.405+(a_n*.05)), gdd[1]*.63, gdd[0]*.04, gdd[1]*.04,chr(64+a_n))
        if B_Created not in Butts:
            Butts.append(B_Created)
        a_n+=1
    while a_n<21:
        B_Created=button(Deepish_Light_Blue, gdd[0]*(.405+((a_n-10)*.05)), gdd[1]*.73, gdd[0]*.04, gdd[1]*.04, chr(64+a_n))
        if B_Created not in Butts:
            Butts.append(B_Created)
        a_n+=1
    while a_n<27:
        B_Created=button(Deepish_Light_Blue, gdd[0]*(.405+((a_n-20)*.05)), gdd[1]*.83, gdd[0]*.04, gdd[1]*.04, chr(64+a_n))
        if B_Created not in Butts:
            Butts.append(B_Created)
        a_n+=1
    print("Game Started")
    
    while Playing:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit()
            if event.type==pygame.VIDEORESIZE:
                new_gdd=[event.size[0],event.size[1]-40]
                gdd[0]=int(new_gdd[0])
                gdd[1]=int(new_gdd[1])
                #new_gd=pygame.transform.scale(gameDisplay,new_gdd)
                #gameDisplay.blit(new_gd,(0,0))
                #pygame.display.update()
            if event.type==pygame.MOUSEMOTION:
                for B in Butts:
                    if B.notclicked:
                        if B.isOver():
                            B.color=Yellow
                        else:
                            B.color=Deepish_Light_Blue
            if event.type==pygame.MOUSEBUTTONDOWN:
                for B in Butts:
                    if B.isOver():
                        if B.notclicked:
                            print(B.text+" is clicked!")
                            print(B.notclicked)
                            B.notclicked=False
                            if B.text in answer:
                                B.color=Green
                                l_ind=answer.index(B.text)
                                
                                for ind in find(answer,answer[l_ind]):
                                    print(ind,Filled)
                                    if Filled[ind]==False:
                                        Filled[ind]=True
                                        Correct+=1
                                        print(la,Correct)
                                        if Correct==len(answer):
                                            gameWon()
                            else:
                                B.color=Red
                                Wrongs+=1
                            break

        #Clean Background
        gameDisplay.fill(White)

        #Title
        Title=font_Title.render("Hangman",True,Black)
        gameDisplay.blit(Title,[gdd[0]*.4,gdd[1]*.05])
        #Caption to the Title
        Caption=font_Caption.render("-Don't kill him!",True,Black)
        gameDisplay.blit(Caption,[gdd[0]*.6,gdd[1]*.05+90])

        for w in range(Wrongs):
            show_shape(Shapes[w])
            if w==4:
                pygame.display.update()
                time.sleep(1)
                gameOver()

        #Blanks
        B_n=1#Blank Number
        space=0
        while B_n<9:
            B_s=[gdd[0]*(.39+(B_n*.05))+space,gdd[1]*.51]#Blank Start position
            B_e=[B_s[0]+(gdd[0]*.03),gdd[1]*.51]
            Blanks.append(pygame.draw.line(gameDisplay,Blue,B_s,B_e,5))
            space+=(gdd[0]*.02)
            B_n+=1
        #Filling Unusable blanks
        unused=8-len(answer)
        ind=7
        for B in reversed(Blanks):
            if unused>0:
                filll = font_Answer_Letters.render("*", True, Black)
                gameDisplay.blit(filll, (B.x + (B.width/2 - filll.get_width()/2), B.y + (B.height/2 - filll.get_height())))
                Filled[ind]=True
                ind-=1
                unused-=1
                
        #Filling user answer
        for lpos in range(len(answer)):
            if Filled[lpos]:
                a_l = font_Answer_Letters.render(answer[lpos], True, Black)#Answer_Letter
                gameDisplay.blit(a_l, (Blanks[lpos].x + (Blanks[lpos].width/2 - a_l.get_width()/2), Blanks[lpos].y + (Blanks[lpos].height/2 - a_l.get_height())))
        
        #Alphabets
        gameDisplay.fill(Subtle_Green,rect=[gdd[0]*.45,gdd[1]*.6,gdd[0]*.5,gdd[1]*.3])#Buttons Background

        #Buttons
        a_n=1#Alphabet_Number
        
        while a_n<11:
            Butts[a_n-1].draw(gameDisplay)
            a_n+=1
        while a_n<21:
            Butts[a_n-1].draw(gameDisplay)
            a_n+=1
        while a_n<27:
            Butts[a_n-1].draw(gameDisplay)
            a_n+=1
        
        clock.tick(60)
        pygame.display.update()

def startPage():

    startP=True
    startButts=[]

    print("Start Menu Opened")
    
    while startP:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit()
            if event.type==pygame.MOUSEMOTION:
                for B in startButts:
                    if B.isOver():
                        B.color=Yellow
                    else:
                        B.color=Deepish_Light_Blue
            if event.type==pygame.MOUSEBUTTONDOWN:
                if startButts[0].isOver():
                    print(startButts[0].text+" is clicked!")
                    Play()
                if startButts[1].isOver():
                    print(startButts[1].text+" is clicked!")
                    gameExit()
    
        #Clean Background
        gameDisplay.fill(White)

        #Title
        Title=font_Title.render("Hangman",True,Black)
        gameDisplay.blit(Title,[gdd[0]*.4,gdd[1]*.05])

        #Instructions

        gameDisplay.fill(Subtle_Green,rect=[gdd[0]*.2,gdd[1]*.15,gdd[0]*.6,gdd[1]*.5])#Instructions Background

        #Heading
        Ins_Heading=font_SubHeading.render("Instructions",True,Blue)
        gameDisplay.blit(Ins_Heading,[gdd[0]*.4,gdd[1]*.17])

        #Points
        Ins_P1=font_General_Text.render("1) Guess the word to save the person.",True,Black)
        gameDisplay.blit(Ins_P1,[gdd[0]*.25,gdd[1]*.27])
        Ins_P2=font_General_Text.render("2) 5 wrong choices will kill him.",True,Black)
        gameDisplay.blit(Ins_P2,[gdd[0]*.25,gdd[1]*.37])
        Ins_P3=font_General_Text.render("3) Ignore ' * ' marked Blanks.",True,Black)
        gameDisplay.blit(Ins_P3,[gdd[0]*.25,gdd[1]*.47])

        #All The Best
        Ins_Wishes=font_Caption.render("All the Best!!!",True,Blue)
        gameDisplay.blit(Ins_Wishes,[gdd[0]*.45,gdd[1]*.55])
        
        #PlayGame Button
        B_PlayGame=button(Deepish_Light_Blue, gdd[0]*.3, gdd[1]*.7, gdd[0]*.1, gdd[1]*.1,"Play!")
        B_PlayGame.draw(gameDisplay)
        if B_PlayGame not in startButts:
            startButts.append(B_PlayGame)

        #ExitGame Button
        B_ExitGame=button(Deepish_Light_Blue, gdd[0]*.6, gdd[1]*.7, gdd[0]*.1, gdd[1]*.1,"Exit")
        B_ExitGame.draw(gameDisplay)
        if B_ExitGame not in startButts:
            startButts.append(B_ExitGame)

        clock.tick(60)
        pygame.display.update()

def gameLoop():

    startPage()
    Play()
    gameOver()
    gameExit()

gameLoop()
