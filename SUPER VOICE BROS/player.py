import pygame
from .config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
      
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = False
        
    def update(self):
        self.vel_y += self.gravity

        self.rect.x += self.vel_x

        self.rect.y += self.vel_y
)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.bottom > SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.on_ground = True
            self.vel_y = 0
        else:
            self.on_ground = False
    
    def move_left(self):
        self.vel_x = -self.speed
    
    def move_right(self):
        self.vel_x = self.speed
    
    def stop(self):
        self.vel_x = 0
    
    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
