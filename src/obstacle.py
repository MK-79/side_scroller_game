import pygame
import os
import random
# settings.pyから地面の高さ(GROUND_Y)などをインポート
from .settings import *

class Obstacle(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()

    # 岩の高さを少し調整（お好みで）
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
    # 【修正】障害物の底面を、地面の高さ(GROUND_Y)に合わせます
    self.rect.bottom = GROUND_Y

  def update(self, speed):
    self.rect.x -= speed
    if self.rect.right < 0:
      self.kill()
