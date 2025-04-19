from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from main import ProductRecommender
import os

# Load model (load once for performance)
recommender = ProductRecommender("product_catalog.csv")

app = FastAPI()

# ---------- Health Check ----------
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ---------- Request Schema ----------
class QueryRequest(BaseModel):
    query: str

# ---------- Response Schema ----------
class Assessment(BaseModel):
    url: str
    adaptive_support: str
    description: str
    duration: int
    remote_support: str
    test_type: List[str]

class RecommendationResponse(BaseModel):
    recommended_assessments: List[Assessment]

# ---------- Recommendation Endpoint ----------
@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_assessments(request: QueryRequest):
    try:
        result = recommender.recommend_simple(request.query)
        print(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")
