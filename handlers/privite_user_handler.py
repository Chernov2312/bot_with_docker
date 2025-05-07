import logging

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_querry import orm_get_plans, orm_add_plans, orm_delete_all_plans, orm_delete_id_plans

logging.basicConfig(level=logging.INFO)
user_router = Router()
data = {"plans":[]}
class AddPlans(StatesGroup):
    plans = State()
    start = State()

class ClearPlans(StatesGroup):
    id = State()

@user_router.message(StateFilter(None), Command('start'))
async def cmd_start(message: Message):
    await message.reply("Работаю")
    logging.info("запущен")


@user_router.message(StateFilter(None), Command('plans_get'))
async def cmd_get(message: Message, session: AsyncSession):
    plans = await orm_get_plans(session)
    await message.reply("планы:", sep="\n")
    k = ""
    if len(plans) == 0:
        await message.reply("планов нет", sep="\n")
    else:
        for i in plans:
            k += str(i.id) + "\n"
            for j in [j for j in i.plans.split("/0")]:
                if j != "":
                    k += j + "\n"
            k += str(i.created).split()[0] + "\n"*2
        await message.reply(k)
    logging.info("Планы вывел")
@user_router.message(StateFilter(None), Command('plans_all_clear'))
async def cmd_get(message: Message, session: AsyncSession):
    await orm_delete_all_plans(session)
    logging.info("Все планы очищены")

@user_router.message(StateFilter(None), Command('plans_id_clear'))
async def cmd_get(message: Message, session: AsyncSession, state: FSMContext):
    logging.info("Запрос id")
    await state.set_state(ClearPlans.id)

@user_router.message(StateFilter(None),Command('plans_set'))
async def cmd_set(message: Message, session: AsyncSession, state: FSMContext):
    await message.reply("Вводите планы по сообщению после чего введите команду подтвердить")
    await state.set_state(AddPlans.start)


@user_router.message(AddPlans.start, Command('plans_set_apply'))
async def cmd_apply(message: Message, session: AsyncSession, state: FSMContext):
    k = ""
    for i in data['plans']:
        k += i + "/0"
    data2 = {"plans": k}
    await orm_add_plans(session, data2)
    await state.clear()
    data["plans"] = []
    logging.info("загружены в бд")

@user_router.message(AddPlans.start, or_f(F.text, F.text == "."))
async def add_name(message: types.Message, state: FSMContext):
    data['plans'].append(message.text)
    logging.info("добавлен")

@user_router.message(ClearPlans.id, or_f(F.text, F.text == "."))
async def add_name(message: types.Message, state: FSMContext, session: AsyncSession):
    await orm_delete_id_plans(session, int(message.text))
    logging.info("Удалён по id")
    await state.clear()

