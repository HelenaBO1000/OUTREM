import pygame
from pygame.locals import *
from sys import exit
import auxiliares

class Personagens(pygame.sprite.Sprite):
    def __init__(self, personagem, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.spritesAnda = []
        self.personagem = personagem
        self.direcao = direcao  # "d" para direita, "e" para esquerda
        self.atual = 0
        self.ultima_atualizacao = pygame.time.get_ticks()

        if personagem == 1:
            path = 'Sprites/Personagens/Rita/png/'
        elif personagem == 2:
            path = 'Sprites/Personagens/Toddy/png/'
        elif personagem == 3:
            path = 'Sprites/Personagens/Tomate/png/'
        else:
            raise ValueError("Personagem deve ser 1, 2 ou 3.")

        # Carregar sprites de caminhada
        if personagem == 2:
            # Para o personagem 2, carregar sprites específicos para direita e esquerda
            if self.direcao == "d":
                for i in range(1, 9):
                    self.spritesAnda.append(f"{path}/Andando/Direita/Andando{i}.png")
            elif self.direcao == "e":
                for i in range(1, 9):
                    self.spritesAnda.append(f"{path}/Andando/Esquerda/Andando{i}.png")
        else:
            # Para os outros personagens, carregar sprites assimétricos (não importa a direção)
            for i in range(1, 9):
                self.spritesAnda.append(f"{path}/Andando/Andando{i}.png")

        self.image = pygame.image.load(self.spritesAnda[self.atual]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (128*3, 128*3))
        self.rect = self.image.get_rect()
        self.rect.center = auxiliares.devolverMeioJanela()  # Posiciona inicialmente no centro
        self.velocidade = 5

    def atualizar_direcao(self, nova_direcao):
        """Atualiza a direção do personagem e recarrega os sprites."""
        if self.direcao != nova_direcao:
            self.direcao = nova_direcao
            self.spritesAnda = []  # Limpa os sprites antigos

            if self.personagem == 1:
                path = 'Sprites/Personagens/Rita/png/'
            elif self.personagem == 2:
                path = 'Sprites/Personagens/Toddy/png/'
            elif self.personagem == 3:
                path = 'Sprites/Personagens/Tomate/png/'
            else:
                raise ValueError("Personagem deve ser 1, 2 ou 3.")

            # Recarregar sprites com a nova direção
            if self.personagem == 2:
                if self.direcao == "d":
                    for i in range(1, 9):
                        self.spritesAnda.append(f"{path}/Andando/Direita/Andando{i}.png")
                elif self.direcao == "e":
                    for i in range(1, 9):
                        self.spritesAnda.append(f"{path}/Andando/Esquerda/Andando{i}.png")
            else:
                for i in range(1, 9):
                    self.spritesAnda.append(f"{path}/Andando/Andando{i}.png")

            # Atualizar a imagem atual
            self.atual = 0
            self.image = pygame.image.load(self.spritesAnda[self.atual]).convert_alpha()
            self.image = pygame.transform.scale(self.image, (128*3, 128*3))

    def update(self):
        """Avança a animação do personagem."""
        agora = pygame.time.get_ticks()
        if agora - self.ultima_atualizacao > 100:  # Ajuste o tempo conforme necessário
            self.atual = (self.atual + 1) % len(self.spritesAnda)
            self.image = pygame.image.load(self.spritesAnda[self.atual]).convert_alpha()
            self.image = pygame.transform.scale(self.image, (128*3, 128*3))
            self.ultima_atualizacao = agora
