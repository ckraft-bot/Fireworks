# pip install pygame
"""
Purpose:
    This will be a visual animation of a firework show. It is sensory friendly.
    The main library we'll be using is the pygame. SOme others include random, time, and math.
    To build this digital show we'll need to have three classes: launcher, explosion effect, projectiles.
"""

import random
import time
import math
import pygame
pygame.init()

WIDTH, HEIGHT = 800,600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Welcome to the sensory friendly firework show!')

FPS = 60

"""
RGB Color code: https://pygame.readthedocs.io/en/latest/1_intro/intro.html
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
"""

COLORS = [  (0, 0, 0),
            (127, 127, 127),
            (255, 255, 255),
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (0, 255, 255),
            (255, 0, 255)
]

class Launcher:
    WIDTH = 20  
    HEIGHT = 20
    COLOR = 'grey'

    def __init__(self, x, y, frequency):
        self.x = x
        self.y = y
        self.frequency = frequency # frequency in ms
        self.start_time = time.time()
        self.fireworks = []
        
    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.WIDTH, self.HEIGHT))
        for firework in self.fireworks:
            firework.draw(win)
        
    def launch(self):
        color = random.choice(COLORS)
        explode_height = random.randrange(50, 400)
        firework = Firework(self.x + self.WIDTH/2, self.y, -5, explode_height, color)
        self.fireworks.append(firework)
        
    def loop(self, max_width, max_height): # defining the window parameters
        current_time = time.time()
        time_elapsed = current_time - self.start_time
        
        # if the time has passed 1 sec then launch another
        if time_elapsed * 1000 >= self.frequency:
            self.start_time = current_time
            self.launch()
            firework_to_remove = []
            for firework in self.fireworks:
                # move fireworks around
                firework.move(max_width, max_height)
                # once the explosion takes places and passes the screen then remove firework 
                # off screen fireworks are dead
                # the firework projectiles are headed for the black hole
                if firework.exploded and len(firework.projectiles) == 0: #
                    firework_to_remove.append(firework)
                    
            # not recycling explosions
            for firework in firework_to_remove:
                self.fireworks.remove(firework)      
                    
class Firework:
    RADIUS = 10
    MAX_PROJECTILES = 50
    MIN_PROJECTILES = 25
    PROJECTILE_VELOCITY = 4 # the moving speed of the firework in any direction
    
    def __init__(self, x, y, y_vel, explode_height, color): # y_vel = upward movement
        self.x = x
        self.y = y
        self.y_vel = y_vel
        self.explode_height = explode_height
        self.color = color
        self.projectiles = []
        self.exploded = False 
        
    def explode(self):
        self.exploded = True
        num_projectiles = random.randrange(self.MIN_PROJECTILES, self.MAX_PROJECTILES)
        if random.randint(0,1) == 0:
            self.create_circular_projectiles(num_projectiles)
        else:
            self.create_star_projectiles
        
    # creating patterns
    """
        thinking through trig:
        circle pattern
            circle has 360 degrees
            360 = 2pi (radians)
            4 quadrants
            four 90 degree angles #https://precal2014.weebly.com/4-2-degrees--radians.html
            angles: pi/2 (90 degrees), pi (180 degrees), 3pi/2 (270 degrees), 2pi (360 degrees)
        sorting out projectile angles along the circle
            SOH, CAH, TOA #https://www.mathsisfun.com/algebra/sohcahtoa.html
            sin(theta) = opposite/hypotenuse **hypotenuse = velocity**
    """
    def create_circular_projectiles(self, num_projectiles):
        # math.pi*2  = 360 degrees, num_projectiles telling projectiles to move evenly along the circle
        angle_diff = math.pi*2/num_projectiles  
        current_angle = 0
        vel = random.randrange(self.PROJECTILE_VELOCITY - 1, 
                                self.PROJECTILE_VELOCITY + 1) # up and down 1 to add variance
        
        for i in range(num_projectiles):
            x_vel = math.sin(current_angle)*vel
            y_vel = math.cos(current_angle)*vel
            color = random.choice(COLORS)
            self.projectiles.append(Projectile(self.x, self.y, x_vel, y_vel, color))
            current_angle += angle_diff
    
    def create_star_projectiles(self):
        angle_diff = math.pi/4
        current_angle = 0 
        num_projectiles = 64                                        # if the following lines were manual calculations, lines 146-148 numbers have to be proportional bc math
        for i in range(1, num_projectiles +1):                            # for i in range(1, 65)                   # for i in range(1, 33)
            vel = self.PROJECTILE_VELOCITY + (i%(num_projectiles/8))      # vel = self.PROJECTILE_VELOCITY + (i%8)  #vel = self.PROJECTILE_VELOCITY + (i%4)
            x_vel = math.sin(current_angle)*vel
            y_vel = math.cos(current_angle)*vel
            color = random.choice(COLORS)
            self.projectiles.append(Projectile(self.x, self.y, x_vel, y_vel, color))
            if(i%(num_projectiles/8)== 0):                                                  # if(i%8 == 0)
                current_angle += angle_diff
            current_angle += angle_diff
    
    def move(self, max_width, max_height):
        # not moving the firework once exploded
        if not self.exploded:
            self.y += self.y_vel # passing a neg vel will go up, passing a pos vel will go down
            if self.y <= self.explode_height:
                self.explode() # then explode
            
        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.move()
            
            if projectile.x >= max_width or projectile.x  < 0:
                projectiles_to_remove.append(projectile)
            elif projectile.y >= max_height or projectile.y < 0:
                projectiles_to_remove.append(projectile)
        for projectile in self.projectiles_to_remove:
            self.projectiles.remove(projectile)
        
        
    def draw(self, win):
        if not self.exploded:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.RADIUS)
        for projectile in self.projectiles:
            projectile.draw(win)

class Projectile:
    WIDTH = 5
    HEIGHT = 10
    ALPHA_DECREMENT = 3  # fading effect/ transparency
    
    def __init__(self, x, y, x_vel, y_vel, color): #  moving x and y velocities to get diagonal, think etch-a-sketch
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.alpha = 255
        
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.alpha = max(0, self.alpha - self.ALPHA_DECREMENT)
        
    def draw(self,win):
        self.draw_rect_alpha(win, self.color + (self.alpha,), self.x, self.y, self.WIDTH, self.HEIGHT)
    """
    The @staticmethod is a built-in decorator that defines a static method in the class in Python. 
    A static method is for a given function. Not universal.
    It is bound to the class and not the object of the class. 
    This method can’t access or modify the class state. 
    It is present in a class because it makes sense for the method to be present in class.
    """
    @staticmethod
    def draw_rect_alpha(surface, color, rect):
        shape_surface = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA) # SRCALPHA enables transparency
        pygame.draw.rect(shape_surface, color, shape_surface.get_rect()) # apply color to shape surface, filling in with color
        surface.blit(shape_surface, rect) # blit overlpays layers, the transparent color shaped surface on top of the other shape
        
        
def draw(launchers):
    win.fill('black') # dark sky enviroment
    for launcher in launchers:
        launcher.draw(win)
    pygame.display.update()

def lauch(self):
    color = random.choice(COLORS)
    explode_height = random.randrange(50, 400)
    firework = Firework(self.x + self.WIDTH/2, self.y, -5, explode_height, color ) # velocity = -5
    self.fireqorks.append(firework)

def main():
    run = True
    clock = pygame.time.Clock()
    launchers = [Launcher(100, HEIGHT - Launcher.HEIGHT, 3000),
                Launcher(300, HEIGHT - Launcher.HEIGHT, 4000),
                Launcher(500, HEIGHT - Launcher.HEIGHT, 2000),
                Launcher(700, HEIGHT - Launcher.HEIGHT, 5000)] 
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        for launcher in launchers:
            launcher.loop(WIDTH, HEIGHT)
        draw(launchers)
        
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()

