from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase




DATABASE_URL ="sqlite:///./expense.db" 
#Database connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

#Crate Session
SessionLocal = sessionmaker(bind=engine) 

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
class Base(DeclarativeBase):
    pass
            

