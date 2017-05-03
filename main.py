import pygame, os, sys, math, time

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
        elif event_key == pygame.K_LEFT: 
            xdir = -1
        elif event_key == pygame.K_UP:
            ydir = -1
            self.nemo = pygame.transform.rotate(self.orig_nemo, 20)
        elif event_key == pygame.K_DOWN:
            ydir = 1 
            self.nemo = pygame.transform.rotate(self.orig_nemo, -20)
        self.rect = self.rect.move(xdir*4, ydir*4)
        #self.rect = self.rect.move(0, ydir*4)

class GameSpace: 
    def main(self): 
        pygame.init()
        self.size = self.width, self.height = 640, 480
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        pygame.mouse.set_visible(True)

        self.player = Nemo(self)
        pygame.key.set_repeat(500, 30)
        self.clock = pygame.time.Clock()

        while 1:  
            self.clock.tick(60) # clock tick regulation
            self.screen.fill(self.black)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    return         
                if event.type == pygame.KEYDOWN: 
                    self.player.move(event.key)
            self.player.tick()
            self.screen.blit(self.player.nemo, self.player.rect)
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
