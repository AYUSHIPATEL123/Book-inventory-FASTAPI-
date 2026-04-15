from pydantic import BaseModel,Field
from typing import Annotated
import enum
from datetime import date
class BooksModel(BaseModel):
    title:Annotated[str,Field(max_length=50)]
    author:str
    category:str
    stock:int
    
class BookOut(BooksModel):
    id:int
    class config:
        from_attribute:True

class UserRole(str,enum.Enum):
    admin="admin"
    user="user"
class UserModel(BaseModel):
    username:str
    email:str
    password:str
    role:UserRole      


class UserOut(BaseModel):
    id:int
    username:str 
    email:str
    role:UserRole
    is_active:bool
    createdAt:date
