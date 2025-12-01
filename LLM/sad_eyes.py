import pygame, sys, time, math, imageio
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sad Robot Face")

# Màu sắc
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,160,255)

frames = []

def capture_frame():
    """Chụp 1 frame pygame -> numpy array (H,W,3)"""
    data = pygame.surfarray.array3d(pygame.display.get_surface())
    data = np.rot90(data, 3)
    data = np.flipud(data)
    return data

def draw_eye(x, y, open_ratio):
    """Vẽ 1 mắt với độ mở open_ratio (0..1)"""
    if open_ratio > 0.2:
        # Mắt mở (ellipse)
        pygame.draw.ellipse(screen, WHITE, (x, y, 200, int(200*open_ratio)))
        pygame.draw.ellipse(screen, BLUE,  (x+30, y+30, 140, int(140*open_ratio)))
        pygame.draw.ellipse(screen, BLACK, (x+60, y+50,  80, int( 80*open_ratio)))
    else:
        # Mắt nhắm: vẽ 1 đường cong mảnh
        rect = pygame.Rect(x, y+90, 200, 40)
        pygame.draw.arc(screen, WHITE, rect, math.radians(0), math.radians(180), 4)

def draw_robot_face(open_ratio=1.0):
    screen.fill(BLACK)

    # ===== Mắt =====
    draw_eye(180, 100, open_ratio)  # trái
    draw_eye(420, 100, open_ratio)  # phải

    # ===== Miệng buồn (cong xuống) =====
    mouth_rect = pygame.Rect(320, 340, 160, 80)  # x, y, w, h
    pygame.draw.arc(screen, WHITE, mouth_rect, math.radians(20), math.radians(160), 6)

    pygame.display.flip()
    frames.append(capture_frame())

# ==== Animation: blink mỗi 3 giây ====
blink_count = 3
fps = 20

for _ in range(blink_count):
    # Giữ mắt mở ~3 giây
    for _ in range(3 * fps):
        draw_robot_face(1.0)
        time.sleep(1/fps)

    # Nhắm mắt dần
    for r in [0.7, 0.4, 0.2, 0.0]:
        draw_robot_face(r)
        time.sleep(1/fps)

    # Mở mắt dần
    for r in [0.2, 0.4, 0.7, 1.0]:
        draw_robot_face(r)
        time.sleep(1/fps)

# ==== Xuất thành GIF ====
imageio.mimsave("robot_sad_blink.gif", frames, fps=fps, loop=0)
print("✅ Đã tạo file robot_sad_blink.gif")
pygame.quit()
