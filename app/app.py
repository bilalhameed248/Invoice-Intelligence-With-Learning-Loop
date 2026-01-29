from fastapi import FastAPI, Request, UploadFile, File, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from controllers.invoice_controller import (process_invoice_upload, process_invoice_feedback)

app = FastAPI(
    title="Invoice Intelligence with Learning Loop",
    description="AI-powered invoice extraction with accounting automation",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def load_ui(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.post("/api/invoice/upload")
async def upload_invoice(file: UploadFile = File(...)):
    """
    1. Accept invoice PDF/Image
    2. OCR → Field Extraction → Accounting Proposal
    """
    response = await process_invoice_upload(file)
    return JSONResponse(content=response)

# ---------------------------------------------------------
# API: Feedback / Learning Loop
# ---------------------------------------------------------

@app.post("/api/invoice/feedback")
async def invoice_feedback(payload: dict = Body(...)):
    """
    Accepts user corrections and stores learning data
    """
    response = await process_invoice_feedback(payload)
    return JSONResponse(content=response)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3636)