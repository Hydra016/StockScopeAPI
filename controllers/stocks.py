from sqlalchemy.orm import Session

def get_quote(db: Session):
    return {
        "message": "This is a quote endpoint"
    }