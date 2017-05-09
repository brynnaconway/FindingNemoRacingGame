import pygame, os, sys, math, time

class Background(pygame.sprite.Sprite):
    def __init__(self, gs, image_name, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_name)
        self.rect = self.rect.move(x, y)
        self.image = pygame.transform.scale(self.image, (1500, 330))
    
    def update(self, key):
        if key == "move":
            self.rect = self.rect.move(-10, 0)
        elif key == "tick":
            return

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_name, timemax, time_start, x, y, count_time): 
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_name)
        self.rect = self.rect.move(x, y)
        self.orig_rect = self.rect
        self.time = time_start
        self.time_max = timemax
        self.orig_image = self.image
        self.count = 0
        self.count_time = count_time

    def tick(self):
        if self.time == self.time_max:
            if self.count < self.count_time:
                self.rect = self.rect.move(0, 4)
                self.count += 1
            elif self.rect.y <= self.orig_rect.y:
                self.time = 0
                self.count = 0
            else: 
                self.rect = self.rect.move(0, -4)
        else:
            self.time += 1

    def update(self, key):
        if key == "move":
            self.rect = self.rect.move(-10, 0)
        elif key == "tick":
            self.tick()

class Nemo(pygame.sprite.Sprite):
    def __init__(self, gs, x, y): 
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.image, self.rect = load_image("nemo_sprite.png")
        self.orig_nemo = self.image
        self.rect = self.rect.move(x, y)
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
        self.image = self.orig_nemo
        if event_key == pygame.K_RIGHT: 
            if self.rect.x +self.image.get_width() < 1370:
                xdir = 1
        elif event_key == pygame.K_UP:
            if self.rect.y + self.image.get_height() > 95:
                ydir = -1
        elif event_key == pygame.K_DOWN:
            if self.rect.y + self.image.get_height() < 337:
                ydir = 1 
        if self.rect.y + self.image.get_height() > 300:
            self.rect = self.rect.move(xdir*3, ydir*3)
        else:
            self.rect = self.rect.move(xdir*10, ydir*10)

    def move_updown(self, event_key):
        xpos, ypos = pygame.mouse.get_pos() 
        x, y = self.rect.center
        xdir = 0
        ydir = 0
        self.image = self.orig_nemo
        if event_key == pygame.K_UP:
            if self.rect.y + self.image.get_height() > 95:
                ydir = -1
        elif event_key == pygame.K_DOWN:
            if self.rect.y + self.image.get_height() < 337:
                ydir = 1 
        if self.rect.y + self.image.get_height() > 300:
            self.rect = self.rect.move(xdir*3, ydir*3)
        else:
            self.rect = self.rect.move(xdir*10, ydir*10)

class Crush(pygame.sprite.Sprite):
    def __init__(self, gs, x, y): 
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.image, self.rect = load_image("crush.png")
        self.orig_crush = self.image
        self.rect = self.rect.move(x, y)
        self.gs = gs
        self.gofast = 0 
        self.collided = 0

    def tick(self): 
        if self.rect.colliderect(self.gs.player.rect):
            while (self.gs.player.rect.x + self.gs.player.image.get_width() < 780):
                self.gs.player.rect = self.gs.player.rect.move(2, 0)
                self.rect = self.rect.move(1, 0)
                self.collided = 1
                time.sleep(.0001)
        if self.collided == 1:
            self.rect = self.rect.move(40, 0)
    
    def update(self, key):
        if key == "move":
            self.rect = self.rect.move(-10, 0)
        elif key == "tick":
            self.tick()



    '''def move(self, event_key):
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
            self.rect = self.rect.move(xdir*10, ydir*10)'''

class Home(pygame.sprite.Sprite):
    def __init__(self, gs, x, y): 
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.image, self.rect = load_image("home.png")
        self.orig_home = self.image
        self.rect = self.rect.move(x, y)
        self.gs = gs

    def tick(self):
        print("hey")

    def update(self, key):
        if key == "move":
            self.rect = self.rect.move(-10, 0)
        elif key == "tick":
            self.tick()


class GameSpace: 
    def main(self): 
        pygame.init()
        self.size = self.width, self.height = 1400, 664
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        pygame.mouse.set_visible(True)

        self.shark = Enemy("shark.png", 60, 35, 675, -124, 78)
        self.jelly = Enemy("jellyfish_sprite.png", 60, 57, 150, -150, 90)
        self.player = Nemo(self, 55, 35)
        self.top_background = Background(self, "ocean_scene.png", 0, 0)
        self.top_background2 = Background(self, "ocean_scene_copy.png", 1500, 0)
        self.top_background3 = Background(self, "ocean_scene_copy.png", 2800, 0)
        self.bottom_background = Background(self, "ocean_scene.png", 0, 0)
        self.crush = Crush(self, 400, 5)
        self.home = Home(self, 4100, 75)
        pygame.key.set_repeat(500, 30)
        self.clock = pygame.time.Clock()
        self.sleep_count = 0
        self.jelly_collision = 0
        self.shark2 = Enemy("shark.png", 60, 35, 1800, -124, 78)
        self.jelly2 = Enemy("jellyfish_sprite.png", 60, 57, 1350, -150, 90)
        self.shark3 = Enemy("shark.png", 60, 35, 2500, -124, 78)
        self.jelly3 = Enemy("jellyfish_sprite.png", 60, 57, 2000, -150, 90)

        self.obstacles = pygame.sprite.Group(self.top_background, self.top_background2, self.top_background3, self.shark, self.jelly, self.crush, self.home, self.shark2, self.shark3, self.jelly2, self.jelly3)

        while 1:  
            self.clock.tick(60) # clock tick regulation
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    return         
                if event.type == pygame.KEYDOWN and self.sleep_count == 0:
                    if (self.player.rect.x + self.player.image.get_width() < 900) or (self.home.rect.x + self.home.image.get_width() < 1400):
                        self.player.move(event.key)
                    else:
                        self.obstacles.update("move")
                        self.player.move_updown(event.key)
            self.player.tick()
            if (self.player.rect.x + self.player.image.get_width() > 75) and self.sleep_count == 0:
                if self.player.rect.x + self.player.image.get_width() < 900:
                    self.player.rect = self.player.rect.move(-1, 0)
            if self.player.rect.colliderect(self.shark.rect):
                self.player = Nemo(self, 55, 35)
                self.player.tick()
            if self.player.rect.colliderect(self.jelly.rect):
                self.jelly_collision = 1
            if self.jelly_collision == 1:
                self.sleep_count+= 1
            if self.sleep_count >= 60:
                self.jelly_collision = 0
                self.sleep_count = 0
            #self.crush.tick()
            #self.shark.tick()
            #self.jelly.tick()
            self.obstacles.update("tick")
            #self.screen.blit(pygame.transform.scale(self.top_background.ocean, (1400, 330)), self.top_background.rect)
            self.screen.blit(pygame.transform.scale(self.bottom_background.image, (1400, 330)), self.bottom_background.rect.move(0, 334))
            if self.crush.rect.x + self.crush.image.get_width() >= 1550:
                self.obstacles.remove(self.crush)
            self.obstacles.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            #self.screen.blit(self.home.home, self.home.rect)
            #self.screen.blit(self.shark.image, self.shark.rect)
            #self.screen.blit(self.jelly.image, self.jelly.rect)
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
