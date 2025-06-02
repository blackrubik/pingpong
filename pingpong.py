from pygame import *

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
style = font.Font(None, 36)
text_first_lose = style.render('Player 1 lose!', 1, (255, 0, 0))
text_second_lose = style.render('Player 2 lose!', 1, (255, 0, 0))


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
        if keys[K_DOWN] and self.rect.y <= mw_heigh:
            self.rect.y += self.speed_x


class Player_Left(GameSprite):
    def movement(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed_x
        if keys[K_s] and self.rect.y <= mw_heigh:
            self.rect.y += self.speed_x

class Ball(GameSprite):
    def update(self):
        self.rect.x += self.speed_x        
        self.rect.y += self.speed_y

        # if self.rect.y > mw_heigh-50 or self.rect.y < 0:
        #     self.rect.y *= -1

player_right = Player_Right('player.jpg', 650, 150, 20, 120, 5, None)
player_left = Player_Left('player.jpg', 30, 150, 20, 120, 5, None)

ball = Ball('ball.png', 350, 150, 55, 55, 3, 3)

game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        mw.blit(bg, (0, 0))

        player_right.reset()
        player_right.movement()    
        
        player_left.reset()
        player_left.movement()    
        
        ball.reset()
        ball.update()

        if (sprite.collide_rect(ball, player_left) or 
        sprite.collide_rect(ball, player_right)):
            ball.speed_x *= -1

        if ball.rect.y >= mw_heigh-55 or ball.rect.y <= 0:
            ball.speed_y *= -1

        if ball.rect.x < 0:
            finish = True
            mw.blit(text_first_lose, (200, 200))   

        if ball.rect.x > mw_width:
            finish = True
            mw.blit(text_second_lose, (200, 200))

        display.update()
        clock.tick(FPS)
