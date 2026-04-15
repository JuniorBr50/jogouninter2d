import pygame
from inimigos import Inimigos

pygame.init()
pygame.mixer.init()

som_batida = pygame.mixer.Sound("som&foto/crash.mp3")

pygame.mixer.music.load("som&foto/Long Away Home.wav")
pygame.mixer.music.play(-1)

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Car Runner")

faixas = [
    LARGURA//2 - 140,
    LARGURA//2,
    LARGURA//2 + 140
]

inimigos = Inimigos(faixas)

carro_img = pygame.image.load("som&foto/car.PNG").convert_alpha()
carro_img = pygame.transform.scale(carro_img, (60, 120))

try:
    fundo_img = pygame.image.load("som&foto/bg.png").convert()
    fundo_img = pygame.transform.scale(fundo_img, (800, 600))
except:
    fundo_img = None

relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 30)

BRANCO = (255,255,255)
PRETO = (0,0,0)
CEU = (135,206,235)

estado_jogo = {
    "jogador_x": LARGURA//2,
    "velocidade": 5,
    "distancia": 0
}

def reiniciar_jogo():
    estado_jogo["jogador_x"] = LARGURA//2
    estado_jogo["velocidade"] = 5
    estado_jogo["distancia"] = 0
    inimigos.lista = []

def desenhar_jogador():
    tela.blit(carro_img, (estado_jogo["jogador_x"] - 30, ALTURA - 120))

def desenhar_hud():
    texto = fonte.render(f"Distância: {int(estado_jogo['distancia'])}", True, PRETO)
    tela.blit(texto, (10,10))

def loop_jogo():
    tempo_spawn = 0

    while True:
        relogio.tick(60)

        deslocamento = int((estado_jogo["distancia"] * 2) % ALTURA)

        if fundo_img:
            tela.blit(fundo_img, (0, deslocamento - ALTURA))
            tela.blit(fundo_img, (0, deslocamento))
        else:
            tela.fill(CEU)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_ESCAPE]:
            return

        if teclas[pygame.K_a]:
            estado_jogo["jogador_x"] -= 5
        if teclas[pygame.K_d]:
            estado_jogo["jogador_x"] += 5

        limite_esquerda = LARGURA // 2 - 170
        limite_direita = LARGURA // 2 + 170

        estado_jogo["jogador_x"] = max(limite_esquerda, min(limite_direita, estado_jogo["jogador_x"]))

        tempo_spawn += 1
        if tempo_spawn > 40:
            inimigos.gerar()
            tempo_spawn = 0

        inimigos.atualizar(estado_jogo["velocidade"])
        inimigos.desenhar(tela)

        desenhar_jogador()

        estado_jogo["distancia"] += estado_jogo["velocidade"] * 0.1
        estado_jogo["velocidade"] += 0.006

        desenhar_hud()

        if inimigos.colisao(estado_jogo["jogador_x"], ALTURA - 90):
            som_batida.play()
            pygame.time.delay(300)
            return "fim"

        pygame.display.flip()

def tela_game_over():
    while True:
        tela.fill(PRETO)
        texto = fonte.render("GAME OVER - ENTER", True, BRANCO)
        tela.blit(texto, (LARGURA//2 - 170, ALTURA//2))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_RETURN]:
            return

def menu():
    opcoes = ["Iniciar", "Continuar"]
    selecionado = 0

    while True:
        tela.fill((20,20,20))

        for i, opcao in enumerate(opcoes):
            cor = BRANCO if i == selecionado else (100,100,100)
            texto = fonte.render(opcao, True, cor)
            tela.blit(texto, (LARGURA//2 - 80, 200 + i*50))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_UP]:
            selecionado = (selecionado - 1) % len(opcoes)
            pygame.time.delay(150)

        if teclas[pygame.K_DOWN]:
            selecionado = (selecionado + 1) % len(opcoes)
            pygame.time.delay(150)

        if teclas[pygame.K_RETURN]:
            if opcoes[selecionado] == "Iniciar":
                reiniciar_jogo()
                resultado = loop_jogo()
                if resultado == "fim":
                    tela_game_over()

            elif opcoes[selecionado] == "Continuar":
                resultado = loop_jogo()
                if resultado == "fim":
                    tela_game_over()

menu()