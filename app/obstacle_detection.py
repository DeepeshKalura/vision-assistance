from fastapi import APIRouter
from  fastapi.responses import StreamingResponse
from model_data.improved_detector import process_frames

router = APIRouter(
    prefix="/stream",
    tags=["other"],
)

@router.get("/", response_class=StreamingResponse, status_code=200)
def video_stream():
    return StreamingResponse(process_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
