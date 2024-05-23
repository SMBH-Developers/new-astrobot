from ._engine import async_session
from ._models import User

from datetime import date

from sqlalchemy.sql.expression import select, update, delete, func


async def registrate_if_not_exists(id_: int):
    async with async_session() as session:
        exists = (await session.execute(select(User.id).where(User.id == id_).limit(1))).one_or_none()
        if exists is None:
            user = User(id=id_)
            session.add(user)
            await session.commit()


async def set_final_quize(id_: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.id == id_).values(passed_question=func.now()))
        await session.commit()


async def check_final_quize(id_: int) -> bool:
    async with async_session() as session:
        exists = (await session.execute(select(User.id).where(User.id == id_, User.passed_question.isnot(None)).limit(1))).one_or_none()
        if exists is None:
            return False
        return True


async def delete_user(id_: int):
    query = delete(User).where(User.id == id_)

    async with async_session() as session:
        await session.execute(query)
        await session.commit()


async def get_count_all_users() -> int:
    query = select(func.count('*')).select_from(User)
    async with async_session() as session:
        count = (await session.execute(query)).scalar_one()
    return count


async def users_for_today() -> int:
    query = select(func.count('*')).select_from(User).where(func.DATE(User.registration_date) == date.today())
    async with async_session() as session:
        count = (await session.execute(query)).scalar_one()
    return count
