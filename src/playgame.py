import pygame
import time
import sys
import cv2
import mediapipe as mp
import random
import math
from src import throw, getDistance, overlay, playgame

pygame.init()
# screen setting
# resolution: 1600X900
screen_width = 1600  # 가로 크기
screen_height = 900  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# File section
hit_sound = pygame.mixer.Sound('sound/hit.mp3')
throw_sound = pygame.mixer.Sound('sound/throw.mp3')
#background = pygame.image.load('image/field_hitter.jpg')
# background = pygame.transform.scale(background, (screen_width, screen_height))
hitter_ready = pygame.image.load('image/hitter_1.png')
pitcher_ready = pygame.image.load('image/pitcher_1.png')
hitter_swing = pygame.image.load('image/hitter_2.png')
pitcher_throw = pygame.image.load('image/pitcher_2.png')
strike_zone = pygame.image.load('image/strike_zone.png')

background = cv2.imread('image/field_hitter.jpg', cv2.IMREAD_UNCHANGED)
# Resize the OpenCV image to match screen dimensions
background = cv2.resize(background, (screen_width, screen_height))

# 이미지 선언
mole_image = cv2.imread('image/mole_tr100.png', cv2.IMREAD_UNCHANGED)
moleh, molew, _ = mole_image.shape

shine_image = cv2.imread('image/shine.png', cv2.IMREAD_UNCHANGED)
shineh, shinew, _ = shine_image.shape

clap_image = cv2.imread('image/clap.png', cv2.IMREAD_UNCHANGED)
claph, clapw, _ = clap_image.shape



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


# pose definition
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()



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



def playgame():
    score = 0
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

            # Capture frame from the camera
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.resize(frame, (screen_width, screen_height))

            # Blend the OpenCV image with the camera stream
            blended_frame = cv2.addWeighted(frame, 0.7, background, 0.3, 0)
            
            # Rotate the blended frame clockwise by 90 degrees
            blended_frame = cv2.rotate(blended_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Convert the blended image from BGR to RGB
            blended_frame_rgb = cv2.cvtColor(blended_frame, cv2.COLOR_BGR2RGB)

            # Convert the OpenCV image to Pygame surface
            img = pygame.surfarray.make_surface(blended_frame_rgb)

            # Display the image in the Pygame window
            screen.blit(img, (0, 0))
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
                screen.blit(hitter_swing, (hitter_ready_x_pos, hitter_ready_y_pos))
                hit_sound.play()
                score += 1
                print(f'게임 점수: {score}')
                pygame.display.update()
            else:
                screen.blit(hitter_ready, (hitter_ready_x_pos, hitter_ready_y_pos))
            pygame.display.flip()

    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
        cap.release()

    """
    global background
    # event setting
    game_start_event = False
    game_over_event = False
    game_pause_event = False
    score=0
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, frame = cap.read()
            image = cv2.flip(frame, 1)
            # blending 처리하여 캠이랑 field 모두 인식할 수 있게 설정
            background = cv2.resize(background, (frame.shape[1], frame.shape[0]))
            alpha = 0.5
            blended_image = cv2.addWeighted(frame, alpha, background, 1 - alpha, 0)
            blended_image = cv2.flip(blended_image, 1)
            # cv2.imshow("Blended Image", blended_image)
            #cv2.waitKey(1)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            # Recolor image to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Make detection하는 부분
            results = pose.process(image)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            # Recolor back to BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            h, w, _ = image.shape        

            present_time = time.time()
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                rightindex = [landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]
                leftindex = [landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]       

                righthand = [rightindex[0]*w, rightindex[1]*h]
                lefthand = [leftindex[0]*w, leftindex[1]*h]            
                # print(int(rightindex[0]*10), int(rightindex[1]*10),int(rightindex[2]*10))
                

                noseindex = [landmarks[0].x, landmarks[0].y]
                nose = [noseindex[0]*w, noseindex[1]*h]

                rightfootindex = [landmarks[31].x, landmarks[31].y]
                leftfootindex = [landmarks[32].x, landmarks[32].y]
                rightfoot = [rightfootindex[0]*w, rightfootindex[1]*h]
                leftfoot = [leftfootindex[0]*w, leftfootindex[1]*h]
                
                if game_start_event == False:
                    cv2.ellipse(blended_image, (w//2, h//2-50), (72, 90) ,0 ,0, 360, (0,0,255), 0)
                    cv2.putText(blended_image, 'Clap to start a Game',
                            (w//2-300, h//2-85),
                            cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (51, 102, 153), 3, cv2.LINE_AA)
                    cv2.putText(blended_image, 'Please keep some distance or adjust your webcam',
                            (w//2-210, h//2+130),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(blended_image, 'to locate your face in circle',
                            (w//2-110, h//2+160),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    overlay(blended_image, w//2-230, h//2-185, 50, 50, clap_image)
                    # print(get_distance(righthand, lefthand))

                    if getDistance.get_distance(righthand, lefthand) < 80 and ( w//2-100 < nose[0] < w//2+100 and h//2-100 < nose[1] < h//2+100):
                        game_start_event = True
                        start_time = time.time()

                if game_start_event == True and time_remaining > 0:
                    # print('남은시간', time_remaining)
                    # print('\n현재시간',present_time)
                    # print('\n시작',start_time)
                    time_remaining = int(time_given - (present_time - start_time))

                    if (rx0-50 < righthand[0] < rx0+50 and ry0-50 < righthand[1] < ry0+50) or (rx0-50 < lefthand[0] < rx0+50 and ry0-50 < lefthand[1] < ry0+50) :
                        overlay(blended_image, rx0, ry0, 50, 50, shine_image)
                        score += 1
                        hit_sound.play()
                        rx0=random.randint(50, 590)
                        ry0=random.randint(50, 430)
                        r0.append(rx0)
                        r0.append(ry0)
                    
                    if (rx1-50 < righthand[0] < rx1+50 and ry1-50 < righthand[1] < ry1+50) or (rx1-50 < lefthand[0] < rx1+50 and ry1-50 < lefthand[1] < ry1+50) :
                        overlay(blended_image, rx1, ry1, 50, 50, shine_image)
                        score += 1
                        hit_sound.play()
                        rx1=random.randint(50, 590)
                        ry1=random.randint(50, 430)
                        r1.append(rx0)
                        r1.append(ry0)

                    cv2.putText(blended_image, 'Score:',
                                (w//2-250, 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 204), 2, cv2.LINE_AA)      

                    cv2.putText(blended_image, str(score),
                            (w//2-130, 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 204), 2, cv2.LINE_AA)         

                    cv2.putText(blended_image, 'Time left:',
                            (w//2+30, 35),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 204), 2, cv2.LINE_AA)      

                    cv2.putText(blended_image, str(time_remaining),
                            (w//2+230, 35),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 204), 2, cv2.LINE_AA) 



                    # image, x, y, w, h, overlay_image (좌측 최상단x,y가 50, 50임) 최하단 430 최우측 590
                    overlay(blended_image, rx0, ry0, 50, 50, mole_image)
                    overlay(blended_image, rx1, ry1, 50, 50, mole_image)                
                
                elif game_start_event == True and time_remaining <= 0:
                    
                    time_remaining = 0
                    game_over_event = True





            except:
                cv2.putText(blended_image, 'Please show your face and keep some distance from your webcam',
                (w//2-260, h//2+220),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                pass    

            # cv2.rectangle(image, (int(righthand[0])-50, int(righthand[1])-50), (int(righthand[0])+50, int(righthand[1])+50), (255,255,255), -1)
            # cv2.rectangle(image, (rx1-50, ry1-50), (rx1+50, ry1+50), rect_color1, -1)          




                # image[ry0:ry0+moleh, rx0:rx0+molew] = mole_image

                # image[ry1:ry1+moleh, rx1:rx1+molew] = mole_image

                # image[10:moleh+10, 20:molew+20] = mole_image

            # 게임종료시에만 실행
            if game_over_event == True:
                
                cv2.rectangle(blended_image, (w//2-170, h//2-130), (w//2+170, h//2+40), (0,0,0), -1)

                cv2.putText(blended_image, 'Game Over',
                (w//2-147, h//2-65),
                cv2.FONT_HERSHEY_SIMPLEX, 1.7, (255, 255, 255), 3, cv2.LINE_AA)
                
                cv2.putText(blended_image, 'Your Score:',
                (w//2-120, h//2),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA) 

                cv2.putText(blended_image, str(score),
                (w//2+80, h//2+3),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)   


            # Render detections

            # mp_drawing.draw_landmarks(
            #     image,
            #     results.pose_landmarks,
            #     mp_pose.POSE_CONNECTIONS,
            #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())  


            cv2.imshow('Whack-A-Mole Game with Mediapipe Pose', cv2.resize(blended_image, None, fx=2.0, fy=2.0))  # 화면크기 2배 키움
            
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()


# def playgame():
#     gamescore = 0
#     running = True
    
#     while running:
#         # 게임 실행 화면
#         screen.blit(background, (0, 0))
#         screen.blit(strike_zone, (strike_zone_x_pos, strike_zone_y_pos))

#         # 사용자가 투구 조건을 입력하면 2초 동안 pitcher_throw 이미지로 변경합니다.
#         throw_condition = throw.throw_condition()
#         if throw_condition:
#             screen.blit(pitcher_throw, (pitcher_ready_x_pos, pitcher_ready_y_pos))
#             throw_sound.play()
#             pygame.display.update()
#         else:
#             screen.blit(pitcher_ready, (pitcher_ready_x_pos, pitcher_ready_y_pos))

#         # 사용자가 스윙 조건을 입력하면 2초 동안 hitter_swing 이미지로 변경합니다.
#         if throw_condition:
#             time.sleep(2)
#             screen.blit(hitter_swing, (hitter_ready_x_pos, hitter_ready_y_pos))
#             hit_sound.play()
#             gamescore += 1
#             print(f'게임 점수: {gamescore}')
#             pygame.display.update()
#             time.sleep(2)  # 2초 동안 대기
#         else:
#             screen.blit(hitter_ready, (hitter_ready_x_pos, hitter_ready_y_pos))
            
        
            
#         pygame.display.update()
    
#     pygame.quit()

"""