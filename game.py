import pygame;
import math;

pygame.init();

WIDTH, HEIGHT = 800, 800;
WIN = pygame.display.set_mode((WIDTH, HEIGHT));
pygame.display.set_caption("Space Simulator");

# there seems to be a problem i can't figure out blank screen
# i think it's because of the scaling



WHITE = (255, 255, 255);
BLACK = (0, 0, 0);
RED = (255, 0, 0);
GREEN = (0, 255, 0);
BLUE = (0, 0, 255);
YELLOW = (255, 255, 0);

FPS = 60;

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:

    AU = 149.6e6 * 1000 # 149.6 million km, in meters
    G = 6.67408e-11
    SCALE = 213 / AU # pixels per meter
    TIMESTEP = 24 * 3600 # one day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0


    # draws the planet on the screen at its current position and orbit path 
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2 # convert to screen coordinates
        y = self.y * self.SCALE + HEIGHT / 2 

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius);
    
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

    # returns the force exerted on this planet by another planet (or the sun)
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        
        return force_x, force_y
    
    # updates the position of this planet based on its current velocity 
    # and the force exerted on it by other planets (or the sun)
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))



def main():

    run = True;
    clock = pygame.time.Clock();

    # establishing our sun     
    sun = Planet(0, 0, 30, YELLOW, 1.989e30);  
    sun.sun = True
    
    # initialize planets, and their velocities (m/s)
    mars = Planet(-1.508 * Planet.AU, 0, 12, RED, 6.39e23);
    mars.y_vel = 24.07e3

    earth = Planet(-1 * Planet.AU, 0, 12, BLUE, 5.972e24);
    earth.y_vel = 29.783e3

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.867e24);
    venus.y_vel = -35.02e3

    mercury = Planet(0.387 * Planet.AU, 0, 8, GREEN, 3.285e23);
    mercury.y_vel = -47.36e3

    # list of planets to be updated and drawn on the screen 
    planets = [sun, mars, earth, venus, mercury];
     

    while run:
        # 60 frames per second 
        clock.tick(FPS);
        WIN.fill(BLACK);

        # event loop 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # updating the position of each planet and drawing them on the screen 
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
            
        pygame.display.update();
    
    pygame.quit();

main();
