import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sorting Algorithms Visualization")

# Generate a random list of values
values = [random.randint(10, 50) for _ in range(20)]
is_sorting = False
sorting_speed = 50  # Initial speed
current_algorithm = None

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)  # Changed default color to light gray
BUTTON_TEXT_COLOR = (0, 0, 0)
CIRCLE_COLOR = (0, 100, 200)
BORDER_COLOR = (0, 0, 0)
SHADOW_COLOR = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
DROPDOWN_BG = (200, 200, 200)
DROPDOWN_TEXT = (0, 0, 0)

# Button properties
button_width = 160
button_height = 30
button_y = 20

algorithm_button = pygame.Rect(50, button_y, button_width, button_height)
speed_button = pygame.Rect(230, button_y, button_width, button_height)
reset_button = pygame.Rect(410, button_y, button_width, button_height)
font = pygame.font.Font(None, 24)

# Dropdown states
algorithm_dropdown = False
speed_dropdown = False

# Speed options
speed_options = {'Slow': 150, 'Medium': 50, 'Fast': 10}
selected_speed = 'Medium'

# Algorithm options
algorithms = ['Bubble Sort', 'Insertion Sort', 'Selection Sort', 'Merge Sort']
selected_algorithm = None

# Bubble sort implementation with visualization
def bubble_sort(arr, speed):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                draw_circles(arr, j, j + 1)
                pygame.display.flip()
                pygame.time.delay(speed)
        draw_circles(arr)
        pygame.display.flip()
        pygame.time.delay(speed)

# Insertion sort implementation with visualization
def insertion_sort(arr, speed):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            draw_circles(arr, j, j + 1)
            pygame.display.flip()
            pygame.time.delay(speed)
            j -= 1
        arr[j + 1] = key
        draw_circles(arr, j + 1, i)
        pygame.display.flip()
        pygame.time.delay(speed)
    draw_circles(arr)
    pygame.display.flip()
    pygame.time.delay(speed)

# Selection sort implementation with visualization
def selection_sort(arr, speed):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        draw_circles(arr, i, min_idx)
        pygame.display.flip()
        pygame.time.delay(speed)
    draw_circles(arr)
    pygame.display.flip()
    pygame.time.delay(speed)

# Merge sort implementation with visualization
def merge_sort(arr, speed):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half, speed)
        merge_sort(right_half, speed)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            draw_circles(arr)
            pygame.display.flip()
            pygame.time.delay(speed)
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
            draw_circles(arr)
            pygame.display.flip()
            pygame.time.delay(speed)

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
            draw_circles(arr)
            pygame.display.flip()
            pygame.time.delay(speed)
    draw_circles(arr)
    pygame.display.flip()
    pygame.time.delay(speed)

def draw_circles(arr, index1=None, index2=None):
    screen.fill(WHITE)
    circle_radius = 20
    gap = 40
    start_x = (screen.get_width() - (len(arr) * (2 * circle_radius + gap) - gap)) // 2
    for i, val in enumerate(arr):
        x = start_x + i * (2 * circle_radius + gap)
        y = screen.get_height() // 2
        color = CIRCLE_COLOR
        if i == index1 or i == index2:
            color = LIGHT_BLUE
        elif i > len(arr) - len(arr[i:]):
            color = GREEN
        pygame.draw.circle(screen, color, (x, y), circle_radius)
        text_surface = font.render(str(val), True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)
        if i == index1 or i == index2:
            pygame.draw.circle(screen, RED, (x, y), circle_radius + 2, width=2)
    draw_buttons()

def draw_buttons():
    algorithm_color = LIGHT_BLUE if is_sorting and current_algorithm == "Bubble Sort" else LIGHT_GRAY
    speed_color = LIGHT_BLUE if is_sorting and current_algorithm == "Insertion Sort" else LIGHT_GRAY
    reset_color = LIGHT_BLUE if is_sorting and current_algorithm == "Selection Sort" else LIGHT_GRAY
    draw_styled_button(screen, algorithm_button, "Select Algorithm", algorithm_color, BUTTON_TEXT_COLOR)
    draw_styled_button(screen, speed_button, f"Speed: {selected_speed}", speed_color, BUTTON_TEXT_COLOR)
    draw_styled_button(screen, reset_button, "Reset Array", reset_color, BUTTON_TEXT_COLOR)
    if algorithm_dropdown:
        draw_dropdown(algorithm_button, algorithms, selected_algorithm)
    if speed_dropdown:
        draw_dropdown(speed_button, speed_options.keys(), selected_speed)

def draw_styled_button(surface, rect, text, bg_color, text_color):
    shadow_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width, rect.height)
    pygame.draw.rect(surface, SHADOW_COLOR, shadow_rect, border_radius=5)
    pygame.draw.rect(surface, bg_color, rect, border_radius=5)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_dropdown(button_rect, options, selected_option):
    dropdown_rect = pygame.Rect(button_rect.x, button_rect.y + button_rect.height, button_rect.width, len(options) * 30)
    pygame.draw.rect(screen, DROPDOWN_BG, dropdown_rect)
    for i, option in enumerate(options):
        option_rect = pygame.Rect(button_rect.x, button_rect.y + button_rect.height + i * 30, button_rect.width, 30)
        if option == selected_option:
            pygame.draw.rect(screen, LIGHT_GRAY, option_rect)
        pygame.draw.rect(screen, BORDER_COLOR, option_rect, 2)
        option_text = font.render(option, True, DROPDOWN_TEXT)
        option_text_rect = option_text.get_rect(center=option_rect.center)
        screen.blit(option_text, option_text_rect)

def handle_sorting_algorithm():
    global is_sorting
    if current_algorithm == "Bubble Sort":
        bubble_sort(values, sorting_speed)
    elif current_algorithm == "Insertion Sort":
        insertion_sort(values, sorting_speed)
    elif current_algorithm == "Selection Sort":
        selection_sort(values, sorting_speed)
    elif current_algorithm == "Merge Sort":
        merge_sort(values, sorting_speed)
    is_sorting = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if algorithm_button.collidepoint(event.pos):
                algorithm_dropdown = not algorithm_dropdown
                speed_dropdown = False
            elif speed_button.collidepoint(event.pos):
                speed_dropdown = not speed_dropdown
                algorithm_dropdown = False
            elif reset_button.collidepoint(event.pos):
                values = [random.randint(10, 50) for _ in range(20)]
                is_sorting = False
            elif algorithm_dropdown:
                for i, algorithm in enumerate(algorithms):
                    option_rect = pygame.Rect(algorithm_button.x, algorithm_button.y + algorithm_button.height + i * 30, algorithm_button.width, 30)
                    if option_rect.collidepoint(event.pos):
                        current_algorithm = algorithm
                        selected_algorithm = algorithm
                        algorithm_dropdown = False
                        is_sorting = True
                        break
            elif speed_dropdown:
                for i, speed in enumerate(speed_options):
                    option_rect = pygame.Rect(speed_button.x, speed_button.y + speed_button.height + i * 30, speed_button.width, 30)
                    if option_rect.collidepoint(event.pos):
                        sorting_speed = speed_options[speed]
                        selected_speed = speed
                        speed_dropdown = False
                        break
            else:
                algorithm_dropdown = False
                speed_dropdown = False
        if event.type == pygame.MOUSEMOTION and is_sorting:
            algorithm_dropdown = False
            speed_dropdown = False

    if is_sorting:
        handle_sorting_algorithm()

    draw_circles(values)
    pygame.display.flip()

pygame.quit()