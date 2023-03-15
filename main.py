from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telega_bot import main_bot
from parser import main_parser


def start():
    main_parser.parser()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(
        main_parser.parser,
        trigger='interval',
        hours=1,
    )
    scheduler.start()
    main_bot.main()


if __name__ == "__main__":
    start()
