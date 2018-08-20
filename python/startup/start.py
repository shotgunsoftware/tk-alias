import os
import sys
import time

import zmq

import tank


tank.LogManager().initialize_base_file_handler("tk-alias")
logger = tank.LogManager.get_logger(__name__)


class AliasEngineBootstrap(object):
    def start(self):
        logger.info("Starting Alias Engine")
        self._wait_for_socket_server()
        self._start_engine()

    def _wait_for_socket_server(self):
        port = os.environ["TK_ALIAS_PORT"]
        context = zmq.Context()
        address = "tcp://localhost:{}".format(port)
        socket = context.socket(zmq.DEALER)
        logger.info("Waiting for socket reponse on port {}".format(port))

        tries_limit = 3600
        tries = 1

        while True:
            try:
                socket.connect(address)
                break
            except Exception as e:
                logger.info("Connection tries: {}, error message: {}".format(tries, e))
                tries += 1

                if tries > tries_limit:
                    logger.info("Retries limit reached")
                    raise

                time.sleep(1)

    def _start_engine(self):
        context = tank.context.deserialize(os.environ.get("TANK_CONTEXT"))
        engine = tank.platform.start_engine('tk-alias', context.tank, context)
        engine.run_qt_loop()


if __name__ == '__main__':
    try:
        alias_engine_bootstrap = AliasEngineBootstrap()
        alias_engine_bootstrap.start()
    except Exception as e:
        logger.exception("Unexpected exception while launching the Alias engine {}.".format(e))
        sys.exit(-1)

    sys.exit(0)
