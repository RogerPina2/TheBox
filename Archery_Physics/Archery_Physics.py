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

incremento_V = 0
valor_speed = 1
valor_life = 5
instante = 0

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

def atirar(Vo, teta):
    g = 10
    Voy = Vo*math.sin(teta)
    Vox = Vo*math.cos(teta)
    t = 0
    posicoes = []
    X = flecha_X
    Y = flecha_Y
    while X < 1200 and Y < 600:
        X = flecha_X + Vox*t
        Y = flecha_Y -Voy*t + (g/2)*t**2
        posicoes.append([int(X),int(Y)])
        t += 1
    print(posicoes)
    return posicoes       
    
def barra_vida(life):
 #5 = vida cheia, 0 = morto
    Lx, Ly = 50,100 #Posição inicial da barra de vida
    Bx, By = 20, 20 # Largura e Altura dos 6 blocos da barra de vida
    for i in range (0,5):
        if i < life:
            pygame.draw.rect(tela,(0,255,0), [Lx+Bx*i, Ly, Bx, By])
        else:
            pygame.draw.rect(tela,(255,0,0), [Lx+Bx*i, Ly, Bx, By])

def barra_speed(speed):
 #20 = mais rapido, 0 = mais lento
    Lx, Ly = 25,200 #Posição inicial da barra de velocidade
    Bx, By = 20, 20 #Largura e Altura dos bloco da vida
    for i in range (0,20):
        if i < speed:
            pygame.draw.rect(tela,(0,0,255), [Lx, Ly+By*(9-i), Bx, By])
        else:
            pygame.draw.rect(tela,(0,0,0), [Lx, Ly+By*(9-i), Bx, By])
    
# ===============   LOOPING PRINCIPAL   ===============
while rodando:
    tempo = relogio.tick(15)
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if valor_speed < 20: # 20 é o máximo de incrementos pra velocidade
                    incremento_V += 5
                    valor_speed +=1
                    print(incremento_V)

            elif event.key == pygame.K_SPACE:
                Vo= 60 + incremento_V
                percurso = True
    
            elif event.key == pygame.K_r:
                flecha.rect.centerx = 100
                flecha.rect.centery = 300
                incremento_V = 0
                valor_speed = 1
                valor_life = 5
                instante = 0
                percurso = False
                
            elif event.key == pygame.K_ESCAPE:
                game2 = None
                game = 'menu'

    # === SEGUNDA PARTE: LÓGICA DO JOGO ===
    if percurso == True:
        if instante == 0: 
            pos_flecha = atirar(Vo,math.pi/6)
        if instante < len(pos_flecha):
            flecha.rect.centerx = pos_flecha[instante][0]
            flecha.rect.centery = pos_flecha[instante][1]
            instante += 1

    if pygame.sprite.spritecollide(flecha,pessoa_group,False):
        percurso=False
        flecha.rect.centerx=1000
  
    if pygame.sprite.spritecollide(flecha,maca_group,False):
       if flecha.rect.centery>100:
            percurso=False
            flecha.rect.centerx=1000

# === TERCEIRA PARTE: GERA SAÍDAS (pinta tela, etc) ===
    if game2 == None:
        if game == 'menu':
            tela.blit(fundo_menu, (0,0))
            game2 = botao(153, 310, 227, 83, Story_Mode, Story_Mode_bright, ['jogo', 'jogo'])
        elif game == 'jogo':
            tela.blit(fundo_jogo, (0,0))
    else:
        tela.blit(fundo_jogo, (0,0))
        barra_vida(valor_life)
        barra_speed(valor_speed)
        flecha_group.draw(tela) # Pinta a imagem do grupo na tela auxiliar.
        arco_group.draw(tela)
        pessoa_group.draw(tela)
        maca_group.draw(tela)
            
    pygame.display.update()
pygame.display.quit()
