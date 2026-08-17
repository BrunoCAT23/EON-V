import pygame
import random
import math
import time

from state_manager import state_manager

pygame.init()

WIDTH = 900
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EON-V Eyes AI System")

clock = pygame.time.Clock()

# ============================================
# COLORS
# ============================================

BG = (0, 0, 0)

EYE_BLUE = (80, 220, 255)
EYE_GLOW = (40, 120, 255)

SCAN_BLUE = (90, 255, 255)

CHARGE_BLUE = (120, 240, 255)

# ============================================
# EYE SETTINGS
# ============================================

eye_size = 108
eye_radius = 28

left_x = 365
right_x = 535

eye_y = 240

# ============================================
# ANIMATION
# ============================================

blink = 1.0

boot_start = time.time()

last_blink = time.time()
blink_delay = random.uniform(3.0, 5.0)

blinking = False
blink_start = 0

charge_level = 0

# ============================================
# DRAW GLOW
# ============================================

def draw_soft_glow(x, y, size, color):

    for i in range(8, 0, -1):

        glow_surface = pygame.Surface(
            (size + i * 12, size + i * 12),
            pygame.SRCALPHA
        )

        alpha = max(2, 10 - i)

        pygame.draw.rect(
            glow_surface,
            (*color, alpha),
            glow_surface.get_rect(),
            border_radius=eye_radius + i
        )

        screen.blit(glow_surface, (x - i * 6, y - i * 6))

# ============================================
# DRAW EYE
# ============================================

def draw_eye(center_x,
             custom_size=None,
             custom_height=None,
             color=None,
             glow=None):

    global blink

    size = custom_size if custom_size else eye_size

    eye_color = color if color else EYE_BLUE
    glow_color = glow if glow else EYE_GLOW

    current_h = custom_height if custom_height else int(size * blink)

    current_h = max(8, current_h)

    x = center_x - size // 2
    y = eye_y - current_h // 2

    # breathing effect
    breathe = math.sin(time.time() * 2.0) * 2
    y += breathe

    # glitch effect
    if state_manager.get_state() == "glitch":

        x += random.randint(-5, 5)
        y += random.randint(-4, 4)

    draw_soft_glow(x, y, size, glow_color)

    pygame.draw.rect(
        screen,
        eye_color,
        (x, y, size, current_h),
        border_radius=eye_radius
    )

    # glass reflection
    glass = pygame.Surface((size, current_h), pygame.SRCALPHA)

    pygame.draw.rect(
        glass,
        (255, 255, 255, 14),
        glass.get_rect(),
        border_radius=eye_radius
    )

    screen.blit(glass, (x, y))

# ============================================
# BLINK
# ============================================

def update_blink():

    global blinking
    global blink_start
    global blink
    global last_blink
    global blink_delay

    if state_manager.get_state() == "sleep":

        blink = 0.10
        return

    now = time.time()

    if not blinking and now - last_blink > blink_delay:

        blinking = True
        blink_start = now

    if blinking:

        t = now - blink_start

        if t < 0.07:

            blink = 1.0 - (t / 0.07)

        elif t < 0.14:

            blink = (t - 0.07) / 0.07

        else:

            blink = 1.0

            blinking = False

            last_blink = now

            blink_delay = random.uniform(2.5, 5.0)

# ============================================
# BOOT
# ============================================

def boot_animation():

    elapsed = time.time() - boot_start

    progress = min(1.0, elapsed / 1.8)

    size = int(108 * progress)

    height = max(8, int(108 * progress))

    if progress < 0.25:

        height = 10

    elif progress < 0.55:

        height = int(108 * progress)

    else:

        size = 108
        height = 108

    draw_eye(
        left_x,
        custom_size=max(20, size),
        custom_height=height
    )

    draw_eye(
        right_x,
        custom_size=max(20, size),
        custom_height=height
    )

# ============================================
# IDLE
# ============================================

def idle_animation():

    draw_eye(left_x)
    draw_eye(right_x)

# ============================================
# LISTENING
# ============================================

def listening_animation():

    pulse = (math.sin(time.time() * 5) + 1) * 0.5

    h = int(80 + pulse * 35)

    draw_eye(left_x, custom_height=h)
    draw_eye(right_x, custom_height=h)

    scan_y = int((math.sin(time.time() * 5) + 1) * 0.5 * 120 + 180)

    pygame.draw.line(
        screen,
        SCAN_BLUE,
        (270, scan_y),
        (630, scan_y),
        3
    )

# ============================================
# THINKING
# ============================================

def thinking_animation():

    pulse = (math.sin(time.time() * 4) + 1) * 0.5

    h = int(55 + pulse * 70)

    draw_eye(left_x, custom_height=h)
    draw_eye(right_x, custom_height=h)

# ============================================
# TALKING
# ============================================

def talking_animation():

    pulse = (math.sin(time.time() * 15) + 1) * 0.5

    h = int(85 + pulse * 35)

    draw_eye(left_x, custom_height=h)
    draw_eye(right_x, custom_height=h)

# ============================================
# AUDIO REACTIVE
# ============================================

def audio_animation():

    fake_audio = (
        math.sin(time.time() * 12)
        + random.random() * 0.5
    )

    h = int(85 + fake_audio * 35)

    draw_eye(left_x, custom_height=h)
    draw_eye(right_x, custom_height=h)

# ============================================
# HOLOGRAM
# ============================================

def hologram_animation():

    pulse = int((math.sin(time.time() * 4) + 1) * 30)

    color = (
        min(255, EYE_BLUE[0] + pulse),
        min(255, EYE_BLUE[1] + pulse),
        255
    )

    draw_eye(
        left_x,
        color=color,
        glow=(70, 180, 255)
    )

    draw_eye(
        right_x,
        color=color,
        glow=(70, 180, 255)
    )

    for _ in range(5):

        y = random.randint(170, 310)

        pygame.draw.line(
            screen,
            (80, 220, 255),
            (260, y),
            (640, y),
            1
        )

# ============================================
# GLITCH
# ============================================

def glitch_animation():

    draw_eye(left_x)
    draw_eye(right_x)

    for _ in range(7):

        x = random.randint(250, 650)
        y = random.randint(170, 310)

        w = random.randint(20, 90)

        pygame.draw.rect(
            screen,
            (80, 220, 255),
            (x, y, w, 3)
        )

# ============================================
# CHARGING
# ============================================

def charging_animation():

    global charge_level

    charge_level += 0.005

    if charge_level > 1:
        charge_level = 0

    h = int(30 + charge_level * 100)

    draw_eye(
        left_x,
        custom_height=h,
        color=CHARGE_BLUE,
        glow=(40, 180, 255)
    )

    draw_eye(
        right_x,
        custom_height=h,
        color=CHARGE_BLUE,
        glow=(40, 180, 255)
    )

    pygame.draw.rect(
        screen,
        (40, 120, 255),
        (300, 380, 300, 8),
        border_radius=4
    )

    pygame.draw.rect(
        screen,
        (100, 230, 255),
        (300, 380, int(300 * charge_level), 8),
        border_radius=4
    )

# ============================================
# SLEEP
# ============================================

def sleep_animation():

    h = 12 + int(math.sin(time.time() * 2) * 2)

    draw_eye(left_x, custom_height=h)
    draw_eye(right_x, custom_height=h)

# ============================================
# MAIN LOOP
# ============================================

def run_eyes():

    running = True

    while running:

        screen.fill(BG)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        update_blink()

        if time.time() - boot_start < 1.8:

            boot_animation()

        else:

            current_state = state_manager.get_state()

            if current_state == "idle":

                idle_animation()

            elif current_state == "listening":

                listening_animation()

            elif current_state == "thinking":

                thinking_animation()

            elif current_state == "talking":

                talking_animation()

            elif current_state == "sleep":

                sleep_animation()

            elif current_state == "glitch":

                glitch_animation()

            elif current_state == "charging":

                charging_animation()

            elif current_state == "audio":

                audio_animation()

            elif current_state == "hologram":

                hologram_animation()

            else:

                idle_animation()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

# ============================================
# START
# ============================================

if __name__ == "__main__":

    run_eyes()