# create_tables.py
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)
print("Все таблицы созданы в app.db!")