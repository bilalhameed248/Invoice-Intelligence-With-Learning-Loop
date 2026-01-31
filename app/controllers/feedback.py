from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import InvoiceFeedback
from controllers.db_config import get_db
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class FeedbackPayload(BaseModel):
    invoice_id: str
    model_version: str
    predicted_fields: Dict
    corrected_fields: Dict
    ocr_text: Optional[str] = None
    confidence: Optional[float] = None
    user_id: Optional[str] = None

async def process_invoice_feedback(payload: FeedbackPayload, db: Session = Depends(get_db)):
    try:
        feedback = InvoiceFeedback(
            invoice_id=payload.invoice_id,
            model_version=payload.model_version,
            ocr_text=payload.ocr_text,
            predicted_fields=payload.predicted_fields,
            corrected_fields=payload.corrected_fields,
            confidence=payload.confidence,
            user_id=payload.user_id,
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)

        return {
            "status": "success",
            "message": "Feedback saved successfully",
            "feedback_id": feedback.id,
            "invoice_id": feedback.invoice_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save feedback: {str(e)}")