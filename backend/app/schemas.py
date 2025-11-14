from pydantic import BaseModel
from typing import Optional

class TicketCreate(BaseModel):
    user_id: str
    message: str

class TicketOut(BaseModel):
    id: int
    user_id: str
    message: str
    status: str
    classification: Optional[dict]
    response: Optional[str]

    class Config:
        orm_mode = True
