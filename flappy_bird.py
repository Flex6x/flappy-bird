import pygame
import sys
import random
from pygame.locals import K_UP


pygame.init()
hintergrund = pygame.image.load("flappy_bird_background.jpg")
background_width = hintergrund.get_width()
screen = pygame.display.set_mode([700, 394])
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")

bird = pygame.image.load('vogel3.png')
bird = pygame.transform.scale(bird, (58.3*1.25, 42.8*1.25))
bird_rect = bird.get_rect(topleft=(100, 100))

icon = pygame.image.load('bird.png')
pygame.display.set_icon(icon)

o1 = pygame.image.load('pipe_bottom.png')
o2 = pygame.image.load('pipe_bottom2.png')
o3 = pygame.image.load('pipe_bottom3.png')
o4 = pygame.image.load('pipe_bottom4.png')
o5 = pygame.image.load('pipe_upper.png')
o6 = pygame.image.load('pipe_upper2.png')
o7 = pygame.image.load('pipe_upper3.png')
o8 = pygame.image.load('pipe_upper4.png')

o1 = pygame.transform.scale(o1, (260*0.5, 479*0.5))
o2 = pygame.transform.scale(o2, (260*0.5, 408*0.5))
o3 = pygame.transform.scale(o3, (260*0.5, 222*0.5))
o4 = pygame.transform.scale(o4, (260*0.5, 390*0.5))
o5 = pygame.transform.scale(o5, (260*0.5, 480*0.5))
o6 = pygame.transform.scale(o6, (260*0.5, 408*0.5))
o7 = pygame.transform.scale(o7, (260*0.5, 222*0.5))
o8 = pygame.transform.scale(o8, (260*0.5, 390*0.5))

pause = pygame.image.load('pause.png')
pause_x = 300  # X-Koordinate
pause_y = 150  # Y-Koordinate
pause = pygame.transform.scale(pause, (100, 100))

gamemover = pygame.image.load('gameover.png')
gameover_x = 250  # X-Koordinate
gameover_y = 65  # Y-Koordinate
gamemover = pygame.transform.scale(gamemover, (413*0.5, 549*0.5))

x, y = 175, 300
x_pos = 0
scroll_speed = 2

gravity = 0.5
jump_strength = -7
bird_velocity = 0

obstacle_timer = 0
obstacle_interval = 1500  # Intervall in Millisekunden, enger gesetzt
obstacle_distance = 300  # Fester Abstand zwischen den Hindernissen

obstacles = pygame.sprite.Group()

_gameover = False

#score

score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX=10
textY=10

timer = 2
first_event = True  

INCREMENT_EVENT = pygame.USEREVENT + 1

pygame.time.set_timer(INCREMENT_EVENT, 3900)

def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -=10   # Geschwindigkeit des Hindernisses
        if self.rect.right < 0:
            self.kill()

def create_obstacle():
    image = random.choice([o1, o2, o3, o4])
    x = 800  # Startpunkt rechts außerhalb des Bildschirms
    if image in [o1]:
        y = 250  # Y-Position für untere Hindernisse
    elif image in [o2]:
        y = 254
    elif image in [o3]:
        y = 320
    elif image in [o4]:
        y = 254
    obstacle = Obstacle(image, x, y)
    obstacles.add(obstacle)

def create_obstacle2():
    image = random.choice([o5, o6, o8])
    x = 800  # Startpunkt rechts außerhalb des Bildschirms

    y = -125  # Y-Position für obere Hindernisse
    obstacle = Obstacle(image, x, y)
    obstacles.add(obstacle)

def zeichnen():
    # Bildschirm löschen
    screen.fill((0, 0, 0))
    # Hintergrundbild zeichnen
    screen.blit(hintergrund, (x_pos, 0))
    screen.blit(hintergrund, (x_pos + background_width, 0))
    # Hindernisse zeichnen
    obstacles.update()
    obstacles.draw(screen)
    # Vogel zeichnen
    screen.blit(bird, bird_rect)
    show_score(textX, textY)
    pygame.display.flip()


sprungvar = -16
go=True

paused = False  # Variable für den Pausenstatus

while go:
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength
            if event.key == pygame.K_p:  # Pause/Resume mit Taste 'P'
                paused = not paused
        
        elif event.type == INCREMENT_EVENT:
            if first_event:
                first_event = False
                # Setze den Timer auf 1500 Millisekunden (1,5 Sekunden)
                pygame.time.set_timer         (INCREMENT_EVENT, 1500)
                score_value += 1  # Erhöhe den Score beim ersten Ereignis
            else:
                score_value += 1
 
    if not paused:  # Spiel nur fortsetzen, wenn nicht pausiert
        # Physik
        bird_velocity += gravity
        y += bird_velocity
        bird_rect.y = y

        # Begrenzung auf den Bildschirm
        if y > 394 - bird.get_height():
            y = 394 - bird.get_height()
            bird_velocity = 0
        if y < 0:
            y = 0
            bird_velocity = 0

        # Hindernisse erstellen
        if pygame.time.get_ticks() - obstacle_timer > obstacle_interval:
            create_obstacle()
            create_obstacle2()
            obstacle_timer = pygame.time.get_ticks()
            obstacle_interval = 1500  # Setze das Intervall zurück, um den gleichen Abstand zu gewährleisten
        
        # Hintergrund scrollen
        x_pos -= scroll_speed
        if x_pos <= -background_width:
            x_pos = 0

        # Kollision überprüfen
        for obstacle in obstacles:
            if bird_rect.colliderect(obstacle.rect):
                _gameover = True
                go = False  # Beende die Schleife, um das Spiel zu stoppen

        if bird_rect.y > 346 or bird_rect.y < 0:
            _gameover = True
            go = False  # Beende die Schleife, um das Spiel zu stoppen

        zeichnen()

    elif paused:
        screen.blit(pause, (pause_x, pause_y))
        pygame.display.flip()
    clock.tick(60)

# Zeige das Game Over Label und Bild an
screen.blit(gamemover, (gameover_x, gameover_y))
pygame.display.flip()
pygame.time.wait(1500)  # nach 1.5 Sekunden quit
pygame.quit()
