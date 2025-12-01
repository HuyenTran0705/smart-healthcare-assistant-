import json
from fastapi import FastAPI, WebSocket, Body
import uvicorn

# >>> NEW
import os, requests

app = FastAPI()
clients = set()

@app.websocket("/ws/face")
async def ws_face(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()  # không xử lý inbound
    except:
        clients.discard(ws)

async def push(msg: dict):
    dead = []
    for c in list(clients):
        try:
            await c.send_text(json.dumps(msg))
        except:
            dead.append(c)
    for d in dead:
        clients.discard(d)

# >>> NEW: HTTP endpoint để các process khác post vào
@app.post("/bus")
async def bus(msg: dict = Body(...)):
    await push(msg)
    return {"ok": True}

# ========= tiện ích cho module khác gọi =========

# >>> NEW: URL server (có thể override bằng env)
SERVER_URL = os.getenv("FACE_BUS_URL", "http://127.0.0.1:8000")

def _send_http(msg: dict, timeout=0.5):
    try:
        requests.post(f"{SERVER_URL}/bus", json=msg, timeout=timeout)
    except Exception as e:
        print("[orchestrator_ws] post failed:", e)

def post_face(expression="neutral", eyes="blink_cycle", mouth="idle", duration_ms=1500, priority=1):
    # đổi sang HTTP để hoạt động cross-process
    _send_http({
        "type":"face","expression":expression,
        "eyes":{"state":eyes},"mouth":{"state":mouth},
        "duration_ms":duration_ms,"priority":priority
    })

def post_talk(evt="start"):
    _send_http({"type": f"talk_{evt}"})

def post_mode(mode: str):
    _send_http({"type":"mode","mode": mode})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Lưu ý: chạy file này trước khi chạy AI.py và face_bus.py