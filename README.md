# Hitting_Ball ⚾

---

#### KOREAN discription

---

## 게임 소개

<img width="1574" alt="Throwing_2" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/ccfec222-1aea-41ac-ade2-baeab47118c5">

⚾ **Hitting Ball** 은 야구 타자(hitter) 입장에서 날라오는 공을 스윙하는 게임입니다. 프로그램을 실행하고 게임에 입장하면 컴퓨터/노트북에 내장된 카메라나, 캠코더를 통해 플레이어를 인식하게 됩니다. 플레이어는 타자 입장이 되어, 언제 어디로 올 지 모르는 공을 올바른 위치에서 올바른 타이밍에 스윙합니다. 올바른 타이밍과 올바른 위치에 스윙을 하면 점수를 획득합니다

모든 플레이어가 야구 배트를 가지고 있지 않고, 야구 배트를 가지고 있더라도 실내에서 야구 배트를 스윙할 환경이 갖춰지지 않은 경우가 대다수 이므로 ✊**주먹을 쥐는 동작을 스윙하는 동작으로 대신합니다.** (손바닥을 핀 상태에서 주먹을 쥐면 스윙으로 판단)

팔을 재빠르게 움직여 공이 날라오는 위치에 다가가 올바른 타이밍에 공을 맞춰보세요!

---

## Prerequisites

* python 3.11 이하 버전이 설치 되어 있어야 합니다(python 3.12 호환 불가)

```
pip install opencv
or
pip install opencv-python
```

```
pip install mediapipe
```

```
pip install pygame
```

```
pip install numpy
```

mac OS에서는 pip 명령어가 작동하지 않는 경우 pip3로 대신하여 사용

* 캠코더 / 카메라가 내장되있거나 연결되어 있어야 합니다
* 외장 카메라를 이용할 경우 src/playgame.py파일을 열어 274번째 line의 cap = cv2.VideoCapture(0)에서 cap = cv2.VideoCapture("카메라번호")로 변경

(23.12.10 기준 mac(Arm) / Windows 실행 가능)

- pygame 라이브러리가 OpenGL 기반이라 Metal 기반 Mac에서 게임 중 아주 드물게 오류가 발생할 수 있습니다. (23.12.10 최대한 해결)

-------

## About folders / files


```
📝mainmenu.py
게임 실행시 python 명령어를 통해 실행해야 하는 파일

📝README.md
게임 소개 / 실행 / 요건 등등에 대해 설명하는 파일

📝record.csv
게임 기록 log 파일
```

📁**src/**

```
📝ai.py
mediapipe 라이브러리를 통해 pose를 감지하고 hit / 게임 시작 조건에 맞는 pose를 판단하는 파일

📝getDistance.py
두 오브젝트 사이의 거리를 계산해 주는 파일

📝overlay.py
screen에 겹쳐여 할 두 image를 알파값을 통해 overlay하는 파일

📝playgame.py
게임의 flow를 다루는 핵심 파일

📝settings.py
게임의 기본적인 설정값을 다루는 파일. 
```

📁**iamge/**
* 게임 이미지 패키지

📁**iamge/**
* 게임 효과음 패키지

----

## 게임 시작
python mainmenu.py
or
python3 mainmenu.py

----

## 메뉴 소개

<img width="1568" alt="Gamemenu" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/be01404b-af90-405f-946d-ecb97d8b2999">

* Game Start : 게임 시작
* View Records : 기록 확인(정확도)

<img width="1591" alt="Records" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/1042daad-3d00-4546-9688-c54b47e2e17c">


* Quit Game : 게임 종료

---

## 게임 설명

1. Hand 인식 대기
<img width="1592" alt="READY" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/9c788d42-0ae6-4423-b646-724d43801539">

* 스크린 상에 손바닥을 비추면 다음 단계로 진행합니다(손바닥을 폈을 때 손가락의 V 모양 인지)
* 스트라이크 존 위쪽에 손을 올려두면 인식률이 높다

2. 투수가 공을 던지기 까지 기다리는 과정(실제 야구에선, 포수와 사인을 주고 받고 던지기를 준비하는 과정)
<img width="1521" alt="waittime" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/bde22535-90c5-43b8-9ce4-e40a8b73030a">

* 1번 과정에서 손을 인식하고 나면, 일정 시간동안 waiting time이 존재 (settings.py에서 조절 가능)

3. 공이 날라오는 과정

<img width="1585" alt="Throwing" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/6398df9a-f8ca-41bd-b25e-8b738017e854">
<img width="1574" alt="Throwing_2" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/5712c676-e093-429f-8314-6093e3d68787">

* Random 속도로 공이 날라온다. (settings.py에서 Speed 조절 가능)
* 공이 날라오기 X초 전 도착 지점을 빨간 원으로 표시한다 ((settings.py에서 X 값 조절 가능))
* 원근법에 따라 공이 가까워 질 수록 커진다 (도착 지점에서는 빨간 원의 크기와 거의 동일 해짐)

4. Swing
* 공이 점점 가까워 지면서 빨간 원과 위치와 크기가 일치하는 시점에 스윙을 한다
* 손바닥을 피고 있다가 공이 도착하는 지점에서 주먹을 쥐면 스윙으로 인지한다
* Tip! 주먹의 위치의 기준은 주먹을 줬을 때 엄지 손가락의 좌표이다

5-1. Hitting
<img width="1570" alt="hitting1" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/ae247487-eb0d-45c7-bb56-d716d47c6252">
<img width="1536" alt="hitting2" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/830c7796-e1f1-4319-8a36-d9918aa16c18">

* 시간 오차범위 내에 스윙을 하고, 오차범위 내 올바른 위치에서 스윙을 한 경우 Hit로 인정한다 (settings.py에서 오차 범위 조절 가능)
* Hitting 문구가 왼쪽 상단 위에 출력 된다
* 점수가 1점 증가한다

5-2. Miss_swing
<img width="1583" alt="Miss_swing" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/f3860140-fb7d-4925-b934-7fe368bd641f">

* 타이밍은 맞았지만, 위치가 정확하지 못해 공을 맞추지 못한 경우이다.
* Miss Swing 문구가 왼쪽 상단 위에 출력된다

5-3. Swing_early
<img width="1578" alt="swing_early1" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/f56f8235-82ab-4f87-b856-66976c6ec238">
<img width="1584" alt="swing_early2" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/3ad39cad-c554-44d3-a938-09dc50fa3622">

* 공이 도착하기 전 너무 일찍 스윙해서 헛스윙이 된 경우이다.
* Swing early 문구가 왼쪽 상단 위에 출력된다

5-4. Swing_lately
<img width="1552" alt="swing_late" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/794c5453-2c05-4173-b4c9-6197ad2b102a">

* 공이 도착하고 나서 스윙을 한 경우이다(너무 늦게 스윙한 경우)
* Swing late 문구가 왼쪽 상단 위에 출력된다.

5-5. Missing_Ball
<img width="1570" alt="missing_Ball" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/b25dd86c-80ed-451d-9705-5836f719edce">

* 스윙하지 않고 그냥 공이 도착할 때 까지 쳐다본 경우이다
* Missing Ball 문구가 왼쪽 상단 위에 출력된다.

6. 5번이 종료되면 다시 1번으로 돌아간다

7. left attempt(남은 기회)가 0이되면 게임이 종료된다.
<img width="1502" alt="game_over" src="https://github.com/DawnGlow/Hitting_Ball/assets/69619752/1c4570cb-7dd9-4f30-a68c-a7bd4fee9d2d">

* 최종 스코어가 출력되고, record.csv 파일에 시간과 기록(정확도)가 저장된다.

---
## Demo Video

https://github.com/DawnGlow/Hitting_Ball/assets/69619752/817a20bc-d824-4c56-a107-850422665fa2

## 추후 발전시킬 기능들
* 타이밍과 타격 위치 오차에 따른 타구 방향 / 세기 결정
* 실제 야구와 같이 스트라이크 / 볼 구분하여 투수가 공을 던지는 Process 추가
* 삼진 / 주루 / 득점 등 실제 야구 플레이와 유사하게 구현
* 투수 모드를 만들어 던지는 것도 사용자가 가능하게 설정


참조) 
* https://www.youtube.com/watch?v=XK3eU9egll8 - OpenCv 이미지 처리 참조
* https://github.com/choo121600/OpenCV_GunGame - 이미지 인식 처리 참조
* https://parkjh7764.tistory.com/88 - Pygame 기본 구조 참조
* https://wallpaperset.com/baseball-field-wallpaper - 게임 이미지 참조
* https://www.youtube.com/watch?v=SvlUj8RjkPc - 게임 사운드 참조
* https://www.youtube.com/watch?v=oke-KpxNf8g - Pose 인식 참조

### Developer
20101238 배준서

### License
This project is licensed under the LGPL-2.1 license

