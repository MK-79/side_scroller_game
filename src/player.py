import pygame
import os
from .settings import *

class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()

    self.walk_frames = []
    self.frame_index = 0
    self.last_update = pygame.time.get_ticks()

    sheet_path = os.path.join('assets', 'images', 'player_sheet.png')
    if os.path.exists(sheet_path):
      sprite_sheet = pygame.image.load(sheet_path).convert()
      sprite_sheet.set_colorkey(WHITE)

      sheet_width, sheet_height = sprite_sheet.get_size()

      frame_w = sheet_width // 4
      frame_h = sheet_height // 4

      for i in range(4):
        frame = sprite_sheet.subsurface(
            (i * frame_w, frame_h * 3, frame_w, frame_h))
        scaled_frame = pygame.transform.scale(
            frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.walk_frames.append(scaled_frame)
    else:
      fallback_surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
      fallback_surface.fill(PLAYER_COLOR)
      self.walk_frames = [fallback_surface for _ in range(4)]

    self.image = self.walk_frames[self.frame_index]
    self.rect = self.image.get_rect()
    self.rect.x = PLAYER_START_X
    self.rect.bottom = GROUND_Y

    self.velocity_y = 0
    self.is_jumping = False

  def jump(self, is_small=False):
    if not self.is_jumping:

      if is_small:
        self.velocity_y = SMALL_JUMP  # 小ジャンプ
      else:
        self.velocity_y = -18  # 　通常ジャンプ
      self.is_jumping = True

  def update_animation(self):
    current_time = pygame.time.get_ticks()
    if current_time - self.last_update >= ANIMATION_COOLDOWN:
      self.frame_index += 1
      if self.frame_index >= len(self.walk_frames):
        self.frame_index = 0
      old_bottom = self.rect.midbottom
      self.image = self.walk_frames[self.frame_index]
      self.rect = self.image.get_rect()
      self.rect.midbottom = old_bottom
      self.last_update = current_time

  def update(self):
    self.update_animation()
    self.velocity_y += GRAVITY
    self.rect.y += self.velocity_y
    if self.rect.bottom >= GROUND_Y:
      self.rect.bottom = GROUND_Y
      self.velocity_y = 0
      self.is_jumping = False
