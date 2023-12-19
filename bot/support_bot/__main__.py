import logging






from support_bot.misc import start_bot
import sys





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    start_bot()
