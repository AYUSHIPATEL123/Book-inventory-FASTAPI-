from fastapi import APIRouter,Depends,HTTPException,status
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import User
from service import hash_pass,verify_pass,required_roles
from schema import UserModel,UserOut
from typing import Annotated

router = APIRouter()

@router.get('/users',response_model=list[UserOut])
async def users(db:Annotated[AsyncSession,Depends(get_db)],access:UserOut=Depends(required_roles("admin","user"))):
    query = select(User)

    if access.role == "user":
        
        query = query.filter(User.id == access.id)
        
        user = await db.execute(query)

        user = user.scalars().all()

        return user

    users = await db.execute(query)
    
    users = users.scalars().all()
    
    return users

@router.put('/update-user/{id}',response_model=UserOut)
async def register(data:UserModel,db:Annotated[AsyncSession,Depends(get_db)],id:int,access:UserOut=Depends(required_roles("admin"))):
     
        user = await db.get(User,id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        user.email=data.email
        user.username=data.username
        user.role=data.role
        user.password = hash_pass(data.password)

        await db.commit()

        await db.refresh(user)

        return user

    
@router.delete('/del-user/{id}')
async def del_user(db:Annotated[AsyncSession,Depends(get_db)],id:int,access:UserOut=Depends(required_roles("admin"))):
     
    user = await db.get(User,id)

    if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db.delete(user)

    await db.commit()
    return {"message":f'user with id {id} has been deleted'}




