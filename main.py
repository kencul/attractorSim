import pygame
import math
import random

# Setup
pygame.init()

# Get the resolution of your actual monitor
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

# Initialize the screen with the FULLSCREEN flag
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# WIDTH, HEIGHT = 1000, 800
# screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Constants
G = 0.5  # Gravitational constant
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
NUM_ORBS = 50

DISTANCE = 50


# Define your two gradient colors
COLOR_START = (255, 50, 50)  # Red
COLOR_END = (50, 255, 255)    # Cyan


class Orb:
    def __init__(self, x, y, mass, color):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.mass = mass
        self.radius = int(mass * 2)
        self.history = []
        self.color = color

    def apply_gravity(self, attractor_pos, attractor_mass, dt):
        # # Calculate distance vector
        direction = attractor_pos - self.pos
        
        # Fixed distance for constant gravitational pull strength

        # Calculate force magnitude: F = G * (m1 * m2) / r^2
        strength = (G * self.mass * attractor_mass) / (DISTANCE ** 2)
        
        # Apply acceleration (Force / mass)
        acceleration = direction.normalize() * strength
        self.vel += acceleration

    def update(self, dt):
        # Keep track of movement for trail effect
        self.history.append(pygame.Vector2(self.pos))
        if len(self.history) > 20: # Length of the trail
            self.history.pop(0)
            
        self.pos += self.vel * dt
        
        # Check for edge collisions and set position and velocity
        # Check Left and Right edges
        if self.pos.x <= self.radius:
            self.pos.x = self.radius
            self.vel.x = 0
        elif self.pos.x >= WIDTH - self.radius:
            self.pos.x = WIDTH - self.radius
            self.vel.x = 0

        # Check Top and Bottom edges
        if self.pos.y <= self.radius:
            self.pos.y = self.radius
            self.vel.y = 0
        elif self.pos.y >= HEIGHT - self.radius:
            self.pos.y = HEIGHT - self.radius
            self.vel.y = 0

    def draw(self, surface):
        # Calculate distance to attractor
        dist = self.pos.distance_to(attractor_pos)
        
        # Map distance to a 0.0 - 1.0 range (t)
        # 500 pixels is the "max distance" for the gradient; adjust as needed
        max_dist = 1500
        t = min(dist / max_dist, 1.0)
        
        # 3. Update the color based on distance
        self.color = lerp_color(COLOR_START, COLOR_END, t)
        
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

def lerp_color(c1, c2, t):
    """Linearly interpolates between two RGB colors."""
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t)
    )

# Initialize Attractor and Orbs
attractor_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
attractor_mass = 100
orbs = [Orb(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(2, 5), lerp_color(COLOR_START, COLOR_END, i/NUM_ORBS)) for i in range(NUM_ORBS)]

# Hide mouse cursor
pygame.mouse.set_visible(False)

pulse_time = 0
attractor_surf_size = 60
attractor_surface = pygame.Surface((attractor_surf_size, attractor_surf_size), pygame.SRCALPHA)

# Main Loop
running = True
while running:
    # Check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # set attractor position to mouse position
    attractor_pos = pygame.Vector2(pygame.mouse.get_pos())
    
    # dt is the time in seconds since the last frame
    dt = clock.tick(180) / (1000/180)

    # Clear the actual screen every frame
    screen.fill((10, 10, 20))
    
    #--------------------------------------------------------------------
    pulse_time += dt * 0.01
    # This creates a value between 0.7 and 1.0 for the size pulse
    pulse_scale = 0.85 + math.sin(pulse_time) * 0.15
    # This creates a value between 100 and 255 for the transparency pulse
    alpha_pulse = 200 + math.sin(pulse_time) * 55
    
    # Clear the attractor surface
    attractor_surface.fill((0, 0, 0, 0))
    
    # 3. Draw a "Glow" (The transparent edges)
    # We draw multiple circles with decreasing alpha to create a soft edge
    glow_radius = int(25 * pulse_scale)
    for r in range(glow_radius, 0, -2):
        # Calculate alpha for this specific ring (fades outward)
        alpha = int((alpha_pulse * (1 - r/glow_radius)) * 0.5)
        pygame.draw.circle(attractor_surface, (255, 255, 0, alpha), (30, 30), r)

    # 4. Draw the core (The solid center)
    pygame.draw.circle(attractor_surface, (255, 255, 0, int(alpha_pulse)), (30, 30), int(8 * pulse_scale))

    # 5. Blit (paste) the surface onto the screen at the mouse position
    screen.blit(attractor_surface, (attractor_pos.x - 30, attractor_pos.y - 30))
    # -----------------------------------------------------------------------------

    # Draw Attractor
    #pygame.draw.circle(screen, YELLOW, (int(attractor_pos.x), int(attractor_pos.y)), 10)

    for orb in orbs:
        orb.apply_gravity(attractor_pos, attractor_mass, dt)
        orb.update(dt)
        orb.draw(screen)
    
    pygame.display.flip()

pygame.quit()