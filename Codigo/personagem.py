"""Personagem jogável: carrega os sprites uma única vez, anima e espelha (flip)."""
import pygame

from auxiliares import carregar_imagem
from configuracoes import PASTA_PERSONAGENS, ESCALA_SPRITE

# Onde estão os sprites de cada personagem (relativo a Personagens/<pasta>).
# "{}" é o número do frame. Se "andando_e" for None, o sprite da direita é
# espelhado (flip) quando o personagem anda para a esquerda.
PERSONAGENS = {
    "rita": {
        "nome": "Rita",
        "pasta": "Rita/Oficial/png",
        "idle": "idle/RitaIdle{}.png",
        "gira": "RitaGira{}.png",
        "andando_d": "Andando/Andando{}.png",
        "andando_e": None,
    },
    "toddy": {
        "nome": "Toddy",
        "pasta": "Toddy/png",
        "idle": "idle/idleAnimation{}.png",
        "gira": "ToddyGira{}.png",
        "andando_d": "Andando/Direita/ToddyAndandoDireita{}.png",
        "andando_e": "Andando/Esquerda/ToddyAndandoEsquerda{}.png",
    },
    "tomate": {
        "nome": "Tomate",
        "pasta": "Tomate/png",
        "idle": "idle/tomateIdle{}.png",
        "gira": "tomateGirando{}.png",
        "andando_d": "Andando/TomateAndando{}.png",
        "andando_e": None,
    },
}
ORDEM = ["rita", "toddy", "tomate"]

TEMPO_FRAME_ANDANDO = 0.10  # segundos por frame
TEMPO_FRAME_IDLE = 0.50
TEMPO_FRAME_GIRA = 0.20

TAMANHO_SPRITE = 128  # todos os sprites são normalizados para 128x128


def _carregar_frames(pasta, padrao, quantidade):
    frames = []
    for i in range(1, quantidade + 1):
        imagem = carregar_imagem(pasta / padrao.format(i))
        # Os sprites de giro do Toddy foram salvos em 32x32 (o resto está em 128x128).
        # Ampliamos por um fator inteiro para ficar no mesmo tamanho dos outros.
        fator = max(1, TAMANHO_SPRITE // imagem.get_width()) * ESCALA_SPRITE
        if fator != 1:
            tamanho = (imagem.get_width() * fator, imagem.get_height() * fator)
            imagem = pygame.transform.scale(imagem, tamanho)
        frames.append(imagem)
    return frames


class Personagem(pygame.sprite.Sprite):
    def __init__(self, chave, direcao="d"):
        super().__init__()
        dados = PERSONAGENS[chave]
        pasta = PASTA_PERSONAGENS / dados["pasta"]

        self.chave = chave
        self.nome = dados["nome"]

        idle = _carregar_frames(pasta, dados["idle"], 2)
        andando_d = _carregar_frames(pasta, dados["andando_d"], 8)
        if dados["andando_e"]:
            andando_e = _carregar_frames(pasta, dados["andando_e"], 8)
        else:
            # Aqui está o flip: espelha na horizontal (True), não na vertical (False)
            andando_e = [pygame.transform.flip(f, True, False) for f in andando_d]
        gira = _carregar_frames(pasta, dados["gira"], 4)
        self.frames = {"idle": idle, "d": andando_d, "e": andando_e, "gira": gira}

        self.direcao = direcao  # "d" ou "e": para onde está virado
        self.x = 0.0            # posição no mundo (centro do personagem)
        self._estado = "idle"   # "idle", "d", "e" ou "gira"
        self._indice = 0
        self._tempo = 0.0
        self.image = idle[0]
        self.rect = self.image.get_rect()

    def definir_movimento(self, direcao):
        """direcao: "d", "e" ou None (parado)."""
        if direcao is not None:
            self.direcao = direcao
        novo_estado = direcao if direcao is not None else "idle"
        if novo_estado != self._estado:
            self._estado = novo_estado
            self._indice = 0
            self._tempo = 0.0

    def girar(self):
        """Fica girando no lugar (usado na tela de seleção)."""
        if self._estado != "gira":
            self._estado = "gira"
            self._indice = 0
            self._tempo = 0.0

    def update(self, dt):
        """Avança a animação. dt em segundos."""
        frames = self.frames[self._estado]
        if self._estado == "idle":
            duracao = TEMPO_FRAME_IDLE
        elif self._estado == "gira":
            duracao = TEMPO_FRAME_GIRA
        else:
            duracao = TEMPO_FRAME_ANDANDO
        self._tempo += dt
        while self._tempo >= duracao:
            self._tempo -= duracao
            self._indice = (self._indice + 1) % len(frames)
        self.image = frames[self._indice]

    def desenhar(self, tela, camera_x, chao_y):
        """Desenha com os pés em chao_y; a posição na tela é a do mundo menos a câmera."""
        self.rect = self.image.get_rect(midbottom=(round(self.x - camera_x), chao_y))
        tela.blit(self.image, self.rect)
