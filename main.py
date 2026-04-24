from fastapi import FastAPI
from routers import books,auth,user
import models
from database import engine,AsyncSessionLocal


app = FastAPI()

app.include_router(books.router,prefix='/book')
app.include_router(auth.router,prefix='/auth')
app.include_router(user.router,prefix='/user')

@app.on_event('startup')
async def crt_tbl():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        
        