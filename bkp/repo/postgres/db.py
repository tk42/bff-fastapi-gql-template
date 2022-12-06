import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base


_protocol: str = os.environ.get("POSTGRES_PROTOCOL")
_user: str = os.environ.get("POSTGRES_USER")
_pass: str = os.environ.get("POSTGRES_PASSWORD")
_host: str = os.environ.get("POSTGRES_HOST")
_port: str = os.environ.get("POSTGRES_PORT")
_db: str = os.environ.get("POSTGRES_DB")

DB_URL = "{}://{}:{}@{}:{}/{}".format(_protocol, _user, _pass, _host, _port, _db)
engine = create_async_engine(DB_URL, echo=True)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession))

Base = declarative_base()


async def get_db():
    async with Session() as session:
        try:
            yield session
        finally:
            session.close()
