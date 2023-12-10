import pygame
import time
import sys
import cv2
import mediapipe as mp
import random
import csv
from src import throw, overlay, settings, ai
from development import debugFunction

# Pygame 초기화
pygame.init()

# screen setting
# resolution: 1600X900
screen_width = settings.screen_width  # 가로 크기
screen_height = settings.screen_height  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
game_state_timer = 0

# 사운드 파일 로드
hit_sound = pygame.mixer.Sound('sound/hit.mp3')  # 볼이 맞았을 때 효과음
throw_sound = pygame.mixer.Sound('sound/throw.mp3')  # 볼을 던질 때 효과음
miss_swing_sound = pygame.mixer.Sound('sound/miss_swing.mp3')  # 헛스윙 효과음

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
# time variable
time_given=30.9
time_remaining = 99

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
pitcher_ready_y_pos = 270

# 스트라이크 존 이미지 크기 초기화
strike_zone_size = strike_zone.get_rect().size
strike_zone_width = strike_zone_size[0]  # 캐릭터 가로 크기
strike_zone_height = strike_zone_size[1]  # 캐릭터 세로 크기

strike_zone_x_pos = 670 # 스트라이크 존의 x좌표
strike_zone_y_pos = 380 # 스트라이크 존의 y좌표


# ball 이미지 크기 초기화
ball_size = ball.get_size()
# 50 X 50
ball_width = ball_size[0]
ball_height = ball_size[1]
ball_x_pos = 830
ball_y_pos = 280

moveball = ball
moveball_size = ball_size
moveball_width = ball_size[0]
moveball_height = ball_size[1]
moveball_x_pos = ball_x_pos
moveball_y_pos = ball_y_pos


# pose definition
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Game states
GAME_READY = 0
GAME_WAIT = 1
GAME_THROW1 = 2
GAME_HIT = 3 # Not used
GAME_MISS_HIT = 4 # 정확한 위치에 스윙 하지 않은 경우
GAME_RESULT_1 = 5 # 일찍스윙 -> 헛스윙
GAME_RESULT_2 = 6 # 스윙 -> hit
GAME_LATE = 7 # 정확한 타이밍 이후
GAME_LATE_HIT = 8 # 늦게스윙 -> 헛스윙
GAME_LOOK = 9 # Just Look
GAME_OVER = 10

# allowed time
allowed_time = settings.allowed_time

game_state = GAME_READY
start_time = 0
score = 0

font = pygame.font.SysFont(None, 55)
instruction_text = font.render("Put your hand (include V) in the strike zone", True, (255, 255, 255))
waiting_text = font.render("Wating time", True, (255, 255, 255))
throw_text = font.render("Focus on ball!", True, (255, 255, 255))
hit_text = font.render("Hitting!", True, (255, 255, 255))
miss_hit_text = font.render("Miss swing!", True, (255, 255, 255))
swing_early_text = font.render("Swing early!", True, (255, 255, 255))
swing_late_text = font.render("Swing late!", True, (255, 255, 255))
look_text = font.render("Missing ball!", True, (255, 255, 255))
text = instruction_text


# 볼 위치를 계산해서 return 해주는 함수
# elapsed_time : 경과 시간, throw_time : 스트라이크 존에 도착하는데 걸리는 시간
# random_pos_x, random_pos_y : 공이 스트라이크 존을 통과하는 위치
def ball_pos_cal(elapsed_time, throw_time, random_pos_x, random_pos_y):
    global moveball
    # 초기 위치
    init_x = ball_x_pos
    init_y = ball_y_pos
    
    # 직선 운동 방정식을 사용하여 현재 위치 계산
    current_x = init_x + (random_pos_x - init_x) * (elapsed_time / throw_time)
    current_y = init_y + (random_pos_y - init_y) * (elapsed_time / throw_time)

    # 공의 크기가 커짐 (원근법)
    # scale_factor = 1 + elapsed_time / (2 * throw_time)
    scale_factor = 1 + elapsed_time / throw_time
    moveball = pygame.transform.scale(ball, (int(ball_size[0] * scale_factor), int(ball_size[1] * scale_factor)))
    # 현재 위치 반환
    return current_x, current_y

# 손 위치가 공 위치와 일치하는지 확인
# def check_hit(frame, ball_position):
#     results = hands.process(frame)

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             hand_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * screen_width)
#             hand_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * screen_height)

#             # 손이 공을 치는지 여부를 판단합니다.
#             distance = getDistance.get_distance((hand_x, hand_y), ball_position)
#             if distance < 30:  # 여기서 50은 임의로 설정한 값입니다. 실제로 조절이 필요할 수 있습니다.
#                 return 2  # 손이 공을 침
#             else:
#                 return 1  # 손은 감지되었지만 공을 치지 않음

#     return 0  # 손을 감지하지 못함


# def pose_condition(frame):
#     results = hands.process(frame)

#     if results.multi_hand_landmarks:
#         hand_landmarks = results.multi_hand_landmarks[0]
#         hand_position = (
#             int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * screen_width),
#             int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * screen_height),
#         )

#         if (
#             strike_zone_x_pos < hand_position[0] < strike_zone_x_pos + strike_zone_width
#             and strike_zone_y_pos < hand_position[1] < strike_zone_y_pos + strike_zone_height
#         ):
#             return True
            
#     return False

def donothing(limit):
    start_time = time.time()
    while (time.time() - start_time) < limit:
        continue

def wait(start_time, wait_time):
    if time.time() - start_time >= wait_time:
        return True
    
# throw 함수에서 사용할 변수들을 선언합니다.
throw_animation_speed = 500  # 공이 이동하는 속도 (픽셀/초)
throw_animation_start_time = None  # 애니메이션 시작 시간

def throw(start_time, throw_time, random_pox_x, random_pox_y, frame):
    global moveball_x_pos, moveball_y_pos, throw_animation_start_time
    current_time = time.time()
    elapsed_time = current_time - start_time
    if throw_animation_start_time is None:
        throw_animation_start_time = current_time

    # 애니메이션 시간에 따라 공의 위치를 계산합니다.
    animation_elapsed_time = current_time - throw_animation_start_time
    moveball_x_pos, moveball_y_pos = ball_pos_cal(
        animation_elapsed_time, throw_time, random_pox_x, random_pox_y
    )
    
    if throw_time - elapsed_time < 0:
        return GAME_LATE
    
    # 공이 도착하기 dest_showtime 전에 예상 위치 출력
    if throw_time - elapsed_time < settings.dest_showtime:
        pygame.draw.circle(screen, (255, 0, 0), (random_pox_x + ball_width, random_pox_y + ball_width), ball_width / 1.3)

    result = ai.check_hit(frame, (moveball_x_pos, moveball_y_pos))
    # 공이 도착하기 allowedtime(0.2초) 전에 스윙하면 헛스윙
    if throw_time - elapsed_time > allowed_time:
        if result in {1, 2}:
            return GAME_RESULT_1
        else:
            return GAME_THROW1
    # 올바른 타이밍 allowedtime(0.2초) 전에 스윙하면 hit인정
    elif throw_time - elapsed_time < allowed_time:
        if result == 2:
            return GAME_RESULT_2
        elif result == 1:
            return GAME_MISS_HIT
        else:
            return GAME_THROW1
        
def late(start_time, throw_time, random_pox_x, random_pox_y, frame):
    global moveball_x_pos, moveball_y_pos, moveball
    moveball_x_pos = random_pox_x
    moveball_y_pos = random_pox_y
    moveball = pygame.transform.scale(ball, (int(ball_size[0] * 2), int(ball_size[1] * 2)))
    # 현재 위치 반환
    current_time = time.time()
    elapsed_time = current_time - start_time
    pygame.draw.circle(screen, (255, 0, 0), (random_pox_x + ball_width, random_pox_y + ball_width), ball_width / 1.3)
    if (elapsed_time > throw_time + settings.next_throwtime):
        return GAME_LOOK
    result = ai.check_hit(frame, (moveball_x_pos, moveball_y_pos))
    if (elapsed_time - throw_time < 0.2):
        if result == 2:
            return GAME_RESULT_2
        elif result == 1:
            return GAME_MISS_HIT
        else:
            return GAME_LATE
    elif (elapsed_time - throw_time < 0.8):
        if result in {1, 2}:
            return GAME_LATE_HIT
        else:
            return GAME_LATE


def playgame(trycount=settings.trycount):
    global game_state, start_time, score, moveball, moveball_x_pos, moveball_y_pos, moveball_size, pitcher_ready, throw_animation_start_time, text
    csv_file = open('record.csv', 'a', newline='')
    csv_writer = csv.writer(csv_file)
    wait_time = random.uniform(settings.wait_min, settings.wait_max)
    throw_time = random.uniform(settings.throw_min, settings.throw_max)
    random_pos_x = random.uniform(678, 938)
    random_pos_y = random.uniform(390, 698)
    game_state = GAME_READY
    text = instruction_text
    score = 0
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)
    pygame.display.set_caption('Camera Stream')
    score_text = font.render(f'score : {score}, left attempt : {trycount}', True, (255, 255, 255))
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
            if (text in {hit_text, miss_hit_text, swing_early_text, swing_late_text, look_text}):
                time.sleep(2)
            # without any condition 항상 출력
            screen.blit(img, (0, 0))
            screen.blit(strike_zone, (strike_zone_x_pos, strike_zone_y_pos))
            
            # 투수와 타자의 이미지 initializing
            hitter = hitter_ready
            pitcher = pitcher_ready
            text = instruction_text
            
            # 공 data initializing
            moveball = ball
            moveball_size = ball_size
            moveball_x_pos = ball_x_pos
            moveball_y_pos = ball_y_pos
            
            if trycount <= 0:
                game_state = GAME_OVER
            
            if game_state == GAME_READY:
                if (ai.pose_condition(frame)):
                    game_state = GAME_WAIT
                    start_time = time.time()
            elif game_state == GAME_WAIT:
                text = waiting_text
                if (wait(start_time, wait_time)):
                    game_state = GAME_THROW1
                    throw_sound.play()
                    start_time = time.time()
            elif game_state == GAME_THROW1:
                pitcher = pitcher_throw
                text = throw_text
                game_state = throw(start_time, throw_time, random_pos_x, random_pos_y, frame)
            elif game_state == GAME_MISS_HIT:
                hitter = hitter_swing
                miss_swing_sound.play()
                trycount-=1
                text=miss_hit_text
                wait_time = random.uniform(settings.wait_min, settings.wait_max)
                throw_time = random.uniform(settings.throw_min, settings.throw_max)
                random_pos_x = random.uniform(settings.zone_x_min, settings.zone_x_max)
                random_pos_y = random.uniform(settings.zone_y_min, settings.zone_y_max)
                moveball = ball
                moveball_size = ball_size
                moveball_x_pos = ball_x_pos
                moveball_y_pos = ball_y_pos
                throw_animation_start_time = None
                game_state = GAME_READY
            elif game_state == GAME_RESULT_2:
                hitter = hitter_swing
                hit_sound.play()
                score+=1
                trycount-=1
                text=hit_text
                wait_time = random.uniform(settings.wait_min, settings.wait_max)
                throw_time = random.uniform(settings.throw_min, settings.throw_max)
                random_pos_x = random.uniform(settings.zone_x_min, settings.zone_x_max)
                random_pos_y = random.uniform(settings.zone_y_min, settings.zone_y_max)
                moveball = ball
                moveball_size = ball_size
                moveball_x_pos = ball_x_pos
                moveball_y_pos = ball_y_pos
                game_state = GAME_READY
                throw_animation_start_time = None
                #sleep
            elif game_state == GAME_RESULT_1:
                hitter = hitter_swing
                miss_swing_sound.play()
                trycount-=1
                text=swing_early_text
                wait_time = random.uniform(settings.wait_min, settings.wait_max)
                throw_time = random.uniform(settings.throw_min, settings.throw_max)
                random_pos_x = random.uniform(settings.zone_x_min, settings.zone_x_max)
                random_pos_y = random.uniform(settings.zone_y_min, settings.zone_y_max)
                moveball = ball
                moveball_size = ball_size
                moveball_x_pos = ball_x_pos
                moveball_y_pos = ball_y_pos
                game_state = GAME_READY
                throw_animation_start_time = None
                #sleep
            elif game_state == GAME_LATE:
                pitcher = pitcher_throw
                text = throw_text
                game_state = late(start_time, throw_time,  random_pos_x, random_pos_y, frame)
            elif game_state == GAME_LATE_HIT:
                hitter = hitter_swing
                miss_swing_sound.play()
                trycount-=1
                text=swing_late_text
                wait_time = random.uniform(settings.wait_min, settings.wait_max)
                throw_time = random.uniform(settings.throw_min, settings.throw_max)
                random_pos_x = random.uniform(settings.zone_x_min, settings.zone_x_max)
                random_pos_y = random.uniform(settings.zone_y_min, settings.zone_y_max)
                moveball = ball
                moveball_size = ball_size
                moveball_x_pos = ball_x_pos
                moveball_y_pos = ball_y_pos
                game_state = GAME_READY
                throw_animation_start_time = None
                #sleep
            elif game_state == GAME_LOOK:
                trycount-=1
                text=look_text
                wait_time = random.uniform(settings.wait_min, settings.wait_max)
                throw_time = random.uniform(settings.throw_min, settings.throw_max)
                random_pos_x = random.uniform(settings.zone_x_min, settings.zone_x_max)
                random_pos_y = random.uniform(settings.zone_y_min, settings.zone_y_max)
                moveball = ball
                moveball_size = ball_size
                moveball_x_pos = ball_x_pos
                moveball_y_pos = ball_y_pos
                game_state = GAME_READY
                throw_animation_start_time = None
                #sleep
            elif game_state == GAME_OVER:
                gameover_text = font.render("GAME OVER", True, (255, 0, 0))
                totalscore_text = font.render(f'Total Score : {score}', True, (255, 0, 0))
                screen.blit(gameover_text, (screen_width // 2, screen_height // 2 - 100))
                screen.blit(totalscore_text, (screen_width // 2, screen_height // 2 + 100))
                pygame.display.flip()
                # Record timestamp and score in CSV file
                current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                csv_writer.writerow([current_timestamp, f'{(100 * score // settings.trycount) if settings.trycount != 0 else 0}%'])
                time.sleep(2)
                return
            else:
                print("error")
                pygame.quit()
            # score_text 업데이트
            score_text = font.render(f'score : {score}, left attempt : {trycount}', True, (255, 255, 255))
            if game_state != GAME_READY:    
                screen.blit(pitcher, (pitcher_ready_x_pos, pitcher_ready_y_pos))
                screen.blit(hitter, (hitter_ready_x_pos, hitter_ready_y_pos))
                screen.blit(moveball, (moveball_x_pos, moveball_y_pos))
            screen.blit(text, (10, 10))
            screen.blit(score_text, (10, 100))
            
            clock.tick(120)
            pygame.display.flip()

                
    except KeyboardInterrupt:
        pass
    finally:
        # pygame.quit()
        cap.release()
