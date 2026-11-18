"""개조: 좌우로 흔들리며 내려오는 적. 기본 Enemy 를 그대로 물려받고 움직임만 추가한다."""
import math
import random

import pygame

from settings import WIDTH, WAVE_AMPLITUDE_MIN, WAVE_AMPLITUDE_MAX, WAVE_SPEED
from entities import Enemy


class WaveEnemy(Enemy):
    """아래로 내려오면서 좌우로 출렁이는 적. 일반 적과 구분되게 붉은 빛이 돈다."""

    def __init__(self):
        super().__init__()
        self.image = self.image.copy()  # load_frame 이 그림을 캐시해서 돌려주므로 복사해서 색을 입힌다
        self.image.fill((255, 140, 140), special_flags=pygame.BLEND_MULT)
        self.amplitude = random.randint(WAVE_AMPLITUDE_MIN, WAVE_AMPLITUDE_MAX)  # 좌우로 흔들리는 폭(픽셀)
        self.phase = random.uniform(0, 2 * math.pi)
        self.age = 0  # 프레임 수. update 가 불릴 때만 늘어서 일시정지 중엔 멈춘다
        # 흔들려도 화면 밖으로 나가지 않도록 중심 위치를 안쪽으로 제한
        low = self.amplitude
        high = WIDTH - self.rect.width - self.amplitude
        self.base_x = min(max(self.rect.x, low), high)

    def update(self):
        super().update()  # 아래로 내려오는 건 기본 적과 같음
        self.age += 1
        self.rect.x = round(self.base_x + self.amplitude * math.sin(self.age * WAVE_SPEED + self.phase))
