from sqlalchemy.orm import Session
import models
import schemas


def get_leads_for_person(db: Session, first_name: str, last_name: str, skip: int = 0, limit: int = 10):
    return db.query(models.Lead).filter(
        models.Lead.first_name == first_name,
        models.Lead.last_name == last_name
    ).offset(skip).limit(limit).all()

def create_lead(db: Session, lead: schemas.LeadCreate):
    db_lead = models.Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def update_lead_state(db: Session, lead_id: int, lead_update: schemas.LeadUpdate):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if db_lead:
        db_lead.state = lead_update.state
        db.commit()
        db.refresh(db_lead)
    return db_lead
