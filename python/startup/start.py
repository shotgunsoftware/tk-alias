import tank
import os
import sys
import time

logger = tank.LogManager.get_logger(__name__)


def main():
    """ Alias Engine start """

    tank.LogManager().initialize_base_file_handler("tk-alias")

    try:
        # Time to wait before start the engine (seconds)
        WAITING_TIME = 10

        counter = 0
        while counter <= WAITING_TIME:
            time.sleep(1)
            counter += 1

        context = tank.context.deserialize(os.environ.get("TANK_CONTEXT"))
        engine = tank.platform.start_engine('tk-alias', context.tank, context)
    except Exception as e:
        logger.exception("Unexpected exception while launching the Alias engine.")
        return -1
    else:
        engine.run_qt_loop()
        return 0


if __name__ == '__main__':
    sys.exit(main())
