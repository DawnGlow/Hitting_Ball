import pygame
import sys
import csv
from src import playgame, settings


pygame.init()

main_background = pygame.image.load('image/main_background.jpg')

# screen setting
# resolution: 1600X900
screen_width = settings.screen_width  # 가로 크기
screen_height = settings.screen_height  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

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
                
class RecordsButton(Button):
    def __init__(self, text, x, y, width, height, color=(255, 255, 255), highlight_color=(200, 200, 200)):
        super().__init__(text, self.show_records, x, y, width, height, color, highlight_color)

    def show_records(self):
        records_menu()

def records_menu():
    records = read_records_from_csv()
    menu = True

    backButton = Button("Back", mainmenu, screen_width // 2 - 50, screen_height - 100, 100, 50)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

            backButton.handle_event(event)

        screen.blit(main_background, (0, 0))

        text = font.render("Records", True, (255, 0, 0))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, text.get_height()))

        display_records(records)

        backButton.draw(screen, font)

        pygame.display.update()
        clock.tick(15)

def display_records(records):
    if not records:
        no_records_text = font.render("No records yet.", True, (255, 255, 255))
        screen.blit(no_records_text, (screen_width // 2 - no_records_text.get_width() // 2, screen_height // 2))
        return

    header_text = font.render("Timestamp | Accuracy", True, (255, 255, 255))
    screen.blit(header_text, (screen_width // 2 - header_text.get_width() // 2, screen_height // 4))

    y_offset = screen_height // 4 + header_text.get_height() + 10

    for record in records:
        record_text = font.render(record, True, (255, 255, 255))
        screen.blit(record_text, (screen_width // 2 - record_text.get_width() // 2, y_offset))
        y_offset += record_text.get_height() + 5

def read_records_from_csv():
    try:
        with open('record.csv', 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Skip the header
            records = [f"{row[0]} | {row[1]}" for row in csv_reader]
        return records
    except FileNotFoundError:
        return []

# 게임 종료
def quitgame():
    pygame.quit()
    sys.exit()

def mainmenu():
    menu = True

    startButton = Button("Game Start", playgame.playgame, screen_width // 2 - 100, screen_height // 2, 200, 50)
    quitButton = Button("Quit Game", quitgame, screen_width // 2 - 100, screen_height // 2 + 200, 200, 50)
    recordsButton = RecordsButton("View Records", screen_width // 2 - 100, screen_height // 2 + 100, 200, 50)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

            startButton.handle_event(event)
            quitButton.handle_event(event)
            recordsButton.handle_event(event)

        screen.blit(main_background, (0, 0))

        text = font.render("Hitting BALL", True, (255, 0, 0))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, text.get_height()))

        startButton.draw(screen, font)
        quitButton.draw(screen, font)
        recordsButton.draw(screen, font)

        pygame.display.update()
        clock.tick(15)

mainmenu()
