import pygame, os, sys, math, time
import cPickle as pickle 

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
    def __init__(self, image_name, timemax, time_start, x, y, count_time, move_dir): 
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_name)
        self.rect = self.rect.move(x, y)
        self.orig_rect = self.rect
        self.time = time_start
        self.time_max = timemax
        self.orig_image = self.image
        self.count = 0
        self.count_time = count_time
        self.move_dir = move_dir


    def tick(self):
        if self.time == self.time_max:
            if self.count < self.count_time:
                self.rect = self.rect.move(0, 4*self.move_dir)
                self.count += 1
            elif self.rect.y == self.orig_rect.y:
                self.time = 0
                self.count = 0
            else: 
                self.rect = self.rect.move(0, -4*self.move_dir)
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

    '''def rotate(self):
        xpos, ypos = pygame.mouse.get_pos() 
        x, y = self.rect.center
        #rotation = -1 * float(math.degrees(math.atan2(float(ypos-y), float(xpos-x))))
        i=4
        b=1
        while i > 0:
            rotation = b*30
            xcenter, ycenter = self.rect.center
            rotate = pygame.transform.rotate
            self.image = rotate(self.orig_nemo, rotation)
            self.rect = self.image.get_rect(center=(xcenter, ycenter))
            i-=1
            self.gs.screen.blit(self.image, self.rect)
            b = b *(-1)'''
        
        

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
        return

    def update(self, key):
        if key == "move":
            self.rect = self.rect.move(-10, 0)
        elif key == "tick":
            self.tick()

class SetUp:
    def __init__(self, nc_offset, shark_offset, jelly_offset, move_dir):
        self.shark = Enemy("shark.png", 60, 35, 675, -150+shark_offset, 82, move_dir)
        self.jelly = Enemy("jellyfish_sprite.png", 60, 35, 150, -150+jelly_offset, 94, move_dir)
        self.player = Nemo(self, 55, 35+nc_offset)
        self.background = Background(self, "ocean_scene.png", 0, 0+nc_offset)
        self.background2 = Background(self, "ocean_scene_copy.png", 1500, 0+nc_offset)
        self.background3 = Background(self, "ocean_scene_copy.png", 2800, 0+nc_offset)
        self.crush = Crush(self, 400, 5+nc_offset)
        self.home = Home(self, 4100, 75+nc_offset)
        pygame.key.set_repeat(500, 30)
        self.sleep_count = 0
        self.jelly_collision = 0
        self.shark2 = Enemy("shark.png", 60, 35, 1800, -124+shark_offset, 82, move_dir)
        self.jelly2 = Enemy("jellyfish_sprite.png", 60, 35, 1350, -150+jelly_offset, 94, move_dir)
        self.shark3 = Enemy("shark.png", 60, 35, 2500, -124+shark_offset, 82, move_dir)
        self.jelly3 = Enemy("jellyfish_sprite.png", 60, 35, 2000, -150+jelly_offset, 94, move_dir)
        self.backgrounds = pygame.sprite.Group(self.background, self.background2, self.background3)
        self.obstacles = pygame.sprite.Group(self.shark, self.jelly, self.home, self.shark2, self.shark3, self.jelly2, self.jelly3)
        
class GameSpace(): 
    def main(self, sendData):
        self.sendData = sendData
        pygame.init()
        size = width, height = 1400, 664
        black = 0,0,0
        self.screen = pygame.display.set_mode(size)
        pygame.mouse.set_visible(True)
        shark_offset = 334 #788
        jelly_offset = 334 #884
        self.top = SetUp(0, 0, 0, 1)
        self.bottom = SetUp(334, shark_offset, jelly_offset, 1)
        #print "got to end of main"
        self.data_counter = 0

    def get_data(self, data): 
        try:
            self.bottom.player.rect = pickle.loads(data) 
        except Exception as e:
            print "ERROR: ", e

    def iteration(self):
        self.data_counter += 1
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                exit(1)         
            if event.type == pygame.KEYDOWN and self.top.sleep_count == 0:
                if (self.top.player.rect.x + self.top.player.image.get_width() < 900) or (self.top.home.rect.x + self.top.home.image.get_width() < 1400):
                    self.top.player.move(event.key)
                else:
                    self.top.obstacles.update("move")
                    self.top.crush.update("move")
                    self.top.player.move_updown(event.key)
        self.top.player.tick()
        if (self.top.player.rect.x + self.top.player.image.get_width() > 75) and self.top.sleep_count == 0:
            if self.top.player.rect.x + self.top.player.image.get_width() < 900:
                self.top.player.rect = self.top.player.rect.move(-1, 0)
        if self.top.player.rect.colliderect(self.top.shark.rect):
            self.top.player = Nemo(self, 55, 35)
            self.top.player.tick()
        if self.top.player.rect.colliderect(self.top.jelly.rect):
            self.top.jelly_collision = 1
        if self.top.jelly_collision == 1:
            #self.player.rotate()
            self.top.sleep_count+= 1
        if self.top.sleep_count >= 60:
            self.top.jelly_collision = 0
            self.top.sleep_count = 0
        self.top.obstacles.update("tick")
        self.top.crush.tick()
        self.top.backgrounds.draw(self.screen)
        self.top.obstacles.draw(self.screen)
        if self.top.crush.rect.x + self.top.crush.image.get_width() < 1550:
            self.screen.blit(self.top.crush.image, self.top.crush.rect) 
        self.screen.blit(self.top.player.image, self.top.player.rect)
        pygame.display.flip()

        if self.data_counter >= 5:
            self.sendData(pickle.dumps(self.top.player.rect.move(0, 334)))
            self.data_counter = 0
        '''for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                return         
            if event.type == pygame.KEYDOWN and self.bottom.sleep_count == 0:
                if (self.bottom.player.rect.x + self.bottom.player.image.get_width() < 900) or (self.bottom.home.rect.x + self.bottom.home.image.get_width() < 1400):
                    self.bottom.player.move(event.key)
                else:
                    self.bottom.obstacles.update("move")
                    self.bottom.player.move_updown(event.key)'''
        #self.bottom.player.rect = self.bottom.player.rect.move()
        self.bottom.player.tick()
        if (self.bottom.player.rect.x + self.bottom.player.image.get_width() > 75) and self.bottom.sleep_count == 0:
            if self.bottom.player.rect.x + self.bottom.player.image.get_width() < 900:
                self.bottom.player.rect = self.bottom.player.rect.move(-1, 0)
        if self.bottom.player.rect.colliderect(self.bottom.shark.rect):
            self.bottom.player = Nemo(self, 55, 35)
            self.bottom.player.tick()
        if self.bottom.player.rect.colliderect(self.bottom.jelly.rect):
            self.bottom.jelly_collision = 1
        if self.bottom.jelly_collision == 1:
            #self.player.rotate()
            self.bottom.sleep_count+= 1
        if self.bottom.sleep_count >= 60:
            self.bottom.jelly_collision = 0
            self.bottom.sleep_count = 0
        self.bottom.obstacles.update("tick")
        self.bottom.crush.tick()
        self.bottom.backgrounds.draw(self.screen)
        if self.bottom.jelly.rect.y >= 332:
            self.bottom.obstacles.draw(self.screen)
        if self.bottom.crush.rect.x + self.bottom.crush.image.get_width() < 1550:
            self.screen.blit(self.bottom.crush.image, self.bottom.crush.rect)
        self.screen.blit(self.bottom.player.image, self.bottom.player.rect)
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


