import pygame
from os.path import join
from sprites import *
from timers import *

class Player(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups, collide_group, bullet_group, enemy_group,safezone):
        super().__init__(groups)
        self.groups=groups
        self.safezone_rect=safezone
        self.lives=5
        self.pos=pos
        self.bullet_group=bullet_group
        self.enemy_sprites=enemy_group
        self.collision_sprites=collide_group
        self.frames=frames
        self.frame_index=0
        self.image=self.frames[self.frame_index]
        self.rect=self.image.get_frect(center=pos)
        self.hitbox_rect=self.rect.inflate(-30,0)
        self.direction=pygame.Vector2(0,0)
        self.player_gravity=25
        self.animation_speed=10
        self.speed=600
        self.able_to_jump=False
        self.in_air=True
        self.flip=False
        self.mask=pygame.mask.from_surface(self.image)
        self.death_timer=Timer(500, func=self.respawn)
        self.alive=True
        self.death_sound=pygame.mixer.Sound(join("audio", "death.ogg"))

        #timers
        self.shoot_timer=Timer(500)

    def __bool__(self):
        return self.alive

    def input(self):
        keys=pygame.key.get_pressed()
        self.direction.x=int(keys[pygame.K_d]) - int(keys[pygame.K_a])

        if pygame.key.get_just_pressed()[pygame.K_w] and self.able_to_jump:
            self.direction.y=-12
            self.able_to_jump=False
            self.in_air=True
        
        if pygame.mouse.get_pressed()[0] and not self.shoot_timer:
                Bullet(self.hitbox_rect.center, (self.groups,self.bullet_group), self.flip)
                Fire(self.groups,self)
                self.shoot_timer.activate()


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
            self.frame_index+=self.animation_speed*dt
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

    def check_enemy_collision(self):
        collided=pygame.sprite.spritecollide(self, self.enemy_sprites, False, pygame.sprite.collide_mask)
        if collided:
            self.death_sound.play()
            self.destroy()

    def destroy(self):
        self.death_timer.activate()
        self.lives-=1
        self.speed=0

    def respawn(self):
        self.hitbox_rect.center=self.pos
        self.rect.center=self.hitbox_rect.center
        self.speed=600
        if self.lives<0:
            self.alive=False

    def check_lives(self):
        return self.lives


    def update(self,dt):
        self.shoot_timer.update()
        self.death_timer.update()
        if not self.death_timer:
            if not self.safezone_rect.contains(self.hitbox_rect):
                self.check_enemy_collision()
            self.animate(dt)
            self.input()
            self.move(dt)
        else:
            self.image = pygame.mask.from_surface(self.frames[0]).to_surface()
            self.image.set_colorkey((0, 0, 0))
        

