from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from modules.paretto import paretto
from modules.ahp import synthesize
from modules.transport import transport_task

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ParettoJSON(BaseModel):
    alternatives: Optional[List] = None
    matrix: List[List]
    comparison: List


class AHPJSON(BaseModel):
    alternatives: Optional[List] = None
    matrix: List[List]
    criteria_matrix: List[List]
    comparison: List


class TransportJSON(BaseModel):
    suppliers: List
    buyers: List
    matrix: List[List]


@app.options("/api/paretto")
async def paretto_options():
    return JSONResponse(content={}, status_code=200)


@app.post("/api/paretto")
def paretto_method(data: ParettoJSON):
    if not data.alternatives:
        data.alternatives = [f"Альтернатива №{i + 1}" for i in range(len(data.matrix[0]))]
    return paretto(
        alternatives=data.alternatives, criteria=data.matrix, comparison=data.comparison
    )


@app.post("/api/ahp")
def ahp_method(data: AHPJSON):
    if not data.alternatives:
        data.alternatives = [f"Альтернатива №{i + 1}" for i in range(len(data.matrix[0]))]
    return synthesize(
        criteria_matrix=data.criteria_matrix,
        values=data.matrix,
        alternatives=data.alternatives,
        comparison=data.comparison,
    )


@app.post("/api/transport_task")
def ahp_method(data: TransportJSON):
    return transport_task(mtx=data.matrix, buyers=data.buyers, suppliers=data.suppliers)
