"""종스크롤 슈팅 게임. 실행: python main.py"""
import sys

import pygame

from settings import (
    WIDTH, HEIGHT, FPS, TITLE, HIGHSCORE_FILE,
    ENEMY_SPAWN_MS, START_LIVES, SCORE_PER_ENEMY, FIRE_INTERVAL, HUNT_SECONDS,
    WHITE, YELLOW, RED, HUD_SHADE, GAME_OVER_SHADE,
)
from entities import Background, Player, Enemy

SPAWN_ENEMY = pygame.USEREVENT + 1  # "적을 하나 만들 때가 됐다"는 타이머 이벤트
PAUSE_ITEMS = ("Resume", "Main Menu", "Quit")  # 일시정지 메뉴 항목 (기본 글꼴은 한글이 안 나와서 영어)


def load_high_score():
    """HIGHSCORE_FILE 에서 최고 점수를 읽어 돌려준다."""
    try:
        with open(HIGHSCORE_FILE, encoding="utf-8") as f:
            return int(f.read().strip())
    except (OSError, ValueError):  # 파일 없음·읽기 실패(OSError), 숫자 아님·인코딩 오류(ValueError)
        return 0


def save_high_score(score):
    """최고 점수를 HIGHSCORE_FILE 에 저장한다."""
    try:
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
            f.write(str(score))
    except OSError:
        pass  # 저장 실패(쓰기 금지 폴더 등)로 게임이 멈추지 않게 함


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 72)
        pygame.time.set_timer(SPAWN_ENEMY, ENEMY_SPAWN_MS)
        self.background = Background()
        # 밝은 배경 위에서도 글자가 보이도록 깔아 줄 반투명 어두운 막
        self.hud_shade = pygame.Surface((WIDTH, 44), pygame.SRCALPHA)
        self.hud_shade.fill(HUD_SHADE)
        self.dark_shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # 시작·게임 오버 화면용
        self.dark_shade.fill(GAME_OVER_SHADE)
        self.high_score = load_high_score()
        self.running = True
        self.on_title = True  # True 면 시작 화면, SPACE 를 누르면 False 가 되며 게임 시작
        self.reset()

    def reset(self):
        """새 판을 시작한다. 스프라이트·점수·생명을 처음 상태로 되돌린다."""
        self.all_sprites = pygame.sprite.Group()  # 화면에 그릴 모든 스프라이트
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.score = 0
        self.lives = START_LIVES
        self.game_over = False
        self.paused = False
        self.pause_index = 0  # 일시정지 메뉴에서 고른 항목
        self.space_down = False  # 게임 중에 스페이스를 새로 눌러 연속 발사가 켜진 상태인가
        self.fire_cooldown = 0  # 다음 연속 발사까지 남은 프레임
        self.hunt_frames = HUNT_SECONDS * FPS  # 사냥 구간 남은 시간(프레임). 프레임으로 세서 일시정지 중엔 멈춘다

    # ---------------- 입력 ----------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.on_title:
                self.handle_title_event(event)  # 시작 화면 입력은 여기서만 처리
            elif self.paused:
                self.handle_pause_event(event)  # 일시정지 중 입력은 여기서만 처리 (적 생성·발사 없음)
            elif event.type == SPAWN_ENEMY and not self.game_over:
                enemy = Enemy()
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_over:
                        self.go_to_title()
                    else:
                        self.paused = True
                        self.pause_index = 0
                        self.space_down = False  # 일시정지 중에 누르고 뗀 키는 이어서 하기 전에 다시 눌러야 연사
                elif event.key == pygame.K_SPACE and not self.game_over:
                    self.fire_bullet()
                    self.space_down = True
                    self.fire_cooldown = FIRE_INTERVAL
                elif event.key == pygame.K_r and self.game_over:
                    self.reset()

    def fire_bullet(self):
        """플레이어 위치에서 총알 한 발을 쏜다."""
        bullet = self.player.shoot()
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def update_autofire(self, keys):
        """스페이스를 누르고 있는 동안 FIRE_INTERVAL 프레임마다 총알을 더 쏜다."""
        if not keys[pygame.K_SPACE]:
            self.space_down = False
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        if self.fire_cooldown == 0 and self.space_down:
            self.fire_bullet()
            self.fire_cooldown = FIRE_INTERVAL

    def handle_title_event(self, event):
        """시작 화면의 입력: SPACE 면 새 판 시작, ESC 면 종료. (적 생성·발사 없음)"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.on_title = False
                self.reset()
            elif event.key == pygame.K_ESCAPE:
                self.running = False

    def handle_pause_event(self, event):
        """일시정지 중의 입력: ↑/↓ 로 고르고 Enter 로 실행, ESC 면 이어서 진행."""
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.paused = False
        elif event.key == pygame.K_UP:
            self.pause_index = (self.pause_index - 1) % len(PAUSE_ITEMS)
        elif event.key == pygame.K_DOWN:
            self.pause_index = (self.pause_index + 1) % len(PAUSE_ITEMS)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            choice = PAUSE_ITEMS[self.pause_index]
            if choice == "Resume":
                self.paused = False
            elif choice == "Main Menu":
                self.go_to_title()
            elif choice == "Quit":
                self.running = False

    def go_to_title(self):
        """메인 메뉴(시작 화면)로 돌아간다. 판은 처음 상태로 돌아가고 최고 점수는 그대로 남는다."""
        self.on_title = True
        self.reset()

    # ---------------- 갱신 ----------------
    def update(self):
        if self.game_over or self.paused:
            return  # 게임 오버·일시정지면 화면(배경 포함)을 멈춤.

        self.background.update()
        if self.on_title:
            return  # 시작 화면에서는 배경만 흐름.

        if self.hunt_frames > 0:
            self.hunt_frames -= 1
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.update_autofire(keys)
        self.bullets.update()
        self.enemies.update()

        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        killed = {enemy for enemies in hits.values() for enemy in enemies}  # 총알 둘이 한 적을 맞혀도 한 번만 셈
        self.score += len(killed) * SCORE_PER_ENEMY

        self.lives -= len(pygame.sprite.spritecollide(self.player, self.enemies, True))

        # 화면 아래로 지나간 적은 없앨 것.
        for enemy in list(self.enemies):
            if enemy.rect.top > HEIGHT:
                enemy.kill()
                self.lives -= 1

        if self.lives <= 0:
            self.end_game()

    def end_game(self):
        """게임 오버 처리."""
        self.game_over = True
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)

    # ---------------- 그리기 ----------------
    def draw_text(self, text, font, color, **position):
        """글자를 화면에 그린다. 예: self.draw_text("Hi", self.font, WHITE, center=(240, 320))"""
        surface = font.render(text, True, color)
        self.screen.blit(surface, surface.get_rect(**position))

    def draw(self):
        self.background.draw(self.screen)
        if self.on_title:
            self.draw_title()
            pygame.display.flip()
            return
        self.all_sprites.draw(self.screen)
        if self.game_over:
            self.screen.blit(self.dark_shade, (0, 0))  # 게임 오버 글자가 잘 보이게
        self.screen.blit(self.hud_shade, (0, 0))  # 점수·생명 글자 뒤 어두운 띠
        self.draw_text(f"LIVES: {self.lives}", self.font, WHITE, topright=(WIDTH - 10, 10))
        self.draw_text(f"SCORE: {self.score}", self.font, WHITE, topleft=(10, 10))
        self.draw_hunt_timer()
        if self.game_over:
            self.draw_game_over()
        if self.paused:
            self.draw_pause()
        pygame.display.flip()

    def draw_hunt_timer(self):
        """화면 위 가운데에 사냥 구간 남은 시간(초)을 그린다. 5초 이하면 빨간색."""
        if self.hunt_frames > 0:
            seconds = (self.hunt_frames + FPS - 1) // FPS  # 올림: 20, 19, ... 1
            color = RED if seconds <= 5 else YELLOW
            self.draw_text(f"HUNT: {seconds}", self.font, color, midtop=(WIDTH // 2, 10))
        else:
            self.draw_text("HUNT: END", self.font, WHITE, midtop=(WIDTH // 2, 10))

    def draw_pause(self):
        """일시정지 화면."""
        cx = WIDTH // 2
        self.screen.blit(self.dark_shade, (0, 0))
        self.draw_text("PAUSED", self.big_font, YELLOW, center=(cx, 200))
        for i, item in enumerate(PAUSE_ITEMS):
            selected = i == self.pause_index
            label = f"> {item} <" if selected else item
            self.draw_text(label, self.font, YELLOW if selected else WHITE, center=(cx, 300 + i * 50))
        self.draw_text("UP/DOWN + ENTER   ESC : Resume", self.font, WHITE, center=(cx, 540))

    def draw_title(self):
        """시작 화면: 게임 이름, 플레이어 그림, 조작 안내, 깜빡이는 시작 안내."""
        cx = WIDTH // 2
        self.screen.blit(self.dark_shade, (0, 0))
        self.draw_text(TITLE, self.big_font, YELLOW, center=(cx, 150))
        self.screen.blit(self.player.image, self.player.image.get_rect(center=(cx, 270)))
        controls = ("LEFT / RIGHT : Move", "SPACE : Shoot", "R : Restart", "ESC : Quit")
        for i, line in enumerate(controls):
            self.draw_text(line, self.font, WHITE, center=(cx, 370 + i * 34))
        if pygame.time.get_ticks() // 500 % 2 == 0:  # 0.5초마다 깜빡임
            self.draw_text("Press SPACE to start", self.font, YELLOW, center=(cx, 540))

    def draw_game_over(self):
        """게임 오버 화면. self.game_over 가 True 일 때 draw() 가 부른다."""
        cx = WIDTH // 2
        self.draw_text("GAME OVER", self.big_font, RED, center=(cx, HEIGHT // 2 - 40))
        self.draw_text(f"SCORE: {self.score}", self.font, WHITE, center=(cx, HEIGHT // 2 + 20))
        self.draw_text(f"HIGH SCORE: {self.high_score}", self.font, YELLOW, center=(cx, HEIGHT // 2 + 60))
        self.draw_text("Press R to restart", self.font, WHITE, center=(cx, HEIGHT // 2 + 120))

    # ---------------- 게임 루프 ----------------
    def step(self):
        """한 프레임: 입력 → 갱신 → 그리기."""
        self.handle_events()
        self.update()
        self.draw()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.step()
        pygame.quit()


if __name__ == "__main__":
    Game().run()
    sys.exit()
