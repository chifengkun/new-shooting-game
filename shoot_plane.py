#-*- encoding: utf-8 -*-
'''
Created on 2022-07-17 13:31:41
updated on 2022-07-29 20:48:01

@author: chifeng
'''
import pygame
import random
import time
from os import path  #这样可以连接路径时不用os.path了

WIDTH,HEIGHTH = 1080,680
turns = 1 #第几波
# score = 0
font_dir = path.join(path.dirname(__file__),'fonts')
img_dir = path.join(path.dirname(__file__),'img') #path.dirname(__file__)代码文件当前目录
sound_dir = path.join(path.dirname(__file__),'sound')
background_dir = path.join(img_dir,'background.jpg')
player_dir = path.join(img_dir,'ships')
enmeys_dir = path.join(img_dir,'enemys')
ammo_dir = path.join(img_dir,'ammo')
explosion_dir = path.join(img_dir,'Explosions')

'''基础设置'''

pygame.mixer.pre_init(44100,-16,2,2048)
pygame.mixer.init()
pygame.init()
pygame.display.set_caption('shooting')
screen = pygame.display.set_mode((WIDTH,HEIGHTH))
gameover = False
clock = pygame.time.Clock()

pygame.mixer.music.load(path.join(sound_dir,'jinitaimei.mp3'))
pygame.mixer.music.play(loops=-1)
background = pygame.image.load(background_dir).convert()#导入背景图片并转换成 方便处理的格式
background = pygame.transform.scale(background,(1080,680))
background_rect = background.get_rect()
shoot_sound = pygame.mixer.Sound(path.join(sound_dir,'Laser_Shoot.wav'))
explosion_sound = pygame.mixer.Sound(path.join(sound_dir,'Explosion.wav'))
hurts_sound = pygame.mixer.Sound(path.join(sound_dir,'Hit_Hurt5.wav'))
boss_hurts_sound = pygame.mixer.Sound(path.join(sound_dir,'niganma.wav'))
supplement_sound = pygame.mixer.Sound(path.join(sound_dir,'Pickup_Coin.wav'))
skill_sound = pygame.mixer.Sound(path.join(sound_dir,'mudamuda.wav'))

'''导入图片'''

player = []
for i in range(1,10):
    player_img = pygame.image.load(path.join(player_dir,f'spaceShips_00{i}.png')).convert()
    player_img = pygame.transform.scale(player_img,(50,50))
    player_img.set_colorkey((0,0,0))
    player.append(player_img)
god_ship = pygame.image.load(path.join(player_dir,'spaceShips_001（gold）.png')).convert()
god_ship = pygame.transform.scale(god_ship,(50,50))
god_ship.set_colorkey((0,0,0))
kun = []
for j in range(1,4):
    kun_img = pygame.image.load(path.join(enmeys_dir,f'{j}.png')).convert()
    kun_img = pygame.transform.scale(kun_img,(60,65))
    kun_img.set_colorkey((255,255,255))
    kun.append(kun_img)
ammos = []
for k in range(1,22):
    k = '%03d'%k
    ammo_img = pygame.image.load(path.join(ammo_dir,f'spaceMissiles_{k}.png')).convert()
    ammo_img = pygame.transform.scale(ammo_img,(9,20))
    ammo_img.set_colorkey((0,0,0))
    ammos.append(ammo_img)
explosion = []
for l in range(9):
    explosion_img = pygame.image.load(path.join(explosion_dir,f'regularExplosion0{l}.png')).convert()
    explosion_img = pygame.transform.scale(explosion_img,(80,80))
    explosion_img.set_colorkey((0,0,0))
    explosion.append(explosion_img)

heart_img = pygame.image.load(path.join(img_dir,'heartFull.png')).convert()
heart_img = pygame.transform.scale(heart_img,(20,20))
heart_img.set_colorkey((0,0,0))
defence_img = pygame.image.load(path.join(img_dir,'denfence.png')).convert()
defence_img = pygame.transform.scale(defence_img,(20,20))
defence_img.set_colorkey((255,255,255))
basketball_img = pygame.image.load(path.join(img_dir,'basketball.png')).convert()
basketball_img = pygame.transform.scale(basketball_img,(70,70))
basketball_img.set_colorkey((255,255,255))

supplements_img = {}
skill_img = pygame.image.load(path.join(img_dir,'skill.png')).convert()
skill_img = pygame.transform.scale(skill_img,(20,20))
skill_img.set_colorkey((0,0,0))
supplements_img['skill'] = skill_img
automissle_img = pygame.image.load(path.join(img_dir,'automissle.png')).convert()
automissle_img = pygame.transform.scale(automissle_img,(20,20))
automissle_img.set_colorkey((0,0,0))
supplements_img['automissle'] = automissle_img
supplements_img['heart'] = heart_img
supplements_img['defence'] = defence_img

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        '''如果需要反转图像用self.image = pygame.transform.flip(player_img,是否左右反转,是否上下翻)'''
        self.image = player[0]
        
        self.rect = self.image.get_rect()#获取精灵位置
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHTH
        self.radius = 20
        # pygame.draw.circle(self.image,self.rect.center,radius=20)
        self.score = 0
        self.lives = 5
        self.defence = 3
        self.skill = 1
        self.is_god = False

        self.is_missle_firing = False
        self.start_missle_time = 0
        self.last_missle_time = 0

        self.last_god_time = 0

    def god_mod(self):
        self.last_god_time = pygame.time.get_ticks()
        self.is_god = True
        self.image = god_ship  

    def change(self):
        now = pygame.time.get_ticks()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.rect.x -=10
        if keystate[pygame.K_RIGHT]:
            self.rect.x +=10
        if self.rect.right >WIDTH:
            self.rect.right =WIDTH
        if self.rect.left <0:
            self.rect.left = 0

        if now - self.last_god_time >5000:
            self.image = player[0]
            self.is_god = False

        if self.is_missle_firing:
            if now - self.start_missle_time < 10000:
                if now - self.last_missle_time>500:
                    missle = auto_missle(self.rect.center)
                    missles.add(missle)
                    self.last_missle_time = now
            else:
                self.is_missle_firing = False

    def fire_missle(self):
        self.is_missle_firing = True
        self.start_missle_time = pygame.time.get_ticks()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = kun[0]
        self.rect = self.image.get_rect()#获取精灵位置
        self.radius = 30
        # pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
        self.rect.x = random.randint(0,WIDTH-self.rect.x)
        self.vy = random.randint(2,5)
        self.vx = random.randint(-3,3)
        self.rect.bottom = 0
        
        self.last_time = pygame.time.get_ticks()#获取运行了时间 毫秒单位
        
    def update(self):
        now = pygame.time.get_ticks()
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right >WIDTH:
            self.vx = -1
        #这两个不能用or连起来  这样会来回鬼畜 因为两个放一起都可以满足导致一直改变速度
        if self.rect.left <0:
            self.vx = 1

        if now - self.last_time >1000:
            for i in range(3):
                self.image = kun[i]

        if self.rect.y > HEIGHTH:#简单判断是否越界，越界进行kill删除，和update写在一起，group同时使用时，可以删除group中对象。
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = kun[0]
        self.image = pygame.transform.scale(self.image,(180,195))
        self.rect = self.image.get_rect()
        self.radius = 90
        self.rect.x = random.randint(0,WIDTH-self.rect.x)
        self.vy = 1
        self.vx = random.randint(-3,3)
        self.rect.bottom = 0
        self.is_appear = False
        self.flag = False
        self.life = 1e+9
        self.last_basketball_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right >WIDTH:
            self.vx = -1
        if self.rect.left <0:
            self.vx = 1

        if self.rect.bottom >HEIGHTH/2:
            self.vy = -1
        if self.rect.top< 0:
            self.vy = 1

        if now - self.last_basketball_time >4000:
            for sp in basketballs: #分裂函数中要有已分裂的限制条件不要无限制分裂，不能和update写一起，因为不是每移动一下就要分裂
                sp.divide()
            bkb = basketball(self.rect.center)
            basketballs.add(bkb)
            self.last_basketball_time = now


    def appear(self,turns):
        self.is_appear = True
        self.rect.x = random.randint(0,WIDTH-self.rect.x)
        self.life = turns
    
    def hide(self):
        global supplements
        drop = supplement(self.rect.center)
        drop.type = 'skill'
        drop.image = supplements_img[drop.type]
        supplements.add(drop)
        self.is_appear = False    
        self.rect.bottom = 0
        self.life = 1e+9
        self.flag = False

class basketball(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.image = basketball_img
        self.image_copy = self.image.copy()
        self.rect = self.image.get_rect()
        self.vy = random.randint(4,6)
        self.vx = random.randint(-5,5)
        self.radius = 70
        self.rect.center = center
        self.last_divide_time = 0
        self.can_divide = True

        # self.last_rotate_time = pygame.time.get_ticks()
        # self.rotate_speed = random.randint(-5,5)
        # self.rotate_angle = 0  #旋转和分裂无法并存

    def update(self):
        self.rect.y +=self.vy
        self.rect.x +=self.vx

        if self.rect.right >WIDTH:
            self.vx = -3
        if self.rect.left <0:
            self.vx = 3

        if self.rect.bottom >HEIGHTH:
            self.vy = -3
        if self.rect.top< 0:
            self.vy = 3

        # self.rotate()


    def divide(self):
        now = pygame.time.get_ticks()
        if now-self.last_divide_time > 10000 and self.can_divide:
            self.image = pygame.transform.scale(self.image,(35,35))
            self.radius = 35
            divides = basketball(self.rect.center)
            divides.image = self.image.copy()
            divides.radius = 35
            divides.can_divide = False
            basketballs.add(divides)
            self.can_divide = False
            self.last_divide_time = now

    # def rotate(self):
    #     nows = pygame.time.get_ticks()
    #     if nows - self.last_rotate_time >30:
            # old_center = self.rect.center
            # self.rotate_angle = (self.rotate_angle + self.rotate_speed ) % 360
            # self.image = pygame.transform.rotate(self.image_copy,self.rotate_angle)
            # self.rect = self.image.get_rect()
            # self.rect_center = old_center
            # self.last_rotate_time = nows           

class bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ammos[15]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
    def update(self):
        self.rect.y -=10

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion[0]
        self.rect = self.image.get_rect()
        self.rect.center=center
        self.frame = 0
        self.last_time = pygame.time.get_ticks()
    def update(self):
        explosion_sound.play()
        now = pygame.time.get_ticks()
        if now - self.last_time >50:
            if self.frame < len(explosion):
                self.image = explosion[self.frame]
                self.frame += 1
            else:
                self.kill()

class supplement(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        random_num = random.random()
        if random_num < 0.5:
            self.type = 'automissle'
        elif random_num < 0.8:
            self.type = 'defence'
        else:
            self.type = 'heart'
        self.image = supplements_img[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rect.y += 5

class auto_missle(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(ammos)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rect.y-=5
        
def draw_text(text, surface, color, font_size, x, y):
    font = pygame.font.Font(path.join(font_dir,'SourceHanSansKR-Normal.otf'),font_size)
    text_surface = font.render(str(text),True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface,text_rect)

def draw_ui():
    draw_text(f'第{turns}波'+' '*40+'socre: '+str(player1.score),screen,(255,255,255),20,WIDTH/2,20)

    heart_img_rect = heart_img.get_rect()
    heart_img_rect.right = WIDTH - 10
    heart_img_rect.top = 20

    defence_img_rect = defence_img.get_rect()
    defence_img_rect.right = WIDTH - 10
    defence_img_rect.top = 50

    skill_img_rect = skill_img.get_rect()
    skill_img_rect.right = WIDTH - 10
    skill_img_rect.top = 80

    for _ in range(player1.lives):
        screen.blit(heart_img, heart_img_rect)
        heart_img_rect.x -= heart_img_rect.width + 10

    for _ in range(player1.defence):
        screen.blit(defence_img,defence_img_rect)
        defence_img_rect.x -= defence_img_rect.width + 10

    for _ in range(player1.skill):
        screen.blit(skill_img,skill_img_rect)
        skill_img_rect.x -= skill_img_rect.width + 10

# def dies(scores):
#     global score,game_state
#     score = scores
#     game_state = 2

def show_menu():
    global game_state,screen
    screen.blit(background,background_rect)

    draw_text('新飞机大战',screen,(255,0,0),70, WIDTH/2, 150)
    draw_text('press space to start',screen,(255,0,0),25, WIDTH/2, 300)
    elist = pygame.event.get()
    for e in elist:
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if e.key == pygame.K_SPACE:
                game_state = 1
    pygame.display.flip()

# def show_score():
#     global game_state,screen,score
#     screen.blit(background,background_rect)
#     draw_text(" 得分：" + str(score)+"  press space to restart",screen,(0,255,0),30,WIDTH/2,300)
#     elist = pygame.event.get()
#     for e in elist:
#         if e.type == pygame.QUIT:
#             pygame.quit()
#             quit()
#         if e.type == pygame.KEYDOWN:
#             if e.key == pygame.K_ESCAPE:
#                 pygame.quit()
#                 quit()
#             if e.key == pygame.K_SPACE:
#                 game_state = 1
#     pygame.display.flip()

game_state = 0#0:menu 1:game 2:restart
player1 = Player()
boss = Boss()
enmeys = pygame.sprite.Group()
bus = pygame.sprite.Group()
exp = pygame.sprite.Group()
missles = pygame.sprite.Group()
supplements = pygame.sprite.Group()
basketballs = pygame.sprite.Group()

for i in range(20):
    enmey = Enemy()
    enmeys.add(enmey)
    
while not gameover:
    clock.tick(0)  #最大帧数60
    if game_state == 0:
        show_menu()
    # elif game_state == 2:
    #     show_score()
    else:
        screen.fill ((255,255,255))
        elist = pygame.event.get()
        for e in elist:
            if e.type == pygame.QUIT:
                gameover = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    gameover = True
                if e.key == pygame.K_SPACE:
                    bu = bullet(player1.rect.centerx,player1.rect.centery)
                    shoot_sound.play()
                    bus.add(bu)
                if e.key == pygame.K_n:    
                    for i in range(20):
                        enmey = Enemy()
                        enmeys.add(enmey)
                if e.key == pygame.K_v:
                    skill_sound.play()
                    if player1.skill > 0:
                        for k in range(21):
                            skillbullet = bullet(50*k+30,HEIGHTH)
                            skillbullet.image = ammos[k]
                            bus.add(skillbullet)
                        player1.skill-=1
                # if e.unicode:#传入值不是方向键为空
                #     try:
                #         '''换皮肤'''
                #         player1.image = player[int(e.unicode)-1]
                #     except:#不是字母或者超过列表的数字
                #         pass
        player1.change()
        
        bus.update()
        enmeys.update()
        exp.update()
        missles.update()
        supplements.update()
        basketballs.update()

        hits_bullets = pygame.sprite.groupcollide(enmeys,bus,True,True)#第一个True表示要删第一个组成员，第二个是要删第二个组成员
        hits_missles = pygame.sprite.groupcollide(enmeys,missles,True,True)
        hits = {}#group 和 group 之间可以这样简化
        hits.update(hits_bullets)
        hits.update(hits_missles)
        for hit in hits:
            exps = Explosion(hit.rect.center)
            exp.add(exps)
            player1.score +=1
            if random.random() > 0.9:
                supplement1 = supplement(hit.rect.center)
                supplements.add(supplement1)
        # print("剩余敌人个数：",len(enmeys))
        if boss.is_appear:
            boss.update()
             
        pygame.sprite.groupcollide(bus,basketballs,True,True)
        pygame.sprite.groupcollide(missles,basketballs,True,True)
        hits = pygame.sprite.spritecollide(player1,supplements,True,pygame.sprite.collide_circle)
        '''spiritecollide 精灵和组之间判定 会返回组对象 可以遍历获取组内精灵的属性'''
        for hit in hits:
            supplement_sound.play()
            if hit.type == 'heart':
                player1.lives += 1
                if player1.lives >8:
                    player1.lives = 8
            elif hit.type == 'defence':
                player1.defence += 1
                if player1.defence > 5:
                    player1.defence = 5
            elif hit.type == 'automissle':
                player1.fire_missle()
            elif hit.type == 'skill':
                player1.skill += 1
                if player1.skill >3:
                    player1.skill = 3


        # pygame.sprite.spritecollide(player1,enmeys,False,pygame.sprite.collide_rect_ratio(0.7)) 0.7比例缩小检测框，未碰撞返回false
        hit_basketball =pygame.sprite.spritecollide(player1,basketballs,True,pygame.sprite.collide_circle)
        hit_enmeys = pygame.sprite.spritecollide(player1,enmeys,True,pygame.sprite.collide_circle)#False表示，碰上后不删敌人
        if hit_basketball or hit_enmeys:
            hurts_sound.play()
            if player1.defence > 0:
                player1.defence -= 1
                if player1.defence == 0:
                    print('you are god now')
                    player1.god_mod()
            elif not player1.is_god:
                player1.lives -=1
            if player1.lives <=0:
                pygame.time.wait(100)
                gameover = True
                # dies(player1.score)

        hit_boss_bus = pygame.sprite.spritecollide(boss,bus,True,pygame.sprite.collide_circle)
        hit_boss_missle = pygame.sprite.spritecollide(boss,missles,True,pygame.sprite.collide_circle)
        if hit_boss_bus or hit_boss_missle:
            if boss.is_appear:
                boss_hurts_sound.play()
            boss.life -=1
            if boss.life <=0:
                boss.hide()
                for e in basketballs:
                    basketballs.remove(e)#boss死了，他的篮球也得没
                player1.score += turns
                turns +=1

        if turns % 10 != 0:    
            '''每10波一个boss'''
            if len(enmeys)<12:#少于12个敌人补充
                for i in range(20):
                    enmey = Enemy()
                    enmeys.add(enmey)
                turns +=1
        elif len(enmeys) == 0 and not boss.flag:
            boss.appear(turns)
            boss.flag = True
   
        
        screen.blit(background,background_rect)
        screen.blit(player1.image,player1.rect)#让player1这个图片在screen上方。不要被screen遮挡，也可以设置player在enemy上方
        screen.blit(boss.image,boss.rect)

        enmeys.draw(screen)
        bus.draw(screen)
        exp.draw(screen)
        supplements.draw(screen)
        missles.draw(screen)
        basketballs.draw(screen)
        draw_ui()
        pygame.display.flip()

#screen.blit()画背景图片不能放在主循环外，因为主循环有个screen.fill(白色) 但如果没有填充白色，精灵移动会残留颜色，所以画背景也放在循环内
#所有调整位置都是先get_rect()获取位置 然后再对得到的位置赋值进行调整   rect.midtop rect.bottom 9个的点选一个改即可
#所有要控制时间的都写在update里面，因为要一直调用，单独写一个函数里面搞个时间条件是没用的，因为只调用了一次