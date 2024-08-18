import pygame as pg
import math
import random
from shapely.geometry import Polygon

def sign(num):
    if num == 0:
        return 1
    return abs(num)/num

def rotate_poly(points, angle):
    rotated_points = []
    for p in points:
        dist = math.dist((0, 0), p)
        a = math.atan(p[1] / (p[0]+ 0.0000000001)) + (math.pi if p[0] < 0 else 0)
        rotated_points.append((dist*math.cos(angle + a), dist*math.sin(angle + a)))
    return rotated_points

def place_poly(points, center):
    new_points = []
    for p in points:
        new_points.append((p[0] + center[0], p[1] + center[1]))
    return new_points

def draw_on_ship(points, angle, position, color, screen):
    adjusted_points = place_poly(rotate_poly(points, angle), position)
    pg.draw.polygon(screen, color, adjusted_points, width=3)

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class Spaceship():
    def __init__(self, starting_coords, starting_angle, color, screen, shooting_type) -> None:
        super().__init__()
        self.position = pg.Vector2(starting_coords)
        self.angle = starting_angle
        self.color = color
        self.velocity = pg.Vector2(0, 0)
        self.angular_velocity = 0
        self.screen = screen
        self.fire = False
        self.bullets = []
        self.health = 100
        self.damage_decay = 0
        self.damage_taken = 0
        self.shooting_type = shooting_type
        self.stun = 0
    
    def fly_forward(self):
        if self.stun > 0:
            return
        MAX_VEL = 10
        accel = 0.2
        self.velocity += pg.Vector2(accel * math.cos(self.angle), accel * math.sin(self.angle)) 
        if math.dist((0, 0), self.velocity) > MAX_VEL:
            self.velocity.scale_to_length(MAX_VEL)
        
        # Draw Fire
        self.fire = True

    
    def fly_turn(self, dir):
        if self.stun > 0:
            return
        MAX_ANG_VEL = 0.05
        accel = 0.002
        self.angular_velocity += accel * dir
        if abs(self.angular_velocity) > MAX_ANG_VEL:
            self.angular_velocity = MAX_ANG_VEL * dir
    
    def update(self):
        if self.damage_decay > 0:
            self.damage_decay -= 1
        elif self.damage_taken > 0:
            self.damage_taken -= 1
        self.hitbox = [
            pg.Vector2(30*math.cos(self.angle), 30*math.sin(self.angle)) + pg.Vector2(17*math.cos(self.angle + math.pi/2), 17*math.sin(self.angle + math.pi/2)) + self.position,
            pg.Vector2(30*math.cos(self.angle), 30*math.sin(self.angle)) + pg.Vector2(17*math.cos(self.angle - math.pi/2), 17*math.sin(self.angle - math.pi/2)) + self.position,
            pg.Vector2(-30*math.cos(self.angle), -30*math.sin(self.angle)) + pg.Vector2(-17*math.cos(self.angle + math.pi/2), -17*math.sin(self.angle + math.pi/2)) + self.position,
            pg.Vector2(-30*math.cos(self.angle), -30*math.sin(self.angle)) + pg.Vector2(-17*math.cos(self.angle - math.pi/2), -17*math.sin(self.angle - math.pi/2)) + self.position,

        ]
        pg.draw.polygon(self.screen, 'green', self.hitbox, 3)
        self.velocity[0] *= 0.98
        self.velocity[1] *= 0.98
        self.angular_velocity *= 0.98
        if abs(self.angular_velocity) < 0.0001:
            self.angular_velocity = 0
        if abs(self.velocity[0]) < 0.001:
            self.velocity[0] = 0
        if abs(self.velocity[1]) < 0.001:
            self.velocity[1] = 0
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.angle += self.angular_velocity
        self.position[0] %= 1366
        self.position[1] %= 768
        self.stun = max(0, self.stun - 1)
        for bullet in self.bullets:
            bullet.update()
            if bullet.clock < 0: self.bullets.remove(bullet)

    def draw_health(self):
        flip = 1 if self.position[1] > 55 else -1
        pg.draw.line(self.screen, '#555555', (clamp(-50+self.position[0], 0, 1366-100), -50*flip+self.position[1]), 
                     (clamp(50+self.position[0], 100, 1366), -50*flip+self.position[1]), 10)
        if self.damage_taken > 0:
            pg.draw.line(self.screen, pg.Color(255, 200, 200), (clamp(-50+self.position[0], 0, 1366-100), -50*flip+self.position[1]), 
                     (clamp(-50+self.health+self.damage_taken+self.position[0], 0+self.health+self.damage_taken, 1366-100+self.health+self.damage_taken), -50*flip+self.position[1]), 10)
        pg.draw.line(self.screen, pg.Color(clamp(int(255-self.health*2.55), 0, 255), clamp(int(self.health*2.55), 0, 255), 0), (clamp(-50+self.position[0], 0, 1366-100), -50*flip+self.position[1]), 
                     (clamp(-50+self.health+self.position[0], self.health, 1366-100+self.health), -50*flip+self.position[1]), 10)
        
        if self.stun > 0:
            charge = []
            detail = 10
            for i in range(detail):
                mult = random.randint(2, 30)
                charge.append((mult*math.cos(i*math.pi/detail*2), mult*math.sin(i*math.pi/detail*2)))
            draw_on_ship(charge, self.angle, self.position, 'yellow', self.screen)

        
class Alpha(Spaceship):
    def __init__(self, starting_coords, starting_angle, color, screen) -> None:
        super().__init__(starting_coords, starting_angle, color, screen, 'tap')
        self.cannon_charge = 0
        self.CANNON_MAX = 50
    def update(self):
        if self.stun > 0:
            self.cannon_charge = 0
        else:
            self.cannon_charge += 1
        return super().update()
    def shoot(self):
        if self.cannon_charge < self.CANNON_MAX or self.stun > 0:
            return
        self.bullets.append(Charge(self.position, self.velocity, self.angle, self.screen))
        self.cannon_charge = 0
    def draw(self):
        ship = [(30, 16), (17, 12), (3, 4), (-3, 4), (-17, 12), (-30, 4), (-25, 0),
                (-30, -4), (-17, -12), (-3, -4), (3, -4), (17, -12), (30, -16), 
                (18, -6), (15, 0), (18, 6)]
        draw_on_ship(ship, self.angle, self.position, self.color, self.screen)

        if not self.stun > 0:
            charge = []
            filled = min(1, self.cannon_charge / self.CANNON_MAX)
            for i in range(10):
                mult = random.randint(5, 10) * filled
                charge.append((mult*math.cos(i*math.pi/5) + 30, mult*math.sin(i*math.pi/5)))
            draw_on_ship(charge, self.angle, self.position, pg.Color(255, 255, int(255-255*filled)), self.screen)

        if self.fire:        
            fire = [(-30, 4), (-50 + random.randint(-3, 3), random.randint(-3, 3)), (-30, -4), (-25, 0)]
            draw_on_ship(fire, self.angle, self.position, 'orange', self.screen)
            self.fire = False
        return super().draw_health()

class Beta(Spaceship):
    def __init__(self, starting_coords, starting_angle, color, screen) -> None:
        super().__init__(starting_coords, starting_angle, color, screen, 'hold')
        self.cannon_cooldown = 5
        self.side = 1
    def update(self):
        self.cannon_cooldown = max(self.cannon_cooldown - 1, 0)
        return super().update()
    def shoot(self):
        if self.cannon_cooldown > 0 or self.stun > 0:
            return
        self.cannon_cooldown = 5
        self.bullets.append(Bullet(self.position, self.velocity, self.angle, self.side, self.screen))
        self.side *= -1
    def draw(self):
        ship = [[-30, 10], [-15, 17], [4, 12], [-15, 6], [15, 2], [20, 6], [30, 2], [30, -2], [20, -6], [15, -2], [-15, -6], [4, -12], [-15, -17], [-30, -10], [-20, 0]]
        draw_on_ship(ship, self.angle, self.position, self.color, self.screen)
        
        if self.fire:        
            fire = [(-25, -5), (-50 + random.randint(-3, 3), random.randint(-3, 3)), (-25, 5), (-20, 0)]
            draw_on_ship(fire, self.angle, self.position, 'orange', self.screen)
            self.fire = False
        return super().draw_health()
class Gamma(Spaceship):
    def __init__(self, starting_coords, starting_angle, color, screen) -> None:
        super().__init__(starting_coords, starting_angle, color, screen, 'hold')
        self.charge = 0
        self.max_charge = 200

    def update(self):
        if self.stun > 0:
            self.bullets = []
            self.charge = 0
        if len(self.bullets):
            self.bullets[0].position = self.position
            self.bullets[0].angle = self.angle
            self.charge -= 1
        else:
            self.charge = min(self.max_charge, self.charge + 1)
        if self.charge == 0:
            self.bullets = []
        super().update()

    def shoot(self):
        if self.stun > 0:
            return
        if self.charge == self.max_charge:
            self.bullets = [Laser(self.position, self.angle, self.screen)]

    def draw(self):
        pg.draw.circle(self.screen, self.color, self.position, 10)
        
        flip = 1 if self.position[1] > 55 else -1
        pg.draw.line(self.screen, '#555555', (clamp(-50+self.position[0], 0, 1366-100), -75*flip+self.position[1]), 
                     (clamp(50+self.position[0], 100, 1366), -75*flip+self.position[1]), 10)
        if self.charge > 0:
            cp = int(self.charge / self.max_charge * 100)
            pg.draw.line(self.screen, 'red', (clamp(-50+self.position[0], 0, 1366-100), -75*flip+self.position[1]), 
                        (clamp(-50+cp+self.position[0], cp, 1366-100+cp), -75*flip+self.position[1]), 10)
        super().draw_health()

class Charge:
    def __init__(self, position, velocity, angle, screen):
        self.position = pg.Vector2(position) + pg.Vector2(20*math.cos(angle), 20*math.sin(angle))
        speed = 20
        self.velocity = pg.Vector2(velocity) + pg.Vector2(speed*math.cos(angle), speed*math.sin(angle))
        self.angle = angle
        self.screen = screen
        self.clock = 100
        self.maxclock = self.clock
        self.size = 1
        self.damage = self.size * 6
    def update(self):
        self.clock -= 1
        self.size += 0.1
        self.damage = self.size * 8
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.draw()
        l = self.size * 10
        w = self.size * 10
        self.hitbox = [
            pg.Vector2(l*math.cos(self.angle), l*math.sin(self.angle)) + pg.Vector2(w*math.cos(self.angle + math.pi/2), w*math.sin(self.angle + math.pi/2)) + self.position,
            pg.Vector2(l*math.cos(self.angle), l*math.sin(self.angle)) + pg.Vector2(w*math.cos(self.angle - math.pi/2), w*math.sin(self.angle - math.pi/2)) + self.position,
            pg.Vector2(-l*math.cos(self.angle), -l*math.sin(self.angle)) + pg.Vector2(-w*math.cos(self.angle + math.pi/2), -w*math.sin(self.angle + math.pi/2)) + self.position,
            pg.Vector2(-l*math.cos(self.angle), -l*math.sin(self.angle)) + pg.Vector2(-w*math.cos(self.angle - math.pi/2), -w*math.sin(self.angle - math.pi/2)) + self.position,
        ]
        pg.draw.polygon(self.screen, 'green', self.hitbox, 3)

    def draw(self):
        charge = []
        detail = 10
        for i in range(detail):
            mult = random.randint(5, 10) * self.size
            charge.append((mult*math.cos(i*math.pi/detail*2), mult*math.sin(i*math.pi/detail*2)))
        draw_on_ship(charge, self.angle, self.position, 'yellow', self.screen)

class Bullet():
    def __init__(self, position, velocity, angle, side, screen):
        self.position = pg.Vector2(position) + pg.Vector2(-10*math.cos(angle), -10*math.sin(angle)) + pg.Vector2(12*math.cos(angle+math.pi/2 * side), 12*math.sin(angle+math.pi/2*side))
        speed = 20
        self.velocity = pg.Vector2(velocity) + pg.Vector2(speed*math.cos(angle), speed*math.sin(angle))
        self.angle = angle
        self.screen = screen
        self.clock = 100
        self.maxclock = self.clock
        self.damage = 2
        self.size = 2
    def update(self):
        self.clock -= 1
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.draw()
        l = 15
        w = self.size * 3
        self.hitbox = [
            pg.Vector2(l*math.cos(self.angle), l*math.sin(self.angle)) + pg.Vector2(w*math.cos(self.angle + math.pi/2), w*math.sin(self.angle + math.pi/2)) + self.position,
            pg.Vector2(l*math.cos(self.angle), l*math.sin(self.angle)) + pg.Vector2(w*math.cos(self.angle - math.pi/2), w*math.sin(self.angle - math.pi/2)) + self.position,
            pg.Vector2(-l*math.cos(self.angle), -l*math.sin(self.angle)) + pg.Vector2(-w*math.cos(self.angle + math.pi/2), -w*math.sin(self.angle + math.pi/2)) + self.position,
            pg.Vector2(-l*math.cos(self.angle), -l*math.sin(self.angle)) + pg.Vector2(-w*math.cos(self.angle - math.pi/2), -w*math.sin(self.angle - math.pi/2)) + self.position,

        ]
        pg.draw.polygon(self.screen, 'green', self.hitbox, 3)
    def draw(self):
        bullet = [[0, 3], [0, -3], [15, 0]]
        draw_on_ship(bullet, self.angle, self.position, 'white', self.screen)

class Laser:
    def __init__(self, position, angle, screen):
        self.position = position
        self.angle = angle
        self.screen = screen
        self.hitbox = []
        self.damage = 0.8
        self.pulse = 0
        self.flare = 0
        self.clock = 3600
    def update(self):
        self.pulse = self.pulse%math.pi + math.pi/100
        self.flare += 50
        self.flare %= 2000
        self.draw()
    def draw(self):
        l = 2000
        w = 10
        self.hitbox = [
            pg.Vector2(l*math.cos(self.angle), l*math.sin(self.angle)) + pg.Vector2(w*math.cos(self.angle + math.pi/2), w*math.sin(self.angle + math.pi/2)) + self.position,
            pg.Vector2(l*math.cos(self.angle), l*math.sin(self.angle)) + pg.Vector2(w*math.cos(self.angle - math.pi/2), w*math.sin(self.angle - math.pi/2)) + self.position,
            pg.Vector2(4*math.cos(self.angle), -4*math.sin(self.angle)) + pg.Vector2(-w*math.cos(self.angle + math.pi/2), -w*math.sin(self.angle + math.pi/2)) + self.position,
            pg.Vector2(4*math.cos(self.angle), -4*math.sin(self.angle)) + pg.Vector2(-w*math.cos(self.angle - math.pi/2), -w*math.sin(self.angle - math.pi/2)) + self.position,
        ]
        pg.draw.circle(self.screen, 'red', self.position + pg.Vector2(self.flare*math.cos(self.angle), self.flare*math.sin(self.angle)), 15)
        nf = (self.flare + 1000)%2000
        pg.draw.circle(self.screen, 'red', self.position + pg.Vector2(nf*math.cos(self.angle), nf*math.sin(self.angle)), 15)
        pg.draw.line(self.screen, 'red', self.position, self.position + pg.Vector2(2000*math.cos(self.angle), 2000*math.sin(self.angle)), int(8 * math.sin(self.pulse) + 16))
        pg.draw.line(self.screen, 'white', self.position, self.position + pg.Vector2(2000*math.cos(self.angle), 2000*math.sin(self.angle)), int(5 * math.sin(self.pulse) + 10))

def checkdamage(ship1: Spaceship, ship2: Spaceship):
    for i in ship1.bullets:
        hit2 = Polygon(ship2.hitbox)
        hitb = Polygon(i.hitbox)
        if hit2.intersects(hitb):
            ship2.health -= i.damage
            ship2.damage_taken += i.damage
            ship2.damage_decay = 30
            if type(i) != Laser: ship1.bullets.remove(i)
            if type(i) == Charge: ship2.stun = 30
            return [1, i.damage]
    for i in ship2.bullets:
        hit1 = Polygon(ship1.hitbox)
        hitb = Polygon(i.hitbox)
        if hit1.intersects(hitb):
            ship1.health -= i.damage
            ship1.damage_taken += i.damage
            ship1.damage_decay = 30
            if type(i) != Laser: ship2.bullets.remove(i)
            if type(i) == Charge: ship1.stun = 30
            return [0, i.damage]
    return [-1, -1]