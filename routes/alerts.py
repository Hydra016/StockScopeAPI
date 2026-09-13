from fastapi import APIRouter, Depends, status, BackgroundTasks
from models.user import UserModal
from typing import List
from controllers import alerts
from utils.db import get_db
from sqlalchemy.orm import Session
from utils.helpers.authentication import is_authenticated
from schemas.alert import AlertCreateSchema, AlertUpdateSchema, AlertResponseSchema

alert_router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

@alert_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[AlertResponseSchema]
)
def get_alerts(
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return alerts.get_alerts(user, db)

@alert_router.get(
    "/{alert_id}",
    status_code=status.HTTP_200_OK,
    response_model=AlertResponseSchema
)
def get_single_alert(
    alert_id: int,
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return alerts.get_single_alert(alert_id, user, db)

@alert_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=AlertResponseSchema
)
def create_alert(
    body: AlertCreateSchema,
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return alerts.create_alert(body, user, db)

@alert_router.post(
    "/check",
    status_code=status.HTTP_200_OK,
    response_model=List[AlertResponseSchema]
)
async def check_alert(
    bg_tasks: BackgroundTasks,
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return await alerts.check_alert(bg_tasks, user, db)

@alert_router.put(
    "/update/{alert_id}",
    status_code=status.HTTP_200_OK,
    response_model=AlertResponseSchema
)
def update_alert(
    body: AlertUpdateSchema,
    alert_id: int,
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return alerts.update_alert(body, alert_id, user, db)

@alert_router.delete(
    "/delete/{alert_id}",
    status_code=status.HTTP_200_OK,
)
def delete_alert(
    alert_id: int,
    user: UserModal = Depends(is_authenticated),
    db: Session = Depends(get_db),
):
    return alerts.delete_alert(alert_id, user, db)