import pygame
import time
import sys
import cv2
import mediapipe as mp
import random
import math
from src import throw, getDistance, overlay, playgame

# Pygame 초기화
pygame.init()

# screen setting
# resolution: 1600X900
screen_width = 1600  # 가로 크기
screen_height = 900  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 사운드 파일 로드
hit_sound = pygame.mixer.Sound('sound/hit.mp3')  # 볼이 맞았을 때 효과음
throw_sound = pygame.mixer.Sound('sound/throw.mp3')  # 볼을 던질 때 효과음

# 이미지 로드
hitter_ready = pygame.image.load('image/hitter_1.png') # 타석에 대기중인 타자
pitcher_ready = pygame.image.load('image/pitcher_1.png') # 공을 던지려고 준비중인 타자
hitter_swing = pygame.image.load('image/hitter_2.png') # 공을 스윙하고 있는 타자
pitcher_throw = pygame.image.load('image/pitcher_2.png') # 공을 던지고 있는 투수
strike_zone = pygame.image.load('image/strike_zone.png') # 스트라이크 존
ball = pygame.image.load('image/ball.png') # 야구공 (투수 위치에서 스트라이크 존 안의 random position에 도착해야함)

background = cv2.imread('image/field_hitter.jpg', cv2.IMREAD_UNCHANGED) # 배경
# Resize the OpenCV image to match screen dimensions
background = cv2.resize(background, (screen_width, screen_height)) # 배경의 크기를 screen의 크기와 일치

"""
# 이미지 선언
mole_image = cv2.imread('image/mole_tr100.png', cv2.IMREAD_UNCHANGED)
moleh, molew, _ = mole_image.shape

shine_image = cv2.imread('image/shine.png', cv2.IMREAD_UNCHANGED)
shineh, shinew, _ = shine_image.shape

clap_image = cv2.imread('image/clap.png', cv2.IMREAD_UNCHANGED)
claph, clapw, _ = clap_image.shape


# time variable
time_given=30.9
time_remaining = 99

rx0=random.randint(50, 590)
ry0=random.randint(50, 430)
# rx0=random.randint(0, 540)
# ry0=random.randint(0, 380)
r0 = []
r0.append(rx0)
r0.append(ry0)


rx1=random.randint(50, 590)
ry1=random.randint(50, 430)
# rx1=random.randint(0,540)
# ry1=random.randint(0,380)
r1 = []
r1.append(rx1)
r1.append(ry1)

"""

# 타자 대기 이미지 크기 초기화
hitter_ready_size = hitter_ready.get_rect().size  # 캐릭터 이미지 사이즈 구하기
hitter_ready_width = hitter_ready_size[0]  # 캐릭터 가로 크기
hitter_ready_height = hitter_ready_size[1]  # 캐릭터 세로 크기

# 캐릭터의 기준 좌표를 캐릭터의 왼쪽 상단으로 둔다.
hitter_ready_x_pos = (1600 / 2) - 1.2 * (hitter_ready_width)  # 화면 가로 절반의 중간에 위치. 좌우로 움직이는 변수
hitter_ready_y_pos = 900 - 1.5 * hitter_ready_height  # 이미지가 화면 세로의 가장 아래 위치

# 투수 대기 이미지 크기 초기화
pitcher_ready_size = pitcher_ready.get_rect().size  # 캐릭터 이미지 사이즈 구하기
pitcher_ready_width = pitcher_ready_size[0]  # 캐릭터 가로 크기
pitcher_ready_height = pitcher_ready_size[1]  # 캐릭터 세로 크기

# 캐릭터의 기준 좌표를 캐릭터의 왼쪽 상단으로 둔다.
pitcher_ready_x_pos = 700
pitcher_ready_y_pos = 200

# 스트라이크 존 이미지 크기 초기화
strike_zone_size = strike_zone.get_rect().size
strike_zone_width = strike_zone_size[0]  # 캐릭터 가로 크기
strike_zone_height = strike_zone_size[1]  # 캐릭터 세로 크기

strike_zone_x_pos = 670 # 스트라이크 존의 x좌표
strike_zone_y_pos = 325 # 스트라이크 존의 y좌표

# ball 이미지 크기 초기화
ball_size = ball.get_rect().size
ball_width = ball_size[0]
ball_height = ball_size[1]


# pose definition
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


# Game states
GAME_READY = 0
GAME_PLAYING = 1
GAME_OVER = 2

game_state = GAME_READY
start_time = 0
score = 0

font = pygame.font.SysFont(None, 55)
instruction_text = font.render("Put your fist in the strike zone", True, (255, 255, 255))

def check_hit(hand_landmarks, ball_position):
    # 손 위치가 공 위치와 일치하는지 확인
    # 실제 위치에 따라 조건을 조절해야 할 수 있음
    if (
        ball_position[0] - 50 < hand_landmarks[0] < ball_position[0] + 50
        and ball_position[1] - 50 < hand_landmarks[1] < ball_position[1] + 50
    ):
        return True
    return False

def playgame():
    global game_state, start_time, score, ball, pitcher_ready
    
    # pitcher_throw 이미지 출력을 위한 변수 추가
    pitcher_throw_time = 0

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)
    pygame.display.set_caption('Camera Stream')
    
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    cap.release()
                    sys.exit()

            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.resize(frame, (screen_width, screen_height))
            blended_frame = cv2.addWeighted(frame, 0.7, background, 0.3, 0)
            blended_frame = cv2.rotate(blended_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            blended_frame_rgb = cv2.cvtColor(blended_frame, cv2.COLOR_BGR2RGB)
            img = pygame.surfarray.make_surface(blended_frame_rgb)

            screen.blit(img, (0, 0))
            screen.blit(strike_zone, (strike_zone_x_pos, strike_zone_y_pos))
            # 스트라이크 존과 텍스트는 항상 출력
            if game_state == GAME_READY:
                screen.blit(instruction_text, (10, 10))

            results = hands.process(frame)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                hand_position = (
                    int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * screen_width),
                    int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * screen_height),
                )

                if (
                    strike_zone_x_pos < hand_position[0] < strike_zone_x_pos + strike_zone_width
                    and strike_zone_y_pos < hand_position[1] < strike_zone_y_pos + strike_zone_height
                ):
                    if game_state == GAME_READY:
                        # 주먹을 감지하고 공을 던지기 전까지 pitcher_ready 이미지 출력
                        if results.multi_hand_landmarks:
                            screen.blit(pitcher_ready, (pitcher_ready_x_pos, pitcher_ready_y_pos))
                        else:
                            screen.blit(instruction_text, (10, 10))
                            start_time = time.time()  # 주먹 인식되면 시간 초기화 및 상태 전환
                            game_state = GAME_PLAYING

                    elif game_state == GAME_PLAYING:
                        elapsed_time = time.time() - start_time
                        if elapsed_time >= 1.3 and elapsed_time <= 2.0:
                            ball_speed = random.uniform(1.3, 2.0)
                            ball_diameter = int((elapsed_time / 2) * 50)
                            ball = pygame.transform.scale(ball, (ball_diameter, ball_diameter))
                            ball_position = (
                                int(pitcher_ready_x_pos + ball_speed * elapsed_time),
                                int(strike_zone_y_pos + random.randint(-50, 50)),
                            )
                            screen.blit(ball, ball_position)
                            if (
                                0.7 * elapsed_time < 1.3 * elapsed_time
                                and check_hit(hand_position, ball_position)
                            ):
                                score += 1
                                hit_sound.play()
                                game_state = GAME_READY
                                if score >= 10:
                                    game_state = GAME_OVER
                                    print("게임 종료! 당신의 점수:", score)
                                else:
                                    hitter_swing_time = time.time()  # 타자가 스윙하는 시간 기록
                                    screen.blit(hitter_ready, (hitter_ready_x_pos, hitter_ready_y_pos))

                        if 0.4 < elapsed_time < 0.8:
                            # 투수가 공을 던지는 동안 pitcher_throw 이미지 출력
                            if time.time() - pitcher_throw_time < 1.5:  # 1.5초 동안 pitcher_throw 이미지 유지
                                screen.blit(pitcher_throw, (pitcher_ready_x_pos, pitcher_ready_y_pos))
                            else:
                                # 타자가 스윙하는 동안 hitter_swing 이미지 출력
                                if time.time() - hitter_swing_time < 0.5:
                                    screen.blit(hitter_swing, (hitter_ready_x_pos, hitter_ready_y_pos))
                                    hitter_ready = hitter_swing

            pygame.display.flip()


    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
        cap.release()
