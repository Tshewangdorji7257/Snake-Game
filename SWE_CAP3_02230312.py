import pygame
import sys
import time
import random

# Initialize pygame
pygame.init()

# Window size
frame_size_x = 720
frame_size_y = 480

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Create game window
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
pygame.display.set_caption('Snake Eater')

# Font settings
font = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 36)

# Function to display text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Load sound effects
pygame.mixer.init()
eat_sound = pygame.mixer.Sound('eating-sound-effect-36186.mp3')  

# Load previous high score
def load_high_score():
    try:
        with open('highscore.txt', 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Save new high score
def save_high_score(score):
    with open('highscore.txt', 'w') as file:
        file.write(str(score))

# Main menu
def main_menu():
    while True:
        game_window.fill(black)
        draw_text('Snake Eater', font_large, white, game_window, frame_size_x//2, frame_size_y//4)
        draw_text('Press 1 for Easy', font, white, game_window, frame_size_x//2, frame_size_y//2)
        draw_text('Press 2 for Medium', font, white, game_window, frame_size_x//2, frame_size_y//2 + 40)
        draw_text('Press 3 for Hard', font, white, game_window, frame_size_x//2, frame_size_y//2 + 80)

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'Easy'
                elif event.key == pygame.K_2:
                    return 'Medium'
                elif event.key == pygame.K_3:
                    return 'Hard'

# Game over screen
def game_over(score):
    high_score = load_high_score()
    if score > high_score:
        save_high_score(score)
        high_score = score

    while True:
        game_window.fill(black)
        draw_text('Game Over', font_large, red, game_window, frame_size_x//2, frame_size_y//4)
        draw_text(f'Your Score: {score}', font, white, game_window, frame_size_x//2, frame_size_y//2)
        draw_text(f'High Score: {high_score}', font, white, game_window, frame_size_x//2, frame_size_y//2 + 40)
        draw_text('Press Enter to play again', font, white, game_window, frame_size_x//2, frame_size_y*3//4)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    return 

# Main game function
def main():
    difficulty = main_menu()
    fps_controller = pygame.time.Clock()
    score = 0

    # Game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction

    # Background colors
    background_colors = [black, blue, red]  # Add more colors as needed
    current_bg_color_index = 0

    # Obstacles
    obstacles = [
        [200, 200],
        [400, 300],
        [600, 100]
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Update direction of snake
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Move the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 10
            food_spawn = False
            current_bg_color_index = (current_bg_color_index + 1) % len(background_colors)
            eat_sound.play()  # Play sound when eating food
        else:
            snake_body.pop()

        # Spawn food on screen
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

        # GFX
        game_window.fill(background_colors[current_bg_color_index])  # Fill window with background color
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Draw obstacles
        for obstacle_pos in obstacles:
            pygame.draw.rect(game_window, red, pygame.Rect(obstacle_pos[0], obstacle_pos[1], 10, 10))

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            game_over(score)
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            game_over(score)
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over(score)

        # Check collision with obstacles
        for obstacle_pos in obstacles:
            if snake_pos[0] == obstacle_pos[0] and snake_pos[1] == obstacle_pos[1]:
                game_over(score)

        # Display score
        draw_text(f'Score: {score}', font, white, game_window, frame_size_x//2, 10)

        # Update game screen
        pygame.display.update()

        # Adjust game speed
        fps_controller.tick(15 + score // 20)

# Start the game
if __name__ == '__main__':
    main()
