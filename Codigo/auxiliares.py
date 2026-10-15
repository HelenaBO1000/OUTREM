"""O que é usado no jogo todo: criar a janela, sair, tamanho da tela e carregar imagens.

Nada aqui é específico de uma cena (andar, câmera, etc. ficam em cenas/).
"""
import sys

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_F11

from configuracoes import TITULO, LARGURA, ALTURA


def iniciar():
    """Inicia o pygame e devolve a tela lógica (LARGURA x ALTURA).

    SCALED faz o pygame ampliar a tela lógica para a janela real
    mantendo a proporção e os pixels nítidos.
    """
    pygame.init()
    pygame.display.set_caption(TITULO)
    return pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED | pygame.FULLSCREEN)


def sair():
    pygame.quit()
    sys.exit()


def tamanho_tela():
    return pygame.display.get_surface().get_size()


def meio_tela():
    largura, altura = tamanho_tela()
    return largura // 2, altura // 2


def tratar_eventos():
    """Cuida dos eventos que valem em qualquer tela (fechar, ESC, F11 = tela cheia).

    Devolve a lista dos outros eventos, para a cena atual tratar.
    """
    restantes = []
    for evento in pygame.event.get():
        if evento.type == QUIT:
            sair()
        elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
            sair()
        elif evento.type == KEYDOWN and evento.key == K_F11:
            pygame.display.toggle_fullscreen()
        else:
            restantes.append(evento)
    return restantes


def carregar_imagem(caminho):
    return pygame.image.load(str(caminho)).convert_alpha()
