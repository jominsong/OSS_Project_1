"""개조: 보스와 보스 탄. 일반 적(Enemy)과는 별도로 다룬다 — main.py 의 self.enemies 에 넣지 않는다."""
import math

import pygame

from entities import load_frame
from settings import (
    WIDTH, HEIGHT, BOSS_FRAME, BOSS_SPEED, BOSS_Y, BOSS_ENTER_SPEED,
    BOSS_BULLET_RADIUS,
)

# 탄 색: (안쪽 색, 테두리 색). 초록 탄은 패링으로 튕겨낼 수 있다(다음 커밋에서 추가).
BULLET_COLORS = {
    "red": ((230, 50, 50), (255, 210, 210)),
    "green": ((60, 220, 90), (210, 255, 220)),
    "reflect": ((255, 215, 0), (255, 255, 200)),  # 패링으로 튕겨낸 탄 (금색)
}
_bullet_images = {}

# 탄막 패턴: 아래 시간표가 PATTERN_CYCLE 프레임마다 반복된다. (각도는 90도가 아래쪽)
PATTERN_CYCLE = 360
SPIRAL_END = 120  # 0 ~ 120: 좌우로 휘어지는 연발
SPIRAL_EVERY = 7
FAN_END = 240  # 120 ~ 240: 플레이어를 노리는 부채꼴
FAN_EVERY = 40
FAN_ANGLES = (-20, 0, 20)  # 가운데(0)가 플레이어를 정확히 노리는 탄
RING_EVERY = 60  # 240 ~ 360: 원형 링
RING_COUNT = 10
GREEN_EVERY = 90  # 위 패턴과 따로, 이 간격마다 플레이어를 노리는 초록 탄(패링용) 한 발. 빨간 탄과 겹쳐 나오게 느리게 쏜다
GREEN_AT = 45  # 한 주기 안에서 초록 탄을 쏘는 시점 (연발·부채꼴·링 발사 프레임과 겹치지 않게)
GREEN_SPEED = 3.5


def bullet_image(kind):
    """탄 그림(원). 같은 종류는 한 번만 만들어 둔다."""
    if kind not in _bullet_images:
        inner, edge = BULLET_COLORS[kind]
        size = BOSS_BULLET_RADIUS * 2
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(image, edge, (BOSS_BULLET_RADIUS, BOSS_BULLET_RADIUS), BOSS_BULLET_RADIUS)
        pygame.draw.circle(image, inner, (BOSS_BULLET_RADIUS, BOSS_BULLET_RADIUS), BOSS_BULLET_RADIUS - 2)
        _bullet_images[kind] = image
    return _bullet_images[kind]


class BossBullet(pygame.sprite.Sprite):
    """보스가 쏘는 탄. angle 은 도(degree), 90 이면 아래쪽."""

    def __init__(self, x, y, angle, speed, kind="red"):
        super().__init__()
        self.kind = kind
        self.image = bullet_image(kind)
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(speed, 0).rotate(angle)
        self.rect = self.image.get_rect(center=(round(x), round(y)))
        self.reflected = False  # 패링으로 튕겨낸 탄은 보스를 향해 날아가고 플레이어를 맞히지 않는다

    def reflect(self):
        """패링으로 튕겨낸다. 방향은 Game 이 매 프레임 보스 쪽으로 맞춰 준다."""
        self.reflected = True
        self.image = bullet_image("reflect")

    def update(self):
        self.pos += self.vel
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        margin = 40
        if not (-margin < self.rect.centerx < WIDTH + margin and -margin < self.rect.centery < HEIGHT + margin):
            self.kill()


class Boss(pygame.sprite.Sprite):
    """화면 위에서 내려와 좌우로 왕복하며 탄막을 쏘는 보스. 체력이 없어서 죽지 않고, 제한시간이 끝나면 사라진다."""

    def __init__(self):
        super().__init__()
        self.image = load_frame(*BOSS_FRAME)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, 0))  # 화면 위 바깥에서 시작
        self.direction = 1
        self.age = 0  # 자리를 잡은 뒤 지난 프레임. 탄막 패턴의 시간표 기준

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

    def shoot(self, target):
        """이번 프레임에 쏠 탄들을 돌려준다. target 은 플레이어 위치(노려 쏘는 탄에 쓴다). 내려오는 중엔 쏘지 않는다."""
        if self.entering:
            return []
        t = self.age % PATTERN_CYCLE
        self.age += 1
        x, y = self.rect.centerx, self.rect.bottom - 20
        bullets = []
        if t % GREEN_EVERY == GREEN_AT:
            aim = math.degrees(math.atan2(target[1] - y, target[0] - x))
            bullets.append(BossBullet(x, y, aim, GREEN_SPEED, "green"))
        if t < SPIRAL_END:
            if t % SPIRAL_EVERY == 0:
                angle = 90 + 60 * math.sin(t / 12)  # 아래쪽을 중심으로 좌우로 휘어짐
                bullets.append(BossBullet(x, y, angle, 3))
        elif t < FAN_END:
            if (t - SPIRAL_END) % FAN_EVERY == 0:
                aim = math.degrees(math.atan2(target[1] - y, target[0] - x))
                bullets += [BossBullet(x, y, aim + a, 4) for a in FAN_ANGLES]
        else:
            if (t - FAN_END) % RING_EVERY == 0:
                offset = 12 if ((t - FAN_END) // RING_EVERY) % 2 else 0  # 링마다 살짝 돌려서 빈틈이 달라지게
                bullets += [BossBullet(x, y, 360 / RING_COUNT * i + offset, 2.5) for i in range(RING_COUNT)]
        return bullets
