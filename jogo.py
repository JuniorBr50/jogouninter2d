import pygame
#init serve pra iniciar tem q ter ele
pygame.init()
#display.set_mode: colocar o formato da tela
tela=pygame.display.set_mode([840,480])
#set_caption: nome do jogo
pygame.display.set_caption('grasi games')
jogo=True
eimage = pygame.image.load("controle.jpg")

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
            print("tooop")


        tela.blit(eimage,(6,9))

        #update do set_mode
        pygame.display.update()