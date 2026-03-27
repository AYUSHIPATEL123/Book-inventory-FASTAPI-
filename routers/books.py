
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated,Optional
from models import Books
from schema import BooksModel,BookOut
from database import get_db


router = APIRouter()

# show books...
@router.get('/books/',response_model=list[BookOut])
async def books(db:Annotated[AsyncSession,Depends(get_db)]):
    
    query = select(Books)
    books = await db.execute(query)
    books = books.scalars().all()
    return books

# show single book
@router.get('/books/{id}', response_model=BookOut)
async def get_book(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await db.get(Books, id)


# add book
@router.post('/addbook/',response_model=BookOut)
async def addBook(data:BooksModel,db:Annotated[AsyncSession,Depends(get_db)]):
    
    book = Books(title=data.title,author=data.author,stock=data.stock,category=data.category)
    
    db.add(book)
    
    await db.commit()
    
    await db.refresh(book)

    return book

# update book
@router.put('/chbook/{id}',response_model=BookOut)
async def chbook(id:int,data:BooksModel,db:AsyncSession=Depends(get_db)):
    
    book = await db.get(Books,id)

    if not book:
        raise HTTPException(status_code=404,detail=f"book with id {id} is not available.")
    
    book.title = data.title
    book.author = data.author
    book.category = data.category
    book.stock = data.stock

    await db.commit()
    
    await db.refresh(book)

    return book

# delete book
@router.delete('/delbook/{id}',response_model=BookOut)
async def delbook(id:int,db:Annotated[AsyncSession,Depends(get_db)]):
    
    book = await db.get(Books,id)

    if not book:
        raise HTTPException(status_code=404,detail=f"book with id {id} is not available.")
    
    await db.delete(book)
    
    await db.commit()

    return book

@router.get('/shbooks/',response_model=BookOut)
async def book_serch(title:str,db:AsyncSession=Depends(get_db)):
    query = select(Books).where(Books.title == title)
    book = await db.execute(query)
    book = book.scalar_one_or_none()
    return book


@router.get('/filbooks/',response_model=list[BookOut])
async def book_filter(author:Optional[str]=None,category:Optional[str]=None,db:AsyncSession=Depends(get_db)):
    if author:
        query = select(Books).where(Books.author == author)
    elif category:
        query = select(Books).where(Books.category == category)    
    
    books = await db.execute(query)
    books = books.scalars().all()
    return books
    