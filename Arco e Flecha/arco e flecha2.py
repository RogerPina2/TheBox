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
    self.rect.centerx = pos_x
    self.rect.centery = pos_y
      
  def move(self):
    self.rect.centerx += self.vx
    self.rect.centery += self.vy

    
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
flecha = Flecha("flecha.png", 100,300,0,0)
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
pressed_keys = pygame.key.get_pressed()

instante = 0
g = 10
teta = math.pi/4

rodando = True
percurso = False
valor=0

while rodando:
    tempo = relogio.tick(15)
    # === PRIMEIRA PARTE: LIDAR COM EVENTOS===  

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                valor += 1000
                print(valor)

            if event.key == pygame.K_SPACE:
                velocidade_inicial=1000+valor
                Vo=(velocidade_inicial)**(1/2)
                Voy = Vo*math.sin(math.pi/6)
                Vox = Vo*math.cos(math.pi/6)
                percurso = True
    
            if event.key == pygame.K_r:
                flecha.rect.centerx = 100
                flecha.rect.centery = 300
                instante=0
                valor=0
                percurso = False

        if event.type == QUIT: # Verifica se o evento atual é QUIT (janela fechou).
            rodando = False

    # === SEGUNDA PARTE: LÓGICA DO JOGO ===
    #Movimento em x e em y
    if percurso == True:
        Voy = Vo*math.sin(math.pi/6)
        Vox = Vo*math.cos(math.pi/6)
        Yo=flecha.rect.centery
        flecha.rect.centerx += Vox*instante
        flecha.rect.centery -= Voy-(g*instante**2)/2
        Vy=Voy-g*instante
        instante += 1

    if pygame.sprite.spritecollide(flecha,pessoa_group,False):
        flecha.rect.centerx=1000
        percurso=False

    if pygame.sprite.spritecollide(flecha,maca_group,False):
       if flecha.rect.centery>100:
            flecha.rect.centerx=1000
            percurso=False

# === TERCEIRA PARTE: GERA SAÍDAS (pinta tela, etc) ===

    tela.blit(fundo, (0, 0)) # Pinta a imagem de fundo na tela auxiliar.

    flecha_group.draw(tela) # Pinta a imagem do grupo na tela auxiliar.
    arco_group.draw(tela)
    pessoa_group.draw(tela)
    maca_group.draw(tela)

    pygame.display.update() # Troca de tela na janela principal.

pygame.display.quit()