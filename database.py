from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine,AsyncSession
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DB_URL = "mysql+aiomysql://root:root@localhost:3306/book-inv"

engine = create_async_engine(SQLALCHEMY_DB_URL,echo=False)

AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
