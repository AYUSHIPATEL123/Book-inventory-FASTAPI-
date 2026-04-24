from fastapi import HTTPException,status,Depends
from passlib.context import CryptContext
from jwt.exceptions import PyJWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os
from models import User
from fastapi_mail import FastMail,MessageSchema
from config.email_config import conf

load_dotenv()

pass_context = CryptContext(schemes=["argon2"],deprecated="auto")


def hash_pass(password:str):
    
    return pass_context.hash(password)


def verify_pass(password:str,hashed_pass:str) -> bool:

    return pass_context.verify(hashed_pass,password)


def get_jwt_token(email:str,role:str):

    try:
        expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("JWT_EXPIRE_TIME_MINUTES")))

        token = jwt.encode(payload={"email":email,"role":role,"exp":expire},key=os.getenv("SECRET_KEY"),algorithm=os.getenv("JWT_ALGORITHM"))

        return token
    
    except PyJWTError as e:
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="envalid credencial")
    

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


def decode_jwt_token(token:str):

    try:
        user_data = jwt.decode(token,key=os.getenv("SECRET_KEY"),algorithms=[os.getenv("JWT_ALGORITHM")])

        email = user_data.get("email")

        return email
    
    except PyJWTError as e:
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=e)
    

async def get_current_user(token:str=Depends(oauth2_schema),db:AsyncSession=Depends(get_db)):

    try:

        email = decode_jwt_token(token)

        query = select(User).filter(User.email == email)

        user = await db.execute(query)

        user = user.scalar_one_or_none()

        return user

        
    except Exception as e:
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))
    

def required_roles(*roles):
    
    async def get_user(user=Depends(get_current_user)):
        
        if user.role not in roles:
            
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not allowed for this action")
        
        return user
    
    return get_user

async def send_email(data:dict):

    message_schema=MessageSchema(
        recipients=[data['email'],],
        subject=data['sub'],
        body=data['body'],
        subtype='plain',
        
    )

    fm = FastMail(conf)

    await fm.send_message(message=message_schema)
    print("email message send successfuly.....")

    return "email message send successfuly"