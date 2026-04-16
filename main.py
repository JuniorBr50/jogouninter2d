import pygame
from inimigos import Inimigos

pygame.init()
pygame.mixer.init()

# Sons
som_vitoria = pygame.mixer.Sound("som&foto/Victory.wav")
som_batida = pygame.mixer.Sound("som&foto/crash.mp3")

pygame.mixer.music.load("som&foto/Long Away Home.wav")
pygame.mixer.music.play(-1)

# Tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Beetle Sunset DEMO")

# Faixas
faixas = [
    LARGURA//2 - 140,
    LARGURA//2,
    LARGURA//2 + 140
]

inimigos = Inimigos(faixas)

# Imagens
carro_img = pygame.image.load("som&foto/fuscaRosa.PNG").convert_alpha()
carro_img = pygame.transform.scale(carro_img, (60, 120))

def carregar_imagem(caminho):
    try:
        img = pygame.image.load(caminho).convert()
        return pygame.transform.scale(img, (LARGURA, ALTURA))
    except:
        return None

fundo_img = carregar_imagem("som&foto/bg.png")
fundo_menu = carregar_imagem("som&foto/menu_iniciar.png")
fundo_vitoria = carregar_imagem("som&foto/vitoria_fusca.png")
fundo_derrota = carregar_imagem("som&foto/gameover_fundo.png")

# Fontes
fonte = pygame.font.Font("som&foto/Pixel Game.otf", 40)
fonte_pequena = pygame.font.Font("som&foto/Pixel Game.otf", 25)
fonte_titulo = pygame.font.Font("som&foto/Pixel Game.otf", 80)

# Cores
BRANCO = (255,255,255)
PRETO = (0,0,0)
CEU = (135,206,235)

relogio = pygame.time.Clock()

estado_jogo = {
    "jogador_x": LARGURA//2,
    "velocidade": 5,
    "distancia": 0
}

# -------------------------

def reiniciar_jogo():
    estado_jogo["jogador_x"] = LARGURA//2
    estado_jogo["velocidade"] = 5
    estado_jogo["distancia"] = 0
    inimigos.lista = []

# -------------------------

def desenhar_jogador():
    tela.blit(
        carro_img,
        (estado_jogo["jogador_x"] - carro_img.get_width()//2,
         ALTURA - carro_img.get_height())
    )

# -------------------------

def desenhar_hud():
    texto = fonte.render(f"Distância: {int(estado_jogo['distancia'])}", True, PRETO)
    tela.blit(texto, (10,10))

# -------------------------

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

        if estado_jogo["distancia"] >= 1000:
            pygame.mixer.music.stop()
            som_vitoria.play()
            return "vitoria"

        desenhar_hud()

        if inimigos.colisao(estado_jogo["jogador_x"], ALTURA - 90):
            som_batida.play()
            pygame.time.delay(300)
            return "fim"

        pygame.display.flip()

# -------------------------

def tela_game_over():
    tempo_piscar = 0
    mostrar = True

    while True:
        relogio.tick(60)

        tempo_piscar += relogio.get_time()
        if tempo_piscar > 500:
            mostrar = not mostrar
            tempo_piscar = 0

        if fundo_derrota:
            tela.blit(fundo_derrota, (0,0))
        else:
            tela.fill((20, 0, 0))

        texto = fonte.render("TENTE NOVAMENTE", True, (255,0,0))
        sombra = fonte.render("TENTE NOVAMENTE", True, (0,0,0))

        x = LARGURA//2 - texto.get_width()//2
        y = ALTURA//2 - 50

        if mostrar:
            tela.blit(sombra, (x+3, y+3))
            tela.blit(texto, (x, y))

        instrucao = fonte_pequena.render("PRESSIONE ENTER", True, BRANCO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, y + 80))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            return

# -------------------------

def tela_vitoria():
    inicio = pygame.time.get_ticks()
    musica_voltou = False

    tempo_piscar = 0
    mostrar = True

    while True:
        relogio.tick(60)

        # controle do piscar
        tempo_piscar += relogio.get_time()
        if tempo_piscar > 500:
            mostrar = not mostrar
            tempo_piscar = 0

        # fundo
        if fundo_vitoria:
            tela.blit(fundo_vitoria, (0, 0))
        else:
            tela.fill((0, 120, 0))

        # texto piscando
        if mostrar:
            texto = fonte.render("VOCE VENCEU!", True, (223,100
                                                            ,0))
            tela.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - 40))

        # instrução (sempre visível)
        instrucao = fonte_pequena.render("PRESSIONE ENTER", True, BRANCO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA//2 + 50))

        # volta música depois de 3s
        if not musica_voltou and pygame.time.get_ticks() - inicio > 3000:
            pygame.mixer.music.play(-1)
            musica_voltou = True

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            return
# -------------------------

def menu():
    tempo_piscar = 0
    mostrar = True

    while True:
        relogio.tick(60)

        tempo_piscar += relogio.get_time()
        if tempo_piscar > 500:
            mostrar = not mostrar
            tempo_piscar = 0

        if fundo_menu:
            tela.blit(fundo_menu, (0,0))
        else:
            tela.fill((20,20,20))

        cor = (255,0,0) if mostrar else (0,120,255)
        titulo = fonte_titulo.render("Beetle Sunset", True, cor)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 80))

        texto = fonte.render("INICIAR", True, cor)
        texto = pygame.transform.scale(texto, (int(texto.get_width()*1.2), int(texto.get_height()*1.2)))
        tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 250))

        controles = fonte.render("A/D - mover | ENTER - selecionar | ESC - sair", True, BRANCO)
        tela.blit(controles, (LARGURA//2 - controles.get_width()//2, ALTURA - 50))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            reiniciar_jogo()
            resultado = loop_jogo()

            if resultado == "fim":
                tela_game_over()
            elif resultado == "vitoria":
                tela_vitoria()

# -------------------------

menu()