from fastapi import APIRouter, Request, WebSocket
from  fastapi.responses import JSONResponse, StreamingResponse
from model_data.improved_detector import process_frames
from pydantic import BaseModel

router = APIRouter(
    prefix="/stream",
    tags=["other"],
)


global webSocket

webSocket = None

@router.get("/", response_class=StreamingResponse, status_code=200)
def video_stream():
    return StreamingResponse(process_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    global webSocket
    webSocket = ws
    await ws.accept()
    while True:
        data = await webSocket.receive_text()
        await webSocket.send_text(f"Message text was: {data}")

class Model(BaseModel):
    message: str
@router.post("/alert")

async def alert_endpoint(Model: Model):
    global webSocket
    ws = webSocket
    if ws:
        await ws.send_text(Model.message)
    return {
        "luck": "muck"
    }