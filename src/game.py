import pygame
import os
import random
from .settings import *
from .player import Player
from .obstacle import Obstacle

class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Side Scroller Jumper")
    self.clock = pygame.time.Clock()
    self.running = True
    self.game_over = False

    self.all_sprites = pygame.sprite.Group()
    self.obstacles = pygame.sprite.Group()

    self.player = Player()
    self.all_sprites.add(self.player)

    self.spawn_timer = random.randint(SPAWN_MIN_MS, SPAWN_MAX_MS)

    bg_path = os.path.join('assets', 'images', 'background.png')
    if os.path.exists(bg_path):
      self.bg_image = pygame.image.load(bg_path).convert()
      self.bg_image = pygame.transform.scale(
          self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
      self.bg_image = None

    self.bg_x = 0
    self.score = 0
    self.current_speed = INITIAL_SCROLL_SPEED

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False

      if not self.game_over:
        if event.type == pygame.KEYDOWN:
          if not self.player.is_jumping:
            # 通常ジャンプ：スペースキー
            if event.key == pygame.K_SPACE:
              self.player.jump(is_small=False)

          # 小ジャンプ：左コントロールキー
            elif event.key == pygame.K_LCTRL:
              self.player.jump(is_small=True)

      else:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE or event.key == pygame.K_LCTRL:
            self.__init__()

  def update(self):
    if not self.game_over:

      self.current_speed = INITIAL_SCROLL_SPEED + (self.score // 500)

      self.player.update()

      for obstacle in self.obstacles:
        obstacle.update(self.current_speed)

      self.spawn_timer -= self.clock.get_time()
      if self.spawn_timer <= 0:
        new_obstacle = Obstacle()
        self.all_sprites.add(new_obstacle)
        self.obstacles.add(new_obstacle)
        self.spawn_timer = random.randint(SPAWN_MIN_MS, SPAWN_MAX_MS)

      self.bg_x -= self.current_speed
      if self.bg_x <= -SCREEN_WIDTH:
        self.bg_x = 0

      if pygame.sprite.spritecollideany(self.player, self.obstacles):
        self.game_over = True

      self.score += 1

  def draw(self):
    if self.bg_image:
      self.screen.blit(self.bg_image, (self.bg_x, 0))
      self.screen.blit(self.bg_image, (self.bg_x + SCREEN_WIDTH, 0))
    else:
      self.screen.fill(WHITE)

    for sprite in self.all_sprites:
      self.screen.blit(sprite.image, sprite.rect)

    font = pygame.font.Font(None, 36)

    score_text = font.render(
        f"Score: {self.score}  Speed: {self.current_speed}", True, BLACK)
    self.screen.blit(score_text, (10, 10))

    if self.game_over:
      game_over_text = font.render(
          "GAME OVER - Press SPACE to Restart", True, BLACK)
      text_rect = game_over_text.get_rect(
          center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
      self.screen.blit(game_over_text, text_rect)

    pygame.display.flip()

  def run(self):
    while self.running:
      self.handle_events()
      self.update()
      self.draw()
      self.clock.tick(FPS)
    pygame.quit()
