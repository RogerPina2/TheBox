import pygame
import math
from pygame.locals import *

# ===============   INICIALIZAÇÃO   ===============
pygame.init()
tela = pygame.display.set_mode((1200,600), 0,32)
pygame.display.set_caption('Archery Physics')
fundo_menu = pygame.image.load('fundo_menu.png').convert()
fundo_jogo = pygame.image.load("fundo 3.jpg").convert()
Story_Mode = pygame.image.load("Story-Mode_227x83.png")
Story_Mode_bright = pygame.image.load("Story-Mode_bright_227x83.png")

relogio = pygame.time.Clock()   
rodando = True
percurso = False
game = 'menu'
game2 = None    

teta = math.pi/4
instante = 0
valor=0
g = 10

# ============== Posições ==================
flecha_X, flecha_Y = 100, 300
arco_X, arco_Y = 100, 300
pessoa_X, pessoa_Y = 1000, 390
maca_X, maca_Y = 1000, 180

# ============== Classes ==================
class Flecha(pygame.sprite.Sprite):
  def __init__(self, arquivo_imagem, pos_x, pos_y, vel_x, vel_y):
    pygame.sprite.Sprite.__init__(self)
    self.vx = vel_x
    self.vy = vel_y
    self.image = pygame.image.load(arquivo_imagem)
    self.rect = self.image.get_rect()
    self.rect.centerx = pos_x
    self.rect.centery = pos_y
    
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

# ===============   Sprites e Grupos   ===============
flecha = Flecha("flecha.png", flecha_X,flecha_Y,0,0)
arco = Arco("arco.png", arco_X, arco_Y, 0)
pessoa = Pessoa("pessoa1.png", pessoa_X, pessoa_Y)
maca = Maca("maca.png",maca_X, maca_Y)

flecha_group = pygame.sprite.Group()
arco_group = pygame.sprite.Group()
pessoa_group = pygame.sprite.Group()
maca_group = pygame.sprite.Group()

flecha_group.add(flecha)
arco_group.add(arco)
pessoa_group.add(pessoa)
maca_group.add(maca)
    
# ===============   FUNÇÕES   ===============
def botao(pos_X, pos_Y, comp, larg, image1, image2, valor):
    mouse = pygame.mouse.get_pos() 
    click = pygame.mouse.get_pressed()
    
    if pos_X+comp > mouse[0] > pos_X and pos_Y+larg > mouse[1] > pos_Y:
        tela.blit(image2, (pos_X, pos_Y))
        if click[0] == 1:
            game = valor[0]
            game2 = valor[1]
            return game, game2

    else:
        tela.blit(image1, (pos_X, pos_Y))
        
def quitgame():
    pygame.quit()
    quit()

# ===============   LOOPING PRINCIPAL   ===============
while rodando:
    tempo = relogio.tick(15)
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                valor += 1000
                print(valor)

            elif event.key == pygame.K_SPACE:
                velocidade_inicial=1000+valor
                Vo=(velocidade_inicial)**(1/2)
                Voy = Vo*math.sin(math.pi/6)
                Vox = Vo*math.cos(math.pi/6)
                percurso = True
    
            elif event.key == pygame.K_r:
                flecha.rect.centerx = 100
                flecha.rect.centery = 300
                instante=0
                valor=0
                percurso = False
                
            elif event.key == pygame.K_ESCAPE:
                game2 = None
                game = 'menu'

    # === SEGUNDA PARTE: LÓGICA DO JOGO ===
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
    if game2 == None:
        if game == 'menu':
            tela.blit(fundo_menu, (0,0))
            game2 = botao(153, 310, 227, 83, Story_Mode, Story_Mode_bright, ['jogo', 'jogo'])
        elif game == 'jogo':
            tela.blit(fundo_jogo, (0,0))
    else:
        tela.blit(fundo_jogo, (0,0))
        flecha_group.draw(tela) # Pinta a imagem do grupo na tela auxiliar.
        arco_group.draw(tela)
        pessoa_group.draw(tela)
        maca_group.draw(tela)
            
    pygame.display.update()
pygame.display.quit()
