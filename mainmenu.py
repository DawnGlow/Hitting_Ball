import pygame
import time
import sys
from src import throw, getDistance, overlay, playgame


pygame.init()

# File section
hit_sound = pygame.mixer.Sound('sound/hit.mp3')
throw_sound = pygame.mixer.Sound('sound/throw.mp3')
background = pygame.image.load('image/field_hitter.jpg')
hitter_ready = pygame.image.load('image/hitter_1.png')
pitcher_ready = pygame.image.load('image/pitcher_1.png')
hitter_swing = pygame.image.load('image/hitter_2.png')
pitcher_throw = pygame.image.load('image/pitcher_2.png')
strike_zone = pygame.image.load('image/strike_zone.png')

main_background = pygame.image.load('image/main_background.jpg')

# screen setting
# resolution: 1600X900
screen_width = 1600  # 가로 크기
screen_height = 900  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 캐릭터 pos
hitter_ready_size = hitter_ready.get_rect().size  # 캐릭터 이미지 사이즈 구하기
hitter_ready_width = hitter_ready_size[0]  # 캐릭터 가로 크기
hitter_ready_height = hitter_ready_size[1]  # 캐릭터 세로 크기
# 캐릭터의 기준 좌표를 캐릭터의 왼쪽 상단으로 둔다.
hitter_ready_x_pos = (screen_width / 2) - 1.2 * (hitter_ready_width)  # 화면 가로 절반의 중간에 위치. 좌우로 움직이는 변수
hitter_ready_y_pos = screen_height - 1.5 * hitter_ready_height  # 이미지가 화면 세로의 가장 아래 위치

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

# 화면 타이틀 설정
pygame.display.set_caption("Hitting_Ball Client")

# Font 설정
font = pygame.font.Font(None, 36)

# 색깔 설정
black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()

class Button:
    def __init__(self, text, callback, x, y, width, height, color=(255, 255, 255), highlight_color=(200, 200, 200)):
        self.text = text
        self.callback = callback
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.highlighted = False

    def draw(self, screen, font):
        if self.highlighted:
            pygame.draw.rect(screen, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.highlighted = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
                
# 게임 종료
def quitgame():
    pygame.quit()
    sys.exit()

def mainmenu():
    menu = True

    startButton = Button("Game Start", playgame.playgame, screen_width // 2 - 100, screen_height // 2, 200, 50)
    quitButton = Button("Quit Game", quitgame, screen_width // 2 - 100, screen_height // 2 + 60, 200, 50)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

            startButton.handle_event(event)
            quitButton.handle_event(event)

        screen.blit(main_background, (0, 0))

        text = font.render("Main Menu", True, white)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))

        startButton.draw(screen, font)
        quitButton.draw(screen, font)

        pygame.display.update()
        clock.tick(15)

mainmenu()
