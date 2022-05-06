from pygame import *
from random import randint, choice
import time as tm

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed_x, player_speed_y, move_keys):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed_x = player_speed_x
        self.speed_y = player_speed_y
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.move_keys = move_keys
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[self.move_keys[0]] and self.rect.y > 0:
            self.rect.y -= self.speed_y *dt/15

        if keys[self.move_keys[1]] and self.rect.y < 350:
            self.rect.y += self.speed_y *dt/15

class Ball(GameSprite):
    def move(self):
        global timing
        self.rect.y += self.speed_y *dt/15
        self.rect.x += self.speed_x *dt/15
        if self.rect.y >= win_height-30:
            self.speed_y = -self.speed_y

        if self.rect.y <= 0:
            self.speed_y = -self.speed_y

        #1
        if sprite.collide_rect(player1, ball) and self.speed_x < 0 and player1.rect.y + 75 >= self.rect.y:
            if self.speed_y > 0 and self.speed_x < 0:
                self.speed_y = -self.speed_y
                self.speed_x = -self.speed_x
            else:
                self.speed_x = -self.speed_x   
            self.speed_x = self.speed_x *1.05

        #2
        if sprite.collide_rect(player1, ball) and self.speed_x < 0 and player1.rect.y + 75 < self.rect.y:
            if self.speed_y < 0 and self.speed_x < 0:
                self.speed_y = -self.speed_y
                self.speed_x = -self.speed_x
            else:
                self.speed_x = -self.speed_x
            self.speed_x = self.speed_x *1.05
        #3
        if sprite.collide_rect(player2, ball) and self.speed_x > 0 and player2.rect.y + 75 >= self.rect.y:
            if self.speed_y > 0 and self.speed_x > 0:
                self.speed_y = -self.speed_y
                self.speed_x = -self.speed_x
            else:
                self.speed_x = -self.speed_x
            self.speed_x = self.speed_x *1.05
        #4
        if sprite.collide_rect(player2, ball) and self.speed_x > 0 and player2.rect.y + 75 < self.rect.y:
            if self.speed_y < 0 and self.speed_x > 0:
                self.speed_y = -self.speed_y
                self.speed_x = -self.speed_x
            else:
                self.speed_x = -self.speed_x
            self.speed_x = self.speed_x *1.05


        if self.rect.x <= 0:
            score[1] = score[1] + 1
            self.rect.x = win_width/2
            self.rect.y = win_height/2
            self.speed_x = choice([-5, 5])
            self.speed_y = choice(random_speedy)
        if self.rect.x >= 700:
            score[0] = score[0] + 1
            self.rect.x = win_width/2
            self.rect.y = win_height/2
            self.speed_x = choice([-5, 5])
            self.speed_y = choice(random_speedy)

img_player1 = "player1.png"
img_player2 = "player2.png"
img_ball = "ball.png"

player1keys = [K_w, K_s]
player2keys = [K_UP, K_DOWN]
random_speedy = [-5,-4,-3,3,4,5]
max_speed = 10

win_width = 700
win_height = 500
display.set_caption("Pin-pong")
window = display.set_mode((win_width, win_height))

player1 = Player(img_player1, 20, 150, 15, 150, 5, 5, player1keys)
player2 = Player(img_player2, 665, 150, 15, 150, 5, 5, player2keys)
ball = Ball(img_ball, win_width/2, win_height/2, 30, 30, choice([-5, 5]), choice(random_speedy), player1keys)

clock = time.Clock()
fps = 60
timing = tm.time()

font.init()
font1 = font.Font(None, 80)
score = [0, 0]
win_txt = font1.render("You Win!", True, (255, 75, 75))

finish = False
run = True 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
            
    if not finish:
        dt = clock.tick(fps)
        draw.rect(window, (200,255,255), Rect(0, 0, win_width, win_height))

        score_txt = font1.render(str(score[0]) + " - " + str(score[1]), True, (0, 0, 0))
        window.blit(score_txt, (300, 10))

        player1.move()
        player2.move()
        ball.move()

        player2.reset()
        player1.reset()
        ball.reset()

        if score[0] >= 5:
            finish = True
            win_txt = font1.render("You Win!", True, (255, 255, 75))
            window.blit(win_txt, (50, 200))

        if score[1] >= 5:
            finish = True
            win_txt = font1.render("You Win!", True, (75, 75, 255))
            window.blit(win_txt, (400, 200))
            
        display.update()
        
    else:
        finish = False
        score[0] = 0
        score[1] = 0

        ball.rect.x = win_width/2
        ball.rect.y = win_height/2
        
        player1.rect.y = 150
        player2.rect.y = 150

        time.delay(3000)
