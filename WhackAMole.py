import pygame
import random
import math
import time

pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack a Mole")
clock = pygame.time.Clock()

# button varibles
RADIUS = 20
GAP = 15
letters = []
start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 400

# fonts
TITLE_FONT = pygame.font.SysFont('googleFont.ttf', 100)
SMAL_FONT = pygame.font.SysFont('googleFont.ttf', 40)

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 252, 0)
GREY = (220, 220, 220)
RED = (255, 0, 0)
LIGHT_GRAY = (211, 211, 211)


# button
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('googleFont.ttf', 40)
            text = font.render(self.text, 1, BLACK)
            win.blit(text, (int(
                self.x + (self.width / 2 - text.get_width() / 2)),
                            int(self.y + (self.height / 2 - text.get_height() / 2))))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


# buttons
start_green_button = Button(GREEN, int(WIDTH * 0.2), int(HEIGHT * 0.8), 100, 80, 'Start')
start_red_button = Button(RED, int(WIDTH * 0.7), int(HEIGHT * 0.8), 100, 80, 'Exit')
try_again_button = Button(GREEN, int(WIDTH / 2 - 60), int(HEIGHT * 0.8), 140, 80, 'Try Again')


# start meny
def start_meny():
    print('Start Meny')
    run = True

    while run:

        # set Background white
        win.fill(WHITE)

        # make buttons to start game
        start_green_button.draw(win, BLACK)
        start_red_button.draw(win, BLACK)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Green Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_green_button.isOver(pos):
                    run = False
            if event.type == pygame.MOUSEMOTION:
                if start_green_button.isOver(pos):
                    start_green_button.color = GREY
                else:
                    start_green_button.color = GREEN

            # Red Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_red_button.isOver(pos):
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEMOTION:
                if start_red_button.isOver(pos):
                    start_red_button.color = GREY
                else:
                    start_red_button.color = RED

        # draw title

        text = TITLE_FONT.render('Whack a mole', 1, BLACK)
        width = round(WIDTH / 2 - text.get_width() / 2)
        height = round(HEIGHT / 2 - text.get_height() / 2)
        win.blit(text, (width, height))

        pygame.display.update()
        clock.tick(15)


counter = 0


class Circle:
    def __init__(self, color, x, y, radius):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius

    def start(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def update(self, x_updated, y_updated):
        pygame.draw.circle(win, BLACK, (x_updated, y_updated), self.radius)

    def isOver(self, pos):
        if self.radius > math.sqrt((self.x - pos[0])**2 + (self.y - pos[1])**2):
            return True
        return False


game_circle = Circle(RED, 400, 250, 30)

time_limit = 10


def game():
    print('Game')
    start_time = time.time()
    global counter
    counter = 0
    global game_circle
    run = True
    while run:

        # Background color
        win.fill(LIGHT_GRAY)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                if game_circle.isOver(pos):
                    game_circle.color = GREEN
                else:
                    game_circle.color = RED
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_circle.isOver(pos):
                    counter += 1
                    game_circle = Circle(RED, random.randint(100, 700), random.randint(100, 400), 30)
                else:
                    counter -= 1

        elapsed_time = time.time() - start_time

        if elapsed_time > 10:
            game_over()

        text = SMAL_FONT.render(f'sekunder: {int(time_limit - elapsed_time)}', 1, BLACK)
        win.blit(text, (WIDTH * 0.75, HEIGHT * 0.1))


        # display counter
        text_counter = SMAL_FONT.render(f'Score: {counter}', 1, BLACK)
        win.blit(text_counter, (WIDTH * 0.1, HEIGHT * 0.1))
        game_circle.start()

        pygame.display.update()
        clock.tick(40)


def game_over():
    print('Game Over')
    while True:
        win.fill(WHITE)

        try_again_button.draw(win, BLACK)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_button.isOver(pos):
                    game()
            if event.type == pygame.MOUSEMOTION:
                if try_again_button.isOver(pos):
                    try_again_button.color = GREY
                else:
                    try_again_button.color = RED

        # Game over text
        text = TITLE_FONT.render('Game Over', 1, BLACK)
        width = round(WIDTH / 2 - text.get_width() / 2)
        height = round(HEIGHT / 2 - text.get_height() / 2)
        win.blit(text, (width, height))

        # Result text
        text = SMAL_FONT.render(f'Your score is: {counter}', 1, BLACK)
        width = round(WIDTH / 2 - text.get_width() / 2)
        height = round(HEIGHT * 0.3)
        win.blit(text, (width, height))


        pygame.display.update()
        clock.tick(15)


start_meny()
game()
pygame.quit()
