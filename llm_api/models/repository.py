from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone

PROMPT_COLLECTION = "prompts"

class PromptRepository:
    def __init__(self, mongo_uri: str, db_name: str):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[PROMPT_COLLECTION]

    async def save_prompt(self, prompt: str, usr_name: str):
        prompt_entry = {
            "prompt": prompt,
            "timestamp": datetime.now(timezone.utc),
        }
        await self.collection.update_one(
            {"user_name": usr_name},
            {"$push": {"prompts": prompt_entry}},
            upsert=True
        )