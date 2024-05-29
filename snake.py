import pygame
import time
import random
import os
import json

initial_snake_speed = 15
window_x = 720
window_y = 480
high_score_file = 'high_scores.json'
power_up_duration = 150
power_up_probability = 0.15
FONT = 'times new roman'

# kolory
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)

# inicjalizacja pygame
pygame.init()
pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

# wczytywanie high scores
def load_high_scores():
    if not os.path.exists(high_score_file):
        return []
    with open(high_score_file, 'r') as file:
        return json.load(file)

# zapisywanie high scores
def save_high_scores(high_scores):
    with open(high_score_file, 'w') as file:
        json.dump(high_scores, file)

# Wyświetlanie wyników
def show_score(score, level, power_up, power_up_time, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f'Score: {score} | Level: {level}', True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)
    
    if power_up:
        power_up_surface = score_font.render(f'Power-Up: {power_up} ({power_up_time})', True, color)
        power_up_rect = power_up_surface.get_rect(topright=(window_x - 10, 10))
        game_window.blit(power_up_surface, power_up_rect)

# Wyświetlanie high scores
def show_high_scores(high_scores):
    game_window.fill(black)
    font = pygame.font.SysFont(FONT, 30)
    title_surface = font.render('High Scores', True, white)
    title_rect = title_surface.get_rect(center=(window_x / 2, 50))
    game_window.blit(title_surface, title_rect)

    for index, score in enumerate(high_scores[:5]):
        score_surface = font.render(f"{index + 1}. {score}", True, white)
        score_rect = score_surface.get_rect(center=(window_x / 2, 100 + index * 40))
        game_window.blit(score_surface, score_rect)

    return_surface = font.render('R - Return', True, white)
    return_rect = return_surface.get_rect(center=(window_x / 2, window_y - 50))
    game_window.blit(return_surface, return_rect)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    show_main_menu(high_scores)
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Instrukcje
def show_instructions(high_scores):
    game_window.fill(black)
    font = pygame.font.SysFont(FONT, 30)

    instructions = [
        "Instructions",
        "-----------------",
        "Use the arrow keys to move the snake.",
        "Press P to pause the game",
        "Red: Snake's head",
        "Green: Snake's body",
        "White: Fruit",
        "Yellow: Power-ups",
        "Blue: Obstacles",
        "Yellow: Power-ups:",
        "  - Double Points: doubles the points for a short time",
        "  - Slow Down: slows the snake down for a short time",
        "",
        "R - Return"
    ]

    for index, line in enumerate(instructions):
        instruction_surface = font.render(line, True, white)
        instruction_rect = instruction_surface.get_rect(center=(window_x / 2, 30 + index * 30))
        game_window.blit(instruction_surface, instruction_rect)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    show_main_menu(high_scores)
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Koniec gry
def game_over(score, high_scores):
    high_scores.append(score)
    high_scores = sorted(high_scores, reverse=True)[:5]
    save_high_scores(high_scores)

    game_window.fill(black)
    font = pygame.font.SysFont(FONT, 50)
    game_over_surface = font.render('GAME OVER! Score: ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect(center=(window_x / 2, window_y / 4))
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    return high_scores

# Menu
def show_main_menu(high_scores):
    game_window.fill(black)
    font = pygame.font.SysFont(FONT, 50)
    play_surface = font.render('P - Play', True, white)
    play_rect = play_surface.get_rect(center=(window_x / 2, window_y / 2 - 100))
    game_window.blit(play_surface, play_rect)

    high_score_surface = font.render('H - High Scores', True, white)
    high_score_rect = high_score_surface.get_rect(center=(window_x / 2, window_y / 2 - 50))
    game_window.blit(high_score_surface, high_score_rect)

    instructions_surface = font.render('I - Instructions', True, white)
    instructions_rect = instructions_surface.get_rect(center=(window_x / 2, window_y / 2))
    game_window.blit(instructions_surface, instructions_rect)

    quit_surface = font.render('Q - Quit', True, white)
    quit_rect = quit_surface.get_rect(center=(window_x / 2, window_y / 2 + 50))
    game_window.blit(quit_surface, quit_rect)

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    waiting = False
                if event.key == pygame.K_h:
                    show_high_scores(high_scores)
                    waiting = False
                if event.key == pygame.K_i:
                    show_instructions(high_scores)
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Gra
def game_loop():
    snake_speed = initial_snake_speed
    level = 1
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    # Przeszkoty
    obstacles = []
    for _ in range(level):
        obstacles.append([random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10])

    # Power-up
    power_up = None
    power_up_time = 0
    power_up_position = [random.randrange(1, (window_x // 10)) * 10,
                         random.randrange(1, (window_y // 10)) * 10]
    power_up_active = True 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_p:
                    pause_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Wrap around (brak babier na krawedziach ekranu)
        if snake_position[0] < 0:
            snake_position[0] = window_x - 10
        if snake_position[0] >= window_x:
            snake_position[0] = 0
        if snake_position[1] < 0:
            snake_position[1] = window_y - 10
        if snake_position[1] >= window_y:
            snake_position[1] = 0

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 20 if power_up == 'Double Points' else 10
            fruit_spawn = False
            snake_speed += 1 if power_up != 'Slow Down' else 0
            if score % 50 == 0:  # Increase level every 50 points
                level += 1
                snake_speed += 2
                for _ in range(level):
                    obstacles.append([random.randrange(1, (window_x // 10)) * 10,
                                      random.randrange(1, (window_y // 10)) * 10])
            
            # spawn Power-up 
            if random.random() < power_up_probability:
                power_up_position = [random.randrange(1, (window_x // 10)) * 10,
                                     random.randrange(1, (window_y // 10)) * 10]
                power_up_active = True

        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

        if snake_position == power_up_position and power_up_active:
            power_up = random.choice(['Double Points', 'Slow Down'])
            power_up_time = power_up_duration
            if power_up == 'Slow Down':
                snake_speed = max(snake_speed - 5, 5)
            power_up_active = False

        game_window.fill(black)

        # wąz 
        for pos in snake_body[1:]:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, red, pygame.Rect(snake_body[0][0], snake_body[0][1], 10, 10))

        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
        
        if power_up_active:
            pygame.draw.rect(game_window, yellow, pygame.Rect(power_up_position[0], power_up_position[1], 10, 10))

        for obstacle in obstacles:
            pygame.draw.rect(game_window, blue, pygame.Rect(obstacle[0], obstacle[1], 10, 10))

        if snake_position in obstacles:
            return score

        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                return score

        show_score(score, level, power_up, power_up_time, white, FONT, 20)

        if power_up_time > 0:
            power_up_time -= 1
        else:
            power_up = None
            snake_speed = initial_snake_speed

        pygame.display.update()
        fps.tick(snake_speed)

def pause_game():
    paused = True
    font = pygame.font.SysFont(FONT, 50)
    pause_surface = font.render('Game Paused. Press P to Continue', True, white)
    pause_rect = pause_surface.get_rect(center=(window_x / 2, window_y / 2))
    game_window.blit(pause_surface, pause_rect)
    pygame.display.flip()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def main():
    high_scores = load_high_scores()
    while True:
        show_main_menu(high_scores)
        score = game_loop()
        high_scores = game_over(score, high_scores)

if __name__ == "__main__":
    main()
