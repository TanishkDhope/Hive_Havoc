import pygame
from os.path import join


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
        self.speed=15
        self.spawn_time=pygame.time.get_ticks()
        if flip: self.direction=pygame.Vector2(-1,0) 
        else: self.direction=pygame.Vector2(1,0)
    
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
        self.image=pygame.image.load(join("graphics", "gun", "fire.png")).convert_alpha()
        self.image=pygame.transform.rotozoom(self.image, 0, 0.7)
        self.image=pygame.transform.flip(self.image,self.player.flip,False)
        self.offset=pygame.Vector2(60,10)
        self.rect=self.image.get_rect(center=self.player_pos+self.offset)
        self.spawn_time=pygame.time.get_ticks()
    
    def destroy(self):
        current_time=pygame.time.get_ticks()
        self.rect=self.image.get_rect(center=self.player_pos+self.offset)

        if current_time-self.spawn_time>=100:
            self.kill()

    
    def update(self,dt):
        self.destroy()
       
    