from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import crud
import models
import schemas
from database import SessionLocal, engine
from auth import verify_token
from email_utils import send_email
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Public endpoint to create a lead
@app.post("/leads/", response_model=schemas.Lead)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    db_lead = crud.create_lead(db=db, lead=lead)
    # Send email to prospect
    prospect_email_content = "Hello, thank you for submitting your lead."
    send_email(to_email=lead.email, subject="Lead Submission Confirmation", content=prospect_email_content)
    # Send email to attorney
    attorney_email_content = f"A new lead has been submitted by {lead.first_name} {lead.last_name}."
    send_email(to_email="attr@example.com", subject="New Lead Submission", content=attorney_email_content)
    return db_lead

# Protected endpoint to read leads for a person (same last name and first name)
@app.get("/leads/", response_model=List[schemas.Lead])
def read_leads(
    first_name: str,
    last_name: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(security)
):
    user = verify_token(credentials)
    leads = crud.get_leads_for_person(db, first_name=first_name, last_name=last_name, skip=skip, limit=limit)
    return leads

# Protected endpoint to update lead state
@app.put("/leads/{lead_id}", response_model=schemas.Lead)
def update_lead_state(
    lead_id: int,
    lead_update: schemas.LeadUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(security)
):
    user = verify_token(credentials)
    db_lead = crud.update_lead_state(db, lead_id, lead_update)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead