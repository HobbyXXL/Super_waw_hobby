from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from database import get_db
from dependency import get_current_user
from models.users import User
from services.activities import ActivityService

router = APIRouter(prefix="/activities", tags=["Activities"])


class CheckInRequest(BaseModel):
    hobby_id: int
    date: Optional[date] = None


class CheckInResponse(BaseModel):
    streak: int
    did_hobby: bool
    message: str
    activity_date: str


class ActivityStatsResponse(BaseModel):
    total_days: int
    current_streak: int
    longest_streak: int
    start_date: str
    end_date: str


@router.post("/check-in", response_model=CheckInResponse)
def check_in(
    body: CheckInRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ActivityService(db)
    result = service.toggle_check_in(current_user.id, body.hobby_id, body.date)
    return CheckInResponse(**result)


@router.get("/stats", response_model=ActivityStatsResponse)
def activity_stats(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ActivityService(db)
    return ActivityStatsResponse(**service.get_stats(current_user.id, start_date, end_date))
