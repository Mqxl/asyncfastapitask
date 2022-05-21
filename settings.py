from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from aioredis import Redis, BlockingConnectionPool


DB_HOST = 'localhost'
DB_NAME = 'ami'
DB_USER = 'ami'
DB_PASSWORD = 'secret'
DB_PORT = 5432

REDIS_HOST = 'localhost'
REDIS_PASSWORD = 'secret'
REDIS_PORT = 6379
REDIS_POOL_SIZE = 100
REDIS_WAIT_TIMEOUT = 60

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'

engine = create_async_engine(
    DATABASE_URL
)
session_factory = sessionmaker(engine, class_=AsyncSession)

session = session_factory()

redis_pool = BlockingConnectionPool.from_url(
    url=REDIS_URL,
    max_connections=REDIS_POOL_SIZE,
    timeout=REDIS_WAIT_TIMEOUT
)
redis = Redis(connection_pool=redis_pool)
