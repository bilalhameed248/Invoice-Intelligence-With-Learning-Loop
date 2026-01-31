# T-OCR: Invoice Intelligence System

An OCR-based invoice processing system built with FastAPI for extracting and managing invoice data.

## Folder Structure

```
T-OCR/
├── app/
│   ├── app.py                      # Main FastAPI application entry point
│   ├── controllers/
│   │   ├── db_config.py           # Database configuration
│   │   ├── extract_fields.py      # Field extraction logic
│   │   ├── invoice_controller.py  # Invoice API endpoints
│   │   └── ocr.py                 # OCR processing logic
│   ├── models/
│   │   └── models.py              # Application models
│   ├── static/
│   │   └── custom_js.js           # Custom JavaScript files
│   └── templates/
│       └── index.html             # Frontend HTML template
├── data/
│   └── OCR.docx                   # Documentation/data files
└── notebook/                       # Jupyter notebooks (empty)
```

## Description

- **app/**: Main application directory containing the FastAPI application
  - **controllers/**: Business logic and controller modules
  - **routes/**: API route definitions
  - **static/**: Static assets (CSS, JS, images)
  - **templates/**: HTML templates for frontend
- **data/**: Storage for data files and documentation
- **notebook/**: Directory for development and analysis notebooks

## Getting Started

Run the application using:
```bash
cd app
uvicorn app:app --host 0.0.0.0 --port 3636 --reload
```

Access the application at `http://0.0.0.0:3636`
