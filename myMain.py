import pygame, os, sys, math, time

class Background(pygame.sprite.Sprite):
    def __init__(self, gs): 
        pygame.sprite.Sprite.__init__(self)
        self.ocean, self.rect = load_image("ocean_scene.png")

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_name, timemax, time_start, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_name)
        self.rect = self.rect.move(x, y)
        self.orig_rect = self.rect
        self.time = time_start
        self.time_max = timemax
        self.orig_image = self.image
        self.count = 0

    def tick(self):
        if self.time == self.time_max:
            if self.count < 78: 
                self.rect = self.rect.move(0, 4)
                self.count += 1
            elif self.rect.y <= self.orig_rect.y:
                self.time = 0
                self.count = 0
            else: 
                self.rect = self.rect.move(0, -4)
        else:
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
            if self.rect.x +self.nemo.get_width() < 1370:
                xdir = 1
        #elif event_key == pygame.K_LEFT: 
         #   xdir = -1
        elif event_key == pygame.K_UP:
            if self.rect.y + self.nemo.get_height() > 95:
                ydir = -1
                #self.nemo = pygame.transform.rotate(self.orig_nemo, 10)
        elif event_key == pygame.K_DOWN:
            if self.rect.y + self.nemo.get_height() < 337:
                ydir = 1 
                #self.nemo = pygame.transform.rotate(self.orig_nemo, -10)
        if self.gs.crush.gofast == 1:
            self.rect = self.rect.move(xdir*25, ydir*25)
        elif self.rect.y + self.nemo.get_height() > 300:
            self.rect = self.rect.move(xdir*3, ydir*3)
        else:
            self.rect = self.rect.move(xdir*10, ydir*10)
        #self.rect = self.rect.move(0, ydir*4)

class Crush(pygame.sprite.Sprite):
    def __init__(self, gs): 
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.crush, self.rect = load_image("crush.png")
        self.orig_crush = self.crush
        self.rect = self.rect.move(900, 5)
        self.gs = gs
        self.gofast = 0 

    def tick(self): 
        if self.rect.colliderect(self.gs.player.rect):
            self.gofast = 1;

    def move(self, event_key):
        xpos, ypos = pygame.mouse.get_pos() 
        x, y = self.rect.center
        xdir = 0
        ydir = 0
        self.crush = self.orig_crush
        if event_key == pygame.K_RIGHT: 
            xdir = 1
        elif event_key == pygame.K_UP:
            if self.rect.y + self.gs.player.nemo.get_height() > 110:
                ydir = -1
                #self.nemo = pygame.transform.rotate(self.orig_nemo, 10)
        elif event_key == pygame.K_DOWN:
            if self.rect.y + self.gs.player.nemo.get_height() < 334:
                ydir = 1 
                #self.nemo = pygame.transform.rotate(self.orig_nemo, -10)
        if self.gs.crush.gofast == 1:
            self.rect = self.rect.move(xdir*22, ydir*22)
        elif self.rect.y + self.gs.nemo.get_height() > 300:
            self.rect = self.rect.move(xdir*3, ydir*3)
        else:
            self.rect = self.rect.move(xdir*10, ydir*10)

class Home(pygame.sprite.Sprite):
    def __init__(self, gs): 
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.home, self.rect = load_image("home.png")
        self.orig_home = self.home
        self.rect = self.rect.move(1250, 175)
        self.gs = gs


class GameSpace: 
    def main(self): 
        pygame.init()
        self.size = self.width, self.height = 1400, 664
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        pygame.mouse.set_visible(True)

        self.shark = Enemy("shark.png", 60, 50, 600, -124)
        self.jelly = Enemy("jellyfish_sprite.png", 60, 40, 150, -150)
        self.player = Nemo(self)
        self.top_background = Background(self)
        self.bottom_background = Background(self)
        self.crush = Crush(self)
        self.home = Home(self)
        pygame.key.set_repeat(500, 30)
        self.clock = pygame.time.Clock()

        while 1:  
            self.clock.tick(60) # clock tick regulation
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    return         
                if event.type == pygame.KEYDOWN:
                    if self.crush.gofast == 1:
                        self.player.move(event.key)
                        self.crush.move(event.key)
                    else: 
                        self.player.move(event.key)
            self.player.tick()
            if self.player.rect.colliderect(self.shark.rect):
                self.player = Nemo(self)
                self.player.tick()
            self.crush.tick()
            self.shark.tick()
            self.jelly.tick()
            self.screen.blit(pygame.transform.scale(self.top_background.ocean, (1400, 330)), self.top_background.rect)
            self.screen.blit(pygame.transform.scale(self.bottom_background.ocean, (1400, 330)), self.bottom_background.rect.move(0, 334))
            self.screen.blit(self.crush.crush, self.crush.rect)
            self.screen.blit(self.player.nemo, self.player.rect)
            self.screen.blit(self.home.home, self.home.rect)
            self.screen.blit(pygame.transform.scale(self.shark.image, (130, 130)), self.shark.rect)
            self.screen.blit(pygame.transform.scale(self.jelly.image, (130, 130)), self.jelly.rect)
            #self.screen.blit(pygame.transform.scale(self.crush.crush, (215, 117)), self.crush.rect)
            
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

def load_sound(name): 
    PATH = "~/paradigms/deathstar/"
    class NoneSound: 
        def play(self): pass
    if not pygame.mixer: 
        return NoneSound()
    FULL_PATH = PATH + name
    try: 
        sound = pygame.mixer.Sound(FULL_PATH)
    except pygame.error: 
        print("Cannot load sound: ", pygame.wav)
        raise SystemExit 
    return sound


if __name__ == "__main__": 
    gs = GameSpace() 
    gs.main()
