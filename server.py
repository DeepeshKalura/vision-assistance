from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import  multimodel, sos, obstacle_detection

app = FastAPI(title="Video Assistance API", version="0.0.1")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)

app.include_router(sos.router)
app.include_router(multimodel.router)
app.include_router(obstacle_detection.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

