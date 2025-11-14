from fastapi import FastAPI, Depends, HTTPException
from . import models, database, tasks
from .schemas import TicketCreate, TicketOut
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
import os

# create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Support Workflow API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/webhook/message", response_model=TicketOut)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    ticket = models.Ticket(user_id=payload.user_id, message=payload.message)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # enqueue a background job to process this ticket
    tasks.process_ticket.delay(ticket.id)

    return ticket

@app.get("/ticket/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
