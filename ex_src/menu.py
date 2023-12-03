import pygame

pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("game menu system")

# 폰트 설정
font = pygame.font.Font(None, 36)

# 게임 메뉴 출력
def draw_menu():
    menu_text = font.render("game_menu", True, (255, 255, 255))
    menu_rect = menu_text.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(menu_text, menu_rect)

# 게임 시작 화면
def draw_start_menu():
    start_text = font.render("game_start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(start_text, start_rect)

# 게임 설정 화면
def draw_settings_menu():
    settings_text = font.render("game_setting", True, (255, 255, 255))
    settings_rect = settings_text.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(settings_text, settings_rect)

# 게임 실행
def run_game():
    running = True
    current_screen = "start"  # 현재 화면 설정

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    current_screen = "settings"  # 설정 화면으로 전환
                elif event.key == pygame.K_r:
                    current_screen = "start"  # 시작 화면으로 전환

        screen.fill((0, 0, 0))

        # 현재 화면에 따라 해당 함수를 호출
        if current_screen == "start":
            draw_start_menu()
        elif current_screen == "settings":
            draw_settings_menu()

        pygame.display.flip()

    pygame.quit()

# 게임 실행
run_game()