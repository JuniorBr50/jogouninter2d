import pygame
from grasi import Player

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Game")

clock = pygame.time.Clock()

# Assets
bg = pygame.image.load("som&foto/grasi quaqua.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

player = Player("assets/menu/player_menu.png")

# Menu
font = pygame.font.SysFont("Arial", 32)

options = ["NEW GAME", "CONTINUE", "OPTIONS"]
selected = 0

# Overlay lateral
overlay = pygame.Surface((300, HEIGHT))
overlay.set_alpha(120)
overlay.fill((0, 0, 0))

running = True

while running:
    screen.blit(bg, (0, 0))
    screen.blit(overlay, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected = (selected + 1) % len(options)

            if event.key == pygame.K_UP:
                selected = (selected - 1) % len(options)

            if event.key == pygame.K_RETURN:
                print("Selecionado:", options[selected])

    # Atualiza player (entrada + idle)
    player.update()
    player.draw(screen)

    # Desenha menu
    for i, text in enumerate(options):
        color = (0, 255, 255) if i == selected else (200, 200, 200)
        render = font.render(text, True, color)
        screen.blit(render, (50, 200 + i * 60))

    pygame.display.update()
    clock.tick(60)

pygame.quit()