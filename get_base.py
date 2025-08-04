import shutil

from aiogram import Router, F
from aiogram.types import FSInputFile, Message
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID, DB_PATH, DB_PASSWORD
from states import GetBaseFilePassword


router = Router()


@router.message(F.text == "Base file")
async def get_password(message: Message, state:FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Parolni kiriting:")
        await state.set_state(GetBaseFilePassword.wait_password)
    else:
        return await message.answer("Sizda bu buyruqdan foydalanishga ruxsat yo‘q.")
    

@router.message(F.text, GetBaseFilePassword.wait_password)
async def get_base_file(message: Message, state:FSMContext):
    if message.text == DB_PASSWORD:
        try:
            shutil.copy(DB_PATH, "base_copy.db")  # Asosiy faylga zarar yetmasligi uchun
            await message.answer_document(FSInputFile("base_copy.db"), caption="Ma'lumotlar bazasi nusxasi")
        except Exception as e:
            await message.answer(f"Xatolik: {e}")()
    else:
        await message.answer("Xato parol kiritdingiz.")
