import pygame
from os.path import join
from sprites import *


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups, collide_group):
        super().__init__(groups)
        self.groups=groups
        self.collision_sprites=collide_group
        self.frames=[]
        self.frame_index=0
        self.init_char()
        self.rect=self.image.get_frect(center=pos)
        self.hitbox_rect=self.rect.inflate(-30,0)
        self.direction=pygame.Vector2(0,0)
        self.player_gravity=0.05
        self.speed=8
        self.able_to_jump=False
        self.in_air=True
        self.flip=False

    def init_char(self):
        self.frames=[pygame.image.load(join("graphics","player",f"{image}.png")).convert_alpha() for image in range(3)]
        self.frame_index=0
        self.image=self.frames[self.frame_index]

    def input(self):
        keys=pygame.key.get_pressed()
        self.direction.x=int(keys[pygame.K_d]) - int(keys[pygame.K_a])

        if pygame.key.get_just_pressed()[pygame.K_w] and self.able_to_jump:
            self.direction.y=-1.25
            self.able_to_jump=False
            self.in_air=True
        
        if pygame.mouse.get_just_pressed()[0]:
            Bullet(self.hitbox_rect.center, self.groups, self.flip)
            Fire(self.groups,self)

    def move(self,dt):
        self.hitbox_rect.centerx+=self.direction.x*self.speed*dt
        self.check_collision("x")
        if self.direction.x<0:
            self.flip=True
        elif self.direction.x>0:
            self.flip=False

        #vertical Movement
        self.direction.y+=self.player_gravity*dt
        self.hitbox_rect.y+=self.direction.y
        self.check_collision("y")
        self.rect.center=self.hitbox_rect.center

    def animate(self,dt):
        if self.direction.x !=0 and not self.in_air:
            self.frame_index+=0.15*dt
            self.image=self.frames[int(self.frame_index) % len(self.frames)]
            self.image=pygame.transform.flip(self.image, self.flip, False)
        else:
            self.frame_index=0
            self.image=self.frames[int(self.frame_index) % len(self.frames)]
            self.image=pygame.transform.flip(self.image, self.flip, False)
        
        if self.in_air:
            self.frame_index=1
            self.image=self.frames[int(self.frame_index) % len(self.frames)]
            self.image=pygame.transform.flip(self.image, self.flip, False)
        
    def check_collision(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction=="x":
                    if self.direction.x>0:
                        self.hitbox_rect.right=sprite.rect.left
                    elif self.direction.x<0:
                        self.hitbox_rect.left=sprite.rect.right

                elif direction=="y":
                    if self.direction.y>0:
                        self.direction.y=0
                        self.able_to_jump=True
                        self.in_air=False
                        self.hitbox_rect.bottom=sprite.rect.top
                    else:
                        self.hitbox_rect.top=sprite.rect.bottom
                        self.direction.y=0

    

    def update(self,dt):
        self.animate(dt)
        self.input()
        self.move(dt)
