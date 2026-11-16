from aiogram import F, Router, html
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.api import save_feedback
from bot.keyboards import BTN_FEEDBACK, main_menu, rating_keyboard, skip_keyboard, stars
from bot.states import FeedbackState

router = Router()


async def ask_rating(message: Message, state: FSMContext, source: str = ""):
    await state.clear()
    await state.update_data(source=source)
    await state.set_state(FeedbackState.rating)
    await message.answer("Xizmatni 1 dan 5 gacha baholang 👇", reply_markup=rating_keyboard())


@router.message(CommandStart(deep_link=True))
async def start_deep_link(message: Message, command: CommandObject, state: FSMContext):
    source = (command.args or "")[:64]
    await ask_rating(message, state, source=source)


@router.message(Command("feedback"))
@router.message(F.text == BTN_FEEDBACK)
async def feedback_start(message: Message, state: FSMContext):
    await ask_rating(message, state)


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi.", reply_markup=main_menu)


@router.callback_query(FeedbackState.rating, F.data.startswith("rating:"))
async def rating_chosen(callback: CallbackQuery, state: FSMContext):
    value = callback.data.split(":", 1)[1]
    if not value.isdigit() or not 1 <= int(value) <= 5:
        await callback.answer("Noto'g'ri baho", show_alert=True)
        return
    rating = int(value)
    await state.update_data(rating=rating)
    await state.set_state(FeedbackState.comment)
    await callback.message.edit_text(f"Bahoingiz: {stars(rating)}\n\nIzoh yozing (ixtiyoriy):", reply_markup=skip_keyboard)
    await callback.answer()


@router.message(FeedbackState.rating)
async def rating_not_chosen(message: Message):
    await message.answer("Iltimos, yuqoridagi yulduzchalardan birini bosing ⭐ (/cancel — bekor qilish)")


@router.callback_query(FeedbackState.comment, F.data == "comment:skip")
async def comment_skipped(callback: CallbackQuery, state: FSMContext):
    text = await finish(state, user_id=callback.from_user.id, comment="")
    await callback.message.edit_text(text)
    await callback.answer()


@router.message(FeedbackState.comment, F.text)
async def comment_written(message: Message, state: FSMContext):
    text = await finish(state, user_id=message.from_user.id, comment=message.text[:1000])
    await message.answer(text, reply_markup=main_menu)


@router.message(FeedbackState.comment)
async def comment_not_text(message: Message):
    await message.answer("Izohni matn ko'rinishida yozing yoki «O'tkazib yuborish»ni bosing.")


async def finish(state: FSMContext, user_id: int, comment: str) -> str:
    data = await state.get_data()
    await state.clear()
    saved = await save_feedback({
        "user_id": user_id,
        "rating": data["rating"],
        "comment": comment,
        "source": data.get("source", ""),
    })
    lines = ["Rahmat! 🙌" if saved else "Rahmat! Hozir saqlab bo'lmadi, keyinroq qayta urinib ko'ring.", f"Baho: {stars(data['rating'])}"]
    if comment:
        lines.append(f"Izoh: {html.quote(comment)}")
    if data.get("source"):
        lines.append(f"Manba: {html.quote(data['source'])}")
    return "\n".join(lines)
