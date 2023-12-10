# screen setting
# resolution: 1600X900
screen_width = 1600  # 가로 크기 / Default : 10
screen_height = 900  # 세로 크기 / Default : 10
allowed_time = 0.2 # 타격 허용 시간 / Default : 10
trycount = 10 # 타격 횟수 / Default : 10

# 값이 낮아질수록 난이도 증가
dest_showtime = 0.6 # 공이 도착하기 (Default :0.6)초 전에 예상 위치 출력

next_throwtime = 0.8 # 이 시간이 지나면 루킹 스트라이크 / default = 0.8

# 투수가 공을 던지기 까지 걸리는 시간
wait_min = 1.5 # default 1.5
wait_max = 2.5 # default 2.5

# 스트라이크 존에 공이 도착하는데 걸리는 시간
# 값이 낮아질수록 난이도 증가
throw_min = 1.3 # default 1.3
throw_max = 2.0 # default 2.0

# 공 위치의 X좌표 범위 
zone_x_min = 678 # default 678
zone_x_max = 938 # default 938

# 공 위치의 Y좌표 범위
zone_y_min = 390 # default 390
zone_y_max = 698 # default 698

# hit 할 때 손과 공 사이의 거리 오차범위
# 값이 올라갈수록 난이도가 쉬워짐
dist = 240