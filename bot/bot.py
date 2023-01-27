from typing import Callable

from telegram.ext import ApplicationBuilder, Application, CommandHandler

from commands import start
from utils import get_environment_variable

TOKEN = get_environment_variable('TOKEN')


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    commands = [
        start,
    ]
    add_command_handlers(application, commands)
    application.run_polling()


def add_command_handlers(application: Application, commands: list[Callable]):
    for command in commands:
        handler = CommandHandler(command.__name__, command)
        application.add_handler(handler)


if __name__ == '__main__':
    main()
