from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from database import Base

class Books(Base):
    __tablename__= "Books"
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    title:Mapped[str]=mapped_column(String(50),index=True)
    author:Mapped[str]=mapped_column(String(50),index=True)
    category:Mapped[str]=mapped_column(String(50),index=True)
    stock:Mapped[int]


