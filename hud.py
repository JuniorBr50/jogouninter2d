import pygame

class HUD:
    def __init__(self, fonte, fonte_pequena):
        self.fonte = fonte
        self.fonte_pequena = fonte_pequena
        self.cor = (0, 0, 0)

    def desenhar(self, tela, distancia):
        distancia_int = int(distancia)

        texto = self.fonte.render(f"{distancia_int} / 1000 m", True, self.cor)
        tela.blit(texto, (10, 10))

        objetivo = self.fonte_pequena.render("Objetivo: alcance 1000 metros", True, self.cor)
        tela.blit(objetivo, (10, 50))