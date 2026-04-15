import pygame
import math

class Player:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 300))

        # posição inicial (fora da tela)
        self.x = -300
        self.y = 250

        self.target_x = 450
        self.speed = 5

        self.state = "entering"
        self.time = 0

    def update(self):
        if self.state == "entering":
            self.x += self.speed

            if self.x >= self.target_x:
                self.x = self.target_x
                self.state = "idle"

        elif self.state == "idle":
            self.time += 0.1

    def draw(self, screen):
        offset_y = 0
        angle = 0

        if self.state == "idle":
            offset_y = math.sin(self.time * 5) * 2
            angle = math.sin(self.time * 3) * 2

        rotated = pygame.transform.rotate(self.image, angle)
        rect = rotated.get_rect(center=(self.x + 150, self.y + 150 + offset_y))

        screen.blit(rotated, rect.topleft)