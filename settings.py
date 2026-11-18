"""게임 전체에서 쓰는 설정값(상수) 모음."""
import os

# 화면
WIDTH = 480
HEIGHT = 640
FPS = 60
TITLE = "Vertical Shooter"

# 파일 위치 (이 파일이 있는 폴더 기준)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")
HIGHSCORE_FILE = os.path.join(BASE_DIR, "highscore.txt")

# 스프라이트 시트에서 잘라 쓸 칸: (파일, (x, y, 가로, 세로), 확대 배율)
PLAYER_FRAME = ("ship.png", (32, 0, 16, 24), 3)        # 48 x 72
BULLET_FRAME = ("laser-bolts.png", (6, 18, 5, 12), 2)  # 10 x 24
ENEMY_FRAMES = (
    ("enemy-small.png", (0, 0, 16, 16), 3),            # 48 x 48
    ("enemy-medium.png", (0, 0, 32, 16), 2),           # 64 x 32
    ("enemy-big.png", (3, 2, 26, 30), 2),              # 52 x 60
)

# 배경 (아래로 흐르는 속도, 픽셀/프레임)
BACKGROUND_IMAGE = "desert-backgorund-looped.png"
CLOUDS_IMAGE = "clouds-transparent.png"
BACKGROUND_SCALE = 2
BACKGROUND_SPEED = 1
CLOUDS_SPEED = 2

# 플레이어
PLAYER_SPEED = 6

# 총알
BULLET_SPEED = 10
FIRE_INTERVAL = 9  # 스페이스를 누르고 있을 때 연속 발사 간격 (프레임, 60FPS 에서 0.15초)

# 적
ENEMY_SPEED_MIN = 2
ENEMY_SPEED_MAX = 4
ENEMY_SPAWN_MS = 700  # 몇 밀리초마다 적이 하나씩 나타나는가

# 좌우로 흔들리는 적 (개조)
WAVE_AMPLITUDE_MIN = 30  # 흔들리는 폭(픽셀)의 범위
WAVE_AMPLITUDE_MAX = 70
WAVE_SPEED = 0.08  # 프레임마다 늘어나는 흔들림 각도(라디안). 한 번 왕복에 약 1.3초
WAVE_CHANCE_BASE = 0.4  # 새 적이 흔들리는 적일 확률. 파워업 레벨이 오를 때마다 늘어남
WAVE_CHANCE_PER_POWER = 0.1
WAVE_CHANCE_MAX = 0.8

# 사냥 구간: 이 시간(초) 안에 적을 잡으면 파워업을 얻는다
HUNT_SECONDS = 20
POWER_MAX = 4  # 파워업 최대 레벨 (사냥 구간에 적을 잡을 때마다 1 오름). 한 번에 나가는 총알 = 1 + 레벨 (최대 5발)
BULLET_SPREAD = 5  # 여러 발이 나갈 때 총알 사이의 가로 간격 (픽셀). 총알 폭(10)보다 작아서 서로 겹치게 촘촘히 나감

# 보스 (개조)
BOSS_FRAME = ("enemy-big.png", (3, 2, 26, 30), 4)  # 104 x 120
BOSS_SCORE = 300  # 첫 보스가 나오는 점수
BOSS_SCORE_STEP = 300  # 보스전이 끝난 점수에서 이만큼 더 모으면 다음 보스
BOSS_HP = 300
BOSS_SECONDS = 20  # 보스전 제한시간(초)
BOSS_SPEED = 2  # 좌우 왕복 속도
BOSS_ENTER_SPEED = 3  # 등장할 때 내려오는 속도
BOSS_Y = 100  # 보스 위쪽 끝 위치 (HUD 아래)

# 게임 규칙
START_LIVES = 10  # 스타터는 3. 적을 놓치면 파워업도 깎여서 넉넉하게 10 으로 늘림
SCORE_PER_ENEMY = 10

# 색 (R, G, B) / 반투명 막 (R, G, B, 투명도)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
RED = (230, 50, 50)
HUD_SHADE = (0, 0, 0, 140)
GAME_OVER_SHADE = (0, 0, 0, 170)
