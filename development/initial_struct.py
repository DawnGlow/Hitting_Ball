import pygame
import cv2
import mediapipe
import numpy as np
from sklearn.linear_model import LogisticRegression

def extract_features(frame):
    # 사람의 윤곽을 찾습니다.
    _, person_contours, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 사람의 윤곽 중 가장 큰 윤곽을 선택합니다.
    person_contour = max(person_contours, key=lambda c: cv2.contourArea(c))

    # 사람의 중심 좌표와 크기를 계산합니다.
    (x, y, w, h) = cv2.boundingRect(person_contour)
    return (int(x + w / 2), int(y + h / 2)), (int(w), int(h))

def train(features, labels):
    # 분류 모델을 학습합니다.
    model = LogisticRegression()
    model.fit(features, labels)

    return model

def predict(model, features):
    # 분류 모델을 사용하여 스윙 여부를 판단합니다.
    predictions = model.predict(features)

    return predictions

def main():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('Mediapipe Feed', frame)
    
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    # # 학습 데이터를 로드합니다.
    # # features, labels = load_data()

    # # 카메라를 켭니다.
    # cap = cv2.VideoCapture(0)

    # while True:
    #     # 프레임을 캡처합니다.
    #     frame = cap.read()
    #     cv2.imshow('Mediapipe Feed', frame)
    #     # 사람을 인식합니다.
    #     person_center, person_size = extract_features(frame)

    #     # 스윙 여부를 판단합니다.
    #     # predictions = predict(model, np.array([person_center, person_size]))

    #     # 결과를 출력합니다.
    #     #if predictions[0] == 1:
    #     #    print("스윙 감지!")
    #     #else:
    #     #    print("스윙 감지 안됨!")
    # # 카메라를 닫습니다.
    # cap.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()