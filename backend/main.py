from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from modules.paretto import paretto
from modules.ahp import synthesize
from modules.transport import transport_task

app = FastAPI()


class ParettoJSON(BaseModel):
    alternatives: List
    matrix: List[List[float]]
    comparison: List[str]


class AHPJSON(BaseModel):
    alternatives: List
    matrix: List[List[float]]
    criteria_matrix: List[List[float]]
    comparison: List[str]


class TransportJSON(BaseModel):
    suppliers: List[float]
    buyers: List[float]
    matrix: List[List[float]]


@app.post("/api/paretto")
def paretto_method(data: ParettoJSON):
    return paretto(
        alternatives=data.alternatives, criteria=data.matrix, comparison=data.comparison
    )


@app.post("/api/ahp")
def ahp_method(data: AHPJSON):
    return synthesize(
        criteria_matrix=data.criteria_matrix,
        values=data.matrix,
        alternatives=data.alternatives,
        comparison=data.comparison,
    )


@app.post("/api/transport_task")
def ahp_method(data: TransportJSON):
    return transport_task(mtx=data.matrix, buyers=data.buyers, suppliers=data.suppliers)
