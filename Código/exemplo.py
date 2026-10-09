import pygame
from pygame.locals import *
from sys import exit
import auxiliaresCorredor

# Inicializa a tela (ajuste para o tamanho desejado)
auxiliaresCorredor.tela = pygame.display.set_mode((1152, 256))
pygame.display.set_caption('OUTREM')

# Cria um grupo de sprites e adiciona o personagem
todas_as_sprites = pygame.sprite.Group()
todas_as_sprites.add(auxiliaresCorredor.personagem)

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Atualiza a posição do personagem em relação ao fundo
    auxiliaresCorredor.atualizar_posicao_personagem()

    # Atualiza a direção e posição do fundo
    auxiliaresCorredor.anda()

    # Atualiza a tela
    auxiliaresCorredor.tela.fill((0, 0, 0))
    pygame.draw.rect(auxiliaresCorredor.tela, (0, 0, 255), (auxiliaresCorredor.xFundo, 0, auxiliaresCorredor.largura, auxiliaresCorredor.altura))

    # Atualiza e desenha os sprites
    todas_as_sprites.update()
    todas_as_sprites.draw(auxiliaresCorredor.tela)

    # Atualiza a janela
    auxiliaresCorredor.janela()