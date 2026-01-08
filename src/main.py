import pygame
import math
import random
from orb import Orb
from config import NUM_ORBS
from screen_dim import ScreenDim

# Setup
pygame.init()

# Get the resolution of your actual monitor
info = pygame.display.Info()

# Initialize the screen with the FULLSCREEN flag
screen_dim = ScreenDim(info)
screen = pygame.display.set_mode((screen_dim.WIDTH, screen_dim.HEIGHT), pygame.FULLSCREEN)
print(f"Screen dimensions: {screen_dim.WIDTH}x{screen_dim.HEIGHT}")
# WIDTH, HEIGHT = 1000, 800
# screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Initialize Attractor and Orbs
attractor_pos = pygame.Vector2(screen_dim.WIDTH // 2, screen_dim.HEIGHT // 2)
attractor_mass = 500
orbs = [Orb(random.randint(0, screen_dim.WIDTH), random.randint(0, screen_dim.HEIGHT), random.uniform(2, 5), screen_dim) for _ in range(NUM_ORBS)]

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
    
    # ----- Attractor Drawing with Pulsing Effect -----
    pulse_time += dt * 0.01
    # value between 0.7 and 1.0 for the size pulse
    pulse_scale = 0.85 + math.sin(pulse_time) * 0.15
    # value between 200 and 255 for the transparency pulse
    alpha_pulse = 200 + math.sin(pulse_time) * 55
    
    # Clear the attractor surface
    attractor_surface.fill((0, 0, 0, 0))
    
    # Draw a transparent edges by drawing multiple circles with decreasing alpha to create a soft edge
    glow_radius = int(25 * pulse_scale)
    for r in range(glow_radius, 0, -2):
        # Calculate alpha for this specific ring
        alpha = int((alpha_pulse * (1 - r/glow_radius)) * 0.5)
        pygame.draw.circle(attractor_surface, (255, 255, 0, alpha), (30, 30), r)

    # Draw the solid center
    pygame.draw.circle(attractor_surface, (255, 255, 0, int(alpha_pulse)), (30, 30), int(8 * pulse_scale))

    # Blit the surface onto the screen at the mouse position
    screen.blit(attractor_surface, (attractor_pos.x - 30, attractor_pos.y - 30))
    # -----------------------------------------------------------------------------

    for orb in orbs:
        orb.apply_gravity(attractor_pos, attractor_mass, dt)
        orb.update(dt)
        orb.draw(screen, attractor_pos)

    pygame.display.flip()

pygame.quit()