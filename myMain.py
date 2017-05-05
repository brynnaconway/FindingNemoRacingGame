import pygame, os, sys, math, time

class Background(pygame.sprite.Sprite):
    def __init__(self, gs): 
        pygame.sprite.Sprite.__init__(self)
        self.ocean, self.rect = load_image("ocean_scene.png")

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_name, timemax, time_start): 
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_name)
        self.rect = self.rect.move(600, 10)
        self.time = time_start
        self.time_max = timemax
        self.orig_image = self.image
        self.count = 0

    def tick(self):
        if self.time == self.time_max:
            if self.count < 32: 
                self.rect = self.rect.move(0, 5)
                self.count += 1
            elif self.count == 64:
                self.time = 0
                self.count = 0
            else: 
                self.rect = self.rect.move(0, -5)
        self.time += 1

class Nemo(pygame.sprite.Sprite):
    def __init__(self, gs): 
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.nemo, self.rect = load_image("nemo_sprite.png")
        self.orig_nemo = self.nemo
        self.rect = self.rect.move(55, 35)
        self.gs = gs

    def tick(self): 
        '''move the deathstar with the mouse'''
        xpos, ypos = pygame.mouse.get_pos() 
        x, y = self.rect.center
        rotation = -1 * float(math.degrees(math.atan2(float(ypos-y), float(xpos-x))))
        xcenter, ycenter = self.rect.center
        rotate = pygame.transform.rotate
        #self.nemo = rotate(self.orig_nemo, rotation)
        #self.rect = self.nemo.get_rect(center=(xcenter, ycenter))
		#self.rect = self.rect.move(4, 0)
		#self.rect = self.rect.move(0, ydir*4)

    def move(self, event_key):
        xpos, ypos = pygame.mouse.get_pos() 
        x, y = self.rect.center
        xdir = 0
        ydir = 0
        self.nemo = self.orig_nemo
        if event_key == pygame.K_RIGHT: 
            xdir = 1
        #elif event_key == pygame.K_LEFT: 
         #   xdir = -1
        elif event_key == pygame.K_UP:
            if self.rect.y + self.nemo.get_height() > 110:
                ydir = -1
                #self.nemo = pygame.transform.rotate(self.orig_nemo, 10)
        elif event_key == pygame.K_DOWN:
            if self.rect.y + self.nemo.get_height() < 334:
                ydir = 1 
                #self.nemo = pygame.transform.rotate(self.orig_nemo, -10)
        if self.rect.y + self.nemo.get_height() > 300:
            self.rect = self.rect.move(xdir*3, ydir*3)
        else:
            self.rect = self.rect.move(xdir*10, ydir*10)
        #self.rect = self.rect.move(0, ydir*4)

class GameSpace: 
    def main(self): 
        pygame.init()
        self.size = self.width, self.height = 1400, 664
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        pygame.mouse.set_visible(True)

        self.shark = Enemy("shark.png", 600, 500)
        self.player = Nemo(self)
        self.top_background = Background(self)
        self.bottom_background = Background(self)
        pygame.key.set_repeat(500, 30)
        self.clock = pygame.time.Clock()

        while 1:  
            self.clock.tick(60) # clock tick regulation
            #self.screen.fill(self.black)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    return         
                if event.type == pygame.KEYDOWN: 
                    self.player.move(event.key)
            self.player.tick()
            self.screen.blit(pygame.transform.scale(self.top_background.ocean, (1400, 330)), self.top_background.rect)
            self.screen.blit(pygame.transform.scale(self.bottom_background.ocean, (1400, 330)), self.bottom_background.rect.move(0, 334))
            self.screen.blit(self.player.nemo, self.player.rect)
            self.screen.blit(pygame.transform.scale(self.shark.image, (70, 70)), self.shark.rect)
            pygame.display.flip()

def load_image(image_name):
    PATH = "Sprites/"
    FULL_PATH = PATH + image_name
    try: 
        image = pygame.image.load(FULL_PATH)
    except pygame.error:
        print("Cannot load image:", FULL_PATH)
        raise SystemExit 
    return image, image.get_rect()

if __name__ == "__main__": 
    gs = GameSpace() 
    gs.main()
