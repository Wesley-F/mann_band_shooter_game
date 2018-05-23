# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1300
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
TITLE = "Mann Band Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Stages
START = 0
PLAYING = 1
END = 2

# Images
background_img = pygame.image.load('assets/images/footballfield.jpg').convert()
start_img = pygame.image.load('assets/images/start_screen.jpg').convert()
end_win_img = pygame.image.load('assets/images/end_screen_win.jpg').convert()
end_lose_img = pygame.image.load('assets/images/end_screen_lose.jpg').convert()
ship_img = pygame.image.load('assets/images/mannbandlogo_game.png')
laser_img = pygame.image.load('assets/images/musicnote.png')
mob1_img = pygame.image.load('assets/images/riversidebandlogo.png')
mob2_img = pygame.image.load('assets/images/mauldinbandlogo.png')
mob3_img = pygame.image.load('assets/images/nationfordbandlogo.png')
mob4_img = pygame.image.load('assets/images/wandobandlogo.png')
bomb_img = pygame.image.load('assets/images/musicnote.png')

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/shoot.ogg')

# Music

# Global Variables
def start_music(stage):
     if stage == START:
          pygame.mixer.music.load("assets/sounds/music2.ogg")
          pygame.mixer.music.play(-1) 

     if stage == PLAYING:
          pygame.mixer.music.load("assets/sounds/music.ogg")
          pygame.mixer.music.play(-1)
          
     if stage == END:
          pygame.mixer.music.load("assets/sounds/music3.ogg")
          pygame.mixer.music.play(-1)
     

def print_score():
     global score
     myFont = pygame.font.SysFont("Times New Roman", 40)
     scoreDisplay = myFont.render("SCORE: " + str(score), 1, BLACK)
     s_rect = scoreDisplay.get_rect()
     s_rect.right = WIDTH - 20
     s_rect.bottom = HEIGHT - 20
     screen.blit(scoreDisplay, s_rect)

     shieldDisplay = myFont.render("SHIELD: " + str(ship.shield), 1, BLACK)
     s_rect = scoreDisplay.get_rect()
     s_rect.right = WIDTH - 20
     s_rect.bottom = HEIGHT - 100
     screen.blit(shieldDisplay, s_rect)

def draw_start():
     screen.blit(start_img, [0,0])

def draw_end():
     if len(mobs) == 0:
          screen.blit(end_win_img, [0,0])
     if len(player) == 0:
          screen.blit(end_lose_img, [0,0])
     display_stats()

def display_stats():
     global score
     shield_left = ship.shield
     score_font = pygame.font.Font(None, 50)
     score_surf = score_font.render(str(score), 1, (0, 0, 0))
     score_pos = [1100, 185]
     screen.blit(score_surf, score_pos)

     if shield_left == 3:
          times_hit = 0
     if shield_left == 2:
          times_hit = 1
     if shield_left == 1:
          times_hit = 2
     if shield_left == 0:
          times_hit = 3
          
     times_hit_font = pygame.font.Font(None, 50)
     times_hit_surf = times_hit_font.render(str(times_hit), 1, (0, 0, 0))
     times_hit_pos = [1100, 300]
     screen.blit(times_hit_surf, times_hit_pos)

     shield_left_font = pygame.font.Font(None, 50)
     shield_left_surf = shield_left_font.render(str(shield_left), 1, (0, 0, 0))
     shield_left_pos = [1100, 435]
     screen.blit(shield_left_surf, shield_left_pos)
 

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        global shield_left

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 3
        self.shield = 3

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self, bombs):
        global shield_left
        
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            # play hit sound
            self.shield -= 1

        hit_list = pygame.sprite.spritecollide(self, mobs, False)
        if len(hit_list) > 0:
            self.shield -= 1

        if self.shield == 0:
            EXPLOSION.play()
            self.kill()
     
        if self.rect.x <= 0:
             self.rect.x = 0
             
        elif self.rect.x >= 1250:
             self.rect.x = 1250
    
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
             self.kill()

    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image, shield, value):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shield = shield
        self.value = value

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self, lasers):
        global score
        global mob_number
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.shield -=1
            if self.shield == 0:
                 EXPLOSION.play()
                 self.kill()
                 score += self.value
                 print(score)

        

class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
             self.kill()
    
    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 50
            

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

def setup():
     global stage, player, mobs, lasers, bombs, fleet, ship, score

     score = 0

     start_music(START)
     
     # Make game objects
     ship = Ship(384, 536, ship_img)
     mob1 = Mob(100, 0, mob1_img, 2, 1)
     mob2 = Mob(250, 0, mob1_img, 2, 1)
     mob3 = Mob(400, 0, mob1_img, 2, 1)
     mob4 = Mob(550, 0, mob1_img, 2, 1)
     mob5 = Mob(175, -100, mob2_img, 10, 2)
     mob6 = Mob(325, -100, mob2_img, 10, 2)
     mob7 = Mob(475, -100, mob2_img, 10, 2)
     mob8 = Mob(175, -300, mob3_img, 20, 5)
     mob9 = Mob(475, -300, mob3_img, 20, 5)
     mob10 = Mob(325, -500, mob4_img, 40, 10)
     
     # Make sprite groups
     player = pygame.sprite.GroupSingle()
     player.add(ship)

     lasers = pygame.sprite.Group()

     mobs = pygame.sprite.Group()
     mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10)

     bombs = pygame.sprite.Group()


     fleet = Fleet(mobs)

     # Game Stage Start
     stage = START


setup()
# Game loop
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               done = True
          elif event.type == pygame.KEYDOWN:
               if stage == START:
                    if event.key == pygame.K_TAB:
                         stage = PLAYING
                         start_music(PLAYING)
                         pygame.mixer.music.play(-1)

               if stage == PLAYING:
                    if event.key == pygame.K_SPACE:
                         ship.shoot()

               if stage == END:
                    if event.key == pygame.K_r:
                         setup()
                    

     if stage == PLAYING:
          pressed = pygame.key.get_pressed()

          if pressed[pygame.K_LEFT]:
               ship.move_left()
          elif pressed[pygame.K_RIGHT]:
               ship.move_right()

         
     # Game logic (Check for collisions, update points, etc.)
     if stage == PLAYING:
          player.update(bombs)
          lasers.update()   
          mobs.update(lasers)
          bombs.update()
          fleet.update()
          if len(mobs) == 0:
               stage = END
               start_music(END)

          if len(player) == 0:
               stage = END
               start_music(END)

        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
     if stage == START:
          draw_start()
          
     if stage == PLAYING:
          screen.blit(background_img, [0,0])
          lasers.draw(screen)
          player.draw(screen)
          bombs.draw(screen)
          mobs.draw(screen)
          print_score()

     if stage == END:
          draw_end()
          

    
    # Update screen (Actually draw the picture in the window.)
     pygame.display.flip()


    # Limit refresh rate of game loop 
     clock.tick(refresh_rate)


# Close window and quit
pygame.quit()

