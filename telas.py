import pygame

class Telas:
    def __init__(self, tela, largura, altura, fonte, fonte_pequena, fonte_titulo,
                 fundo_menu, fundo_vitoria, fundo_derrota, relogio):

        self.tela = tela
        self.LARGURA = largura
        self.ALTURA = altura

        self.fonte = fonte
        self.fonte_pequena = fonte_pequena
        self.fonte_titulo = fonte_titulo

        self.fundo_menu = fundo_menu
        self.fundo_vitoria = fundo_vitoria
        self.fundo_derrota = fundo_derrota

        self.relogio = relogio

        self.BRANCO = (255,255,255)

    def menu(self):
        tempo_piscar = 0
        mostrar = True

        while True:
            self.relogio.tick(60)

            tempo_piscar += self.relogio.get_time()
            if tempo_piscar > 500:
                mostrar = not mostrar
                tempo_piscar = 0

            if self.fundo_menu:
                self.tela.blit(self.fundo_menu, (0,0))
            else:
                self.tela.fill((20,20,20))

            cor = (255,0,0) if mostrar else (0,120,255)

            titulo = self.fonte_titulo.render("Beetle Sunset", True, cor)
            self.tela.blit(titulo, (self.LARGURA//2 - titulo.get_width()//2, 80))

            texto = self.fonte.render("INICIAR", True, cor)
            texto = pygame.transform.scale(
                texto,
                (int(texto.get_width()*1.2), int(texto.get_height()*1.2))
            )

            self.tela.blit(texto, (self.LARGURA//2 - texto.get_width()//2, 250))

            controles = self.fonte_pequena.render(
                "A/D - mover | ENTER - selecionar | ESC - sair",
                True,
                self.BRANCO
            )

            self.tela.blit(controles, (self.LARGURA//2 - controles.get_width()//2, self.ALTURA - 40))

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if pygame.key.get_pressed()[pygame.K_RETURN]:
                return "iniciar"


    def game_over(self):
        tempo_piscar = 0
        mostrar = True

        while True:
            self.relogio.tick(60)

            tempo_piscar += self.relogio.get_time()
            if tempo_piscar > 500:
                mostrar = not mostrar
                tempo_piscar = 0

            if self.fundo_derrota:
                self.tela.blit(self.fundo_derrota, (0,0))
            else:
                self.tela.fill((20, 0, 0))

            if mostrar:
                texto = self.fonte.render("TENTE NOVAMENTE", True, (255,0,0))
                self.tela.blit(texto, (self.LARGURA//2 - texto.get_width()//2, self.ALTURA//2 - 50))

            instrucao = self.fonte_pequena.render("PRESSIONE ENTER", True, self.BRANCO)
            self.tela.blit(instrucao, (self.LARGURA//2 - instrucao.get_width()//2, self.ALTURA//2 + 50))

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if pygame.key.get_pressed()[pygame.K_RETURN]:
                return "menu"

    def vitoria(self):
        inicio = pygame.time.get_ticks()
        musica_voltou = False

        tempo_piscar = 0
        mostrar = True

        while True:
            self.relogio.tick(60)

            tempo_piscar += self.relogio.get_time()
            if tempo_piscar > 500:
                mostrar = not mostrar
                tempo_piscar = 0

            if self.fundo_vitoria:
                self.tela.blit(self.fundo_vitoria, (0, 0))
            else:
                self.tela.fill((0, 120, 0))

            if mostrar:
                texto = self.fonte.render("VOCE VENCEU!", True, (255,200,0))
                self.tela.blit(texto, (self.LARGURA//2 - texto.get_width()//2, self.ALTURA//2 - 40))

            instrucao = self.fonte_pequena.render("PRESSIONE ENTER", True, self.BRANCO)
            self.tela.blit(instrucao, (self.LARGURA//2 - instrucao.get_width()//2, self.ALTURA//2 + 50))

            if not musica_voltou and pygame.time.get_ticks() - inicio > 3000:
                pygame.mixer.music.play(-1)
                musica_voltou = True

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if pygame.key.get_pressed()[pygame.K_RETURN]:
                return "menu"