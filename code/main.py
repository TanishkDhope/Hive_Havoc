import pygame
from os.path import join
from settings import *
from player import *
from sprites import *
from groups import *
from pytmx.util_pygame import load_pygame
from timers import *
from random import randint


class Game:
    def __init__(self):
        pygame.init()
        self.clock=pygame.time.Clock()
        self.running=True
        self.display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("Gravity Shards")
        self.score=0


        #timers
        self.bee_timer=Timer(1000, func=self.create_bee, repeat=True, autostart=True)

        #sprites
        self.all_sprites=AllSprites()
        self.collision_sprites=pygame.sprite.Group()
        self.Bullet_sprites=pygame.sprite.Group()
        self.enemy_sprites=pygame.sprite.Group()

        #setup
        self.load_images()
        self.setup()

       #sounds
        self.death_sound=pygame.mixer.Sound(join("audio","impact.ogg"))
        self.music=pygame.mixer.Sound(join("audio","music.wav")).play(loops=-1)

        #Important rect
        self.safezone_rect=None

        #GUI Elements
        self.hearts=GUI(self.heart_frames,(130,50),self.all_sprites,self.player)

        #Fonts
        self.dragon_hunter=pygame.font.Font(join("fonts","dragonHunter","font.otf"), 36)
        self.pixel=pygame.font.Font(join("fonts", "Pixel", "font.ttf"),45)

        #text
        self.score_text=Text(self.display_surface, (1100,40), self.pixel, "X 000", "#3C362A")
        
        

    def setup(self):
        map=load_pygame(join("data", "maps", "world.tmx"))
        self.map_width=map.width*TILE_SIZE
        self.map_height=map.height*TILE_SIZE

        for x,y,image in map.get_layer_by_name("Main").tiles():
            Sprite(image, (x*TILE_SIZE,y*TILE_SIZE), (self.all_sprites,self.collision_sprites))

        for x,y,image in map.get_layer_by_name("Decoration").tiles():
            Collision_sprites(image, (x*TILE_SIZE,y*TILE_SIZE), self.all_sprites)
        
        for zone in map.get_layer_by_name("Zones"):
            if zone.name=="SafeZone":
                self.safezone_rect=pygame.FRect(zone.x,zone.y,zone.width,zone.height)


        for obj in map.get_layer_by_name("Entities"):
            
            if obj.name=="Player":
                self.player=Player(self.player_frames,(obj.x,obj.y),self.all_sprites, self.collision_sprites, self.Bullet_sprites,self.enemy_sprites,self.safezone_rect)
            if obj.name=="Worm":
                self.create_worm(obj)


    def load_images(self):
        self.bee_frames=[pygame.image.load(join("graphics","enemies","bee",f"{image}.png")).convert_alpha() for image in range(2)]
        self.worm_frames=[pygame.image.load(join("graphics","enemies","worm",f"{image}.png")).convert_alpha() for image in range(2)]
        self.player_frames=[pygame.image.load(join("graphics","player",f"{image}.png")).convert_alpha() for image in range(3)]
        self.heart_frames=[pygame.image.load(join("graphics","icons",f"tile00{image}.png")).convert_alpha() for image in range(6)]

    def create_bee(self):
        pos=(randint(WINDOW_WIDTH,self.map_width),randint(0,self.map_height))
        Bee(self.bee_frames,pos,(self.all_sprites,self.enemy_sprites))
    def create_worm(self,obj):
        Worm(self.worm_frames, pygame.FRect(obj.x,obj.y,obj.width,obj.height), (self.all_sprites,self.enemy_sprites))

    def check_collision(self):
        for bullet in self.Bullet_sprites:
            collided=pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if collided: 
                self.death_sound.play()
                bullet.kill()
                for sprite in collided:
                    if isinstance(sprite, Worm):
                        self.score+=10
                    else:
                        self.score+=20
                    sprite.destroy()

    def run(self): 
        #dt

        #event loop
        while self.running:
            dt=self.clock.tick(FRAMERATE)/1000
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False


            self.display_surface.fill("#fcdfcd")

            #UPDATE
            self.all_sprites.update(dt)
            self.check_collision()


            #timer
            self.bee_timer.update()

            #DRAW
            self.all_sprites.draw(self.display_surface, self.player.rect.center)
            self.score_text.draw(self.score)

             #check_player_alive
            if not self.player:
                self.running=False
            
            pygame.display.update()
        pygame.quit()
 

if __name__=="__main__":
    game=Game()
    game.run()

    