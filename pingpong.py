from pygame import *

mw_width = 700
mw_heigh = 500

mw = display.set_mode((mw_width, mw_heigh))
display.set_caption('Ping Pong')

clock = time.Clock()
FPS = 60

bg = transform.scale(
    image.load('CAE8F3.png'),
    (mw_width, mw_heigh)
)

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


class Player_Right(GameSprite):
    def movement(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < mw_heigh:
            self.rect.y += self.speed


class Player_Left(GameSprite):
    def movement(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < mw_width:
            self.rect.y += self.speed

class Ball(GameSprite):
    def update(self):
        self.rect.x += self.speed        
        self.rect.y += self.speed

player_right = Player_Right('Vertical_Rectangle_Red.jpg', 650, 150, 20, 120, 5)
player_left = Player_Left('Vertical_Rectangle_Red.jpg', 30, 150, 20, 120, 5)

ball = Ball('orange_ball.png', 350, 150, 55, 55, 5)

game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    while not finish:
        mw.blit(bg, (0, 0))

        player_right.reset()
        player_right.movement()    
        
        player_left.reset()
        player_left.movement()    
        
        ball.reset()
        ball.update()

        if (sprite.collide_rect(ball, player_left) or 
        sprite.collide_rect(ball, player_right)):
            ball.speed *= -1

        if ball.rect.x >= mw_width or ball.rect.x <= 0:
            ball.speed *= -1

        display.update()
        clock.tick(FPS)
