# Invoice Intelligence with Learning Loop

An OCR-based invoice processing system built with FastAPI for extracting and managing invoice data.

## Folder Structure

```
Teera_ai/
├── app/
│   ├── app.py                      # FastAPI main application entry point
│   ├── invoice_feedback.db         # SQLite database for feedback storage
│   ├── controllers/
│   │   ├── data_extraction.py      # Data extraction and parsing logic
│   │   ├── db_config.py            # Database configuration and setup
│   │   ├── feedback.py             # Feedback management functionality
│   │   ├── invoice_controller.py   # API endpoints for invoice operations
│   │   └── ocr.py                  # OCR processing and recognition
│   ├── models/
│   │   └── models.py               # Data models and schemas
│   ├── static/
│   │   ├── custom_css.css          # Custom styling
│   │   ├── custom_js.js            # Frontend JavaScript logic
│   │   └── invoices/               # Invoice storage directory
│   └── templates/
│       └── index.html              # Main HTML interface
├── data/
│   ├── OCR.docx                    # Documentation and notes
│   ├── pdf_sample_invoice.pdf      # Sample invoice for testing
├── notebook/
│   ├── Donut-ITT.ipynb            # Donut model research and experiments
│   ├── OCR-R&D.ipynb              # OCR research and development
│   ├── Sample-LayoutLmv3_training_invoice_dataset.ipynb  # LayoutLMv3 training notebook
│   └── invoice_output/            # Output storage for notebook experiments
├── README.md                        # This file
└── requirements.txt                 # Python dependencies
```

## About This Project

This is a system designed to automate invoice processing using modern OCR and deep learning techniques. The project combines multiple approaches to extract structured data from invoice documents. It includes a frontend interface for uploading and managing invoices, backend API services for processing, and research notebooks exploring different ML models for document analysis. The system stores extracted data in a database and allows users to provide feedback on accuracy for model improvements.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv or conda)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/bilalhameed248/Invoice-Intelligence-With-Learning-Loop.git
cd Teera_ai
```

### Step 2: Create Virtual Environment

Using venv:
```bash
python -m venv venv
```

Activate virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Database

The SQLite database is automatically initialized on first run. If you need to manually set it up:

```bash
cd app
python -c "from controllers.db_config import create_db; create_db()"
cd ..
```

## Getting Started

Run the application using:

```bash
cd app
uvicorn app:app --host 0.0.0.0 --port 3636 --reload
```

Access the application at `http://localhost:3636`

### Using the Application

1. Open your browser and navigate to `http://localhost:3636`
2. Upload an invoice PDF or image file
3. The system will process the invoice and extract:
   - Vendor information
   - Invoice number and date
   - Line items and amounts
   - Tax calculations
   - Suggested accounting entries
4. Review the extracted data and provide feedback for model improvement

### Troubleshooting

**Port Already in Use:**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Module Not Found Errors:**
Make sure the virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

**Database Issues:**
Reset the database by removing `app/invoice_feedback.db` and restarting the application
