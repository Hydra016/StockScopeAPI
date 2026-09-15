from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.note import StockNoteModel
from models.user import UserModal
from schemas.note import StockNoteCreateSchema, StockNoteUpdateSchema

def get_owned_note(note_id: int, user: UserModal, db: Session) -> StockNoteModel:
    note = (
        db.query(StockNoteModel)
        .filter(StockNoteModel.id == note_id, StockNoteModel.user_id == user.id)
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note

def create_note(
    body: StockNoteCreateSchema,
    user: UserModal,
    db: Session,
):
    symbol = body.symbol.strip().upper()

    if symbol == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Symbol cannot be empty",
        )

    existing_note = (
        db.query(StockNoteModel)
        .filter(
            StockNoteModel.symbol == symbol,
            StockNoteModel.user_id == user.id,
            StockNoteModel.title == body.title.strip(),
            StockNoteModel.content == body.content.strip(),
        )
        .first()
    )

    if existing_note:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Same note already exist",
        )

    new_note = StockNoteModel(
        symbol=symbol,
        user_id=user.id,
        title=body.title.strip(),
        content=body.content.strip()
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

def get_notes(user: UserModal, db: Session):
    return db.query(StockNoteModel).filter(StockNoteModel.user_id == user.id).all()

def update_note(body: StockNoteUpdateSchema, note_id: int, user: UserModal, db: Session):
    note = get_owned_note(note_id, user, db)

    if body.title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title should not be empty",
        )

    if body.content.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content should not be empty",
        )

    note.title = body.title.strip()
    note.content = body.content.strip()
    note.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(note)

    return note

def delete_note(note_id: int, user: UserModal, db: Session):
    note = get_owned_note(note_id, user, db)

    db.delete(note)
    db.commit()

    return "Note Deleted Successfully"