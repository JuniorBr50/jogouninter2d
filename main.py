import pygame
from inimigos import Inimigos
from jogador import Jogador
from hud import HUD
from telas import Telas
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

# Imagem jogador
carro_img = pygame.image.load("som&foto/fuscaRosa.PNG").convert_alpha()
carro_img = pygame.transform.scale(carro_img, (60, 120))

# Criar jogador
jogador = Jogador(LARGURA//2, LARGURA, ALTURA, carro_img)

# Função carregar imagem
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
hud = HUD(fonte, fonte_pequena)

# Cores
BRANCO = (255,255,255)
PRETO = (0,0,0)
CEU = (135,206,235)

relogio = pygame.time.Clock()
telas = Telas(
    tela,
    LARGURA,
    ALTURA,
    fonte,
    fonte_pequena,
    fonte_titulo,
    fundo_menu,
    fundo_vitoria,
    fundo_derrota,
    relogio
)
estado_jogo = {
    "velocidade": 5,
    "distancia": 0
}

# -------------------------

def reiniciar_jogo():
    jogador.x = LARGURA//2
    estado_jogo["velocidade"] = 5
    estado_jogo["distancia"] = 0
    inimigos.lista = []

# -------------------------


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

        # Movimento jogador
        jogador.mover(teclas)

        # Inimigos
        tempo_spawn += 1
        if tempo_spawn > 40:
            inimigos.gerar()
            tempo_spawn = 0

        inimigos.atualizar(estado_jogo["velocidade"])
        inimigos.desenhar(tela)

        # Desenhar jogador
        jogador.desenhar(tela)

        # Atualizar jogo
        estado_jogo["distancia"] += estado_jogo["velocidade"] * 0.1
        estado_jogo["velocidade"] = min(12, estado_jogo["velocidade"] + 0.005)

        # Vitória
        if estado_jogo["distancia"] >= 1000:
            pygame.mixer.music.stop()
            som_vitoria.play()
            return "vitoria"

        hud.desenhar(tela, estado_jogo["distancia"])

        # Colisão
        if inimigos.colisao(jogador.x, ALTURA - 90):
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

        if mostrar:
            texto = fonte.render("TENTE NOVAMENTE", True, (255,0,0))
            tela.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - 50))

        instrucao = fonte_pequena.render("PRESSIONE ENTER", True, BRANCO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA//2 + 50))

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

        tempo_piscar += relogio.get_time()
        if tempo_piscar > 500:
            mostrar = not mostrar
            tempo_piscar = 0

        if fundo_vitoria:
            tela.blit(fundo_vitoria, (0, 0))
        else:
            tela.fill((0, 120, 0))

        if mostrar:
            texto = fonte.render("VOCE VENCEU!", True, (255,0,0))
            tela.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - 40))

        instrucao = fonte_pequena.render("PRESSIONE ENTER", True, BRANCO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA//2 + 50))

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
while True:
    acao = telas.menu()

    if acao == "iniciar":
        reiniciar_jogo()
        resultado = loop_jogo()

        if resultado == "fim":
            telas.game_over()
        elif resultado == "vitoria":
            telas.vitoria()

# -------------------------

