import pygame
import math
import random
from config import GRAVITY, COLOR_START, COLOR_MIDDLE, COLOR_END, DISTANCE, COLOR_MODE, MAX_SPEED
from screen_dim import ScreenDim
import pygame

class Orb:
    def __init__(self, x, y, mass, screen_dim, color = COLOR_START):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.mass = mass
        self.radius = int(mass * 2)
        self.history = []
        self.color = color
        self.screen_dim = screen_dim

    def apply_gravity(self, attractor_pos, attractor_mass, dt):
        # # Calculate distance vector
        direction = attractor_pos - self.pos

        # Calculate force magnitude: F = G * (m1 * m2) / r^2
        strength = (GRAVITY * self.mass * attractor_mass) / (DISTANCE ** 2)
        
        # Apply acceleration (Force / mass)
        acceleration = direction.normalize() * strength
        self.vel += acceleration * dt
        
    @staticmethod # static because it doesn't acces member vars and is only used in this class 
    def lerp_color(c1, c2, t):
        """Linearly interpolates between two RGB colors."""
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t)
        )

    def update(self, dt):
        # Keep track of movement for trail effect
        self.history.append(pygame.Vector2(self.pos))
        if len(self.history) > 20: # Length of the trail
            self.history.pop(0)
        self.pos += self.vel * dt
    
        #print(f"Screen dimensions in Orb.update: {screen_dim.width}x{screen_dim.height}")

        # Check for edge collisions and set position and velocity
        # Check Left and Right edges
        if self.pos.x <= self.radius:
            self.pos.x = self.radius
            self.vel.x = 0
        elif self.pos.x >= self.screen_dim.WIDTH - self.radius:
            self.pos.x = self.screen_dim.WIDTH - self.radius
            self.vel.x = 0

        # Check Top and Bottom edges
        if self.pos.y <= self.radius:
            self.pos.y = self.radius
            self.vel.y = 0
        elif self.pos.y >= self.screen_dim.HEIGHT - self.radius:
            self.pos.y = self.screen_dim.HEIGHT - self.radius
            self.vel.y = 0

    def draw(self, surface, attractor_pos):
        # Calculate distance to attractor
        if COLOR_MODE == "speed":
            speed = self.vel.length()
            max_speed = MAX_SPEED
            
            t = min(speed / max_speed, 1.0)
        elif COLOR_MODE == "distance":
            dist = self.pos.distance_to(attractor_pos)
            max_dist = 900
        
            # Map distance to a 0.0 - 1.0 range (t)
            # 500 pixels is the "max distance" for the gradient; adjust as needed
            t = min(dist / max_dist, 1.0)
        
        # Add middle color in the gradient (COLOR_MIDDLE)
        if t <= 0.5:
            self.color = Orb.lerp_color(COLOR_START, COLOR_MIDDLE, 2 * t)
        else:
            self.color = Orb.lerp_color(COLOR_MIDDLE, COLOR_END, 2 * (t - 0.5))
        
        history_len = len(self.history)
        if history_len > 2:
            for i in range(history_len - 1):
                p1 = self.history[i]
                p2 = self.history[i + 1]
                thickness = int(self.radius * 2 * (i / history_len))
                if thickness < 1: thickness = 1
                
                pygame.draw.line(surface, self.color, p1, p2, thickness)
                # Add a circle at the joint to smooth the corners
                pygame.draw.circle(surface, self.color, (int(p1.x), int(p1.y)), thickness // 3)
            
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
       

