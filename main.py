from pygame import*
from random import randint
from time import sleep
font.init()

WIDTH=600
HEIGHT=500
FPS=60
WHITE=(255,255,255)
RED=(150,0,0)
GREEN=(0,150,0)
RESTART=3000
win_score=10
BACKGROUND=(randint(0,255),randint(0,255),randint(0,255))

window=display.set_mode((WIDTH,HEIGHT))
display.set_caption("PING_PONG")
clock=time.Clock()

font_text=font.Font(None,36)
font_score=font.Font(None,36)

lose1=font_text.render("PLAYER 1 LOSE",True,RED)
lose2=font_text.render("PLAYER 2 LOSE",True,RED)
win1=font_text.render("PLAYER 1 WIN",True,GREEN)
win2=font_text.render("PLAYER 2 WIN",True,GREEN)

score1=0
score2=0
class GameSprite(sprite.Sprite):
    def __init__(self,img:str,x:int,y:int,w:int,h:int):
        super().__init__()
        self.image=transform.scale(image.load(img),(w,h))
       
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self,up:str,down:str,img:str,x:int,y:int,w:int,h:int,speed:int):
        super().__init__(img,x,y,w,h)
        self.speed=speed
        self.up=up
        self.down=down

    def update(self):
        keys=key.get_pressed()
        if keys[self.up]and self.rect.y>5:
            self.rect.y-=self.speed
        if keys[self.down]and self.rect.y<HEIGHT-150:
            self.rect.y+=self.speed

class Ball(GameSprite):
    def __init__(self,img:str,x:int,y:int,w:int,h:int,dx:int,dy:int):
        super().__init__(img,x,y,w,h)
        self.dx=dx
        self.dy=dy

    def update(self):
        self.rect.x+=self.dx
        self.rect.y+=self.dy

racket1=Player(K_w,K_s,"racket.png",30,200,50,150,4)
racket2=Player(K_UP,K_DOWN,"racket.png",520,200,50,150,4)
ball=Ball("tenis_ball.png",200,200,50,50,3,3)

run=True
finish=False

while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
    
    if not finish:
        window.fill(BACKGROUND)
        ball.reset()
        racket1.reset()
        racket2.reset()

        ball.update()
        racket1.update()
        racket2.update()

        if ball.rect.y> HEIGHT-50 or ball.rect.y<0:
            ball.dy*=-1
        if sprite.collide_rect(racket1,ball)or sprite.collide_rect(racket2,ball):
            ball.dx*=-1
        if ball.rect.x<racket1.rect.x:
            score2+=1
            ball.rect.x=200
            ball.rect.y=200
        if ball.rect.x>racket2.rect.x:
            score1+=1
            ball.rect.x=200
            ball.rect.y=200
        
        


        score_text=f"{score1}:{score2}"
        score_img=font_score.render(score_text,True,WHITE)
        score_rect=score_img.get_rect(center=(WIDTH//2,50))
        window.blit(score_img,score_rect)

        if score1==win_score:
            finish=True
            window.blit(win1,(HEIGHT//2,WIDTH//2))
            display.update()
            time.delay(2000)
            window.blit(lose2,(HEIGHT//2+50,WIDTH//2+50))
            
        if score2==win_score:
            finish=True
            window.blit(win2,(HEIGHT//2,WIDTH//2)) 
            display.update()
            time.delay(2000)
            window.blit(lose1,(HEIGHT//2+50,WIDTH//2+50))
    else:
        score2=0
        score1=0
        finish=False
        ball.rect.x=200
        ball.rect.y=200
        ball.dx=3
        ball.dy=3
        time.delay(RESTART)

    display.update()
    clock.tick(FPS)