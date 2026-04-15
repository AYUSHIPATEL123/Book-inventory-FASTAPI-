from sqlalchemy import String,Date ,func,text
from sqlalchemy.orm import Mapped ,mapped_column 
from database import Base
from datetime import date
class Books(Base):
    __tablename__= "books"

    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    title:Mapped[str]=mapped_column(String(50),index=True)
    author:Mapped[str]=mapped_column(String(50),index=True)
    category:Mapped[str]=mapped_column(String(50),index=True)
    stock:Mapped[int]

class User(Base):
    __tablename__ = "users"
    
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    username:Mapped[str]=mapped_column(String(500),index=True)
    password:Mapped[str]=mapped_column(String(500))
    email:Mapped[str]=mapped_column(String(500),index=True,unique=True)
    role:Mapped[str]=mapped_column(String(200),index=True)

    is_active:Mapped[bool]=mapped_column(default=True)
    createdAt:Mapped[Date]=mapped_column(Date(),default=date.today)

