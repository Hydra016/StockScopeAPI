from fastapi import APIRouter, Depends, status, BackgroundTasks
from models.user import UserModal
from typing import List
from controllers import notes
from utils.db import get_db
from sqlalchemy.orm import Session
from utils.helpers.authentication import is_authenticated
from schemas.note import StockNoteCreateSchema, StockNoteResponseSchema, StockNoteUpdateSchema

notes_router = APIRouter(prefix="/api/notes", tags=["Notes"])

@notes_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=StockNoteResponseSchema
)
def create_note(
    body: StockNoteCreateSchema,
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return notes.create_note(body, user, db)

@notes_router.get(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=List[StockNoteResponseSchema]
)
def get_notes(
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return notes.get_notes(user, db)

@notes_router.put(
    "/update/{note_id}",
    status_code=status.HTTP_200_OK,
    response_model=StockNoteResponseSchema
)
def update_note(body: StockNoteUpdateSchema, note_id: int, user: UserModal = Depends(is_authenticated), db: Session = Depends(get_db)):
    return notes.update_note(body, note_id, user, db)

@notes_router.delete(
    "/delete/{note_id}",
    status_code=status.HTTP_200_OK,
)
def delete_note(note_id: int,  user =  Depends(is_authenticated), db = Depends(get_db)):
    return notes.delete_note(note_id, user, db)