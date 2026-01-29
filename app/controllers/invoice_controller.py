import os, uuid
from datetime import datetime
from fastapi import UploadFile
from .ocr import OCR

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVOICE_DIR = os.path.join(BASE_DIR, "static", "invoices")
os.makedirs(INVOICE_DIR, exist_ok=True)


async def process_invoice_upload(file: UploadFile) -> dict:
    filename = f"{uuid.uuid4().hex[:10]}_{file.filename}"
    file_path = os.path.join(INVOICE_DIR, filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # TODO: Add your OCR and extraction logic here
    # For now, returning dummy data
    extracted_data = {
        "vendor_name": "ABC Traders Pvt Ltd",
        "invoice_number": "INV-223",
        "invoice_date": "2026-01-12",
        "tax_amount": 141.00,
        "total_amount": 2491.00
    }
    
    accounting_proposal = {
        "debit_account": "Office Expense",
        "credit_account": "Accounts Payable"
    }
    
    return {
        "status": "success",
        "extracted_data": extracted_data,
        "accounting_proposal": accounting_proposal,
        "confidence_score": 0.68,
        "model_version": "v1.0"
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
