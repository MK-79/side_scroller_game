import pygame
import os
import random
from .settings import *

class Obstacle(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()

    height = random.randint(40, 80)

    image_path = os.path.join('assets', 'images', 'obstacle.png')
    if os.path.exists(image_path):
      self.image = pygame.image.load(image_path).convert()
      self.image.set_colorkey(BLACK)
      self.image = pygame.transform.scale(
          self.image, (OBSTACLE_WIDTH, height))
    else:
      self.image = pygame.Surface((OBSTACLE_WIDTH, height))
      self.image.fill(OBSTACLE_COLOR)

    self.rect = self.image.get_rect()
    self.rect.inflate_ip(-20, -20)
    self.rect.x = SCREEN_WIDTH
    self.rect.bottom = GROUND_Y

  def update(self, speed):
    self.rect.x -= speed
    if self.rect.right < 0:
      self.kill()
