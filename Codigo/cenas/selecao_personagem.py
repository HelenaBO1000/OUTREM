"""Tela de escolha do personagem.

O personagem selecionado cresce e gira; os outros ficam parados (idle).
"""
import pygame
from pygame.locals import K_a, K_d, K_LEFT, K_RIGHT, K_RETURN, K_KP_ENTER, K_SPACE

from auxiliares import carregar_fundo_do_jogo, desenhar_fundo_repetido
from configuracoes import LARGURA, ALTURA
from personagem import Personagem, ORDEM

COR_TEXTO = (240, 240, 240)
COR_DESTAQUE = (255, 220, 80)

ESCALA_NORMAL = 0.6
ESCALA_SELECIONADO = 1.0   # quanto o personagem selecionado cresce
VELOCIDADE_CRESCER = 10    # quanto maior, mais rápido ele cresce/encolhe
CENTRO_Y = ALTURA // 2     # os três ficam com o MEIO do sprite nesta altura (meio da tela)
TITULO_Y = 34
TAMANHO_SPRITE = 128       # altura original do sprite


class SelecaoPersonagem:
    def __init__(self):
        self.personagens = [Personagem(chave) for chave in ORDEM]
        self.fundo = carregar_fundo_do_jogo()
        self.indice = 0
        self._atualizar_giro()
        # escala atual de cada um (anima suavemente até a escala alvo)
        self.escalas = [ESCALA_SELECIONADO if i == 0 else ESCALA_NORMAL
                        for i in range(len(self.personagens))]
        self.fonte_titulo = pygame.font.Font(None, 44)
        self.fonte = pygame.font.Font(None, 28)
        self.proxima = None

    def _atualizar_giro(self):
        """Só o personagem selecionado gira; os outros ficam parados (idle)."""
        for i, personagem in enumerate(self.personagens):
            if i == self.indice:
                personagem.girar()
            else:
                personagem.definir_movimento(None)

    def tratar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key in (K_LEFT, K_a):
            self.indice = (self.indice - 1) % len(self.personagens)
            self._atualizar_giro()
        elif evento.key in (K_RIGHT, K_d):
            self.indice = (self.indice + 1) % len(self.personagens)
            self._atualizar_giro()
        elif evento.key in (K_RETURN, K_KP_ENTER, K_SPACE):
            escolhido = self.personagens[self.indice].chave
            self.proxima = ("corredor", {"personagem": escolhido})

    def atualizar(self, dt):
        for i, personagem in enumerate(self.personagens):
            personagem.update(dt)
            alvo = ESCALA_SELECIONADO if i == self.indice else ESCALA_NORMAL
            self.escalas[i] += (alvo - self.escalas[i]) * min(1.0, VELOCIDADE_CRESCER * dt)

    def _texto(self, tela, fonte, texto, cor, centro):
        imagem = fonte.render(texto, True, cor)
        tela.blit(imagem, imagem.get_rect(center=centro))

    def desenhar(self, tela):
        desenhar_fundo_repetido(tela, self.fundo)
        self._texto(tela, self.fonte_titulo, "Selecione o personagem", COR_TEXTO,
                    (LARGURA // 2, TITULO_Y))

        coluna = LARGURA // len(self.personagens)
        for i, personagem in enumerate(self.personagens):
            centro_x = coluna * i + coluna // 2
            escolhido = i == self.indice

            imagem = personagem.image
            escala = self.escalas[i]
            tamanho = (round(imagem.get_width() * escala), round(imagem.get_height() * escala))
            imagem = pygame.transform.scale(imagem, tamanho)  # scale (não smoothscale) mantém os pixels nítidos
            tela.blit(imagem, imagem.get_rect(center=(centro_x, CENTRO_Y)))

            # o nome fica logo abaixo do tamanho máximo, na mesma altura para todos
            nome_y = CENTRO_Y + int(TAMANHO_SPRITE * ESCALA_SELECIONADO) // 2 + 22
            cor = COR_DESTAQUE if escolhido else COR_TEXTO
            self._texto(tela, self.fonte, personagem.nome, cor, (centro_x, nome_y))
