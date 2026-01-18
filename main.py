from pygame import *
from random import choice

mixer.init()
bgms = mixer.music
bgms.load("bg.mp3")
bgms.play(loops=-1)

sound_1 = mixer.Sound("amaterasu.mp3")


# Important Classes
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.speed = speed
        self.w = w
        self.h = h
        self.img = img
        self.image = transform.scale(image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player1(GameSprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__(img, x, y, w, h, speed)
        self.smash_cooldown = 0

    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x <= 600 - 65:
            self.rect.x += self.speed
        if key_pressed[K_LEFT] and self.rect.x >= 5:
            self.rect.x -= self.speed

        if self.smash_cooldown > 0:
            self.smash_cooldown -= 1

    def sm(self, ball):
        global speed_x, speed_y
        key_pressed = key.get_pressed()

        if key_pressed[K_SPACE] and self.smash_cooldown == 0:
            self.smash_cooldown = 20
            sound_1.play()

            # ubah sprite smash
            self.image = transform.scale(image.load("p1-sm.png"), (100, 100))

            # taruh bola pas di atas player
            ball.rect.centerx = self.rect.centerx
            ball.rect.bottom = self.rect.top

            # smash ke atas (lebih kenceng)
            speed_y = -8
            speed_x = choice([-4, -2, 2, 4])


class Player2(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_d] and self.rect.x <= 600 - 65:
            self.rect.x += self.speed
        if key_pressed[K_a] and self.rect.x >= 5:
            self.rect.x -= self.speed


# setting jendela game
window = display.set_mode((600, 500))
display.set_caption("PING-PONG")
background = transform.scale(image.load("background.png"), (600, 500))

# setting FPS
fps = time.Clock()

player1 = Player1("p1.png", 500, 350, 100, 100, 5)
player2 = Player2("p2.png", 500, 50, 100, 100, 5)

ball = GameSprite("ball.png", 300, 50, 50, 50, 10)

speed_x = 3
speed_y = 3

# looping game
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))

    # player 1
    player1.reset()
    player1.update()
    player1.sm(ball)

    # balikin sprite normal kalau tidak smash
    if not key.get_pressed()[K_SPACE]:
        player1.image = transform.scale(image.load("p1.png"), (100, 100))

    # player 2
    player2.reset()
    player2.update()

    # ball movement
    ball.rect.x += speed_x
    ball.rect.y += speed_y

    # pantul atas/bawah
    if ball.rect.y < 0:
        speed_y *= -1
        

    if ball.rect.y > 450:
        speed_y *= -1
    

    # pantul kiri/kanan
    if ball.rect.x > 550 or ball.rect.x < 0:
        speed_x *= -1
       

    # collision player
    if sprite.collide_rect(ball, player1):
        speed_y *= -1

    if sprite.collide_rect(ball, player2):
        speed_y *= -1

    ball.reset()
    fps.tick(60)
    display.update()
