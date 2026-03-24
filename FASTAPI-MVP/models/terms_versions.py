from sqlalchemy import Column, Integer, String, Text, Boolean
from database import Base

class TermsVersion(Base):
    __tablename__ = "terms_versions"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, unique=True, nullable=False)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, default=False)