from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InvoiceFeedback(Base):
    __tablename__ = "invoice_feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(String, nullable=False, index=True)           
    model_version = Column(String, nullable=False)                    
    ocr_text = Column(String, nullable=True)                          
    predicted_fields = Column(JSON, nullable=False)                   
    corrected_fields = Column(JSON, nullable=False)                  
    user_id = Column(String, nullable=True)                           
    confidence = Column(Float, nullable=True)                         
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<InvoiceFeedback(invoice_id='{self.invoice_id}', model_version='{self.model_version}')>"