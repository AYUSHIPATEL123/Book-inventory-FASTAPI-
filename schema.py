from pydantic import BaseModel,Field
from typing import Annotated

class BooksModel(BaseModel):
    title:Annotated[str,Field(max_length=50)]
    author:str
    category:str
    stock:int
    
class BookOut(BooksModel):
    id:int
    class config:
        from_attribute:True