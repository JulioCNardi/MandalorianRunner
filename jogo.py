import pygame 
import sys 
from random import randint
import os
from pygame.locals import*


diretorio_principal = os.path.dirname(__file__)
diretorio_sprites = os.path.join(diretorio_principal, 'img')

resolucao = WIDTH, HEIGHT = 800, 400

pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)
tela = pygame.display.set_mode(resolucao)
pygame.display.set_caption('MANDALORIAN RUNNER')
relogio = pygame.time.Clock()
jogo_ativo = False
tempo_inicial = 0
pontuacaoMostra = 0


# coloca o ceu
ceu_surface = pygame.image.load('img/ceu.png').convert_alpha()
# coloca o chao
chao_surface = pygame.image.load('img/chao.png').convert_alpha()


#coloca hud
def mostra_pontuacao():
    pontuacao = int(pygame.time.get_ticks() / 1000) - tempo_inicial # Conta ms desde que pygame iniciou
    pontuacao_surface = pygame.font.Font('font/Pixeled.ttf', 20)
    pontuacao_text_surface = pontuacao_surface.render(f'{pontuacao} m', False, 'Black')
    pontuacao_rect = pontuacao_text_surface.get_rect(center = (400, 20))
    tela.blit(pontuacao_text_surface,pontuacao_rect)
    return pontuacao


# coloca textos de game over
gameOver_surface = pygame.font.Font('font/Pixeled.ttf', 20)
gameOver_text_surface = gameOver_surface.render('GROGU FOI CAPTURADO', False, 'white')
gameOver_rect = gameOver_text_surface.get_rect(center = (400, 20))

reiniciar_surface = pygame.font.Font('font/Pixeled.ttf', 20)
reiniciar_text_surface = reiniciar_surface.render('APERTE ESPAÇO PARA JOGAR', False, 'white')
reiniciar_rect = reiniciar_text_surface.get_rect(center = (400, 360))

# menu inicial
bg_surface = pygame.image.load('img/menubg.jpg').convert_alpha()
titulo_surface = pygame.font.Font('font/DistantGalaxy.ttf', 60)
titulo_text_surface = titulo_surface.render('MANDALORIAN RUNNER', False, 'white')
titulo_rect = titulo_text_surface.get_rect(center = (400, 200))


#Coloca Grogu
sprite_sheet = pygame.image.load(os.path.join(diretorio_sprites, 'GROGUs.png'))

class Grogu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.imagens_grogu = []
        for i in range(4):
            img = sprite_sheet.subsurface((i*32,0), (32,32)) #Conficurqação do spritesheet
            img = pygame.transform.scale(img, (32*7, 32*7))
            self.imagens_grogu.append(img)
            
        #Tamanho do sprite
        self.index_lista = 0
        self.image = self.imagens_grogu[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (400, 200)
        
        #Velocidade do sprite
    def update(self):
        if self.index_lista > 3:
            self.index_lista = 0
        self.index_lista += 0.1
        self.image = self.imagens_grogu[int(self.index_lista)]
    
        
spritesGrogu = pygame.sprite.Group()
grogu = Grogu()
spritesGrogu.add(grogu)

# Inimigos #
    #Coloca bantha
bantha_surface = pygame.image.load('img/Inimigo/bantha.png').convert_alpha()
    #coloca laser
laser_surface = pygame.image.load('img/Inimigo/laser.png').convert_alpha()


obstasculos_rect_lista = []

#Obstaculos (user event)

obstasculos_timer = pygame.USEREVENT + 1 # Temporizador
pygame.time.set_timer(obstasculos_timer, 1400)

def obstaculo_movement(obstaculo_lista):
    if obstaculo_lista:
        for obstaculo_rect in obstaculo_lista:
            obstaculo_rect.x -= 4

            if obstaculo_rect.bottom == 300:
                tela.blit(bantha_surface,obstaculo_rect)
            else: 
                tela.blit(laser_surface,obstaculo_rect)

        obstaculo_lista = [obstaculo for obstaculo in obstaculo_lista if obstaculo.x > -100]

        return obstaculo_lista
    else: return []

def colisao(player, obstaculos):
    if obstaculos:
        for obstacle_rect in obstaculos:
            if player.colliderect(obstacle_rect): return False
    return True
        
# Player
    #Coloca Mandolariano
player_surface = pygame.image.load('img/Player/Mando.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))
player_gravidade = 0

#Sons
musicPrincipal = pygame.mixer.Sound('sound/music.mp3')
menuMusic = pygame.mixer.Sound('sound/menu.mp3')
gameOverMusic = pygame.mixer.Sound('sound/gameover.mp3')



while True:
    menuMusic.set_volume(0.1) 
    gameOverMusic.set_volume(0.1) 
    # loop que checa para fechar o jogo e função dos botões
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        if jogo_ativo == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravidade = -17
        elif jogo_ativo == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jogo_ativo = 1
                
                tempo_inicial = int(pygame.time.get_ticks() / 1000 )

        if event.type == obstasculos_timer and jogo_ativo == True:
            if randint (0, 2):
                obstasculos_rect_lista.append(bantha_surface.get_rect(midbottom = (randint(900, 1100), 300)))
            else: 
                obstasculos_rect_lista.append(laser_surface.get_rect(midbottom = (randint(900, 1100), 210)))

    

    if jogo_ativo == True:
        # Toca musica
        gameOverMusic.stop()
        menuMusic.stop()
        musicPrincipal.play()
        musicPrincipal.set_volume(0.2) 

        tela.blit(ceu_surface,(0,0)) #ajusta posicao do sprite
        tela.blit(chao_surface,(0,300))
        pontuacaoMostra =  mostra_pontuacao()

        
        #Player
        player_gravidade += 0.8 # Faz a gravidade do player
        player_rect.y += player_gravidade
        if player_rect.bottom >= 300: player_rect.bottom = 300
        tela.blit(player_surface, player_rect)

        # Movimento Obstaculo
        obstasculos_rect_lista  = obstaculo_movement(obstasculos_rect_lista)


        # colisao
        jogo_ativo = colisao(player_rect, obstasculos_rect_lista)
        

    elif jogo_ativo == False: # Game over

        if pontuacaoMostra == 0:
            menuMusic.play()
            

            tela.blit(bg_surface,(0,0))
            tela.blit(titulo_text_surface, titulo_rect)
            tela.blit(reiniciar_text_surface,reiniciar_rect)

        else:
            musicPrincipal.stop()
            gameOverMusic.play()
            

            tela.blit(bg_surface,(0,0))
            tela.blit(gameOver_text_surface,gameOver_rect)
            tela.blit(reiniciar_text_surface,reiniciar_rect)
            player_rect.midbottom = (80, 300)
            obstasculos_rect_lista.clear()
            player_gravidade = 0

            pontuacaoMessage_surface = pygame.font.Font('font/Pixeled.ttf', 20)
            pontuacaoMessage_text_surface = pontuacaoMessage_surface.render(f'VOCE ANDOU: {pontuacaoMostra} m', False, 'white')
            pontuacaoMessage_rect = pontuacaoMessage_text_surface.get_rect(center = (400, 60))
            tela.blit(pontuacaoMessage_text_surface, pontuacaoMessage_rect)

            spritesGrogu.draw(tela)
            spritesGrogu.update()
            

    pygame.display.update()
    relogio.tick(60) 