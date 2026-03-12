import asyncio
import os

from aiogram import Bot, Dispatcher

from app.bot.onboarding import router as onboarding_router


async def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("Set BOT_TOKEN environment variable")

    bot = Bot(token=token)
    dispatcher = Dispatcher()
    dispatcher.include_router(onboarding_router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
