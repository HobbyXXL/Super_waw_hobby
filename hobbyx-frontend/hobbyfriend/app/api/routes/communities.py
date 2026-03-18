from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db_dep, get_current_user
from app.services.community_service import CommunityService

router = APIRouter(prefix="/communities", tags=["communities"])

@router.post("/")
def create(data: dict, db: Session = Depends(get_db_dep), user=Depends(get_current_user)):
    return CommunityService(db).create(user.id, data)

@router.post("/{community_id}/join")
def join(community_id: int, db: Session = Depends(get_db_dep), user=Depends(get_current_user)):
    return CommunityService(db).join(user.id, community_id)

@router.get("/{community_id}/members")
def members(community_id: int, db: Session = Depends(get_db_dep)):
    return CommunityService(db).members(community_id)
