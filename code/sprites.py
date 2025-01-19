import pygame
from os.path import join
from timers import *
from math import sin
from random import randint


class Sprite(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(topleft=pos)
        self.ground=True


class GUI(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups,player):
        super().__init__(groups)
        self.player=player
        self.frame_index=0
        self.frames=frames
        self.image=self.frames[self.frame_index]
        self.rect=self.image.get_frect(center=pos)
        self.gui=True
        self.mask=pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.lives=self.player.check_lives()
        self.frame_index=5-self.lives
        self.image=self.frames[self.frame_index]

        

class Collision_sprites(pygame.sprite.Sprite):
    def __init__(self, image, pos, groups):
        super().__init__(groups)
        self.image=image
        self.rect=self.image.get_frect(topleft=pos)
        
class Bullet(pygame.sprite.Sprite):

    def __init__(self,pos,groups,flip):
        super().__init__(groups)
        self.image=pygame.image.load(join("graphics", "gun", "bullet.png")).convert_alpha()
        self.image=pygame.transform.rotozoom(self.image, 0, 0.7)
        self.image=pygame.transform.flip(self.image,flip,False)
        self.rect=self.image.get_rect(center=(pos[0]+10,pos[1]+15))
        self.speed=1000
        self.spawn_time=pygame.time.get_ticks()
        if flip: self.direction=pygame.Vector2(-1,0) 
        else: self.direction=pygame.Vector2(1,0)
        self.mask=pygame.mask.from_surface(self.image)
        self.shoot_sound=pygame.mixer.Sound(join("audio","shoot.wav")).play()


    
    def destroy(self):
        current_time=pygame.time.get_ticks()
        if current_time-self.spawn_time>=1000:
            self.kill()

    
    def update(self,dt):
        self.destroy()
        self.rect.center+=self.direction*self.speed*dt

class Fire(pygame.sprite.Sprite):
    
    def __init__(self,groups,player):
        super().__init__(groups)
        self.player=player
        self.player_pos=player.rect.center
        self.og_image=pygame.image.load(join("graphics", "gun", "fire.png")).convert_alpha()
        self.og_image=pygame.transform.rotozoom(self.og_image, 0, 0.8)
        self.y_offset=pygame.Vector2(0,8)
        self.image=self.og_image
        self.flip_image=pygame.transform.flip(self.og_image, True, False)
        self.rect=self.image.get_rect(midleft=self.player.rect.midright)
        self.spawn_time=pygame.time.get_ticks()
        self.bullet_timer=Timer(duration=200, autostart=True)

        if self.player.flip:
            self.rect.midright=self.player.rect.midleft+self.y_offset
            self.image=self.flip_image
        else:
            self.rect.midleft=self.player.rect.midright+self.y_offset


    
    def update(self,dt):
        self.bullet_timer.update()
        if not self.bullet_timer.active:
            self.kill()
        
        if self.player.flip:
            self.rect.midright=self.player.rect.midleft+self.y_offset
            self.image=self.flip_image
        else:
            self.rect.midleft=self.player.rect.midright+self.y_offset
            self.image=self.og_image


class Bee(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups):
        super().__init__(groups)
        self.frames=frames
        self.frame_index=0
        self.image=self.frames[self.frame_index]
        self.rect=self.image.get_frect(center=pos)
        self.animation_speed=10
        self.amplitude=randint(50,100)
        self.frequency=randint(1000,4000)
        self.speed=randint(200,400)
        self.mask=pygame.mask.from_surface(self.image)
        self.death_timer=Timer(500, func=self.kill)

    def move(self,dt):
        self.rect.centerx-=self.speed*dt
        self.rect.y+=sin(pygame.time.get_ticks()/self.frequency)*self.amplitude*dt
        if self.rect.centerx<=-600:
            self.kill()
            
    def destroy(self):
        self.death_timer.activate()
        self.image=pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey("black")

    def animate(self,dt):
        self.frame_index+=self.animation_speed*dt
        self.image=self.frames[int(self.frame_index)% len(self.frames)]
    
    def update(self,dt):
        self.death_timer.update()
        if not self.death_timer:
            self.animate(dt)
            self.move(dt)

class Worm(pygame.sprite.Sprite):
    def __init__(self,frames,rect,groups):
        super().__init__(groups)
        self.frames=frames
        self.main_rect=rect
        self.frame_index=0
        self.image=self.frames[self.frame_index]
        self.rect=self.image.get_frect(bottomleft=rect.bottomleft)
        self.animation_speed=3
        self.direction=pygame.Vector2(1,0)
        self.speed=randint(70,95)
        self.mask=pygame.mask.from_surface(self.image)
        self.timer=Timer(500,func=self.kill)

    def destroy(self):
        self.timer.activate()
        self.image=pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey("black")
    


    def move(self,dt):
        self.rect.center+=self.direction*self.speed*dt
        if not self.main_rect.contains(self.rect):
            self.direction*=-1
            self.frames=[pygame.transform.flip(image,True, False) for image in self.frames]
    
       
    def animate(self,dt):
        self.frame_index+=self.animation_speed*dt
        self.image=self.frames[int(self.frame_index)% len(self.frames)]
    
    def update(self,dt):
        self.timer.update()
        if not self.timer:
            self.move(dt)
            self.animate(dt)

class Text():
    def __init__(self,display_surface,pos,font,text,color):
        self.display_surface=display_surface
        self.pos=pos
        self.font=font
        self.color=color
    
    def draw(self,score):
        self.text_surf=self.font.render(f"X {score}", True, self.color)
        self.display_surface.blit(self.text_surf, self.pos)
