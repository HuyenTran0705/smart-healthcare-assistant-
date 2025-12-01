import pygame, sys, time, math, imageio
import numpy as np
import math, time
import face_bus
face_bus.start()   # bật listener nền

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Smiling Robot Face Blink")
clock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,160,255)

frames = []

def capture_frame():
    data = pygame.surfarray.array3d(pygame.display.get_surface())
    data = np.rot90(data, 3)
    data = np.flipud(data)
    return data

def draw_eye(x, y, open_ratio):
    """Vẽ một con mắt"""
    if open_ratio > 0.2:
        # Mắt mở (ellipse)
        pygame.draw.ellipse(screen, WHITE, (x, y, 200, int(200*open_ratio)))
        pygame.draw.ellipse(screen, BLUE,  (x+30, y+30, 140, int(140*open_ratio)))
        pygame.draw.ellipse(screen, BLACK, (x+60, y+50, 80, int(80*open_ratio)))
    else:
        # Mắt nhắm (vẽ 1 đường cong mảnh)
        rect = pygame.Rect(x, y+90, 200, 40)
        pygame.draw.arc(screen, WHITE, rect, math.radians(0), math.radians(180), 4)

def draw_robot_face(eye_open=1.0, mouth_open=0.20):
    screen.fill(BLACK)

    # Mắt trái/phải
    draw_eye(180, 100, eye_open)
    draw_eye(420, 100, eye_open)

    # Miệng — scale theo mouth_open (0.0..1.0)
    # base: 160x80, ta thay đổi độ cao cung miệng theo mouth_open
    base_rect = pygame.Rect(320, 340, 160, 80)
    h = int(20 + 60 * mouth_open)               # 20..80
    mouth_rect = pygame.Rect(base_rect.x, base_rect.y + (80 - h), 160, h)
    pygame.draw.arc(screen, WHITE, mouth_rect, math.radians(200), math.radians(340), 6)

    pygame.display.flip()



# ==== Animation: blink mỗi 3 giây ====
blink_count = 3  # số lần chớp trong GIF
fps = 20

for _ in range(blink_count):
    # Giữ mắt mở ~3 giây
    for _ in range(3 * fps):
        draw_robot_face(1)
        time.sleep(1/fps)

    # Nhắm mắt dần
    for r in [0.7,0.4,0.2,0]:
        draw_robot_face(r)
        time.sleep(1/fps)

    # Mở mắt dần
    for r in [0.2,0.4,0.7,1]:
        draw_robot_face(r)
        time.sleep(1/fps)

# ==== Xuất thành GIF ====
imageio.mimsave("robot_blink_3s.gif", frames, fps=fps, loop=0)
print("✅ Đã tạo file robot_blink_3s.gif")
pygame.quit()

