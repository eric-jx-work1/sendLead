from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import crud
import models
import schemas
from database import SessionLocal, engine
from auth import authenticate_user, create_access_token
from email_utils import send_email
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
import shutil

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fake users database
fake_users_db = {
    "attorney": {
        "username": "attorney",
        "full_name": "Attorney User",
        "email": "attorney@example.com",
        "hashed_password": "123qweasd",  # Replace with hashed password in a real app
        "disabled": False,
    }
}

@app.post("/token")
def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Public endpoint to create a lead
    # TODO sendGrid API key setup
    # # Send email to prospect
    # prospect_email_content = "Hello, thank you for submitting your lead."
    # send_email(to_email=lead.email, subject="Lead Submission Confirmation", content=prospect_email_content)
    # # Send email to attorney
    # attorney_email_content = f"A new lead has been submitted by {lead.first_name} {lead.last_name}."
    # send_email(to_email="attr@example.com", subject="New Lead Submission", content=attorney_email_content)
@app.post("/leads/", response_model=schemas.Lead)
def create_lead(
    first_name: str,
    last_name: str,
    email: str,
    db: Session = Depends(get_db),
    resume: UploadFile = File(...)
):
    file_location = f"resumes/{resume.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(resume.file, file_object)

    lead_data = schemas.LeadCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        resume=file_location
    )
    db_lead = crud.create_lead(db=db, lead=lead_data)
    return db_lead

# Protected endpoint to read leads for a person (same last name and first name)
@app.get("/leads/", response_model=List[schemas.Lead])
def read_leads(
    first_name: str,
    last_name: str,
    limit: int = 10,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    print(token)
    leads = crud.get_leads_for_person(db, first_name=first_name, last_name=last_name, limit=limit)
    return leads

# Protected endpoint to update lead state
@app.put("/leads/{lead_id}", response_model=schemas.Lead)
def update_lead_state(
    lead_id: int,
    lead_update: schemas.LeadUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    print(token)
    db_lead = crud.update_lead_state(db, lead_id, lead_update)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead