import time
from typing import Tuple
import pygame

from face_detection.face_detection_mediapipe import FaceMeshObj
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


def update_target(new_target, current_target, start_target_time, current_x, start_x):
    max_dist = 0.01
    if abs(new_target - current_target) < max_dist:
        return current_target, start_target_time, start_x
    return new_target, time.time(), current_x


def lerp(target, start, percentage):
    return start + (target - start) * percentage


def lerp_percent(start_target_time, time_to_use):
    return (time.time() - start_target_time) / time_to_use


@pygame_main_application(fullscreen=FULLSCREEN, resolution=DEFAULT_RESOLUTION)
def main(screen: pygame.Surface, resolution: Tuple[int], clock: pygame.time.Clock):
    running = True
    start_time = time.time()
    image_data = load_image_data()
    offset = (0, 0)

    myfont = pygame.font.SysFont("monospace", 75)
    time_to_use = 1
    start_target_time = start_time

    i = -1
    fmObj = FaceMeshObj()
    current_x, current_y = 0.5, 0.5
    start_x = current_x
    next_target_x = current_x
    coord_iterator = iter(fmObj.detect_face())
    while running:
        i += 1
        start_time = time.time()
        target_x, target_y, z = next(coord_iterator)
        delta_time = time.time()-start_time
        start_time = time.time()
        new_frame, new_offset, needs_update = get_new_frame(
            image_data,
            1-target_x,
            1-target_y,
            resolution,
        )
        delta_time_2 = time.time()-start_time
        print(f"times: {delta_time:.2f}, {delta_time_2:.2f}")

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
        label = myfont.render("angle x" + str(round(target_x, 3)), 1, BLACK)
        screen.blit(label, (0, 100))
        label = myfont.render("angle y" + str(round(1 - target_y, 3)), 1, BLACK)
        screen.blit(label, (0, 190))
        # Flip the display

        pygame.display.flip()

        clock.tick(TARGET_FRAME_RATE)


def application():
    main()
