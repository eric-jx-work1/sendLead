from sqlalchemy.orm import Session
import models
import schemas

def create_lead(db: Session, lead: schemas.LeadCreate):
    db_lead = models.Lead(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        resume=lead.resume,
        state="PENDING"
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_leads_for_person(db: Session, first_name: str, last_name: str, limit: int):
    return db.query(models.Lead).filter(models.Lead.first_name == first_name, models.Lead.last_name == last_name).limit(limit).all()

def update_lead_state(db: Session, lead_id: int, lead_update: schemas.LeadUpdate):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if db_lead:
        for key, value in lead_update.dict().items():
            setattr(db_lead, key, value)
        db.commit()
        db.refresh(db_lead)
    return db_lead
