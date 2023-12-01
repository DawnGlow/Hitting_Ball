import pygame
import time
import cv2
import mediapipe as mp
import numpy as np
from sklearn.linear_model import LogisticRegression
from src import getDistance, overlay, swing

pygame.init()

# File section
hit_sound = pygame.mixer.Sound('sound/hit.mp3')
background = pygame.image.load('image/field_hitter.jpg')
hitter_ready = pygame.image.load('image/hitter_1.png')
hitter_swing = pygame.image.load('image/hitter_2.png')

# 점으로 손가락 마디 표시
# 핸드 이미지 위에 랜드 마크 그리기 위함
mp_drawing = mp.solutions.drawing_utils

# 핸드 랜드마크 표시 스타일용
mp_drawing_styles = mp.solutions.drawing_styles

# mediapipe pose class 초기화
mp_pose = mp.solutions.pose


# screen setting
# resolution : 1600X900
screen_width = 1600 #가로 크기
screen_height = 900 #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 캐릭터 pos
hitter_ready_size = hitter_ready.get_rect().size #캐릭터 이미지 사이즈 구하기
hitter_ready_width = hitter_ready_size[0] #캐릭터 가로 크기
hitter_ready_height = hitter_ready_size[1] #캐릭터 세로 크기
#캐릭터의 기준 좌표를 캐릭터의 왼쪽 상단으로 둔다.
hitter_ready_x_pos = (screen_width / 2) - 1.2 * (hitter_ready_width) #화면 가로 절반의 중간에 위치. 좌우로 움직이는 변수
hitter_ready_y_pos = screen_height - 1.5 * hitter_ready_height #이미지가 화면 세로의 가장 아래 위치

#화면 타이틀 설정
pygame.display.set_caption("Hitting_Ball Client")

running = True #게임 진행 여부에 대한 변수 True : 게임 진행 중
while running:
    for event in pygame.event.get(): #이벤트의 발생 여부에 따른 반복문
        if event.type == pygame.QUIT: #창을 닫는 이벤트 발생했는가?
            running = False
    screen.blit(background, (0, 0))
    if swing.swing_condition():
        screen.blit(hitter_swing, (hitter_ready_x_pos, hitter_ready_y_pos))
        pygame.display.update()
        time.sleep(2)  # 2초 동안 대기
    else:
        screen.blit(hitter_ready, (hitter_ready_x_pos, hitter_ready_y_pos))

    pygame.display.update()



#pygame 종료
pygame.quit()