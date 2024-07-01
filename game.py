import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1000, 700))
colors = {
    'black': (0, 0, 0), 'grey': (192, 192, 192), 'red': (255, 0, 0),
    'white': (255, 255, 255), 'blue': (0, 0, 255), 'yellow': (255, 255, 0)
}
points = [
    (100, 100), (500, 100), (900, 100), (900, 375), (900, 650), (500, 650),
    (100, 650), (100, 375), (200, 200), (500, 200), (800, 200), (800, 375),
    (800, 550), (500, 550), (200, 550), (200, 375), (300, 300), (500, 300),
    (700, 300), (700, 375), (700, 450), (500, 450), (300, 450), (300, 375)
]
win_points = [
    ((100, 100), (500, 100), (900, 100)), ((900, 100), (900, 375), (900, 650)),
    ((900, 650), (500, 650), (100, 650)), ((100, 650), (100, 375), (100, 100)),
    ((200, 200), (500, 200), (800, 200)), ((800, 200), (800, 375), (800, 550)),
    ((800, 550), (500, 550), (200, 550)), ((200, 550), (200, 375), (200, 200)),
    ((300, 300), (500, 300), (700, 300)), ((700, 300), (700, 375), (700, 450)),
    ((700, 450), (500, 450), (300, 450)), ((300, 450), (300, 375), (300, 300)),
    ((100, 100), (200, 200), (300, 300)), ((500, 100), (500, 200), (500, 300)),
    ((900, 100), (800, 200), (700, 300)), ((900, 375), (800, 375), (700, 375)),
    ((900, 650), (800, 550), (700, 450)), ((500, 650), (500, 550), (500, 450)),
    ((100, 650), (200, 550), (300, 450)), ((100, 375), (200, 375), (300, 375))
]
circles = {'red': [], 'blue': []}
turn = 'red'
scores = {'red': 0, 'blue': 0}
sum = 0
ai = 0
username = input("What's your name: ")
pygame.display.set_caption(username)

font = pygame.font.Font(None, 35)
select1 = font.render('User', True, colors['yellow'])
select2 = font.render('AI - Easy', True, colors['yellow'])
select3 = font.render('AI - Medium', True, colors['yellow'])
select4 = font.render('AI - Hard', True, colors['yellow'])
restart1 = font.render('Restart', True, colors['yellow'])

restart = restart1.get_rect(center=(500, 680))
rect1 = select1.get_rect(center=(500, 50))
rect2 = select2.get_rect(center=(500, 100))
rect3 = select3.get_rect(center=(500, 150))
rect4 = select4.get_rect(center=(500, 200))

def draw_board(screen, points, colors):
    for point in points:
        pygame.draw.circle(screen, colors['grey'], point, 20)
    for i in range(23):
        if i == 7 or i == 15: continue
        pygame.draw.line(screen, colors['grey'], points[i], points[i + 1], 7)
    pygame.draw.line(screen, colors['grey'], points[7], points[0], 7)
    pygame.draw.line(screen, colors['grey'], points[15], points[8], 7)
    pygame.draw.line(screen, colors['grey'], points[22], points[16], 7)
    for j in range(8):
        pygame.draw.line(screen, colors['grey'], points[j], points[j + 16], 7)

    pygame.draw.circle(screen, colors['black'], (375, 375) if turn != 'red' else (625, 375), 40)
    pygame.draw.circle(screen, colors['yellow'], (375, 375) if turn == 'red' else (625, 375), 40)
    pygame.draw.circle(screen, colors['red'], (375, 375), 35)
    pygame.draw.circle(screen, colors['blue'], (625, 375), 35)

    font = pygame.font.Font(None, 28)
    if ai == 0: text = font.render('User    Vs    User', True, colors['white'])
    if ai == 1: text = font.render('User  Vs  AI-Easy', True, colors['white'])
    if ai == 2: text = font.render('User  Vs  AI-Medium', True, colors['white'])
    if ai == 3: text = font.render('User  Vs  AI-Hard', True, colors['white'])
    screen.blit(text, (423, 365))

def draw_selection_circle():
    for color, points1 in circles.items():
        for point in points1:
            pygame.draw.circle(screen, colors[color], point, 15)

def update_scores(circles, turn):
    scores[turn] = 0
    for item1 in win_points:
        if all(item in circles[turn] for item in item1):
            scores[turn] += 1

def medium_ai(circles, valid_tuples, win_points):
    for point in valid_tuples:
        for win_point in win_points:
            if point in win_point and all(p in circles['red'] or p == point for p in win_point):
                return point
    return random.choice(valid_tuples)

def hard_ai(circles, valid_tuples, win_points):
    for point in valid_tuples:
        for win_point in win_points:
            if point in win_point and all(p in circles['blue'] or p == point for p in win_point):
                return point
    for point in valid_tuples:
        for win_point in win_points:
            if point in win_point and all(p in circles['red'] or p == point for p in win_point):
                return point
    return random.choice(valid_tuples)

def draw_scores():
    font = pygame.font.Font(None, 35)
    red_score_text = font.render(f"Score Of Red : {scores['red']}", True, colors['red'])
    blue_score_text = font.render(f"Score Of Blue : {scores['blue']}", True, colors['blue'])
    screen.blit(red_score_text, (50, 20))
    screen.blit(blue_score_text, (700, 20))
    font = pygame.font.Font(None, 25)
    if (sum == 24 and ai == 0) and scores['blue'] > scores['red']:
        scoreboard = font.render('Blue win', True, colors['blue'])
        screen.blit(scoreboard, (400, 20))
    elif (sum == 24 and ai == 0) and scores['blue'] < scores['red']:
        scoreboard = font.render('Red win', True, colors['red'])
        screen.blit(scoreboard, (400, 20))
    elif (sum == 24 and ai == 0) and scores['blue'] == scores['red']:
        scoreboard = font.render('Draw', True, colors['yellow'])
        screen.blit(scoreboard, (400, 20))
    elif (sum == 12 and (ai == 1 or ai == 2 or ai == 3)) and scores['blue'] == scores['red']:
        scoreboard = font.render('Draw', True, colors['yellow'])
        screen.blit(scoreboard, (400, 20))
    elif (sum == 12 and (ai == 1 or ai == 2 or ai == 3)) and scores['blue'] < scores['red']:
        scoreboard = font.render('Red win', True, colors['red'])
        screen.blit(scoreboard, (400, 20))
    elif (sum == 12 and (ai == 1 or ai == 2 or ai == 3)) and scores['blue'] > scores['red']:
        scoreboard = font.render('Blue win', True, colors['blue'])
        screen.blit(scoreboard, (400, 20))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect1.collidepoint(event.pos):
                ai = 0
                running = False
            elif rect2.collidepoint(event.pos):
                ai = 1
                running = False
            elif rect3.collidepoint(event.pos):
                ai = 2
                running = False
            elif rect4.collidepoint(event.pos):
                ai = 3
                running = False
    screen.fill(colors['black'])
    screen.blit(select1, rect1)
    screen.blit(select2, rect2)
    screen.blit(select3, rect3)
    screen.blit(select4, rect4)
    pygame.display.flip()

runnin = True
while runnin:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnin = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for point in points:
                if pygame.Rect(point[0] - 20, point[1] - 20, 40, 40).collidepoint(mouse_pos):
                    if point not in circles['red'] and point not in circles['blue']:
                        circles[turn].append(point)
                        update_scores(circles, turn)
                        turn = 'blue' if turn == 'red' else 'red'
                        sum += 1

                        if turn == 'blue' and ai == 1:
                            valid_tuples = [t for t in points if t not in circles['red'] and t not in circles['blue']]
                            random_point = random.choice(valid_tuples)
                            circles[turn].append(random_point)
                            update_scores(circles, turn)
                            turn = 'red'
                        if turn == 'blue' and ai == 2:
                            valid_tuples = [t for t in points if t not in circles['red'] and t not in circles['blue']]
                            point = medium_ai(circles, valid_tuples, win_points)
                            circles[turn].append(point)
                            update_scores(circles, turn)
                            turn = 'red'
                        if turn == 'blue' and ai == 3:
                            valid_tuples = [t for t in points if t not in circles['red'] and t not in circles['blue']]
                            point = hard_ai(circles, valid_tuples, win_points)
                            circles[turn].append(point)
                            update_scores(circles, turn)
                            turn = 'red'

            if restart.collidepoint(event.pos):
                circles = {'red': [], 'blue': []}
                turn = 'red'
                scores = {'red': 0, 'blue': 0}
                sum = 0
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if rect1.collidepoint(event.pos):
                                ai = 0
                                running = False
                            elif rect2.collidepoint(event.pos):
                                ai = 1
                                running = False
                            elif rect3.collidepoint(event.pos):
                                ai = 2
                                running = False
                            elif rect4.collidepoint(event.pos):
                                ai = 3
                                running = False
                    screen.fill(colors['black'])
                    screen.blit(select1, rect1)
                    screen.blit(select2, rect2)
                    screen.blit(select3, rect3)
                    screen.blit(select4, rect4)
                    pygame.display.flip()

    screen.fill(colors['black'])
    screen.blit(restart1, restart)
    draw_board(screen, points, colors)
    draw_scores()
    draw_selection_circle()
    pygame.display.flip()

pygame.quit()
sys.exit()