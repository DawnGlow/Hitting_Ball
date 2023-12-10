import pygame
import sys

pygame.init()

# 화면 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Resizing Circular Image")

# 이미지 불러오기
image_path = "image/ball.png"  # 구 형태 이미지 파일 경로를 설정하세요
image = pygame.image.load(image_path)
original_size = image.get_size()

# 시작 시간 저장
start_time = pygame.time.get_ticks()

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 현재 경과 시간 계산
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    # 이미지 크기 조절
    scale_factor = min(2, elapsed_time / 2000)  # 최대 2배까지, 2초 동안 증가
    scaled_image = pygame.transform.scale(image, (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor)))

    screen.fill((255, 255, 255))  # 화면을 흰색으로 채우기

    # 이미지 표시
    image_rect = scaled_image.get_rect(center=(width // 2, height // 2))
    screen.blit(scaled_image, image_rect)

    pygame.display.flip()

    # 2초가 지나면 종료
    if elapsed_time >= 2000:
        break

# 2초 후에 프로그램 종료
pygame.quit()
sys.exit()
