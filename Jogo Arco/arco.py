import pygame
import math
import numpy as np
from pygame.locals import *

class Flecha(pygame.sprite.Sprite):
  def __init__(self, arquivo_imagem, pos_x, pos_y):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load(arquivo_imagem)
    self.rect = self.image.get_rect()
    self.rect.x = pos_x
    self.rect.y = pos_y
    
class Arco(pygame.sprite.Sprite):
  def __init__(self, arquivo_imagem, pos_x, pos_y):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load(arquivo_imagem)
    self.rect = self.image.get_rect()
    self.rect.x = pos_x
    self.rect.y = pos_y

# ===============   INICIALIZAÇÃO   ===============
pygame.init()
tela = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Arco e Flecha v1.0')
fundo = pygame.image.load("fundo-800X600.jpg").convert() # Carrega imagem de fundo.

# Cria flecha|arco e adiciona em um grupo de Sprites.
flecha = Flecha("flecha-80x15.png", 140,365)
flecha_group = pygame.sprite.Group()
flecha_group.add(flecha)
arco = Arco("arco-90X160.png", 100, 300)
arco_group = pygame.sprite.Group()
arco_group.add(arco)


# ===============   LOOPING PRINCIPAL   ===============
rodando = True
percurso = False;
relogio = pygame.time.Clock()

deltaT = 1/30
instante = 0
Voy = -70
Vox = 20
g = 10
teta = 0


while rodando:
    tempo = relogio.tick(30)
    # === PRIMEIRA PARTE: LIDAR COM EVENTOS ===
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_UP]:
        percurso = True;
        Ltempo = np.arange(0,2,deltaT)
        
    for event in pygame.event.get(): # Para cada evento não-processado na lista de eventos:
        if event.type == QUIT: # Verifica se o evento atual é QUIT (janela fechou).
            rodando = False

    # === SEGUNDA PARTE: LÓGICA DO JOGO ===
    #DeltaSy entre t=(N+1) e t =(N) = Voy-(g/2)*(2*N+1)
    if percurso == True:
        flecha.rect.x += Vox
        flecha.rect.y += Voy+(g/2)*(2*instante+1)
        Vy = Voy - g*instante
        teta = Vy/Vox
        flecha.image = pygame.transform.rotate(flecha.image, teta)
        instante += 1
        if instante == len(Ltempo):
            instante = 0
            percurso = False

# === TERCEIRA PARTE: GERA SAÍDAS (pinta tela, etc) ===

    tela.blit(fundo, (0, 0)) # Pinta a imagem de fundo na tela auxiliar.

    flecha_group.draw(tela) # Pinta a imagem do grupo na tela auxiliar.
    arco_group.draw(tela)

    pygame.display.update() # Troca de tela na janela principal.

pygame.display.quit()
