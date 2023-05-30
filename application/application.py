import time
from typing import Tuple
import pygame
import numpy as np

from face_detection.face_detection_mediapipe import FaceMeshObj
from .frame_func import get_new_frame
from .load_gif import load_gif

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


animation_speed = 0.10
background_animation_speed = 0.5
transition_speed = 0.05


def set_alpha(surf, image):
    view = np.array(surf.get_view("A"), copy=False)
    view[:, :] = image[:, :, 3]


@pygame_main_application(fullscreen=FULLSCREEN, resolution=DEFAULT_RESOLUTION)
def main(screen: pygame.Surface, resolution: Tuple[int], clock: pygame.time.Clock):
    print(resolution)
    running = True
    start_time = time.time()
    offset = (0, 0)

    gif_frames = load_gif("starrynight-seamless.gif", resolution)
    num_gif_frames = len(gif_frames)
    myfont = pygame.font.SysFont("monospace", 75)
    time_to_use = 1
    start_target_time = start_time

    i = -1
    fmObj = FaceMeshObj()
    current_x, current_y = 0.5, 0.5
    increasing = True
    delta_time_2 = 0
    target_x = 0

    files = np.load("paths.npy")
    num_styles = files.shape[0]
    current_style = 0
    style_progress = 0
    next_style = np.random.choice(range(1, num_styles))
    while running:
        i += 1
        start_time = time.time()
        # target_x, target_y, z = next(coord_iterator)

        delta_time = time.time() - start_time

        if increasing:
            target_x, target_y, z = (
                min(target_x + animation_speed * delta_time_2, 1),
                0,
                0,
            )
            if target_x == 1:
                increasing = False
        else:
            target_x, target_y, z = (
                max(target_x - animation_speed * delta_time_2, 0),
                0,
                0,
            )
            if target_x == 0:
                increasing = True

        style_progress += delta_time_2 * transition_speed
        if style_progress > 1:
            style_progress -= 1
            current_style = next_style
            next_style += 1
            if next_style == num_styles:
                next_style = 0
        start_time = time.time()
        new_frame, new_offset, needs_update = get_new_frame(
            target_x,
            files,
            current_style,
            next_style,
            style_progress,
            resolution,
        )
        delta_time_2 = time.time() - start_time

        time_index = time.time() * background_animation_speed
        time_index = int((time_index - int(time_index)) * num_gif_frames)
        background_frame = gif_frames[time_index]
        background_frame = pygame.surfarray.make_surface(background_frame[:, :, :3])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        if needs_update:
            offset = new_offset
            frame = pygame.surfarray.make_surface(new_frame[:, :, :3]).convert_alpha()
            set_alpha(frame, new_frame)

        screen.fill(BACKGROUND_COLOR)

        screen.blit(background_frame, (0, 0))

        screen.blit(frame, offset)

        # label = myfont.render("fps" + str(clock.get_fps())[:4], 1, BLACK)
        # screen.blit(label, (0, 10))
        # label = myfont.render("angle x" + str(round(target_x, 3)), 1, BLACK)
        # screen.blit(label, (0, 100))
        # label = myfont.render(
        #    "style progress " + str(f"{style_progress:.2f}"), 1, BLACK
        # )
        # screen.blit(label, (0, 190))

        pygame.display.flip()

        clock.tick(TARGET_FRAME_RATE)


def application():
    main()
