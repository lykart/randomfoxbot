from asyncio import run
from misc import dp
from handlers.defaultHandlers import CounterMiddleware, set_default_commands
import handlers


async def main():
    dp.middleware.setup(CounterMiddleware())

    commands = await set_default_commands()
    await dp.bot.set_my_commands(commands=commands)

    await dp.start_polling(dp)

if __name__ == '__main__':
    run(main())
