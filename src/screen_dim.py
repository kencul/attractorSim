# c:\Users\Ken\Documents\GitHub\attractorSim\src\screen_dim.py
import pygame

class ScreenDim:
    def __init__(self, info):
        """Initialize screen dimensions. Called only once due to singleton logic."""
        self.WIDTH = info.current_w
        self.HEIGHT = info.current_h