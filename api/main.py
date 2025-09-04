from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from loop_creator.generator import LoopParams, generate_loop


app = FastAPI(title="FEA Loop API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoopRequest(BaseModel):
    duration_seconds: float = 2.0
    fps: int = 60
    radius: float = 100.0
    center_x: float = 0.0
    center_y: float = 0.0
    phase0_rad: float = 0.0
    elasticidade: float = 0.5
    fluidez: float = 0.5
    inercia: float = 0.5
    amolecimento: float = 0.2
    loops: int = 1
    pre_roll_loops: int = 3


class LoopFrameResponse(BaseModel):
    index: int
    time: float
    x: float
    y: float
    travel_angle: float
    orientation: float
    scale_tangent: float
    scale_normal: float


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/generate_loop", response_model=dict)
def api_generate_loop(req: LoopRequest) -> dict:
    params = LoopParams(**req.dict())
    frames = generate_loop(params)
    payload: List[LoopFrameResponse] = [
        LoopFrameResponse(
            index=f.index,
            time=f.time,
            x=f.x,
            y=f.y,
            travel_angle=f.travel_angle,
            orientation=f.orientation,
            scale_tangent=f.scale_tangent,
            scale_normal=f.scale_normal,
        ).dict()
        for f in frames
    ]
    return {"params": req.dict(), "frames": payload}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)


