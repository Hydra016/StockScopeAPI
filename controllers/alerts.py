from datetime import datetime

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session

from models.alert import AlertModel
from models.user import UserModal
from schemas.alert import AlertCreateSchema, AlertUpdateSchema
from services.mail import MailService
from services.price_evaluation import PriceEvaluationService


def get_owned_alert(
    alert_id: int,
    user: UserModal,
    db: Session,
) -> AlertModel:
    alert = (
        db.query(AlertModel)
        .filter(
            AlertModel.id == alert_id,
            AlertModel.user_id == user.id,
        )
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    return alert


def create_alert(
    body: AlertCreateSchema,
    user: UserModal,
    db: Session,
):
    symbol = body.symbol.strip().upper()

    if symbol == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Symbol cannot be empty",
        )

    if body.target_price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price should be more than 0",
        )

    if body.condition not in ("ABOVE", "BELOW"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid condition",
        )

    existing_alert = (
        db.query(AlertModel)
        .filter(
            AlertModel.symbol == symbol,
            AlertModel.user_id == user.id,
            AlertModel.target_price == body.target_price,
            AlertModel.condition == body.condition,
        )
        .first()
    )

    if existing_alert:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alert with same symbol, target price and condition already exists",
        )

    new_alert = AlertModel(
        symbol=symbol,
        user_id=user.id,
        target_price=body.target_price,
        condition=body.condition,
        is_active=True,
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert


def get_alerts(
    user: UserModal,
    db: Session,
):
    alerts = (
        db.query(AlertModel)
        .filter(AlertModel.user_id == user.id)
        .all()
    )

    return alerts


def get_single_alert(
    alert_id: int,
    user: UserModal,
    db: Session,
):
    return get_owned_alert(alert_id, user, db)


def update_alert(
    body: AlertUpdateSchema,
    alert_id: int,
    user: UserModal,
    db: Session,
):
    alert = get_owned_alert(alert_id, user, db)

    updates = body.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    if "target_price" in updates:
        if updates["target_price"] is None or updates["target_price"] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Price should be more than 0",
            )

    if "condition" in updates:
        if updates["condition"] not in ("ABOVE", "BELOW"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid condition",
            )

    for field, value in updates.items():
        setattr(alert, field, value)

    # If the user reactivates an alert,
    # treat it as waiting to trigger again.
    if updates.get("is_active") is True:
        alert.triggered_at = None

    db.commit()
    db.refresh(alert)

    return alert


def delete_alert(
    alert_id: int,
    user: UserModal,
    db: Session,
):
    alert = get_owned_alert(alert_id, user, db)

    db.delete(alert)
    db.commit()

    return {
        "message": "Alert deleted successfully"
    }


async def check_alert(
    bg_tasks: BackgroundTasks,
    user: UserModal,
    db: Session,
):
    active_alerts = (
        db.query(AlertModel)
        .filter(
            AlertModel.user_id == user.id,
            AlertModel.is_active == True,
        )
        .all()
    )

    for alert in active_alerts:
        triggered = await PriceEvaluationService(
            alert=alert
        ).evaluate(db=db)

        if triggered:
            alert.is_active = False
            alert.triggered_at = datetime.utcnow()

            db.commit()
            db.refresh(alert)

            bg_tasks.add_task(
                MailService().send_alert_email,
                [user.email],
                alert.symbol,
                alert.target_price,
            )

    return get_alerts(user, db)