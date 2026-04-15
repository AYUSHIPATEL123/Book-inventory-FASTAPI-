from fastapi import APIRouter,Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from schema import UserOut , UserModel
from database import get_db
from models import User
from service import hash_pass,verify_pass

router = APIRouter()

@router.post('/register',response_model=UserOut)
async def register(data:UserModel,db:Annotated[AsyncSession,Depends(get_db)]):
    user = User(username=data.username,email=data.email,password=hash_pass(data.password),role=data.role)

    db.add(user)

    await db.commit()

    await db.refresh(user)

    return user


