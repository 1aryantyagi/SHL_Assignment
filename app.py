from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from main import ProductRecommender
import os

# Load model (load once for performance)
try:
    recommender = ProductRecommender("product_catalog.csv")
except Exception as e:
    print(f"❌ Failed to initialize recommender: {e}")
    recommender = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://shl-frontend-two.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        if not recommender:
            raise Exception("Recommender not initialized.")
        print(f"Received query: {request.query}")
        result = recommender.recommend_simple(request.query)
        print("Recommendation result:", result)
        return result
    except Exception as e:
        print("❌ Error during recommendation:", str(e))
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")

