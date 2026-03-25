from pydantic import BaseModel,Field
from typing import Annotated

class Books(BaseModel):
    title:Annotated[str,Field(max_length=50)]
    author:str
    category:str
    stock:int
    
