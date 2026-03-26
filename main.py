from fastapi import FastAPI
from routers import books
import models
from database import engine,AsyncSessionLocal


app = FastAPI()

app.include_router(books.router)

@app.on_event('startup')
async def crt_tbl():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        
        
