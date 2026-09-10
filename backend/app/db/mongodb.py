import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None
    in_memory_store: dict = {
        "projects": {},
        "scenes": {},
        "conversations": {}
    }

db_manager = MongoDB()

async def get_database():
    return db_manager.db

async def connect_to_mongo():
    try:
        db_manager.client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=2000
        )
        # Verify connection
        await db_manager.client.admin.command('ping')
        db_manager.db = db_manager.client[settings.DATABASE_NAME]
        logger.info(f"Connected to MongoDB at {settings.MONGODB_URI}/{settings.DATABASE_NAME}")
    except Exception as e:
        logger.warning(f"MongoDB connection failed: {e}. Falling back to high-performance local memory store.")
        db_manager.db = None

async def close_mongo_connection():
    if db_manager.client:
        db_manager.client.close()
        logger.info("MongoDB connection closed.")
