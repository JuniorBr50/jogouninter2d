import pygame
import random

pygame.init()
pygame.mixer.init()
crash_sound = pygame.mixer.Sound("som&foto/crash.mp3")
screen = pygame.display.set_mode((800,600))

pygame.mixer.music.load("som&foto/Long Away Home.wav")
pygame.mixer.music.play(-1)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # TEM que vir antes
lanes = [
    WIDTH//2 - 140,
    WIDTH//2,
    WIDTH//2 + 140
]
car_img = pygame.image.load("som&foto/car.PNG").convert_alpha()
car_img = pygame.transform.scale(car_img, (60, 120))
enemy_img = pygame.image.load("som&foto/inimigo.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (60, 120))

try:
    bg_img = pygame.image.load("som&foto/bg.png").convert()
    bg_img = pygame.transform.scale(bg_img, (800, 600))
except:
    bg_img = None
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Runner")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Cores
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
YELLOW = (255,255,0)
SKY = (135,206,235)
ROAD = (50,50,50)

# Estado global do jogo (permite continuar)
game_state = {
    "player_x": WIDTH//2,
    "speed": 5,
    "distance": 0,
    "enemies": []
}

def reset_game():
    game_state["player_x"] = WIDTH//2
    game_state["speed"] = 3
    game_state["distance"] = 0
    game_state["enemies"] = []

def spawn_enemy():
    x = random.choice(lanes)
    game_state["enemies"].append([x, -100])


def draw_player():
    screen.blit(car_img, (game_state["player_x"] - 30, HEIGHT - 120))

def draw_enemies():
    for e in game_state["enemies"]:
        screen.blit(enemy_img, (e[0]-30, e[1]))

def update_enemies():
    for e in game_state["enemies"]:
        e[1] += game_state["speed"]

def remove_enemies():
    game_state["enemies"] = [e for e in game_state["enemies"] if e[1] < HEIGHT+100]

def collision():
    player_rect = pygame.Rect(
        game_state["player_x"] - 18,  # aumentou lateral
        HEIGHT - 90,
        36,  # largura maior
        60
    )

    for e in game_state["enemies"]:
        enemy_rect = pygame.Rect(
            e[0] - 18,
            e[1] + 40,
            36,
            60
        )

        if player_rect.colliderect(enemy_rect):
            return True

    return False

def draw_hud():
    txt = font.render(f"Distância: {int(game_state['distance'])}", True, BLACK)
    screen.blit(txt, (10,10))

def game_loop():
    spawn_timer = 0

    while True:
        clock.tick(60)
        offset = int((game_state["distance"] * 2) % HEIGHT)

        if bg_img:
            screen.blit(bg_img, (0, offset - HEIGHT))
            screen.blit(bg_img, (0, offset))
        else:
            screen.fill(SKY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            return  # volta pro menu mantendo estado

        if keys[pygame.K_a]:
            game_state["player_x"] -= 5
        if keys[pygame.K_d]:
            game_state["player_x"] += 5
        # limite da tela (considerando largura do carro = 60)
        road_left = WIDTH // 2 - 170
        road_right = WIDTH // 2 + 170

        game_state["player_x"] = max(road_left, min(road_right, game_state["player_x"]))

        spawn_timer += 1
        if spawn_timer > 40:
            spawn_enemy()
            spawn_timer = 0

        update_enemies()
        remove_enemies()


        draw_enemies()
        draw_player()

        game_state["distance"] += game_state["speed"] * 0.1
        game_state["speed"] += 0.006

        draw_hud()

        if collision():
            crash_sound.play()
            pygame.time.delay(300)  # pequena pausa pra ouvir o som
            return "gameover"

        pygame.display.flip()

def game_over():
    while True:
        screen.fill(BLACK)
        txt = font.render("GAME OVER - ENTER", True, WHITE)
        screen.blit(txt, (WIDTH//2 - 170, HEIGHT//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return

def options_menu():
    volume = 5
    while True:
        screen.fill((30,30,30))

        txt = font.render(f"Volume: {volume}", True, WHITE)
        screen.blit(txt, (WIDTH//2 - 100, HEIGHT//2))

        txt2 = font.render("ESC para voltar", True, WHITE)
        screen.blit(txt2, (WIDTH//2 - 140, HEIGHT//2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            volume = max(0, volume-1)
        if keys[pygame.K_RIGHT]:
            volume = min(10, volume+1)
        if keys[pygame.K_ESCAPE]:
            return

def menu():
    options = ["Iniciar", "Continuar", "Opções"]
    selected = 0

    while True:
        screen.fill((20,20,20))

        for i, opt in enumerate(options):
            color = WHITE if i == selected else (100,100,100)
            txt = font.render(opt, True, color)
            screen.blit(txt, (WIDTH//2 - 80, 200 + i*50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            selected = (selected - 1) % len(options)
            pygame.time.delay(150)

        if keys[pygame.K_DOWN]:
            selected = (selected + 1) % len(options)
            pygame.time.delay(150)

        if keys[pygame.K_RETURN]:
            if options[selected] == "Iniciar":
                reset_game()
                result = game_loop()
                if result == "gameover":
                    game_over()

            elif options[selected] == "Continuar":
                result = game_loop()
                if result == "gameover":
                    game_over()

            elif options[selected] == "Opções":
                options_menu()

# Start
menu()