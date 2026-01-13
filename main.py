from pygame import *

#Important Classes
class GameSprite (sprite.Sprite):
    def __init__(self,img,x,y,w,h,speed):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_UP] and self.rect.x <= 700-65:
            self.rect.y += self.speed
        if key_pressed[K_DOWN] and self.rect.x >= 5:
            self.rect.y -= self.speed
    



#setting jendela game

window = display.set_mode((600,500))
display.set_caption("PING-PONG")
background = transform.scale(image.load("background.png"),(600,500))

#setting FPS
fps = time.Clock()

#looping game
game = True
while game is True:
    for e in event.get():
        if e.type == QUIT:
            game = False
    window.blit(background,(0,0))
    fps.tick(60)
    display.update()