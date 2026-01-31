from fastapi import FastAPI, Request, UploadFile, File, Body, Depends
import uvicorn
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from controllers.invoice_controller import (process_invoice_upload)
from controllers.db_config import create_db, get_db
from controllers.feedback import *

app = FastAPI(
    title="Invoice Intelligence with Learning Loop",
    description="AI-powered invoice extraction with accounting automation",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    create_db()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def load_ui(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.post("/api/invoice/upload")
async def upload_invoice(file: UploadFile = File(...)):
    response = await process_invoice_upload(file)
    print(f"response: {response}")
    return JSONResponse(content=response)

@app.post("/api/invoice/feedback")
async def invoice_feedback(payload: dict = Body(...), db: Session = Depends(get_db)):
    try:
        validated = FeedbackPayload(**payload)
    except Exception as e:
        return JSONResponse(status_code=422, content={"detail": f"Invalid payload: {str(e)}"}        )
    response = await process_invoice_feedback(validated, db)
    print("response:",response)
    return JSONResponse(content=response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3636)
