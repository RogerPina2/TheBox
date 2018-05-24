import pygame
import math
import numpy as np
from pygame.locals import *

# ================ Classes ===================

class Flecha(pygame.sprite.Sprite):
    def __init__(self, arquivo_imagem, pos_x, pos_y, vel_x, start_angle):
        pygame.sprite.Sprite.__init__(self)
        
        self.vx = vel_x
        self.vy = -(start_angle)
        self.original = pygame.image.load(arquivo_imagem)
        self.image = pygame.transform.rotate(self.original, start_angle)
        self.rotate = pygame.transform.rotate(self.original, start_angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.centery = pos_y

    
class Arco(pygame.sprite.Sprite):
    def __init__(self, arquivo_imagem, pos_x, pos_y, start_angle):
        pygame.sprite.Sprite.__init__(self)

        self.original = pygame.image.load(arquivo_imagem)
        self.rotate = pygame.transform.rotate(self.original, start_angle)
        self.image = pygame.transform.rotate(self.original, start_angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.centery = pos_y
    

# ===============   INICIALIZAÇÃO   ===============
pygame.init()
tela = pygame.display.set_mode((1200, 600), 0, 32)
pygame.display.set_caption('Arco e Flecha')
fundo = pygame.image.load("fundo 3.jpg").convert() # Carrega imagem de fundo.

# Cria flecha|arco e adiciona em um grupo de Sprites.
flecha = Flecha("flecha.png", 100, 300, 10, 50)
flecha_group = pygame.sprite.Group()
flecha_group.add(flecha)

arco = Arco("arco.png", 100, 300, 0)
arco_group = pygame.sprite.Group()
arco_group.add(arco)

# ===============   LOOPING PRINCIPAL   ===============
jogo = True
tiro = False
angulo_flecha = -3
instante = 0
relogio = pygame.time.Clock()

while jogo:
    tempo = relogio.tick(15)
    
    # === PRIMEIRA PARTE: LIDAR COM EVENTOS=== 
    for event in pygame.event.get():
        if event.type == QUIT:
            jogo = False
    
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_a]:
        tiro = True;
        
    if pressed_keys[K_BACKSPACE]:
        flecha.rect.x = 100
        flecha.rect.y = 225
        flecha.image = flecha.rotate
        instante = 0
        tiro = False
        
    # === SEGUNDA PARTE: LÓGICA DO JOGO ===
    if tiro == True:
        flecha.rect.x += flecha.vx
        flecha.rect.y += flecha.vy + instante*3
        flecha.image = pygame.transform.rotate(flecha.image, angulo_flecha)
        
        instante += 1
    
    #mouse = pygame.mouse.get_pos()
    #print(mouse)
    
    #if flecha.rect.y >= 300:
      #  tiro = False

    
    
    
    
    
# === TERCEIRA PARTE: GERA SAÍDAS (pinta tela, etc) ===

    tela.blit(fundo, (0, 0)) # Pinta a imagem de fundo na tela auxiliar.
    
    flecha_group.draw(tela) # Pinta a imagem do grupo na tela auxiliar.
    arco_group.draw(tela)
    
    pygame.display.update() # Troca de tela na janela principal.

pygame.display.quit()




