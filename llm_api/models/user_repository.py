from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from typing import Optional, Dict
from passlib.context import CryptContext
from llm_api.config import settings

USER_COLLECTION = "users"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def __init__(self, mongo_uri: str, db_name: str):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[USER_COLLECTION]

    async def _ensure_indexes(self):
        """Create indexes on user collection"""
        await self.collection.create_index("username", unique=True)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    async def create_user(self, username: str, password: str) -> Dict:
        """Create a new user with hashed password"""
        # Ensure indexes exist before creating user
        await self._ensure_indexes()
        
        hashed_password = self.get_password_hash(password)
        user_doc = {
            "username": username,
            "hashed_password": hashed_password,
            "calls_today": 0,
            "last_reset": datetime.now(timezone.utc),
            "created_at": datetime.now(timezone.utc),
        }
        try:
            result = await self.collection.insert_one(user_doc)
            user_doc["_id"] = result.inserted_id
            # Remove hashed_password from return
            user_doc.pop("hashed_password", None)
            return user_doc
        except Exception as e:
            if "duplicate key" in str(e).lower():
                raise ValueError(f"Username '{username}' already exists")
            raise e

    async def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        user = await self.collection.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])  # Convert ObjectId to string
        return user

    async def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate a user by username and password"""
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user["hashed_password"]):
            return None
        # Return user without password hash
        user_dict = {
            "username": user["username"],
            "calls_today": user.get("calls_today", 0),
            "last_reset": user.get("last_reset", datetime.now(timezone.utc)),
        }
        return user_dict

    async def update_user_usage(self, username: str, calls_today: int, last_reset: datetime):
        """Update user usage statistics"""
        await self.collection.update_one(
            {"username": username},
            {"$set": {"calls_today": calls_today, "last_reset": last_reset}}
        )

