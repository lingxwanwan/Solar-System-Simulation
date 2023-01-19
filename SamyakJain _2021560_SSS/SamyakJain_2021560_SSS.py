import pygame
import math
import random

L = []
for i in range(80):
    L.append((random.randint(0, 800), random.randint(0, 800)))
H = []
for i in range(80):
    H.append((random.randint(0, 255), 0,random.randint(0, 255)))
pygame.init()
wi, he = 800, 800
S_S = pygame.display.set_mode((wi, he))
pygame.display.set_caption('Solar System Simulation by Anshuman and Samyak')
WHITE = (255, 255, 255)
VENUS = (240, 190, 73)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (169, 169, 169)
FONT = pygame.font.SysFont("impact", 16)
print('Welcome to the Solar System Simulator!!!\n'
      'Select the options to control the simulator!\n'
      'Spacebar: Pause the application\n'
      '1: Fast forward the application\n'
      '2: Decrease the speed of the application\n'
      'x: Unpause/Resume when paused, otherwise, exit the application\n')


def paused(pause):
    key_input = pygame.key.get_pressed()
    while pause:
        for event in pygame.event.get():


            if event.type == pygame.QUIT:
                if key_input[pygame.K_SPACE]:
                    pause = False
class Planet:
    A_U = 149.6e9
    G = 6.67e-11
    SCALE = 250 / A_U  # 1AU = 100 pixels
    relative_time = 3600 * 24  # 1 day

    def __init__(planet, name, x, y, radius, color, mass):
        planet.n = name
        planet.x = x
        planet.y = y
        planet.r = radius
        planet.color = color
        planet.mass = mass

        planet.orbit = []
        planet.sun = False
        planet.distance_to_sun = 0

        planet.x_vel = 0
        planet.y_vel = 0

    def draw(xin, win):
        x = xin.x * xin.SCALE + wi / 2
        y = xin.y * xin.SCALE + he / 2

        if len(xin.orbit) > 2:
            updated_points = []
            for point in xin.orbit:
                x, y = point
                x = x * xin.SCALE + wi / 2
                y = y * xin.SCALE + he / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, WHITE, False, updated_points, 1)

        pygame.draw.circle(win, xin.color, (x, y), xin.r)

        if not xin.sun:
            lengthen = FONT.render(f'{xin.n}' +" " + f'{"{:.3e}".format(xin.distance_to_sun / 1000)}km', 1, WHITE)
            win.blit(lengthen, (x - lengthen.get_width() / 2, y - lengthen.get_height() / 2))

    def attraction(self, o):
        o_x, o_y = o.x, o.y
        d_x = o_x - self.x
        d_y = o_y - self.y
        length = math.sqrt(d_x ** 2  + d_y ** 2)

        if o.sun:
            self.distance_to_sun = length

        force = self.G * self.mass * o.mass / length ** 2
        theta = math.atan2(d_y, d_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(joi, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if joi == planet:
                continue

            fx, fy = joi.attraction(planet)
            total_fx += fx
            total_fy += fy

        joi.x_vel += total_fx / joi.mass * joi.relative_time
        joi.y_vel += total_fy / joi.mass * joi.relative_time

        joi.x += joi.x_vel * joi.relative_time
        joi.y += joi.y_vel * joi.relative_time
        joi.orbit.append((joi.x, joi.y))
    # class moon(Planet):joi


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet("Sun", 0, 0, 30, YELLOW, 1.99e30)
    sun.sun = True

    e = Planet("Earth", -1 * Planet.A_U, 0, 20, BLUE, 5.974e24)
    e.y_vel = 29.783 * 1000

    m = Planet("Mars", -1.524 * Planet.A_U, 0, 15, RED, 6.4e23)
    m.y_vel = 24.077 * 1000

    me = Planet("Mercury", 0.387 * Planet.A_U, 0, 10, DARK_GREY, 3.3e23)
    me.y_vel = -47.4 * 1000

    v = Planet("Venus", 0.723 * Planet.A_U, 0, 16, VENUS, 4.87e24)
    v.y_vel = -35.02 * 1000

    planets = [sun, e, m, me, v]
    clk = 30
    while run:

        clock.tick(clk)
        S_S.fill((0, 0, 0))

        for event in pygame.event.get():
            key_input = pygame.key.get_pressed()
            if key_input[pygame.K_1]:
                clk += 5
            if key_input[pygame.K_2]:
                if clk <= 5:
                    pass
                else:
                    clk -= 5
            if key_input[pygame.K_SPACE]:
                paused(True)

            if key_input[pygame.K_x]:
                run = False
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(S_S)


        for i in L:

            pygame.draw.circle(S_S,(255-random.randint(10, 255), 255-random.randint(20, 255),255), i, 1)
        pygame.display.update()
    pygame.quit()


main()