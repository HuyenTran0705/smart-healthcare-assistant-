
import asyncio, json, time
import pygame
from pathlib import Path
import websockets
from imageio import v2 as imageio

WIDTH, HEIGHT = 800, 600
BASE = Path(__file__).parent  # thư mục chứa GIF

# ---- Load GIF an toàn & mượt ----
def load_gif_as_surfaces(path: Path):
    reader = imageio.get_reader(path)
    frames = []
    for i, im in enumerate(reader):
        # duration mỗi frame (try đọc meta; fallback 0.06s)
        try:
            md  = reader.get_meta_data(index=i)
            dur = md.get("duration", 0.06)
            if isinstance(dur, (int, float)) and dur > 5:  # ms -> s
                dur = dur / 1000.0
        except Exception:
            dur = 0.06
        # kẹp để khỏi lag
        dur = max(0.04, float(dur))

        
        surf = pygame.image.frombuffer(im.tobytes(), im.shape[1::-1], "RGB").convert()
        surf = pygame.transform.smoothscale(surf, (WIDTH, HEIGHT))
        surf = pygame.transform.flip(surf, False, True)
        frames.append((surf, dur))
    reader.close()
    if not frames:
        raise RuntimeError(f"No frames read from: {path}")
    return frames

# ---- Player ----
class GifPlayer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.mode = "neural"
        self.packs = {}
        self.idx = 0
        self.next_time = 0.0

    def load(self, name, path: Path):
        self.packs[name] = load_gif_as_surfaces(path)

    def set_mode(self, name):
        if name in self.packs and name != self.mode:
            print(f"[PLAYER] switch -> {name}")
            self.mode = name
            self.idx = 0
            self.next_time = 0.0

    def draw(self):
        pack = self.packs[self.mode]
        now = time.time()
        if now >= self.next_time:
            surf, dur = pack[self.idx]
            self.idx = (self.idx + 1) % len(pack)
            self.next_time = now + dur
        # blit frame hiện tại (idx đã tăng, nên hiển thị khung trước đó)
        surf, _ = pack[self.idx - 1]
        self.screen.blit(surf, (0, 0))
        pygame.display.flip()

# ---- WS listener ----
async def ws_listener(player: GifPlayer):
    uri = "ws://127.0.0.1:8000/ws/face"
    while True:
        try:
            async with websockets.connect(uri) as ws:
                print("[WS] connected")

                # --- HEARTBEAT: giữ kết nối sống ---
                async def _hb():
                    while True:
                        try:
                            await ws.send("ping")  # server đang await receive_text()
                        except Exception:
                            return
                        await asyncio.sleep(5)
                asyncio.create_task(_hb())  # <<< MISSING: chạy heartbeat

                player.set_mode("neural")

                while True:
                    try:
                        msg = await ws.recv()
                        data = json.loads(msg)
                    except Exception:
                        continue

                    t = data.get("type")
                    if t == "mode":
                        print("[WS] mode ->", data.get("mode"))
                        player.set_mode(data.get("mode", "neural"))
                    elif t == "talk_start":
                        print("[WS] talk_start")
                        player.set_mode("happy")   # fallback
                    elif t == "talk_end":
                        print("[WS] talk_end")
                        player.set_mode("neural")
        except Exception as e:
            print("[WS] reconnect in 0.5s:", e)
            await asyncio.sleep(0.5)


# ---- Main loop ----
async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Face (GIF)")
    clock = pygame.time.Clock()

    player = GifPlayer(screen)
    # chỉnh tên GIF cho đúng file của bạn
    player.load("neural", BASE / "robot_neutral_blink.gif")
    player.load("happy",  BASE / "robot_blink_3s.gif")
    player.load("sad",    BASE / "robot_sad_blink.gif")

    # debug: in số frame
    print("neural frames:", len(player.packs["neural"]))
    print("happy  frames:", len(player.packs["happy"]))
    print("sad    frames:", len(player.packs["sad"]))

    # chạy WS song song
    asyncio.create_task(ws_listener(player))

    # vòng lặp hiển thị
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); return
        # phím tắt đổi mode test nhanh
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]: player.set_mode("neural")
        if keys[pygame.K_2]: player.set_mode("happy")
        if keys[pygame.K_3]: player.set_mode("sad")

        player.draw()
        clock.tick(60)

if __name__ == "__main__":
    asyncio.run(main())
