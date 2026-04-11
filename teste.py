import sys

import pygame
pygame.init()
#display.set_mode: colocar o formato da tela
tela=pygame.display.set_mode([840,480])
#set_caption: nome do jogo
imagem=pygame.image.load("controle.jpg")
x,y=30,40
if __name__ =='__main__':
    print("jogo de jogo")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    tela.blit(imagem,(x,y))
    pygame.display.update()
