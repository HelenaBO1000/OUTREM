"""Ponto de entrada do jogo. Para jogar: python main.py"""
import pygame

import auxiliares
from configuracoes import FPS
from cenas.selecao_personagem import SelecaoPersonagem
from cenas.corredor import Corredor

# Para criar uma cena nova: crie a classe em cenas/ e registre aqui.
CENAS = {
    "selecao": SelecaoPersonagem,
    "corredor": Corredor,
}


def main():
    tela = auxiliares.iniciar()
    relogio = pygame.time.Clock()
    cena = SelecaoPersonagem()

    while True:
        dt = relogio.tick(FPS) / 1000  # segundos desde o último frame

        for evento in auxiliares.tratar_eventos():
            cena.tratar_evento(evento)
        cena.atualizar(dt)
        cena.desenhar(tela)
        pygame.display.flip()

        if cena.proxima is not None:
            nome, argumentos = cena.proxima
            cena = CENAS[nome](**argumentos)


if __name__ == "__main__":
    main()
