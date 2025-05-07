from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Plans


async def orm_add_plans(session: AsyncSession, data: dict):
    obj = Plans(
        plans=data["plans"],
    )
    session.add(obj)
    await session.commit()


async def orm_get_plans(session: AsyncSession):
    query = select(Plans)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_update_plans(session: AsyncSession, plan_id: int, data):
    query = update(Plans).where(Plans.id == plan_id).values(
        plans=data["plans"],
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_all_plans(session: AsyncSession):
    query = delete(Plans)
    await session.execute(query)
    await session.commit()

async def orm_delete_id_plans(session: AsyncSession, id:int):
    query = delete(Plans).where(Plans.id== id)
    await session.execute(query)
    await session.commit()
