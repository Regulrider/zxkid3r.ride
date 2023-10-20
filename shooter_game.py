#Создай собственный Шутер!
from random import *
import pygame
print('hello world')
WIDTH = 1200 #2500 
HEIGHT = 400#800
TIKRATE = 150
COLOR = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My_Tipical_Day')

clock = pygame.time.Clock()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, speed, image, cd):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = speed
        self.cd= cd
        self.base_cd = cd

    def draw(self):
        window.blit(self.image, self.rect.topleft)

class Player(Sprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.centerx -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.centerx += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.centery -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.centery += self.speed
        if self.cd > 0:
            self.cd -= 1
        if keys[pygame.K_SPACE] and game.state == 'play':
            if self.cd == 0:
                self.cd = self.base_cd
                laser_Sound.play()
                lasers.add(Laser(self.rect.centerx, self.rect.top, -10))



class  Enemy(Sprite):
    def update(self):
        self.rect.centery += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((3, 13))
        self.image.fill(COLOR)
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()

    def draw(self):
        window.blit(self.image, self.rect.topleft)

class GameManager():
    def __init__(self):
        self.state = 'play'
        self.score = 0
        self.score_font =pygame.font.SysFont('consolas', 30)
        self.score_text = self.score_font.render('0', True, WHITE)

    def show_score(self):
        window.blit(self.score_text, (10, 10))

    def update_score(self):
        self.score += 1 
        self.score_text = self.score_font.render(str(self.score), True, WHITE)

    def restart(self):
        self.state = 'play'
        self.score = 0
        self.score_text = self.score_font.render('0', True, WHITE)
        player.rect.center = (700, 500)
        for e in enemies:
            e.kill()
    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and self.state== 'game_over':
                        self.restart()
game = GameManager()

player = Player(700, 500, 100, 100, 7, 'quadro.png', TIKRATE // 25)

enemies = pygame.sprite.Group()
enemy_spawn_kd = TIKRATE

lasers = pygame.sprite.Group()

laser_Sound = pygame.mixer.Sound('fire.ogg')

bg = pygame.image.load('shosse.jpg')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

my_font = pygame.font.SysFont('Arial', 70)
game_over_text = my_font.render('На штраф стоянку!', True, WHITE)

my_font = pygame.font.SysFont('Arial', 40)
restart_over_text = my_font.render('Нажми пробел что бы заплатить штраф', True, WHITE)

run = True

while run:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            run = False
    game.update(events)  
    
    if game.state == 'play':
    
        window.blit(bg, (0, 0))
        
        if enemy_spawn_kd == 0:
            enemy_spawn_kd = TIKRATE
            enemies.add(Enemy(randint(500, 900), -100, 250, 100, 3, 'dps.png', TIKRATE // 2 ))
        else:
            enemy_spawn_kd -= 1
        
        player.update()
        enemies.update()
        lasers.update()

        player.draw()
        enemies.draw(window)
        lasers.draw(window)
        game.show_score()

        if pygame.sprite.spritecollideany(player, enemies):
            game.state = 'game_over'

        shots = pygame.sprite.groupcollide(lasers, enemies, True, True)
        if len(shots) > 0:
            game.update_score()
            print(game.score)

    if game.state == 'game_over':
        window.blit(bg, (0, 0))
        window.blit(game_over_text,(250, 100))
        window.blit(restart_over_text,(250, 175))
    pygame.display.flip()
    clock.tick(TIKRATE)
#ты лучшая
