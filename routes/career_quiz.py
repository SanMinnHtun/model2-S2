"""Career quiz prediction API."""

from pathlib import Path
from typing import List

import joblib
import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator

from career_diagnostic import QUESTIONS, TARGET_ROLES


MODEL_PATH = Path(__file__).resolve().parents[1] / "career_diagnostic_pipeline.joblib"
router = APIRouter(prefix="/api/v1/career", tags=["Model 2: IT Career Diagnostic"])


class CareerQuizRequest(BaseModel):
    answers: List[int]

    @validator("answers", pre=True)
    def validate_answers(cls, answers: List[int]) -> List[int]:
        if not isinstance(answers, list):
            raise ValueError("answers must be a list")
        if len(answers) != 10:
            raise ValueError("answers must contain exactly 10 integers")
        if any(type(value) is not int or not 0 <= value <= 4 for value in answers):
            raise ValueError("every answer must be an integer from 0 to 4")
        return answers


@router.get("/questions")
def get_questions() -> dict[str, object]:
    """Return the quiz bank in a frontend-friendly, stable format."""
    return {
        "questions": [
            {
                "id": f"Q{index}",
                "text": item["question"],
                "options": [
                    {"value": option_index, "label": label}
                    for option_index, label in enumerate(item["options"])
                ],
            }
            for index, item in enumerate(QUESTIONS, start=1)
        ]
    }


@router.post("/predict")
def predict_career(request: CareerQuizRequest) -> dict[str, object]:
    if not MODEL_PATH.is_file():
        raise HTTPException(status_code=503, detail="Career model is not available. Run train_career_model.py first.")
    try:
        model = joblib.load(MODEL_PATH)
        features = np.asarray(request.answers, dtype=int).reshape(1, -1)
        predicted_role = str(model.predict(features)[0])
        probabilities = model.predict_proba(features)[0]
        classes = model.named_steps["classifier"].classes_
        # Keep a fixed nine-role response shape, even if a class was absent from
        # the synthetic training labels. Missing classes have zero probability.
        probability_map = {role: 0.0 for role in TARGET_ROLES}
        probability_map.update({str(role): float(probability) for role, probability in zip(classes, probabilities)})
        confidence = probability_map[predicted_role]
        return {"predicted_role": predicted_role, "confidence": confidence, "probabilities": probability_map}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Career prediction failed.") from exc
