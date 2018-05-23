import pygame
import math
import numpy as np
from pygame.locals import *

class Flecha(pygame.sprite.Sprite):
  def __init__(self, arquivo_imagem, pos_x, pos_y):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load(arquivo_imagem)
    self.rect = self.image.get_rect()
    self.rect.centerx = pos_x
    self.rect.centery = pos_y
    self.speedx=0
    self.speedy=0
      
  def update(self):

    self.speedx=0
    self.speedy=0

    percurso = False
    instante = 0
    Vo=(10000)**(1/2)
    Voy = Vo*math.sin(math.pi/4)
    g = 10

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_SPACE]:
        percurso = True

    while  percurso and pressed_keys[K_SPACE]:
        self.speedy = Vo*math.sin(math.pi/6)
        self.speedx = Vo*math.cos(math.pi/6)        
        if percurso == True:
            self.rect.centerx += 5
            self.rect.centery -= 5
            self.speedy=Voy-g*instante
            instante += 1

    if pressed_keys[K_r]:
        self.rect.centerx = 100
        self.rect.centery = 300
        instante=0
        percurso = False
    
class Arco(pygame.sprite.Sprite):
  def __init__(self, arquivo_imagem, pos_x, pos_y, start_angle):
    pygame.sprite.Sprite.__init__(self)

    self.original= pygame.image.load(arquivo_imagem)
    self.rotate (start_angle)
    self.rect = self.image.get_rect()
    self.rect.centerx = pos_x
    self.rect.centery = pos_y
    
  def rotate(self, angle):
    self.image = pygame.transform.rotate(self.original, angle)

class Pessoa(pygame.sprite.Sprite):
  def __init__(self, arquivo_imagem, pos_x, pos_y):
    pygame.sprite.Sprite.__init__(self)

    self.image= pygame.image.load(arquivo_imagem)
    self.rect = self.image.get_rect()
    self.rect.centerx = pos_x
    self.rect.centery = pos_y

class Maca(pygame.sprite.Sprite):
  def __init__(self, arquivo_imagem, pos_x, pos_y):
    pygame.sprite.Sprite.__init__(self)

    self.image= pygame.image.load(arquivo_imagem)
    self.rect = self.image.get_rect()
    self.rect.centerx = pos_x
    self.rect.centery = pos_y

# ===============   INICIALIZAÇÃO   ===============
pygame.init()
tela = pygame.display.set_mode((1200, 600), 0, 32)
pygame.display.set_caption('Arco e Flecha')
fundo = pygame.image.load("fundo 3.jpg").convert() # Carrega imagem de fundo.

# Cria flecha|arco e adiciona em um grupo de Sprites.
flecha = Flecha("flecha.png", 100,300)
flecha_group = pygame.sprite.Group()
flecha_group.add(flecha)

arco = Arco("arco.png", 100, 300, 0)
arco_group = pygame.sprite.Group()
arco_group.add(arco)

pessoa = Pessoa("pessoa1.png", 1000, 390)
pessoa_group = pygame.sprite.Group()
pessoa_group.add(pessoa)

maca = Maca("maca.png",1000,180)
maca_group = pygame.sprite.Group()
maca_group.add(maca)

# ===============   LOOPING PRINCIPAL   ===============

relogio = pygame.time.Clock()   
    
rodando = True

while rodando:
    tempo = relogio.tick(15)
    # === PRIMEIRA PARTE: LIDAR COM EVENTOS===   

    for event in pygame.event.get(): # Para cada evento não-processado na lista de eventos:
        if event.type == QUIT: # Verifica se o evento atual é QUIT (janela fechou).
            rodando = False

    # === SEGUNDA PARTE: LÓGICA DO JOGO ===
    #Movimento em x e em y

    if pygame.sprite.spritecollide(flecha,pessoa_group,False) or pygame.sprite.spritecollide(flecha,maca_group,False):
        flecha.rect.centerx=1000         

# === TERCEIRA PARTE: GERA SAÍDAS (pinta tela, etc) ===

    tela.blit(fundo, (0, 0)) # Pinta a imagem de fundo na tela auxiliar.

    flecha_group.draw(tela) # Pinta a imagem do grupo na tela auxiliar.
    arco_group.draw(tela)
    pessoa_group.draw(tela)
    maca_group.draw(tela)


    pygame.display.update() # Troca de tela na janela principal.
    flecha_group.update()

pygame.display.quit()