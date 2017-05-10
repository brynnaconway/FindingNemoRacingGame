import pygame, os, sys, math, time
import cPickle as pickle 

# Paradigms Final Project
# Leah Plofchan and Brynna Conway

# create background ocean image
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

# obstacles contained in this class
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

    # moves obstacles up and down
    def tick(self):
        if self.time == self.time_max:
            if self.count < self.count_time:
                self.rect = self.rect.move(0, 6*self.move_dir)
                self.count += 1
            elif self.rect.y == self.orig_rect.y:
                self.time = 0
                self.count = 0
            else: 
                self.rect = self.rect.move(0, -6*self.move_dir)
        else:
            self.time += 1

    def update(self, key):
        if key == "move":
            self.rect = self.rect.move(-10, 0) # move obstacle left as nemo moves right to simulate moving window
        elif key == "tick":
            self.tick()

# main player class
class Nemo(pygame.sprite.Sprite):
    def __init__(self, gs, x, y): 
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.image, self.rect = load_image("nemo_sprite.png")
        self.orig_nemo = self.image
        self.rect = self.rect.move(x, y)
        self.gs = gs

    def tick(self): 
        xpos, ypos = pygame.mouse.get_pos() 
        x, y = self.rect.center
        rotation = -1 * float(math.degrees(math.atan2(float(ypos-y), float(xpos-x))))
        xcenter, ycenter = self.rect.center
        rotate = pygame.transform.rotate

    # place restrictions on nemo's movement
    def move(self, event_key):
        xpos, ypos = pygame.mouse.get_pos() 
        x, y = self.rect.center
        xdir = 0
        ydir = 0
        self.image = self.orig_nemo
        if event_key == pygame.K_RIGHT:         # dont allow moving off the edge of the screen
            if self.rect.x +self.image.get_width() < 1370:
                xdir = 1
        elif event_key == pygame.K_UP:          
            if self.rect.y + self.image.get_height() > 95:
                ydir = -1
        elif event_key == pygame.K_DOWN:
            if self.rect.y + self.image.get_height() < 337:
                ydir = 1 
        if self.rect.y + self.image.get_height() > 300:     # slow down speed in the coral/reef area of screen
            self.rect = self.rect.move(xdir*3, ydir*3)
        else:                                                  # normal speed
            self.rect = self.rect.move(xdir*13, ydir*13)

    # function for once nemo has reached end and can only move up/down
    def move_updown(self, event_key):
        xpos, ypos = pygame.mouse.get_pos() 
        x, y = self.rect.center
        xdir = 0
        ydir = 0
        self.image = self.orig_nemo
        if event_key == pygame.K_UP:
            if self.rect.y + self.image.get_height() > 95:      # check boundaries
                ydir = -1
        elif event_key == pygame.K_DOWN:
            if self.rect.y + self.image.get_height() < 337:     # check boundaries
                ydir = 1 
        if self.rect.y + self.image.get_height() > 300:
            self.rect = self.rect.move(xdir*3, ydir*3)          # slow pace in coral
        else:
            self.rect = self.rect.move(xdir*10, ydir*10)           # normal speed
        
        
# turtle ("Crush") class
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
        pass
    
    def update(self, key):
        if key == "move":                       # move left to simulate whole window moving
            self.rect = self.rect.move(-10, 0)
        elif key == "tick":
            self.tick()

# marlin and dory images 
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
        if key == "move":                   # move from off the screen to be at the end of screen by the time nemo reaches
            self.rect = self.rect.move(-10, 0)
        elif key == "tick":
            self.tick()

# instantiate/initialize all objects of various classes
class SetUp:
    def __init__(self, nc_offset, shark_offset, jelly_offset, move_dir):
        self.shark = Enemy("shark.png", 60, 35, 675, -150+shark_offset, 62, move_dir)
        self.jelly = Enemy("jellyfish_sprite.png", 60, 35, 150, -150+jelly_offset, 62, move_dir)
        self.player = Nemo(self, 55, 35+nc_offset) # main player
        self.background = Background(self, "ocean_scene.png", 0, 0+nc_offset)
        self.background2 = Background(self, "ocean_scene_copy.png", 1500, 0+nc_offset)  # extend screen
        self.background3 = Background(self, "ocean_scene_copy.png", 2800, 0+nc_offset)  # extend screen more
        self.crush = Crush(self, 400, 5+nc_offset)      # turtle that will boost speed
        self.home = Home(self, 2800, 75+nc_offset)      # end goal
        pygame.key.set_repeat(500, 30)
        self.sleep_count = 0
        self.jelly_collision = 0
        # more objects of the obstacles that appear on the path
        self.jelly2 = Enemy("jellyfish_sprite.png", 60, 35, 1000, -150+jelly_offset, 62, move_dir)
        self.shark2 = Enemy("shark.png", 60, 35, 1400, -150+shark_offset, 62, move_dir)
        self.jelly3 = Enemy("jellyfish_sprite.png", 60, 35, 1800, -150+jelly_offset, 62, move_dir)
        self.shark3 = Enemy("shark.png", 60, 35, 2300, -150+shark_offset, 62, move_dir)
        self.jelly4 = Enemy("jellyfish_sprite.png", 60, 35, 2600, -150+jelly_offset, 62, move_dir)
        self.backgrounds = pygame.sprite.Group(self.background, self.background2, self.background3) # organize backgrounds
        self.win_image, self.win_rect = load_image("win.png")
        self.win_rect = self.win_rect.move(100, 10)             # end of game winning message
        self.lose_image, self.lose_rect = load_image("game_over.jpg")
        self.lose_rect = self.lose_rect.move(100, 10)           # end of game losing message
        self.obstacles = pygame.sprite.Group(self.shark, self.jelly, self.shark2, self.shark3, self.jelly2, self.jelly3, self.jelly4)
        
# main game state
class GameSpace(): 
    def main(self, sendData):
        self.sendData = sendData
        pygame.init()
        size = width, height = 1400, 664 # screen window size
        black = 0,0,0
        self.screen = pygame.display.set_mode(size)
        pygame.mouse.set_visible(True)
        shark_offset = 334          # vertical offset for bottom screen
        jelly_offset = 334          # used to create bottom sprites
        self.top = SetUp(0, 0, 0, 1)        # dimensions begin at the top of the screen
        self.bottom = SetUp(334, shark_offset, jelly_offset, 1)     # offset dimensions
        self.data_counter = 0
        self.other_moved = 0
        self.top_collided = 0
        self.bottom_collided = 0
        self.other_collided = 0
        self.lost = 0
        self.won = 0

    # received data from other player via network connection
    def get_data(self, data): 
        try:
            if data.split(".")[1][0] == "1":        # parse data for indication of player movement
                self.other_moved = 1
                self.bottom.player.rect = pickle.loads(data)
                self.other_collided = int(data.split(".")[1][1])
            elif data.split(".")[1][0] == "0":      # no player movement
                self.other_moved = 0
                self.bottom.player.rect = pickle.loads(data)
                self.other_collided = int(data.split(".")[1][1])
        except Exception as e:
            print "ERROR: ", e

    # main activity loop
    def iteration(self):
        self.moved = 0
        self.data_counter += 1
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:   # exit game
                pygame.quit()   
            if event.type == pygame.KEYDOWN and self.top.sleep_count == 0:
                self.moved = 1
                if (self.top.player.rect.x + self.top.player.image.get_width() < 900) or (self.top.home.rect.x + self.top.home.image.get_width() < 1400): #within bounds
                    self.top.player.move(event.key)
                else:
                    self.top.obstacles.update("move")           # constantly move all other screen objects in addition to nemo to create active game
                    self.top.crush.update("move")
                    self.top.backgrounds.update("move")
                    self.top.home.update("move")
                    self.top.player.move_updown(event.key)
        self.top.player.tick()
        if (self.top.player.rect.x + self.top.player.image.get_width() > 75) and self.top.sleep_count == 0:
            if self.top.player.rect.x + self.top.player.image.get_width() < 900:
                self.top.player.rect = self.top.player.rect.move(-1, 0)                 # constant movement of nemo left to simulate water current

        # collision with obstacles 
        if self.top.player.rect.colliderect(self.top.shark.rect):
            self.top.player = Nemo(self, 55, 35)
            self.top.player.tick()
        if self.top.player.rect.colliderect(self.top.jelly.rect):
            self.top.jelly_collision = 1
        if self.top.jelly_collision == 1:
            self.top.sleep_count+= 1
        if self.top.sleep_count >= 60:
            self.top.jelly_collision = 0
            self.top.sleep_count = 0

        # next set of collisions 
        if self.top.player.rect.colliderect(self.top.shark2.rect):
            self.top.player = Nemo(self, 55, 35)
            self.top.player.tick()
        if self.top.player.rect.colliderect(self.top.jelly2.rect):
            self.top.jelly_collision = 1
        if self.top.jelly_collision == 1:
            self.top.sleep_count+= 1
        if self.top.sleep_count >= 40:
            self.top.jelly_collision = 0
            self.top.sleep_count = 0

        # more collisions 
        if self.top.player.rect.colliderect(self.top.shark3.rect):
            self.top.player = Nemo(self, 55, 35)
            self.top.player.tick()
        if self.top.player.rect.colliderect(self.top.jelly3.rect):
            self.top.jelly_collision = 1
        if self.top.jelly_collision == 1:
            self.top.sleep_count+= 1
        if self.top.sleep_count >= 40:
            self.top.jelly_collision = 0
            self.top.sleep_count = 0

        # last possible collision
        if self.top.player.rect.colliderect(self.top.jelly4.rect):
            self.top.jelly_collision = 1
        if self.top.jelly_collision == 1:
            self.top.sleep_count+= 1
        if self.top.sleep_count >= 40:
            self.top.jelly_collision = 0
            self.top.sleep_count = 0

        self.top.obstacles.update("tick")
        if self.top.crush.rect.colliderect(self.top.player.rect):
            while (self.top.player.rect.x + self.top.player.image.get_width() < 780):   
                self.top.player.rect = self.top.player.rect.move(2, 0)      # simulate movement with turtle (i.e. turtle carries nemo to go fast)
                self.top.crush.rect = self.top.crush.rect.move(1, 0)
                self.top_collided = 1
                time.sleep(.0001)
        if self.top_collided == 1:
            self.top.crush.rect = self.top.crush.rect.move(40, 0)           # zoom forward on screen once in contact with turtle
        # update screen
        self.top.backgrounds.draw(self.screen)
        self.top.obstacles.draw(self.screen)
        self.screen.blit(self.top.home.image, self.top.home.rect)
        if self.top.crush.rect.x + self.top.crush.image.get_width() < 1550:
            self.screen.blit(self.top.crush.image, self.top.crush.rect) 
        if self.won == 1:     # display winning message
            self.screen.blit(self.top.win_image, self.top.win_rect)
        if self.lost == 1:   # display losing message
            self.screen.blit(self.top.lose_image, self.top.lose_rect)
        self.screen.blit(self.top.player.image, self.top.player.rect)
        pygame.display.flip()

        # send user data over network
        if self.data_counter >= 5:
            self.sendData(pickle.dumps(self.top.player.rect.move(0, 334)))
            self.sendData(str(self.moved))
            self.sendData(str(self.top_collided))
            self.data_counter = 0
      
        self.last_rect = self.bottom.shark.rect.x +1    # used to detect shark movement
        if self.bottom.sleep_count == 0:
            # update entire screen
            if (self.bottom.player.rect.x + self.bottom.player.image.get_width() >= 900) and (self.bottom.home.rect.x + self.bottom.home.image.get_width() >= 1400) and self.other_moved == 1:
                self.bottom.obstacles.update("move")
                self.bottom.backgrounds.update("move")
                self.bottom.crush.update("move")
                self.bottom.home.update("move")
                self.last_rect = self.bottom.shark.rect.x

        self.bottom.player.tick()
        if (self.bottom.player.rect.x + self.bottom.player.image.get_width() > 75) and self.bottom.sleep_count == 0:
            if self.bottom.player.rect.x + self.bottom.player.image.get_width() < 900:
                self.bottom.player.rect = self.bottom.player.rect.move(-1, 0)           # water current simulation
        if self.bottom.player.rect.colliderect(self.bottom.shark.rect):     # move nemo back to left edge of screen upon collision
            self.bottom.player = Nemo(self, 55, 35)
            self.bottom.player.tick()
        if self.bottom.player.rect.colliderect(self.bottom.jelly.rect):     # freeze nemo upon collision with jellyfish
            self.bottom.jelly_collision = 1
        if self.bottom.jelly_collision == 1:
            self.bottom.sleep_count+= 1
        if self.bottom.sleep_count >= 60:
            self.bottom.jelly_collision = 0
            self.bottom.sleep_count = 0
        self.bottom.obstacles.update("tick")

        if self.other_collided:
            self.top_collided = 0
            # ensure matching movement of crush between screens
            while (self.bottom.crush.rect.x + self.bottom.crush.image.get_width() < 780):
                self.bottom.crush.rect = self.bottom.crush.rect.move(1, 0)
                self.bottom_collided = 1
                time.sleep(.0001)
        if self.other_collided == 1:
            self.bottom.crush.rect = self.bottom.crush.rect.move(40, 0) # zoom crush ahead
        # update screen
        self.bottom.backgrounds.draw(self.screen)
        self.screen.blit(self.bottom.home.image, self.bottom.home.rect)     # display home end goal
        if self.bottom.jelly.rect.y >= 332:
            self.bottom.obstacles.draw(self.screen)
        if self.bottom.crush.rect.x + self.bottom.crush.image.get_width() < 1550:
            self.screen.blit(self.bottom.crush.image, self.bottom.crush.rect)
            self.other_collided = 0

        self.screen.blit(self.bottom.player.image, self.bottom.player.rect)

        if self.top.player.rect.colliderect(self.top.home.rect):        # player 1 made it home -- winner
            self.screen.blit(self.top.win_image, self.top.win_rect)
            self.won = 1
        if self.bottom.player.rect.colliderect(self.bottom.home.rect):  # player 2 made it home -- winner
            self.screen.blit(self.top.lose_image, self.top.lose_rect)
            self.lost = 1

        pygame.display.flip()

# function used to load all sprite images for game
def load_image(image_name):
    PATH = "Sprites/"
    FULL_PATH = PATH + image_name
    try: 
        image = pygame.image.load(FULL_PATH)
    except pygame.error:
        print("Cannot load image:", FULL_PATH)
        raise SystemExit 
    return image, image.get_rect()


