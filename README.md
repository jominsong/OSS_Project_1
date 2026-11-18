# Vertical Shooter (S/W engineering proj 1)

화면 아래쪽 플레이어 비행기를 좌우로 움직이며 총알을 쏘아, 위에서 내려오는 적을 맞히는 종스크롤 슈팅 게임.

## 실행 방법

- Python 3.10–3.13, pygame 2.x
  - Python 3.14 에서는 pygame 2.6.1 이 설치되지 않으니, 3.10–3.13 중 하나를 사용할 것.

```bash
pip install pygame
python main.py
```

## 조작

| 키 | 동작 |
|---|---|
| ← / → | 좌우 이동 |
| Space | 시작 화면에서 게임 시작 / 게임 중 총알 발사 |
| R | 게임 오버 후 다시 시작 |
| Esc | 종료 (시작 화면에서도) |

## 파일 구성

| 파일 | 내용 |
|---|---|
| `main.py` | 게임 루프 — 입력 처리, 갱신, 그리기, 점수·생명·게임 오버 |
| `entities.py` | 그림 불러오기(`load_frame`), 배경(`Background`), 스프라이트 클래스 — `Player`, `Bullet`, `Enemy` |
| `settings.py` | 화면 크기·속도·색 같은 상수 |
| `assets/` | 그림 — ansimuz CC0 픽셀 아트 (출처: `assets/CREDITS.md`) |
| `AI_USAGE.md` | 생성형 AI 사용 기록 |

## 구현한 기능

- [x] F1 플레이어 이동 — ←/→ 키를 누르고 있는 동안 `PLAYER_SPEED`만큼 이동, 화면 좌우 끝 밖으로 나가지 않음
- [x] F2 총알 발사 — Space로 플레이어 위쪽 가운데에서 총알 발사, 위로 날아가 화면 밖으로 나가면 제거, 게임 오버 중에는 발사 안 됨
- [x] F3 적 명중과 점수 — 총알과 적이 부딪히면 둘 다 제거되고 적 하나당 10점, 왼쪽 위에 `SCORE: N` 표시
- [x] F4 피격과 게임 오버 — 적이 닿거나 화면 아래로 지나가면 생명 1 감소, 생명 0이면 게임 오버(`GAME OVER`와 이번 판 점수 표시)
- [x] F5 재시작과 최고 점수 — 게임 오버에서 R로 재시작, 최고 점수를 `highscore.txt`에 저장해 다시 실행해도 유지, `HIGH SCORE`와 `Press R to restart` 표시

> `highscore.txt`는 게임을 하면 자동으로 생기는 파일이라 `.gitignore`로 저장소에서 제외했습니다.
