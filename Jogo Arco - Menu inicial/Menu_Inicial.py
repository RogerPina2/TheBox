# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:28:53 2018

@author: roger.pina
"""

import pygame
import math
import numpy as np
from pygame.locals import *

# ============== Classes ==================

# ===============   INICIALIZAÇÃO   ===============
pygame.init()

tela = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Arco e Flecha v1.0')

fundo = pygame.image.load("fundo.png").convert()
Story_Mode = pygame.image.load("Story-Mode_227x83.png").convert()
Story_Mode_bright = pygame.image.load("Story-Mode_bright_227x83.png").convert()

def botão(pos_X, pos_Y, comp, larg, image1, image2, action=None):
    mouse = pygame.mouse.get_pos() 
    click = pygame.mouse.get_pressed()
    
    if pos_X+comp > mouse[0] > pos_X and pos_Y+larg > mouse[1] > pos_Y:
        tela.blit(image2, (pos_X, pos_Y))
        if click[0] == 1 and action != None:
            action()
    else:
        tela.blit(image1, (pos_X, pos_Y))

def quitgame():
    pygame.quit()
    quit()
        
# ===============   LOOPING PRINCIPAL   ===============
start = True
relogio = pygame.time.Clock()

while start:
    
    tempo = relogio.tick(30)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            start = False
            
# === TERCEIRA PARTE: GERA SAÍDAS (pinta tela, etc) ===
    
    tela.blit(fundo, (0, 0))
    
    botão(153, 310, 227, 83, Story_Mode, Story_Mode_bright, quitgame)
    
    #if 153+227 > mouse[0] > 153 and 310+83 > mouse[1] > 310:
     #   tela.blit(Story_mode_bright, (153, 310))
    #else:
     #   tela.blit(Story_mode, (153, 310))
        
    pygame.display.update()
    
pygame.display.quit()
