import pygame
import time
from src import throw

gamescore = 0

pygame.init()

# File section
hit_sound = pygame.mixer.Sound('sound/hit.mp3')
throw_sound = pygame.mixer.Sound('sound/throw.mp3')
background = pygame.image.load('image/field_hitter.jpg')
hitter_ready = pygame.image.load('image/hitter_1.png')
pitcher_ready = pygame.image.load('image/pitcher_1.png')
hitter_swing = pygame.image.load('image/hitter_2.png')
pitcher_throw = pygame.image.load('image/pitcher_2.png')
strike_zone = pygame.image.load('image/strike_zone.png')

# screen setting
# resolution: 1600X900
screen_width = 1600  # 가로 크기
screen_height = 900  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 캐릭터 pos
hitter_ready_size = hitter_ready.get_rect().size  # 캐릭터 이미지 사이즈 구하기
hitter_ready_width = hitter_ready_size[0]  # 캐릭터 가로 크기
hitter_ready_height = hitter_ready_size[1]  # 캐릭터 세로 크기
# 캐릭터의 기준 좌표를 캐릭터의 왼쪽 상단으로 둔다.
hitter_ready_x_pos = (screen_width / 2) - 1.2 * (hitter_ready_width)  # 화면 가로 절반의 중간에 위치. 좌우로 움직이는 변수
hitter_ready_y_pos = screen_height - 1.5 * hitter_ready_height  # 이미지가 화면 세로의 가장 아래 위치

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

# 화면 타이틀 설정
pygame.display.set_caption("Hitting_Ball Client")

# Font 설정
font = pygame.font.Font(None, 36)

# 색깔 설정
black = (0, 0, 0)
white = (255, 255, 255)

# 게임 메뉴 상태 설정
MENU_MAIN = 0
MENU_GAME = 1
current_menu = MENU_MAIN

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the mouse click is within the "게임 시작" button area
            mouse_x, mouse_y = event.pos
            if screen_width // 2 - 100 < mouse_x < screen_width // 2 + 100 and screen_height // 2 + 50 < mouse_y < screen_height // 2 + 100:
                current_menu = MENU_GAME

    screen.fill(black)

    if current_menu == MENU_MAIN:
        # Main Menu
        text = font.render("Main Menu", True, white)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))

        # 게임 실행 버튼
        pygame.draw.rect(screen, white, (screen_width // 2 - 100, screen_height // 2 + 50, 200, 50))
        text = font.render("Run Game", True, black)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 50 + text.get_height() // 2))

        # 상점 메뉴 버튼
        pygame.draw.rect(screen, white, (screen_width // 2 - 100, screen_height // 2 + 150, 200, 50))
        text = font.render("Shop", True, black)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + 150 + text.get_height() // 2))

    elif current_menu == MENU_GAME:
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

    pygame.display.update()

# pygame 종료
pygame.quit()