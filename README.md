# Hitting_Ball

---

#### KOREAN discription

---

# Hitting_Ball

---

### 게임 소개

---

**Hitting Ball** 은 야구 타자(hitter) 입장에서 날라오는 공을 스윙하는 게임입니다. 프로그램을 실행하고 게임에 입장하면 컴퓨터/노트북에 내장된 카메라나, 캠코더를 통해 플레이어를 인식하게 됩니다. 플레이어는 타자 입장이 되어, 언제 어디로 올 지 모르는 공을 올바른 위치에서 올바른 타이밍에 스윙합니다. 올바른 타이밍과 올바른 위치에 스윙을 하면 점수를 획득합니다

모든 플레이어가 야구 배트를 가지고 있지 않고, 야구 배트를 가지고 있더라도 실내에서 야구 배트를 스윙할 환경이 갖춰지지 않은 경우가 대다수 이므로 **주먹을 쥐는 동작을 스윙하는 동작으로 대신합니다.** 

팔을 재빠르게 움직여 공이 날라오는 위치에 다가가 올바른 타이밍에 공을 맞춰보세요!

---

#### Prerequisites

----

python 3.11 이하 버전이 설치 되어 있어야 합니다(python 3.12 호환 불가)

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



(23.12.10 기준 mac(Arm) / Windows 실행 가능)

- pygame 라이브러리가 OpenGL 기반이라 Metal 기반 Mac에서 게임 중 아주 드물게 오류가 발생할 수 있습니다. (23.12.10 최대한 해결)

-------

#### About folders / files

-------

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

```
📝mainmenu.py
게임 실행시 python 명령어를 통해 실행해야 하는 파일

📝README.md
게임 소개 / 실행 / 요건 등등에 대해 설명하는 파일

📝record.csv
게임 기록 log 파일
```
----

### Demo Video

https://github.com/DawnGlow/Hitting_Ball/assets/69619752/817a20bc-d824-4c56-a107-850422665fa2

참조) https://www.youtube.com/watch?v=XK3eU9egll8
https://github.com/choo121600/OpenCV_GunGame
https://parkjh7764.tistory.com/88
https://wallpaperset.com/baseball-field-wallpaper
https://www.youtube.com/watch?v=SvlUj8RjkPc