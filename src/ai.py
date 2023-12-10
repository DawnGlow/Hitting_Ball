import cv2
import mediapipe as mp
from src import getDistance, settings

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def check_hit(frame, ball_position):
    

    # 손을 감지할 프레임을 RGB로 변환
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 손 감지 수행
    results = hands.process(rgb_frame)

    # 주먹이 감지되었는지 확인
    punch_detected = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 주먹 관련 랜드마크 인덱스
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # 주먹을 펼친 상태인지 확인
            is_punching = (
                thumb_tip.y < index_tip.y and
                thumb_tip.y < middle_tip.y and
                thumb_tip.y < ring_tip.y and
                thumb_tip.y < pinky_tip.y
            )

            if is_punching:
                punch_detected = True
                punch_position = (int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0]))

                # 주먹의 위치와 볼의 위치를 비교하여 펀치 여부 판단
                # distance = ((punch_position[0] - ball_position[0])**2 + (punch_position[1] - ball_position[1])**2)**0.5
                distance = getDistance.get_distance(punch_position, ball_position)
                if distance < settings.dist:  # 여기서 240은 임의로 설정한 값
                    return 2  # 주먹 위치와 ball_position이 일치함
                else:
                    return 1  # 주먹 위치와 ball_position이 일치하지 않음

    # 주먹을 감지하지 못한 경우
    return 0

def pose_condition(frame):
    results = hands.process(frame)
    # Initialize MediaPipe Hand model

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

        # 손가락 V 모양을 판별하기 위한 지점 인덱스
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        # 손가락 V 모양 판별 (검지와 중지의 끝 지점이 특정 위치에 있을 때)
        v_shape_detected = (
            index_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y and
            middle_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
        )

        if v_shape_detected:
            return True

    return False