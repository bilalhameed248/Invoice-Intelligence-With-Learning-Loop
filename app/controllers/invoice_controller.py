import os, uuid
from datetime import datetime
from fastapi import UploadFile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVOICE_DIR = os.path.join(BASE_DIR, "static", "invoices")
os.makedirs(INVOICE_DIR, exist_ok=True)


async def process_invoice_upload(file: UploadFile) -> dict:
    invoice_id = f"INV-{uuid.uuid4().hex[:10]}"
    _, ext = os.path.splitext(file.filename)
    filename = f"{invoice_id}{ext}"
    file_path = os.path.join(INVOICE_DIR, filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "invoice_id": invoice_id,
        "filename": filename,
        "file_path": f"/static/invoices/{filename}",
        "uploaded_at": datetime.utcnow().isoformat(),
        "status": "uploaded"
    }

# ---------------------------------------------------------
# Feedback (Stub for Learning Loop)
# ---------------------------------------------------------
async def process_invoice_feedback(payload: dict) -> dict:
    """
    Stores user corrections (learning loop placeholder)
    """

    return {
        "message": "Feedback received",
        "invoice_id": payload.get("invoice_id"),
        "timestamp": datetime.utcnow().isoformat()
    }
