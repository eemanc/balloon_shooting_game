import os
import pygame # version 2.0.1

pygame.init()

is_playing = True
balloon_popped = False

# game window
width = 500
height = 300

# screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Balloon Shooting Game')

# background
background = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets/background.jpg'))

# shooter
class Shooter:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        shooter = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets/shooter.png'))
        screen.blit(shooter, (self.x, self.y))

shooter = Shooter(width-85, height-180)

# balloon
class Balloon:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        balloon = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets/balloon.png'))
        screen.blit(balloon, (self.x, self.y))

    # detect collision by checking if balloon and bullet coordinates intersect
    def detect_collision(self):
        global balloon_popped
        for bullet in bullets:
            if (bullet.x > self.x and bullet.x < self.x + 43 and 
                bullet.y > self.y and bullet.y < self.y + 58):
                bullets.remove(bullet)
                self.y = 400
                balloon_popped = True

def move_balloon():
    global balloon_speed
    balloon.y += balloon_speed
    if balloon.y <= 0 or balloon.y >= (height-50):
        balloon_speed *= -1

balloon = Balloon(10, 10)
balloon_speed = 0.09

# bullets
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, (107, 110, 110), pygame.Rect(self.x-6, self.y+15, 10, 10))
        self.x -= 0.9

bullets = []

# text on when balloon is shot down
def game_over(shots):
    font = pygame.font.SysFont('', 40)
    game_over = font.render("You win!", True, (0, 0, 0))
    score = font.render("Missed shots: " + str(shots-1), True, (0, 0, 0))
    screen.blit(game_over, (180, 100))
    screen.blit(score, (130, 150))


missed_shots = 0

while is_playing:
    # draw screen
    screen.blit(background, (0,0))
    shooter.draw()
    balloon.draw()
    move_balloon()

    # move shooter
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and shooter.y > 7:
            shooter.y -= 0.09
    elif pressed[pygame.K_DOWN] and shooter.y < height-50:
            shooter.y += 0.09

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            is_playing = False
        # shoot bullet
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(Bullet(shooter.x, shooter.y))
            missed_shots += 1

    # draw bullets
    for bullet in bullets:
        bullet.draw()

    # check for collision
    balloon.detect_collision()
    if balloon_popped:
        game_over(missed_shots)

    pygame.display.update()