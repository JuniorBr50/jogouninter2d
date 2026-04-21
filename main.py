import pygame
from inimigos import Inimigos
from jogador import Jogador
from hud import HUD
from telas import Telas

pygame.init()
pygame.mixer.init()

# sons
som_vitoria = pygame.mixer.Sound("som&foto/Victory.wav")
som_batida = pygame.mixer.Sound("som&foto/crash.mp3")

pygame.mixer.music.load("som&foto/Long Away Home.wav")
pygame.mixer.music.play(-1)

# config básica
LARGURA = 800
ALTURA = 600

screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Beetle Sunset DEMO")

clock = pygame.time.Clock()

# pistas
faixas = [
    LARGURA // 2 - 140,
    LARGURA // 2,
    LARGURA // 2 + 140
]

# entidades
inimigos = Inimigos(faixas)

carro = pygame.image.load("som&foto/fuscaRosa.PNG").convert_alpha()
carro = pygame.transform.scale(carro, (60, 120))

player = Jogador(LARGURA // 2, LARGURA, ALTURA, carro)

# função simples de carregar imagem
def carregar(caminho):
    try:
        img = pygame.image.load(caminho).convert()
        return pygame.transform.scale(img, (LARGURA, ALTURA))
    except:
        return None

# imagens
bg = carregar("som&foto/bg.png")
menu_bg = carregar("som&foto/menu_iniciar.png")
win_bg = carregar("som&foto/vitoria_fusca.png")
lose_bg = carregar("som&foto/gameover_fundo.png")

# fontes
fonte = pygame.font.Font("som&foto/Pixel Game.otf", 40)
fonte_menor = pygame.font.Font("som&foto/Pixel Game.otf", 25)
fonte_grande = pygame.font.Font("som&foto/Pixel Game.otf", 80)

hud = HUD(fonte, fonte_menor)

telas = Telas(
    screen,
    LARGURA,
    ALTURA,
    fonte,
    fonte_menor,
    fonte_grande,
    menu_bg,
    win_bg,
    lose_bg,
    clock
)

# estado do jogo
velocidade = 5
distancia = 0

def resetar():
    global velocidade, distancia
    player.x = LARGURA // 2
    velocidade = 5
    distancia = 0
    inimigos.lista.clear()

def jogar():
    global velocidade, distancia

    spawn_timer = 0

    while True:
        dt = clock.tick(60)

        # fundo
        desloc = int((distancia * 2) % ALTURA)

        if bg:
            screen.blit(bg, (0, desloc - ALTURA))
            screen.blit(bg, (0, desloc))
        else:
            screen.fill((135, 206, 235))

        # eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            return None

        player.mover(keys)

        # spawn inimigos
        spawn_timer += 1
        if spawn_timer >= 40:
            inimigos.gerar()
            spawn_timer = 0

        inimigos.atualizar(velocidade)
        inimigos.desenhar(screen)

        player.desenhar(screen)

        # progressão
        distancia += velocidade * 0.1

        if velocidade < 12:
            velocidade += 0.005

        # vitória
        if distancia >= 1000:
            pygame.mixer.music.stop()
            som_vitoria.play()
            return "win"

        hud.desenhar(screen, distancia)

        # colisão
        if inimigos.colisao(player.x, ALTURA - 90):
            som_batida.play()
            pygame.time.delay(300)
            return "lose"

        pygame.display.update()

def tela_fim():
    blink = 0
    mostrar = True

    while True:
        clock.tick(60)
        blink += clock.get_time()

        if blink > 500:
            mostrar = not mostrar
            blink = 0

        if lose_bg:
            screen.blit(lose_bg, (0, 0))
        else:
            screen.fill((20, 0, 0))

        if mostrar:
            txt = fonte.render("TENTE NOVAMENTE", True, (255, 0, 0))
            screen.blit(txt, (LARGURA // 2 - txt.get_width() // 2, ALTURA // 2 - 50))

        info = fonte_menor.render("PRESSIONE ENTER", True, (255, 255, 255))
        screen.blit(info, (LARGURA // 2 - info.get_width() // 2, ALTURA // 2 + 50))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            return

def tela_win():
    inicio = pygame.time.get_ticks()
    voltou = False

    blink = 0
    mostrar = True

    while True:
        clock.tick(60)
        blink += clock.get_time()

        if blink > 500:
            mostrar = not mostrar
            blink = 0

        if win_bg:
            screen.blit(win_bg, (0, 0))
        else:
            screen.fill((0, 120, 0))

        if mostrar:
            txt = fonte.render("VOCE VENCEU!", True, (255, 0, 0))
            screen.blit(txt, (LARGURA // 2 - txt.get_width() // 2, ALTURA // 2 - 40))

        info = fonte_menor.render("PRESSIONE ENTER", True, (255, 255, 255))
        screen.blit(info, (LARGURA // 2 - info.get_width() // 2, ALTURA // 2 + 50))

        # volta música depois de 3s
        if not voltou and pygame.time.get_ticks() - inicio > 3000:
            pygame.mixer.music.play(-1)
            voltou = True

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            return

# loop principal
while True:
    escolha = telas.menu()

    if escolha == "iniciar":
        resetar()
        resultado = jogar()

        if resultado == "lose":
            tela_fim()
        elif resultado == "win":
            tela_win()