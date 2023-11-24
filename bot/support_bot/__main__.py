import logging
import sys

from support_bot.misc import start_bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    start_bot()
