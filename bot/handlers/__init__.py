from aiogram import Router

from bot.handlers import echo, feedback, start

router = Router()
router.include_routers(feedback.router, start.router, echo.router)
