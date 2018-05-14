import pygame
import math
import numpy as np
from pygame.locals import *

class Flecha(pygame.sprite.Sprite):
  def __init__(self, arquivo_imagem, pos_x, pos_y, vel_x, vel_y):
    pygame.sprite.Sprite.__init__(self)

    self.vx = vel_x
    self.vy = vel_y
    self.image = pygame.image.load(arquivo_imagem)
    self.rect = self.image.get_rect()
    self.rect.x = pos_x
    self.rect.y = pos_y
      
  def move(self):
    self.rect.x += self.vx
    self.rect.y += self.vy

    
class Arco(pygame.sprite.Sprite):
  def __init__(self, arquivo_imagem, pos_x, pos_y, start_angle):
    pygame.sprite.Sprite.__init__(self)

    self.original= pygame.image.load(arquivo_imagem)
    self.rotate (start_angle)
    self.rect = self.image.get_rect()
    self.rect.x = pos_x
    self.rect.y = pos_y
    
  def rotate(self, angle):
    self.image = pygame.transform.rotate(self.original, angle)

# ===============   INICIALIZAÇÃO   ===============
pygame.init()
tela = pygame.display.set_mode((1200, 600), 0, 32)
pygame.display.set_caption('Arco e Flecha')
fundo = pygame.image.load("fundo 3.jpg").convert() # Carrega imagem de fundo.

# Cria flecha|arco e adiciona em um grupo de Sprites.
flecha = Flecha("flecha.png", 100,375,0,0)
flecha_group = pygame.sprite.Group()
flecha_group.add(flecha)

arco = Arco("arco.png", 100, 300, 0)
arco_group = pygame.sprite.Group()
arco_group.add(arco)


# ===============   LOOPING PRINCIPAL   ===============
rodando = True
percurso = False
relogio = pygame.time.Clock()   

instante = 0
Vo=(10000)**(1/2)
Voy = Vo*math.sin(math.pi/4)
Vox = Vo*math.cos(math.pi/4)
g = 10
teta = math.pi/4

while rodando:
    tempo = relogio.tick(15)
    # === PRIMEIRA PARTE: LIDAR COM EVENTOS===   
    
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_a]:
        percurso = True;
        
    if pressed_keys[K_BACKSPACE]:
        flecha.rect.x = 100
        flecha.rect.y = 375
        percurso = False
  

    for event in pygame.event.get(): # Para cada evento não-processado na lista de eventos:
        if event.type == QUIT: # Verifica se o evento atual é QUIT (janela fechou).
            rodando = False

    # === SEGUNDA PARTE: LÓGICA DO JOGO ===
    #Movimento em x e em y
    if percurso == True:
        Yo=flecha.rect.y
        flecha.rect.x += Vox*instante
        flecha.rect.y -= Voy-(g*instante**2)/2
        Vy=Voy-g*instante
        teta = Vy/Vox
#        flecha.image = pygame.transform.rotate(flecha.image, teta)
        instante += 1
        
        if flecha.rect.x>900:            
            instante = 0
            percurso = False
        if flecha.rect.y>500:
            instante = 0
            percurso = False
            

# === TERCEIRA PARTE: GERA SAÍDAS (pinta tela, etc) ===

    tela.blit(fundo, (0, 0)) # Pinta a imagem de fundo na tela auxiliar.

    flecha_group.draw(tela) # Pinta a imagem do grupo na tela auxiliar.
    arco_group.draw(tela)

    pygame.display.update() # Troca de tela na janela principal.

pygame.display.quit()
