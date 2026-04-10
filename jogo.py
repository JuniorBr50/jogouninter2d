import pygame
#init serve pra iniciar tem q ter ele
pygame.init()
#display.set_mode: colocar o formato da tela
tela=pygame.display.set_mode([840,480])
#set_caption: nome do jogo
pygame.display.set_caption('grasi games')
jogo=True
def draw():
    # fill: a cor da sua tela
    tela.fill([187, 48, 120])
    jogador = pygame.Rect(400, 300, 100, 100)
    pygame.draw.rect(tela, [255, 255, 255], jogador)
# if name main : ele é o play,tem q ter
if __name__ =='__main__':
    print("jogo de jogo")
    while jogo:
        #Isso é um laço que percorre todos os eventos que aconteceram no jogo naquele momento
        for evento in pygame.event.get():
        #Para cada evento que aconteceu agora, execute algo ou seja feche o jogo
            if evento.type==pygame.QUIT:
                 jogo=False
        #se voce apertar primerio o 'w' vai printar
            elif evento.type==pygame.KEYDOWN:
                if evento.key==pygame.K_w:
                    print("jogo de jogo")
        #pra pressionar a tecla
        top=pygame.key.get_pressed()
        if top[pygame.K_SPACE]:
            print("tario")
        draw()

        #update do set_mode
        pygame.display.update()