from datetime import date, timedelta
from sqlalchemy.orm import Session
from models.user_activity import UserActivity, ActivityType
class ActivityService:
    def __init__(self, db: Session):
        self.db = db

    def toggle_check_in(self, user_id: str, hobby_id: int, activity_date: date | None = None) -> dict:
        target_date = activity_date or date.today()
        existing = (
            self.db.query(UserActivity)
            .filter(
                UserActivity.user_id == user_id,
                UserActivity.hobby_id == hobby_id,
                UserActivity.activity_date == target_date,
                UserActivity.activity_type == ActivityType.DID_HOBBY.value,
            )
            .first()
        )
        if existing:
            self.db.delete(existing)
            self.db.commit()
            did_hobby = False
            message = "Отметка снята"
        else:
            self.db.add(
                UserActivity(
                    user_id=user_id,
                    hobby_id=hobby_id,
                    activity_date=target_date,
                    activity_type=ActivityType.DID_HOBBY.value,
                )
            )
            self.db.commit()
            did_hobby = True
            message = "Great job!"

        streak = self._calculate_streak(user_id)
        return {
            "streak": streak,
            "did_hobby": did_hobby,
            "message": message,
            "activity_date": target_date.isoformat(),
        }

    def get_stats(self, user_id: str, start_date: date | None, end_date: date | None) -> dict:
        end = end_date or date.today()
        start = start_date or (end - timedelta(days=30))
        activities = (
            self.db.query(UserActivity)
            .filter(
                UserActivity.user_id == user_id,
                UserActivity.activity_date >= start,
                UserActivity.activity_date <= end,
                UserActivity.activity_type == ActivityType.DID_HOBBY.value,
            )
            .all()
        )
        unique_days = {a.activity_date for a in activities}
        return {
            "total_days": len(unique_days),
            "current_streak": self._calculate_streak(user_id),
            "longest_streak": self._calculate_longest_streak(user_id),
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
        }

    def _calculate_streak(self, user_id: str) -> int:
        activities = (
            self.db.query(UserActivity.activity_date)
            .filter(
                UserActivity.user_id == user_id,
                UserActivity.activity_type == ActivityType.DID_HOBBY.value,
            )
            .distinct()
            .order_by(UserActivity.activity_date.desc())
            .all()
        )
        if not activities:
            return 0
        dates = {row[0] for row in activities}
        streak = 0
        expected = date.today()
        while expected in dates:
            streak += 1
            expected -= timedelta(days=1)
        return streak

    def _calculate_longest_streak(self, user_id: str) -> int:
        rows = (
            self.db.query(UserActivity.activity_date)
            .filter(
                UserActivity.user_id == user_id,
                UserActivity.activity_type == ActivityType.DID_HOBBY.value,
            )
            .distinct()
            .order_by(UserActivity.activity_date.asc())
            .all()
        )
        if not rows:
            return 0
        dates = sorted({row[0] for row in rows})
        longest = current = 1
        for i in range(1, len(dates)):
            if dates[i] - dates[i - 1] == timedelta(days=1):
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        return longest
