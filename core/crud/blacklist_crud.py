from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Blacklist

async def get_user(user_id: int, session: AsyncSession) -> Blacklist:
    query = select(Blacklist).where(Blacklist.user_id == user_id)
    result = await session.execute(query)
    result = result.scalar_one_or_none()
    return result

async def ban_user(user_id: int, reason: str | None, session: AsyncSession):
    try:
        user = Blacklist(
            user_id=user_id,
            reason=reason
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError:
        pass


async def unban_user(user_id: int, session: AsyncSession):
    user: Blacklist = await get_user(user_id, session)
    if user:
        await session.delete(user)
        await session.commit()
        return user