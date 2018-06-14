import pygame
import time
import math
import random
from pygame.locals import *

# ============== Posições ==================
larguraTela, alturaTela = 1200, 600
flecha_X, flecha_Y = 110, 420
arco_X, arco_Y = 120, 420
pessoa_X, pessoa_Y = 1000, 450
maca_X, maca_Y = 1000, 330

# ===============   INICIALIZAÇÃO   ===============
pygame.init()
pygame.mixer.music.load("song.wav")
tela = pygame.display.set_mode((larguraTela,alturaTela), 0,32)
pygame.display.set_caption('Archery Physics')
font = pygame.font.SysFont(None, 25)
relogio = pygame.time.Clock()   
 
# ===============   Imagens   ===============
fundo_menu = pygame.image.load('fundo_menu.png').convert()
fundo_jogo = pygame.image.load("fundo 3.jpg").convert()
fundo_tutorial = pygame.image.load("fundo_tutorial.png")
Game_Over = pygame.image.load("Game_Over.png")
You_Win = pygame.image.load("You_Win.png")
Story_Mode = pygame.image.load("Story-Mode_227x83.png")
Story_Mode_bright = pygame.image.load("Story-Mode_bright_227x83.png")
Tutorial = pygame.image.load("Tutorial.png")
Tutorial_bright = pygame.image.load("Tutorial_bright.png")
Menu = pygame.image.load("Menu.png")
Menu_bright = pygame.image.load("Menu_bright.png")
Jogar_Novamente = pygame.image.load("Jogar_Novamente.png")
Jogar_Novamente_bright = pygame.image.load("Jogar_Novamente_bright.png")
Next_Level = pygame.image.load("Next_Level.png")
Next_Level_bright = pygame.image.load("Next_Level_bright.png")
Mini_Flecha = pygame.image.load("Mini_Flecha.png")

# ===============   Variáveis   ===============
rodando = True  #Loop principal do jogo
fim_percurso = False #True enquanto estiver na posição do final do seu percurso
percurso = False #True enquanto a flecha estiver em movimento
gameOver= False #True enquanto jogador nao decidir se continua ou sai depois que perder
segura_W = False #True enquanto pressionar w
recomeca = False # True pra reinciar a flecha

modos = {'jogo' : 0, 'tutorial' : 0, 'game_over' : 0, 'jogar_dnv' : 0, 'menu' : 0, 'win' : 0}
max_V = 100 #máxima incremento a velocidade inicial(Vo = 60)
valor_speed = 1 #valor da velocidade mostrada na barra (1 a 100)
valor_life = 3  #valor da vida do personagem (3 a 0)
instante = 0 #contador pra movimentar a flecha
numero_de_flechas = 5 #Numero de flechas do jogador

# ============== Classes ==================
class Flecha(pygame.sprite.Sprite):
   def __init__(self, arquivo_imagem, pos_x, pos_y):
     pygame.sprite.Sprite.__init__(self)
     self.image = pygame.image.load(arquivo_imagem)
     self.rect = self.image.get_rect()
     self.rect.centerx = pos_x
     self.rect.centery = pos_y
  
class Arco(pygame.sprite.Sprite):
   def __init__(self, arquivo_imagem, pos_x, pos_y):
     pygame.sprite.Sprite.__init__(self)
     self.image= pygame.image.load(arquivo_imagem)
     self.rect = self.image.get_rect()
     self.rect.centerx = pos_x
     self.rect.centery = pos_y
     

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

flecha = Flecha("flecha.png", flecha_X,flecha_Y)
arco = Arco("arco.png", arco_X, arco_Y)
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
def botao(pos_X, pos_Y, image1, image2, arg, arg2):
     mouse = pygame.mouse.get_pos() 
     click = pygame.mouse.get_pressed()
     comp = 227
     larg = 83
     
     if pos_X+comp > mouse[0] > pos_X and pos_Y+larg > mouse[1] > pos_Y:
         tela.blit(image2, (pos_X, pos_Y))
         if click[0] == 1:
             i = 0
             while i < len(arg):
                 modos[arg[i]] = arg2[i]
                 i += 1
     else:
         tela.blit(image1, (pos_X, pos_Y))

def quitgame():
     pygame.quit()
     quit()
 
def atirar(Vo, teta):
    g = 10
    Voy = Vo*math.sin(teta)
    Vox = Vo*math.cos(teta)
    
    #Quando machuca o amigo, vc fica com medo e sua inacuracia aumenta
    print(teta)
    inac = random.randint(0,100)*0.01*(4-valor_life)
    ang = inac*teta
    print(ang)
    t = 0
    posicoes = []
    X = flecha_X
    Y = flecha_Y
    while X < larguraTela and Y < alturaTela:
        X = flecha_X + Vox*t
        Y = flecha_Y -Voy*t + (g/2)*t**2
        posicoes.append([int(X),int(Y)])
        t += 1
    return posicoes       
    
def barra_vida(life):
 #3 = vida cheia, 0 = morto
    Lx, Ly = 900,50 #Posição inicial da barra de vida
    Bx, By = 80, 20 # Largura e Altura dos 4 blocos da barra de vida
    for i in range (0,3):
        if i < life:
            pygame.draw.rect(tela,(0,255,0), [Lx+Bx*i, Ly, Bx, By])
        else:
            pygame.draw.rect(tela,(255,0,0), [Lx+Bx*i, Ly, Bx, By])

def barra_speed(speed):
    Lx, Ly = 25,150 #Posição inicial da barra de velocidade
    Bx, By = 20, 3 #Largura e Altura dos bloco da vida
    for i in range (0,max_V):
        if i < speed:
            pygame.draw.rect(tela,(0,0,255), [Lx, Ly+By*(max_V-i), Bx, By])
        else:
            pygame.draw.rect(tela,(0,0,0), [Lx, Ly+By*(max_V-i), Bx, By])
 
# ===============   LOOPING PRINCIPAL   ===============

pygame.mixer.music.play(-1)
while rodando:
    tempo = relogio.tick(15)
    if recomeca == True: #Recomeça a partida
        recomeca = False
        percurso = False
        fim_percurso = False
        flecha.rect.centerx = flecha_X
        flecha.rect.centery = flecha_Y
        valor_speed = 1
        instante = 0
        
    # ---------  Eventos  ---------
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            quitgame()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if valor_speed < max_V and fim_percurso == False and modos['game_over'] == 0 and modos['win'] == 0: 
                    segura_W = True
                
            elif event.key == pygame.K_ESCAPE:
                modos['jogo'] = 0
                modos['tutorial'] = 0
                modos['game_over'] = 0
                modos['win'] = 0 
                recomeca = True
                valor_life = 3
                numero_de_flechas = 5
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w and modos['game_over'] == 0 and modos['win'] == 0: 
                segura_W  = False
                if fim_percurso == False:
                    Vel= 60 + valor_speed
                    percurso = True
    
    # === SEGUNDA PARTE: LÓGICA DO JOGO ===
    if valor_life == 0:     #Se vida = 0 -> Gameover, recomeça e enche a vida
        modos['game_over'] = 1
        valor_life = 3
        numero_de_flechas = 5
        recomeca = True
        
    if fim_percurso == True: #Espera 1 seg. e recomeça se a flecha estiver no fim do percurso
        time.sleep(1)
        recomeca = True
        
    if percurso == True: #Calcula a trajetoria da flecha e move ela pela tela
        if instante == 0: #Calcula a trajetoria da flecha se ainda não foi calculada
            pos_flecha = atirar(Vel,math.pi/6)
            numero_de_flechas -= 1
        if instante < len(pos_flecha): #Move a flecha pela trajetoria calculada
            fx = pos_flecha[instante][0]
            fy = pos_flecha[instante][1]
            if fx < larguraTela and fy < alturaTela:
                flecha.rect.centerx = fx
                flecha.rect.centery = fy
                instante += 1
            else:
                fim_percurso = True


    if segura_W == True: # Enquanto o botão estiver pressionado adiciona 2 ao valor da velocidade
        valor_speed +=2
 
    if pygame.sprite.spritecollide(flecha,pessoa_group,False):
        fim_percurso = True
        if percurso == True:
            valor_life -= 1
        percurso=False
        flecha.rect.centerx=1000    

    if pygame.sprite.spritecollide(flecha,maca_group,False):
        fim_percurso = True
        modos['win'] = 1
        valor_life = 3
        numero_de_flechas = 5
        recomeca = True
        
        if flecha.rect.centery>100:
            percurso=False
            flecha.rect.centery = 180
            flecha.rect.centerx=1000
    
    if flecha.rect.centery>alturaTela or flecha.rect.centerx>larguraTela:
        fim_percurso = True
        recomeca = True
        
    if numero_de_flechas == 0 and fim_percurso == True:
        modos['game_over'] = 1
        valor_life = 3
        numero_de_flechas = 5
        recomeca = True
        
# === TERCEIRA PARTE: GERA SAÍDAS (pinta tela, etc) ===
    
    if modos['jogo'] == 1:
        tela.blit(fundo_jogo, (0,0))
        tela.blit(fundo_jogo, (0,0))
        tela.blit(Mini_Flecha, (20,20))
        barra_vida(valor_life)
        barra_speed(valor_speed)
        flecha_group.draw(tela)
        arco_group.draw(tela)
        pessoa_group.draw(tela)
        maca_group.draw(tela)
        screen_text = font.render('x {0}'.format(numero_de_flechas), True, (0,0,0))
        tela.blit(screen_text, [70,40])
        
        if modos['game_over'] == 1:
            flecha_group.draw(tela)
            tela.blit(Game_Over, (301,151))
            botao(350, 310, Menu, Menu_bright, ['jogo','game_over','tutorial'], [0,0,0])
            botao(625, 310, Jogar_Novamente, Jogar_Novamente_bright, ['game_over'], [0])
            
        elif modos['win'] == 1:
            flecha_group.draw(tela)
            maca_group.draw(tela)
            tela.blit(You_Win, (301,151))
            botao(350, 310, Menu, Menu_bright, ['jogo','win'], [0,0])
            botao(625, 310, Next_Level, Next_Level_bright, ['win'], [0])
        
    elif modos['tutorial'] == 1:
        tela.blit(fundo_tutorial, (0,0))
        botao(485, 480, Menu, Menu_bright, ['jogo','game_over','tutorial'], [0,0,0])
 
    else: 
        tela.blit(fundo_menu, (0,0))
        botao(153, 310, Story_Mode, Story_Mode_bright, ['jogo'], [1])
        botao(487, 310, Tutorial, Tutorial_bright, ['tutorial'], [1])    

    pygame.display.update()
pygame.display.quit()
