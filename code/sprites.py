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
        self.speed=20
        self.spawn_time=pygame.time.get_ticks()
        if flip: self.direction=pygame.Vector2(-1,0) 
        else: self.direction=pygame.Vector2(1,0)
        self.mask=pygame.mask.from_surface(self.image)

    
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
        self.animation_speed=0.1
        self.amplitude=randint(5,15)
        self.frequency=randint(400,600)
        self.speed=randint(2,7)
        self.mask=pygame.mask.from_surface(self.image)
        self.death_timer=Timer(1000, func=self.kill)

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
        self.animation_speed=0.1
        self.direction=pygame.Vector2(1,0)
        self.speed=randint(2,7)
        self.mask=pygame.mask.from_surface(self.image)
        self.timer=Timer(1000,func=self.kill)

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

        
        