import pygame
from os.path import join
from settings import *
from player import *
from sprites import *
from groups import *
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        pygame.init()
        self.clock=pygame.time.Clock()
        self.running=True
        self.display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("Gravity Shards")

        #timers

        #sprites
        self.all_sprites=AllSprites()
        self.collision_sprites=pygame.sprite.Group()
        self.Bullet_sprites=pygame.sprite.Group()

        #setup
        self.setup()
        
        

    def setup(self):
        map=load_pygame(join("data", "maps", "world.tmx"))

        for x,y,image in map.get_layer_by_name("Main").tiles():
            Sprite(image, (x*TILE_SIZE,y*TILE_SIZE), (self.all_sprites,self.collision_sprites))

        for x,y,image in map.get_layer_by_name("Decoration").tiles():
            Collision_sprites(image, (x*TILE_SIZE,y*TILE_SIZE), self.all_sprites)

        for obj in map.get_layer_by_name("Entities"):
            if obj.name=="Player":
                self.player=Player((obj.x,obj.y),self.all_sprites, self.collision_sprites)

       



    def run(self): 
        #dt
        dt=self.clock.tick(FRAMERATE)/1000

        #event loop
        while self.running:

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False


            self.display_surface.fill("#fcdfcd")

            #UPDATE
            self.all_sprites.update(dt)


            #DRAW
            self.all_sprites.draw(self.display_surface, self.player.rect.center)

             
            pygame.display.update()
        pygame.quit()
 

if __name__=="__main__":
    game=Game()
    game.run()

