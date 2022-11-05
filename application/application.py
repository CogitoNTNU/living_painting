import time
from typing import Tuple
import pygame

from face_detection.face_detection_mediapipe import face_mesh_obj
from .frame_func import get_new_frame, load_image_data

WINDOW_NAME = "Living painting"
TARGET_FRAME_RATE = 60
BACKGROUND_COLOR = (0, 0, 0)
FULLSCREEN = True
DEFAULT_RESOLUTION = (800, 800)  # if not fullscreen
BLACK = (255, 0, 0)


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
    image_data = load_image_data()
    offset = (0, 0)

    myfont = pygame.font.SysFont("monospace", 75)

    i = -1
    fmObj = face_mesh_obj()

    coord_iterator = iter(fmObj.detect_face())
    while running:
        i += 1

        x, y, z = next(coord_iterator)
        # Did the user click the window close button?

        current_time = (start_time - time.time()) * 1000  # in milliseconds
        new_frame, new_offset, needs_update = get_new_frame(
            image_data,
            x,
            y,
            current_time,
            clock.get_time(),
            resolution,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        if needs_update:
            offset = new_offset
            frame = pygame.surfarray.make_surface(new_frame)
            # Fill the background with white

        screen.fill(BACKGROUND_COLOR)

        # Draw a solid blue cle in the center
        screen.blit(frame, offset)

        label = myfont.render("fps" + str(clock.get_fps())[:4], 1, BLACK)
        screen.blit(label, (0, 10))
        label = myfont.render("angle x" + str(round(x, 3)), 1, BLACK)
        screen.blit(label, (0, 100))
        label = myfont.render("angle y" + str(round(1 - y, 3)), 1, BLACK)
        screen.blit(label, (0, 190))
        # Flip the display

        pygame.display.flip()

        clock.tick(TARGET_FRAME_RATE)


def application():
    main()
