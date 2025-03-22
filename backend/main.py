from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from chat_service import get_legal_advice
from database import create_db, SessionLocal, ChatHistory
from pydantic import BaseModel

app = FastAPI()

PAGE_SIZE = 10

create_db()

class ChatRequest(BaseModel):
    question: str
    conversation_id: str = "default"  # conv id for tracking placeholder

class ChatHistoryResponse(BaseModel):
    question: str
    answer: str
    created_at: datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 # updated to have timestamps
@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    answer = get_legal_advice(request.question, request.conversation_id)
    
    chat_entry = ChatHistory(question=request.question, answer=answer, created_at=datetime.utcnow())
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)
    
    print(f"Returning: {chat_entry.created_at}")
    return {
        "question": request.question,
        "answer": answer,
        "created_at": chat_entry.created_at.isoformat()
    }

@app.get("/chat-history")
async def chat_history(page: int = 1, db: Session = Depends(get_db)):
    skip = (page - 1) * PAGE_SIZE
    chat_history = db.query(ChatHistory).order_by(desc(ChatHistory.created_at)).offset(skip).limit(PAGE_SIZE).all()
    
    return {
        "page": page,
        "page_size": PAGE_SIZE,
        "total": db.query(ChatHistory).count(),
        "data": [
            {
                "id": entry.id,
                "question": entry.question,
                "answer": entry.answer,
                "created_at": entry.created_at
            } for entry in chat_history
        ]
    }

@app.delete("/delete-chat")
async def delete_all_chats(db: Session = Depends(get_db)):
    db.query(ChatHistory).delete()
    db.commit()
    return {"message": "All chat history deleted successfully"}