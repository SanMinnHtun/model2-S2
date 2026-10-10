"""Career quiz prediction API."""

import logging
from pathlib import Path
from typing import Any, Optional

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from career_diagnostic import QUESTIONS, TARGET_ROLES


MODEL_PATH = Path(__file__).resolve().parents[1] / "career_diagnostic_pipeline.joblib"
router = APIRouter(prefix="/api/v1/career", tags=["Model 2: IT Career Diagnostic"])
logger = logging.getLogger(__name__)
_model: Optional[Any] = None


def load_model() -> None:
    """Load the trained pipeline once, using the absolute path above."""
    global _model
    _model = None

    if not MODEL_PATH.is_file():
        logger.error("Career model file was not found: %s", MODEL_PATH)
        return

    try:
        _model = joblib.load(MODEL_PATH)
    except Exception:
        logger.exception("Failed to load career model from %s", MODEL_PATH)
        return

    logger.info("Loaded career model from %s", MODEL_PATH)


def model_is_loaded() -> bool:
    return _model is not None


class CareerQuizRequest(BaseModel):
    # Keep raw JSON types so strings, floats, and booleans are rejected rather
    # than silently coerced to integers by Pydantic.
    answers: Any


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
    answers = request.answers
    if not isinstance(answers, list) or len(answers) != len(QUESTIONS):
        raise HTTPException(
            status_code=422,
            detail="answers must be a list containing exactly 10 integers from 0 to 4",
        )
    if any(type(value) is not int or not 0 <= value <= 4 for value in answers):
        raise HTTPException(
            status_code=422,
            detail="every answer must be an integer from 0 to 4",
        )

    if _model is None:
        raise HTTPException(
            status_code=503,
            detail="Career model is not loaded. Check the Render build and runtime logs.",
        )

    try:
        features = pd.DataFrame([answers], columns=[f"Q{index}" for index in range(1, 11)])
        predicted_role = str(_model.predict(features)[0])
        probabilities = _model.predict_proba(features)[0]
        classes = _model.named_steps["classifier"].classes_
        # Keep a fixed nine-role response shape, even if a class was absent from
        # the synthetic training labels. Missing classes have zero probability.
        probability_map = {role: 0.0 for role in TARGET_ROLES}
        probability_map.update({str(role): float(probability) for role, probability in zip(classes, probabilities)})
        confidence = probability_map[predicted_role]
        return {"predicted_role": predicted_role, "confidence": confidence, "probabilities": probability_map}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Career prediction failed")
        raise HTTPException(status_code=500, detail=f"Career prediction failed: {exc}") from exc
