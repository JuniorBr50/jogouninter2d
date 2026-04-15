import pygame
import random

class Inimigos:
    def __init__(self, faixas):
        self.faixas = faixas
        self.lista = []

        self.imagem = pygame.image.load("som&foto/inimigo.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (60, 120))

    def gerar(self):
        x = random.choice(self.faixas)
        self.lista.append([x, -100])

    def atualizar(self, velocidade):
        for inimigo in self.lista:
            inimigo[1] += velocidade

        self.lista = [i for i in self.lista if i[1] < 700]

    def desenhar(self, tela):
        for inimigo in self.lista:
            tela.blit(self.imagem, (inimigo[0]-30, inimigo[1]))

    def colisao(self, jogador_x, jogador_y):
        jogador_rect = pygame.Rect(jogador_x - 18, jogador_y, 36, 60)

        for inimigo in self.lista:
            inimigo_rect = pygame.Rect(inimigo[0] - 18, inimigo[1] + 40, 36, 60)

            if jogador_rect.colliderect(inimigo_rect):
                return True

        return False