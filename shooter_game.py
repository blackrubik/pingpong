from pygame import *
from random import randint
from time import time as timer

mw_width = 700
mw_heigh = 500

mw = display.set_mode((mw_width, mw_heigh))
display.set_caption('Shooter')

clock = time.Clock()
FPS = 60

bg = transform.scale(
    image.load('galaxy.jpg'),
    (700, 500)
)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


font.init()
style = font.SysFont("Arial", 36)
style_end = font.SysFont('Arial', 190)
style_life = font.SysFont('Arial', 120)

text_lose = style_end.render('You lose!', 1, (255, 0, 0))
text_win = style_end.render('You win!', 1, (0, 255, 0))


lost = 0
score = 0
life = 3
num_fire = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, 
                player_x, player_y, 
                player_width, player_heidh, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), 
                                    (player_width, player_heidh))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def movement(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700-85:
            self.rect.x += self.speed

        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700-85:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullets('bullet.png', self.rect.centerx, 
                        self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        global lost
        if self.rect.y > 500-85:
            self.rect.x = randint(0, 500-85)
            self.rect.y = 0
            self.speed = randint(1,3)
            lost += 1

class Bullets(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -50:
            self.kill()

ufos = sprite.Group()
for i in range(5):
    ufo = Enemy('ufo.png', 
                  randint(80, 700-85), 
                  0, 85, 85, randint(1,3))
    ufos.add(ufo) 
    
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', 
                  randint(30, 700-80), 
                  -40, 80, 50, randint(1,2))
    asteroids.add(asteroid)


player = Player('rocket.png', 350, 410, 85, 85, 5)

bullets = sprite.Group()

game = True
finish_game = False
show_score_text = True
rel_time = False


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    player.fire()
                    fire_sound.play()
                    num_fire += 1

                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if not finish_game:
        mw.blit(bg, (0, 0))

        ufos.update()
        ufos.draw(mw)        
        
        bullets.update()
        bullets.draw(mw)

        player.reset()
        player.movement()

        asteroids.update()
        asteroids.draw(mw)


        text_missed = style.render(
            'Missed: ' + str(lost), 1, (255, 255, 255)
    )
        text_score = style.render(
            'Score: ' + str(score), 1, (255, 255, 255)
    )
        if show_score_text:
            mw.blit(text_score, (10, 15))

        mw.blit(text_missed, (10, 40))


        if rel_time == True:
            now_time = timer()

            if now_time - last_time == 3:
                reload = style.render('Wait, reload....', 1, (150, 0, 0))
                mw.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        if (sprite.spritecollide(player, ufos, True) or 
        sprite.spritecollide(player, asteroids, True)):
            life -= 1

        collides = sprite.groupcollide(ufos, bullets, True, True)
        for c in collides:
            score += 1
            enemy = Enemy('ufo.png', 
                  randint(80, 700-85), 
                  0, 85, 85, randint(1,3))
            ufos.add(enemy) 

        if life == 0:
            finish_game = True
            mw.blit(text_lose, (60, 170))

        if score == 11:
            mw.blit(text_win, (60, 170))
            finish_game = True

        if lost >= 3:
            finish_game = True
            mw.blit(text_lose, (60, 170))

        
        if life == 3:
            life_color = (0, 150, 0)        
        if life == 2:
            life_color = (150, 150, 0)        
        if life == 1:
            life_color = (150, 0, 0)
           
        text_life = style_life.render(str(life), 1, life_color)
        mw.blit(text_life, (640, 10))

    display.update()
    clock.tick(FPS)