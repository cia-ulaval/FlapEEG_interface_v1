import pygame
import random
import threading
from threading import Event
from screen_recorder import screen_recorder

# Initialize constants
size = width, height = 1536, 864
GRAY = (68, 68, 68)

# Function to display the chronometer
def display_timer(screen, font, start_time):
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Calculate elapsed seconds
    timer_text = f"{elapsed_time}s"
    timer_surface = font.render(timer_text, True, (255, 255, 255))  # White text
    screen.blit(timer_surface, (10, 10))  # Display timer at the top-left corner

# Function to display the bird for a set duration
def display_bird(screen, flapEEG, background, font, start_time, clock, duration):
    # Random position for the bird
    x = random.randint(0, width - flapEEG.get_width())
    y = random.randint(0, height - flapEEG.get_height())

    # Display the bird for the specified duration
    end_time = pygame.time.get_ticks() + duration
    while pygame.time.get_ticks() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Draw the background, bird, and timer
        screen.blit(background, (0, 0))
        screen.blit(flapEEG, (x, y))
        display_timer(screen, font, start_time)
        pygame.display.flip()
        clock.tick(60)

# Main function
def main():
    pygame.init()

    stop_event = Event()

    recorder_thread = threading.Thread(target=screen_recorder, args=("game_session", 60.0, (1920, 1080), stop_event))
    recorder_thread.start()

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True

    # Load and scale the background image
    background = pygame.image.load("asset/bg.png")
    background = pygame.transform.scale(background, size)

    # Load Flappy Bird image
    flapEEG = pygame.image.load("asset/brainMidFlap.png")
    flapEEG = pygame.transform.scale(flapEEG, (150, 150))
    flapEEG.set_colorkey(GRAY)

    # Font for the timer
    font = pygame.font.SysFont("comicsans", 30)
    start_time = pygame.time.get_ticks()

    # Draw the background image and wait 5 seconds before starting
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.time.wait(5)

    # Set the next bird display time
    next_bird_time = pygame.time.get_ticks() + random.randint(1000, 3000)

    # Main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the background
        screen.blit(background, (0, 0))

        # Display the continuous timer
        display_timer(screen, font, start_time)

        # Check if it's time to display the bird
        if pygame.time.get_ticks() >= next_bird_time:
            display_bird(screen, flapEEG, background, font, start_time, clock, 1000)
            next_bird_time = pygame.time.get_ticks() + random.randint(1000, 3000)  # Schedule next bird

        # Update the screen
        pygame.display.flip()

        # Limit frame rate
        clock.tick(60)

    pygame.quit()
    print("Exiting game. Stopping screen recorder...")

    stop_event.set()
    recorder_thread.join()
    print("Recorder thread stopped.")

# Run the game
if __name__ == "__main__":
    main()
