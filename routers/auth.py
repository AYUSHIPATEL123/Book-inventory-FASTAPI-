from fastapi import APIRouter,Depends,HTTPException,status
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schema import UserOut , UserModel ,Login
from database import get_db
from models import User
from service import hash_pass,verify_pass,get_jwt_token,get_current_user



router = APIRouter()

@router.post('/register',response_model=UserOut)
async def register(data:UserModel,db:Annotated[AsyncSession,Depends(get_db)]):
     
    try:

        user = User(username=data.username,email=data.email,password=hash_pass(data.password),role=data.role)

        db.add(user)

        await db.commit()

        await db.refresh(user)

        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,detail=f'{e}')

@router.post('/login')
async def login(data:Login,db:AsyncSession=Depends(get_db)):
    
        query = select(User).filter(User.email == data.email)

        user = await db.execute(query)

        user = user.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid email")
        
        if not verify_pass(user.password,data.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid password")
        
        token = get_jwt_token(user.email,user.role)
            
        user_data = {
            "email":user.email,
            "user_role":user.role,
            "jwt_token":token
        }

        return user_data

    
