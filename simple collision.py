import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))

warrimg= pygame.image.load('Knight idle.png')
rect= warrimg.get_rect()
vel=10
obstacle = pygame.Rect(400,200,80,80)

def quit_game():
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

run=True
while run:
    quit_game()
    screen.fill((255,255,255))

    userInput = pygame.key.get_pressed()
    if userInput[pygame.K_LEFT]:
        rect.x -= vel
    if userInput[pygame.K_RIGHT]:
        rect.x += vel
    if userInput[pygame.K_UP]:
        rect.y -= vel
    if userInput[pygame.K_DOWN]: 
        rect.y -= vel   

    screen.blit(warrimg, rect)
    pygame.draw.rect(screen, (0,0,0), obstacle, 4)

    if rect.colliderect(obstacle):
        pygame.draw.rect(screen, (255,0,0), rect, 4)

    pygame.time.delay(30)
    pygame.display.update()
            
