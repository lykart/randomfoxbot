from aiogram import executor


from misc import dp
from handlers.defaultHandlers import CounterMiddleware
import handlers


if __name__ == "__main__":
    dp.middleware.setup(CounterMiddleware())
    executor.start_polling(dp, skip_updates=True)
