from fastapi import APIRouter


router = APIRouter()

@router.get('books/')
async def books():
    print("+++++++++++++++")