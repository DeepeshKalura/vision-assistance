from fastapi import APIRouter, Request, WebSocket
from  fastapi.responses import JSONResponse, StreamingResponse
from model_data.improved_detector import process_frames

router = APIRouter(
    prefix="/stream",
    tags=["other"],
)

webSocket =  None


@router.get("/", response_class=StreamingResponse, status_code=200)
def video_stream():
    return StreamingResponse(process_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.websocket("/")
async def alert_endpoints(websocket: WebSocket):
    global webSocket
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"{data}")

@router.post("/alert")
async def alert_endpoint(request: Request):
    global websocket
    if websocket:
        data = await request.json()
        await websocket.send_text(data['message'])
    return JSONResponse(status_code=200)