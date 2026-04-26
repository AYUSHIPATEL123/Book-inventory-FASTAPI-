from fastapi import FastAPI,Request
from routers import books,auth,user
import models
from database import engine
from config.looging_config import make_logger

app = FastAPI()

app.include_router(books.router,prefix='/book')
app.include_router(auth.router,prefix='/auth')
app.include_router(user.router,prefix='/user')

@app.on_event('startup')
async def crt_tbl():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        
logger = make_logger(__name__)

@app.middleware('http')  
async def logg_request(request:Request,call_next):

    logger.info(f"Request: {request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")
    
    return response
    