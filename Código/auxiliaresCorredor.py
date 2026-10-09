import pygame
from pygame.locals import *
from sys import exit
from corredorClasses import Personagens

pygame.init()

largura = 1152  # largura vagão do trem
altura = 256    # altura vagão do trem
telaCheia = False
pygame.display.set_caption('OUTREM')
tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Variável para controlar a posição do fundo
xFundo = int((largura - altura) / 2)

# Instância única do personagem (supondo que login.personagem seja 1, 2 ou 3)
# Substitua `login.personagem` pelo valor correto ou passe-o como parâmetro
personagem = Personagens(1, "d")  # Exemplo: personagem 1 olhando para a direita

def janela():
    global telaCheia, tela
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F11):
            pygame.quit()
            exit()
    pygame.display.flip()
    clock.tick(60)

def devolverMeioJanela():
    larguraAtual, alturaAtual = pygame.display.get_surface().get_size()
    meio_x = int(larguraAtual // 2)
    meio_y = int(alturaAtual // 2)
    return meio_x, meio_y

def anda():
    global xFundo
    if pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT]:
        xFundo += 20
        personagem.atualizar_direcao("e")

    elif pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT]:
        xFundo -= 20
        personagem.atualizar_direcao("d")
    return xFundo

def atualizar_posicao_personagem():
    """Atualiza a posição do personagem em relação ao fundo."""
    personagem.rect.centerx = devolverMeioJanela() - xFundo
    personagem.rect.centery = devolverMeioJanela()
