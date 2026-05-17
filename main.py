from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import model 
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
model.Base.metadata.create_all(bind=engine)

class choiceBased(BaseModel):
    Choice_text : str
    Is_correct : bool

class questionBased(BaseModel):
    Question_text : str
    choices : List[choiceBased]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/questions/{question_id}")
async def read_question(question_id: int, db = db_dependency):
    result = db.query(model.Questions).filter(model.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="question is not found")
    return result

@app.get("/questions/{question_id}")
async def read_question(question_id: int, db = db_dependency):
    result = db.query(model.Questions).filter(model.Choices.id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="choices are not found")
    return result

@app.post("/questions/")
async def create_questions(question: questionBased, db: db_dependency):

    db_question = model.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in question.choices:
        db_choice = model.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    db.commit()