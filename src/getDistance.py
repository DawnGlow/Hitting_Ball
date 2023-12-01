import math

# 두 점 사이의 거리
def get_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance