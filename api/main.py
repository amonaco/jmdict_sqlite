from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Progress, Entry
import random

Base.metadata.create_all(bind=engine)

app = FastAPI(title="JLPT Flashcards API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- USERS ----------

@app.post("/login")
def login(name: str):
    token = secrets.token_hex(16)
    return {"token": token, "user_id": 1}


@app.post("/users")
def create_user(name: str, db: Session = Depends(get_db)):
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ---------- FLASHCARD ----------

@app.get("/flashcard/{user_id}/{level}")
def get_flashcard(user_id: int, level: str, db: Session = Depends(get_db)):
    entries = db.query(Entry).filter(Entry.jlpt_level == level).all()
    if not entries:
        raise HTTPException(404, "No entries for level")

    entry = random.choice(entries)

    return {
        "entry_id": entry.id,
        "question": f"Word ID {entry.id}",
        "hint": "Look at kanji/readings tables"
    }

# ---------- ANSWER ----------

@app.post("/answer")
def answer(user_id: int, entry_id: int, correct: bool, db: Session = Depends(get_db)):
    prog = db.query(Progress).filter_by(
        user_id=user_id,
        entry_id=entry_id
    ).first()

    if not prog:
        prog = Progress(user_id=user_id, entry_id=entry_id)
        db.add(prog)

    if correct:
        prog.correct += 1
    else:
        prog.wrong += 1

    db.commit()

    return {"status": "updated"}

