from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


from database import Base

class User(Base):
    __tablename__ = "users"
    
    id:Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    name:Mapped[str]=mapped_column(String (255))
    email:Mapped[str]=mapped_column(String(255))
    hash_password:Mapped[str]=mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),
                                                 onupdate=lambda: datetime.now(timezone.utc))

class Transaction(Base):
    __tablename__ = "transactions"
    
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)  
    amount:Mapped[float]=mapped_column(Float)
    type:Mapped[str]=mapped_column(String(200))
    category:Mapped[str]=mapped_column(String(200))
    description:Mapped[str]=mapped_column(String(255))
    user_id:Mapped[int]= mapped_column(Integer,ForeignKey("users.id")) 
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),
                                                     onupdate=lambda: datetime.now(timezone.utc)) 