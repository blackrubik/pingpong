from pygame import *
from time import time as timer

mw_width = 700
mw_heigh = 500

mw = display.set_mode((mw_width, mw_heigh))
display.set_caption('Ping Pong')

clock = time.Clock()
FPS = 60

bg = transform.scale(
    image.load('bg.png'),
    (mw_width, mw_heigh)
)

font.init()
style = font.Font(None, 96)
style_small = font.Font(None, 36)

text_first_lose = style.render('Player 1 lose!', 1, (255, 0, 0))
text_second_lose = style.render('Player 2 lose!', 1, (255, 0, 0))
text_press_e = style_small.render('Press E to start new game', 1, (255, 0, 0))
text_press_ecs = style_small.render('Press ECS to leave', 1, (255, 0, 0))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, 
                player_x, player_y, 
                player_width, player_heidh, player_speed_x, player_speed_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), 
                                    (player_width, player_heidh))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed_x = player_speed_x       
        self.speed_y = player_speed_y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player_Right(GameSprite):
    def movement(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed_x
        if keys[K_DOWN] and self.rect.y < mw_heigh-120:
            self.rect.y += self.speed_x

    def new_game(self):
        self.rect.x = 650
        self.rect.y = 150


class Player_Left(GameSprite):
    def movement(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed_x
        if keys[K_s] and self.rect.y <= mw_heigh-120:
            self.rect.y += self.speed_x

    def new_game(self):
        self.rect.x = 30
        self.rect.y = 150

class Ball(GameSprite):
    def update(self):
        self.rect.x += self.speed_x        
        self.rect.y += self.speed_y

        if self.rect.y > mw_heigh-50 or self.rect.y < 0:
            self.rect.y *= -1

    def new_game(self):
        self.rect.x = 350
        self.rect.y = 150

        self.speed_x = 3
        self.speed_y = 3

player_right = Player_Right('player.jpg', 650, 150, 20, 120, 5, None)
player_left = Player_Left('player.jpg', 30, 150, 20, 120, 5, None)

ball = Ball('ball.png', 350, 150, 55, 55, 3, 3)

first_time = timer()

game = True
finish = False
can_start_new = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if can_start_new == True:
            if e.type == KEYDOWN:
                if e.key == K_e:
                    first_time = timer()

                    player_left.new_game()
                    player_right.new_game()
                    ball.new_game()

                    finish = False
                    can_start_new = False

                if e.key == K_ESCAPE:
                    game = False


    if not finish:
        mw.blit(bg, (0, 0))

        player_right.reset()
        player_right.movement()    
        
        player_left.reset()
        player_left.movement()    
        
        ball.reset()
        ball.update()


        second_time = timer()
        now_time = round(second_time-first_time, 1)
        time_speed_up = round(second_time-first_time, 1)

        text_timer = style_small.render('Time: ' + str(now_time), 1, (0, 0, 0))
        mw.blit(text_timer, (300, 20))


        if time_speed_up >= 5.0:
            ball.speed_x *= 1.001

            time_speed_up = 0

        if (sprite.collide_rect(ball, player_left) or 
        sprite.collide_rect(ball, player_right)):
            ball.speed_x *= -1

        if ball.rect.y >= mw_heigh-55 or ball.rect.y <= 0:
            ball.speed_y *= -1

        if ball.rect.x < 0:
            finish = True
            mw.blit(text_first_lose, (135, 200))   
            mw.blit(text_press_e, (260, 280))
            mw.blit(text_press_ecs, (260, 310))
            can_start_new = True

        if ball.rect.x > mw_width:
            finish = True
            mw.blit(text_second_lose, (135, 200))
            mw.blit(text_press_e, (260, 280))            
            mw.blit(text_press_ecs, (260, 310))
            can_start_new = True
        display.update()
        clock.tick(FPS)
