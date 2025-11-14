import os
from celery import Celery
from .database import SessionLocal
from .models import Ticket
from .utils import classify_prompt, generate_reply_prompt, call_openai
import json

CELERY_BROKER = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

worker_app = Celery("worker_app", broker=CELERY_BROKER, backend=CELERY_BACKEND)

@worker_app.task(bind=True)
def process_ticket(self, ticket_id: int):
    db = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return {"error": "ticket not found"}

        # 1) classification
        prompt = classify_prompt(ticket.message)
        raw = call_openai(prompt, max_tokens=200)
        try:
            classification = json.loads(raw)
        except Exception:
            # fallback: simple auto classification
            classification = {"category": "general", "sentiment": "neutral", "priority": "low", "missing_info": False}

        ticket.classification = classification
        db.add(ticket)
        db.commit()

        # 2) generate reply
        reply_prompt = generate_reply_prompt(ticket.message, classification)
        reply = call_openai(reply_prompt, max_tokens=200)
        ticket.response = reply
        # simple routing rule
        if classification.get("priority") in ("high", "urgent") or classification.get("missing_info"):
            ticket.status = "needs_human"
        else:
            ticket.status = "auto_responded"
        db.add(ticket)
        db.commit()
        return {"ticket_id": ticket_id, "status": ticket.status}

    finally:
        db.close()
