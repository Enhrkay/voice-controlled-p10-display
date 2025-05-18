import pygame
import sys
import speech_recognition as sr

# Pygame setup
pygame.init()

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 16
LED_SIZE = 20
LED_MARGIN = 2

SCREEN_WIDTH = MATRIX_WIDTH * (LED_SIZE + LED_MARGIN)
SCREEN_HEIGHT = MATRIX_HEIGHT * (LED_SIZE + LED_MARGIN)

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # Yellow text

# Start with a large font size and adjust down if needed
INITIAL_FONT_SIZE = 70
FONT_NAME = "Bell MT"
font_size = INITIAL_FONT_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🎤 Fitted Voice-Controlled P10 Display")

clock = pygame.time.Clock()

message = " P10 Display!  "

# Speech recognition setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_adjustment_ratio = 1.5
recognizer.pause_threshold = 0.5
# recognizer.operation_timeout = 5  # Removed timeout to listen indefinitely

def get_fitting_font(message, max_height):
    global font_size
    font = pygame.font.SysFont(FONT_NAME, font_size, bold=True)
    text_surface = font.render(message, True, YELLOW)
    while text_surface.get_height() > max_height and font_size > 10:
        font_size -= 1
        font = pygame.font.SysFont(FONT_NAME, font_size, bold=True)
        text_surface = font.render(message, True, YELLOW)
    return font, text_surface

def callback(recognizer, audio):
    global message, text_surface, text_width, scroll_x, font_size, FONT
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        message = "  " + text + "  "
        font_size = INITIAL_FONT_SIZE  # reset font size on new message
        FONT, text_surface = get_fitting_font(message, SCREEN_HEIGHT)
        text_width = text_surface.get_width()
        scroll_x = SCREEN_WIDTH
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"API error: {e}")

with mic as source:
    recognizer.adjust_for_ambient_noise(source)

FONT, text_surface = get_fitting_font(message, SCREEN_HEIGHT)
text_width = text_surface.get_width()
scroll_x = SCREEN_WIDTH
scroll_speed = 3

stop_listening = recognizer.listen_in_background(mic, callback)

def draw_matrix():
    for row in range(MATRIX_HEIGHT):
        for col in range(MATRIX_WIDTH):
            x = col * (LED_SIZE + LED_MARGIN)
            y = row * (LED_SIZE + LED_MARGIN)
            pygame.draw.circle(screen, (30, 30, 30), (x + LED_SIZE // 2, y + LED_SIZE // 2), LED_SIZE // 2)

def draw_text(x_offset):
    text_y = (SCREEN_HEIGHT - text_surface.get_height()) // 2
    screen.blit(text_surface, (x_offset, text_y))

running = True
while running:
    screen.fill(BLACK)
    draw_matrix()
    draw_text(scroll_x)

    scroll_x -= scroll_speed
    if scroll_x < -text_width:
        scroll_x = SCREEN_WIDTH

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

stop_listening(wait_for_stop=False)
pygame.quit()
sys.exit()
