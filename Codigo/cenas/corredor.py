"""Cena do corredor do trem (a janela principal).

A função andar mora aqui porque só faz sentido neste corredor: ela mexe na
posição do personagem e na câmera deste vagão.

Camadas, de trás para frente:
  1. fundo do jogo (preto; depois entram os desenhos)
  2. vagão (imagem grande que desliza com a câmera)
  3. personagem
"""
import pygame
from pygame.locals import K_a, K_d, K_LEFT, K_RIGHT

from auxiliares import carregar_imagem
from configuracoes import LARGURA, ALTURA, PASTA_AMBIENTES
from personagem import Personagem

VELOCIDADE = 200      # pixels por segundo
LIMITE_BORDA = 90     # o personagem não passa dessa distância das pontas do vagão
CHAO_NO_VAGAO = 220   # y do chão dentro da imagem do vagão (pés do personagem)
COR_FUNDO_JOGO = (0, 0, 0)


def _limitar(valor, minimo, maximo):
    return max(minimo, min(valor, maximo))


class Corredor:
    def __init__(self, personagem="rita"):
        self.fundo_vagao = carregar_imagem(PASTA_AMBIENTES / "corredor/png/corredorCompleto.png")
        self.largura_vagao = self.fundo_vagao.get_width()
        # o vagão (256 de altura) fica centralizado na tela; sobra faixa preta em cima e embaixo
        self.vagao_y = (ALTURA - self.fundo_vagao.get_height()) // 2

        self.personagem = Personagem(personagem)
        self.personagem.x = self.largura_vagao / 2
        self.camera_x = 0
        self._atualizar_camera()

        self.proxima = None  # mudar de cena: ("nome_da_cena", {argumentos})

    # --- eventos / lógica --------------------------------------------------

    def tratar_evento(self, evento):
        pass  # (portas, interações etc. entram aqui depois)

    def andar(self, dt):
        """Lê o teclado, move o personagem pelo vagão e vira o sprite."""
        teclas = pygame.key.get_pressed()
        esquerda = teclas[K_a] or teclas[K_LEFT]
        direita = teclas[K_d] or teclas[K_RIGHT]

        direcao = None
        if direita and not esquerda:
            direcao = "d"
        elif esquerda and not direita:
            direcao = "e"

        if direcao is not None:
            passo = VELOCIDADE * dt * (1 if direcao == "d" else -1)
            self.personagem.x = _limitar(
                self.personagem.x + passo, LIMITE_BORDA, self.largura_vagao - LIMITE_BORDA
            )
        self.personagem.definir_movimento(direcao)

    def _atualizar_camera(self):
        """Câmera segue o personagem, parando nas pontas do vagão.

        No meio do vagão o personagem fica parado no centro da tela e o fundo
        é que desliza. Perto das pontas a câmera trava e é o personagem que anda.
        """
        alvo = self.personagem.x - LARGURA / 2
        self.camera_x = round(_limitar(alvo, 0, self.largura_vagao - LARGURA))

    def atualizar(self, dt):
        self.andar(dt)
        self._atualizar_camera()
        self.personagem.update(dt)

    # --- desenho -----------------------------------------------------------

    def desenhar(self, tela):
        tela.fill(COR_FUNDO_JOGO)                                # 1. fundo do jogo
        tela.blit(self.fundo_vagao, (-self.camera_x, self.vagao_y))  # 2. vagão
        self.personagem.desenhar(                                # 3. personagem
            tela, self.camera_x, self.vagao_y + CHAO_NO_VAGAO
        )
