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
        if keys[K_LEFT] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_RIGHT] and self.rect.y < mw_width-85:
            self.rect.y += self.speed


class Player_Left(GameSprite):
    def movement(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_d] and self.rect.y < mw_width-85:
            self.rect.y += self.speed

game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    mw.blit(bg, (0, 0))

    display.update()
    clock.tick(FPS)