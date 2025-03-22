from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from chat_service import get_legal_advice
from database import create_db, SessionLocal, ChatHistory
from pydantic import BaseModel

app = FastAPI()

create_db()

class ChatRequest(BaseModel):
    question: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    answer = get_legal_advice(request.question)
    
    chat_entry = ChatHistory(question=request.question, answer=answer, created_at=datetime.utcnow())
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)
    
    return {"question": request.question, "answer": answer}

@app.get("/chat-history")
async def chat_history(db: Session = Depends(get_db)):
    chat_history = db.query(ChatHistory).all()
    return [{"question": entry.question, "answer": entry.answer, "created_at": entry.created_at} for entry in chat_history]

@app.delete("/delete-chat")
async def delete_chat(db: Session = Depends(get_db)):
    db.query(ChatHistory).delete()
    db.commit()
    return {"message": "Chat history deleted successfully"}
