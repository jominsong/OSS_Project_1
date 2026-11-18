"""개조: 보스. 일반 적(Enemy)과는 별도로 다룬다 — main.py 의 self.enemies 에 넣지 않는다."""
import pygame

from entities import load_frame
from settings import WIDTH, BOSS_FRAME, BOSS_SPEED, BOSS_Y, BOSS_ENTER_SPEED


class Boss(pygame.sprite.Sprite):
    """화면 위에서 내려와 좌우로 왕복하는 보스. 체력이 없어서 죽지 않고, 제한시간이 끝나면 사라진다."""

    def __init__(self):
        super().__init__()
        self.image = load_frame(*BOSS_FRAME)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, 0))  # 화면 위 바깥에서 시작
        self.direction = 1

    @property
    def entering(self):
        """아직 자리를 잡으러 내려오는 중인가."""
        return self.rect.top < BOSS_Y

    def update(self):
        if self.entering:
            self.rect.y = min(self.rect.y + BOSS_ENTER_SPEED, BOSS_Y)
            return
        self.rect.x += self.direction * BOSS_SPEED
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.direction = -1
