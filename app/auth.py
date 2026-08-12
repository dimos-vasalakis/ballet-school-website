import asyncio

import bcrypt
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def hash_password(password: str) -> str:
    hashed = await asyncio.to_thread(bcrypt.hashpw, password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


async def verify_password(password: str, hashed_password: str) -> bool:
    return await asyncio.to_thread(bcrypt.checkpw, password.encode("utf-8"), hashed_password.encode("utf-8"))


async def get_current_user(request: Request, db: AsyncSession) -> User | None:
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return await db.get(User, user_id)
