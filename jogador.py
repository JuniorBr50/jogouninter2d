import pygame

class Jogador:
    def __init__(self, x, largura_tela, altura_tela, imagem):
        self.x = x
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.img = imagem
        self.velocidade = 5

    def mover(self, teclas):
        if teclas[pygame.K_a]:
            self.x -= self.velocidade
        if teclas[pygame.K_d]:
            self.x += self.velocidade

        # limites da pista
        limite_esq = self.largura_tela // 2 - 170
        limite_dir = self.largura_tela // 2 + 170

        self.x = max(limite_esq, min(limite_dir, self.x))

    def desenhar(self, tela):
        tela.blit(
            self.img,
            (self.x - self.img.get_width()//2,
             self.altura_tela - self.img.get_height())
        )