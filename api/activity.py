from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas, database

router = APIRouter()

# Эндпоинт для отметки активности
@router.post("/activity/mark", response_model=schemas.ActivityMarkResponse)
def mark_activity(
    request: schemas.ActivityMarkRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(models.get_current_user_optional)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    activity = models.UserActivity(
        user_id=current_user.id,
        hobby_id=request.hobby_id,
        duration_minutes=request.duration_minutes,
        activity_date=datetime.utcnow()
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    return schemas.ActivityMarkResponse(
        id=activity.id,
        message="Activity marked successfully",
        current_streak=1
    )

# Эндпоинт для создания поста
@router.post("/posts/", response_model=schemas.PostResponse)
def create_post(
    post_data: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(models.get_current_user_optional)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    new_post = models.PortfolioWork(
        user_id=current_user.id,
        hobby_id=post_data.hobby_id,
        title=post_data.title,
        description=post_data.description,
        is_public=post_data.is_public,
        created_at=datetime.utcnow()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return schemas.PostResponse(
        id=new_post.id,
        title=new_post.title,
        hobby_id=new_post.hobby_id,
        created_at=new_post.created_at
    )

# Эндпоинт для поиска пользователей
@router.get("/users/search", response_model=list[schemas.UserSearchResult])
def search_users(
    query: str = Query(..., min_length=1),
    limit: int = Query(10, le=50),
    db: Session = Depends(database.get_db)
):
    users = db.query(models.User).filter(
        models.User.is_verified == True,
        (models.User.login.ilike(f"%{query}%")) | (models.User.email.ilike(f"%{query}%"))
    ).limit(limit).all()
    
    return [
        schemas.UserSearchResult(
            id=u.id,
            login=u.login,
            avatar_url=u.avatar_url
        ) for u in users
    ]