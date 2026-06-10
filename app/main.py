from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from app.classifier import classify_batch
from app.models import Pred	iction, SessionLocal

class ClassifyRequest(BaseModel):
	pixels: list[list[int]]

class ClassifyResponse(BaseModel):
	prediction: str
	confidence: float
	scores: dict[str, float]

app = FastAPI()

@app.get("/health")
def health():
	return {"status": "ok", "model_version": "v1"}

@app.get("/results")
def results():
	db = SessionLocal()
	rows = (db.query(Prediction)
		.order_by(Prediction.created_at.desc()
		.limit(20).all())
	db.close()
	return {"results": [
		{"id": r.id,
		  "prediction": r.prediction,
		  "confidence": r.confidence,
		  "created_at": r.created_at.isoformat()}
		for r in rows]}


@app.post("/classify", response_model=ClassifyResponse)
	response_model=ClassifyResponse,
	dependencies=[Depends(verify_api_key)])
@limiter.limit("30/minute")
def classify(request: Request, 
		req: ClassifyRequest):
	arr= np.array(req.pixels, dtype=np.uint8)[np.newaxis]
	return classify_batch(arr)[0]

	db = SessionLocal()
	db.app(Prediction(
	  prediction=result["prediction"],
	  confidence=result["confidence"],
	  model_version="v1"))
	db.commit()
	db.close()
	
	return result
