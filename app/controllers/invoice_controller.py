import os, uuid
from datetime import datetime
from fastapi import UploadFile
# from .ocr import Invoice_OCR
from .data_extraction import DataExtraction

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVOICE_DIR = os.path.join(BASE_DIR, "static", "invoices")
os.makedirs(INVOICE_DIR, exist_ok=True)

# ocr_obj = Invoice_OCR()
data_ext_obj = DataExtraction()

async def process_invoice_upload(file: UploadFile) -> dict:
    filename = f"{uuid.uuid4().hex[:10]}_{file.filename}"
    file_path = os.path.join(INVOICE_DIR, filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # ocr_output_dir = ocr_obj.image_ocr(file_path)
    # if not ocr_output_dir:
    #     return {"status": "error", "error": "OCR processing failed"}
    
    ocr_output_dir = os.path.join(BASE_DIR, "data", "ocr_output/image_sample_invoice_res.json")
    # ocr_output_dir = 'app/data/ocr_output/image_sample_invoice_res.json'
    extracted_data = data_ext_obj.rule_based_extraction(ocr_output_dir)
    
    # Sample response structure
    sample_basic_invoice_data = {
        "vendor_name": "---",
        "invoice_number": "0001",
        "invoice_date": "1900-00-00",
        "tax_amount": 00.00,
        "total_amount": 00.00
    }
    
    sample_accounting_entry = {
        "debit_account": "Office Expense",
        "credit_account": "Accounts Payable"
    }
    
    return {
        "status": "success",
        "extracted_data": extracted_data['basic_invoice_data'] if 'basic_invoice_data' in extracted_data else sample_basic_invoice_data,
        "accounting_proposal": extracted_data['accounting_entry'] if 'accounting_entry' in extracted_data else sample_accounting_entry,
        "confidence_score": extracted_data['confidence_score'] if 'confidence_score' in extracted_data else 0,
        "model_version": "v1.0"
    }
