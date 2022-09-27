import time
from typing import Tuple
import pygame
from .frame_func import get_new_frame

WINDOW_NAME = "Living painting"
TARGET_FRAME_RATE = 30
BACKGROUND_COLOR = (0, 0, 0)
FULLSCREEN = True
DEFAULT_RESOLUTION = (800, 800)  # if not fullscreen


class TimeHandler:
    def __init__(self, target_framerate: int = 24) -> None:
        self.target_framerate = target_framerate
        self.start_time = time.time()
        self.frame_time = self.start_time

    def get_wait_time(self) -> int:
        """In milliseconds"""
        end_time = time.time()
        diff_time = self.frame_time - end_time
        wait_time = int((1000 - diff_time * 1000) / self.target_framerate)
        return wait_time

    def reset(self):
        self.frame_time = time.time()

    def get_time_from_start(self) -> float:
        """In seconds"""
        return time.time() - self.start_time


def pygame_main_application(fullscreen: bool, resolution: Tuple[int]):
    """Handle creating the pygame environment before starting,
    and tearing it down when finished"""

    def decorator(func):
        def wrapper():
            pygame.init()
            clock = pygame.time.Clock()
            if not fullscreen:
                window_resolution = resolution
                screen = pygame.display.set_mode(window_resolution)
            else:
                screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
                info = pygame.display.Info()
                window_resolution = info.current_w, info.current_h
            func(screen, window_resolution, clock)
            pygame.quit()

        return wrapper

    return decorator


@pygame_main_application(fullscreen=FULLSCREEN, resolution=DEFAULT_RESOLUTION)
def main(screen: pygame.Surface, resolution: Tuple[int], clock: pygame.time.Clock):
    running = True
    start_time = time.time()
    while running:
        # Did the user click the window close button?

        current_time = (start_time - time.time()) * 1000  # in milliseconds
        new_frame, needs_update = get_new_frame(
            0.0, 0.0, current_time, clock.get_time(), resolution
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        if needs_update:
            frame = pygame.surfarray.make_surface(new_frame)
            # Fill the background with white

        screen.fill(BACKGROUND_COLOR)

        # Draw a solid blue cle in the center
        screen.blit(frame, (0, 0))

        # Flip the display

        pygame.display.flip()

        clock.tick(TARGET_FRAME_RATE)


def application():
    main()
