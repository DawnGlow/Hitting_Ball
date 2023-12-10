import pygame
import time
from src import throw

# File section
hit_sound = pygame.mixer.Sound('sound/hit.mp3')
throw_sound = pygame.mixer.Sound('sound/throw.mp3')
background = pygame.image.load('image/field_hitter.jpg')
hitter_ready = pygame.image.load('image/hitter_1.png')
pitcher_ready = pygame.image.load('image/pitcher_1.png')
hitter_swing = pygame.image.load('image/hitter_2.png')
pitcher_throw = pygame.image.load('image/pitcher_2.png')
strike_zone = pygame.image.load('image/strike_zone.png')

# 캐릭터 pos
hitter_ready_size = hitter_ready.get_rect().size  # 캐릭터 이미지 사이즈 구하기
hitter_ready_width = hitter_ready_size[0]  # 캐릭터 가로 크기
hitter_ready_height = hitter_ready_size[1]  # 캐릭터 세로 크기
# 캐릭터의 기준 좌표를 캐릭터의 왼쪽 상단으로 둔다.
hitter_ready_x_pos = (1600 / 2) - 1.2 * (hitter_ready_width)  # 화면 가로 절반의 중간에 위치. 좌우로 움직이는 변수
hitter_ready_y_pos = 900 - 1.5 * hitter_ready_height  # 이미지가 화면 세로의 가장 아래 위치

pitcher_ready_size = pitcher_ready.get_rect().size  # 캐릭터 이미지 사이즈 구하기
pitcher_ready_width = pitcher_ready_size[0]  # 캐릭터 가로 크기
pitcher_ready_height = pitcher_ready_size[1]  # 캐릭터 세로 크기
# 캐릭터의 기준 좌표를 캐릭터의 왼쪽 상단으로 둔다.
pitcher_ready_x_pos = 700
pitcher_ready_y_pos = 200

strike_zone_size = strike_zone.get_rect().size
strike_zone_width = strike_zone_size[0]  # 캐릭터 가로 크기
strike_zone_height = strike_zone_size[1]  # 캐릭터 세로 크기

strike_zone_x_pos = 670
strike_zone_y_pos = 325

def hit_mode(screen):
    # 게임 실행 화면
    screen.blit(background, (0, 0))
    screen.blit(strike_zone, (strike_zone_x_pos, strike_zone_y_pos))

    # 사용자가 투구 조건을 입력하면 2초 동안 pitcher_throw 이미지로 변경합니다.
    throw_condition = throw.throw_condition()
    if throw_condition:
        screen.blit(pitcher_throw, (pitcher_ready_x_pos, pitcher_ready_y_pos))
        throw_sound.play()
        pygame.display.update()
    else:
        screen.blit(pitcher_ready, (pitcher_ready_x_pos, pitcher_ready_y_pos))

        # 사용자가 스윙 조건을 입력하면 2초 동안 hitter_swing 이미지로 변경합니다.
    if throw_condition:
        time.sleep(2)
        screen.blit(hitter_swing, (hitter_ready_x_pos, hitter_ready_y_pos))
        hit_sound.play()
        gamescore += 1
        print(f'게임 점수: {gamescore}')
        pygame.display.update()
        time.sleep(2)  # 2초 동안 대기
    else:
        screen.blit(hitter_ready, (hitter_ready_x_pos, hitter_ready_y_pos))