import pygame
import math
import numpy as np
from pygame.locals import *

# ===============   INICIALIZAÇÃO   ===============
pygame.init()
tela = pygame.display.set_mode((1200, 600), 0, 32)
pygame.display.set_caption('Arco e Flecha')
fundo = pygame.image.load("fundo 3.jpg").convert() # Carrega imagem de fundo.

relogio = pygame.time.Clock()   
instante = 0
rodando = True
percurso = False

flecha_X = 100
flecha_Y = 300
pessoa_X = 1000
pessoa_Y = 390

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

flecha = Flecha("flecha.png", flecha_X,flecha_Y,0,0)
flecha_group = pygame.sprite.Group()
flecha_group.add(flecha)

arco = Arco("arco.png", 100, 300, 0)
arco_group = pygame.sprite.Group()
arco_group.add(arco)

pessoa = Pessoa("pessoa1.png", pessoa_X, pessoa_Y)
pessoa_group = pygame.sprite.Group()
pessoa_group.add(pessoa)

maca = Maca("maca.png",1000,180)
maca_group = pygame.sprite.Group()
maca_group.add(maca)

def atirar(Vo, teta):
    g = 10
    Voy = Vo*math.sin(teta)
    Vox = Vo*math.cos(teta)
    t = 0
    posicoes = []
    X = flecha_X
    while X < pessoa_X:
        X = flecha_X + Vox*t
        Y = flecha_Y -Voy*t + (g/2)*t**2
        posicoes.append([X,Y])
        t+= 1
    return posicoes       
    
# ===============   LOOPING PRINCIPAL   ===============
while rodando:
    tempo = relogio.tick(15)
    # === PRIMEIRA PARTE: LIDAR COM EVENTOS===   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                percurso = True
            elif event.key == pygame.K_r:
                percurso = False
                instante=0
                flecha.rect.centerx = 100
                flecha.rect.centery = 300

    # === SEGUNDA PARTE: LÓGICA DO JOGO ===
    if percurso == True:
        pos_flecha = atirar(110,math.pi/4) 
        flecha.rect.centerx = pos_flecha[instante][0]
        flecha.rect.centery = pos_flecha[instante][1]
        instante += 1

    if pygame.sprite.spritecollide(flecha,pessoa_group,False):
        flecha.rect.centerx=1000
        percurso=False

    if pygame.sprite.spritecollide(flecha,maca_group,False):
       if flecha.rect.centery>100:
            percurso=False
            flecha.rect.centerx=1000

# === TERCEIRA PARTE: GERA SAÍDAS (pinta tela, etc) ===
    tela.blit(fundo, (0, 0))
    flecha_group.draw(tela)
    arco_group.draw(tela)
    pessoa_group.draw(tela)
    maca_group.draw(tela)
    pygame.display.update()

pygame.display.quit()