from sqlalchemy.orm import Session
from models import ECG, Lead
from schemas import ECGSchema

def create_ecg(db: Session, ecg: ECGSchema):
    db_ecg = ECG(date=ecg.date)
    db.add(db_ecg)
    db.commit()
    db.refresh(db_ecg)
    
    for lead in ecg.leads:
        db_lead = Lead(ecg_id=db_ecg.id, name=lead.name, signal=lead.signal)
        db.add(db_lead)
    db.commit()
    return db_ecg

def get_ecg_insights(db: Session, ecg_id: int):
    db_ecg = db.query(ECG).filter(ECG.id == ecg_id).first()
    if not db_ecg:
        return None
    
    from utils import zero_crossings
    insights = {}
    for lead in db_ecg.leads:
        zero_crossing_count = zero_crossings(lead.signal)
        insights[lead.name] = zero_crossing_count
    
    return insights
