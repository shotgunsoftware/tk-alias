import zmq
import time

# Session

class Session(object):
    """
    The Session class manages communication.
    """

    def __init__(self, port):
        """
        Initialize the Session.

        :param int port: The port number.
        """
        self._port = port
        self._context = zmq.Context()

    def _socket_address(self):
        """
        Return the socket's address in ZeroMQ address format.

        :return: The socket address.
        :rtype: str
        """
        return "tcp://localhost:{}".format(self._port)

    def connect(self):
        """
        Start the connection.
        """
        self._socket = self._context.socket(zmq.DEALER)

        retries_limit = 10

        def connect_retrying(socket, retries=0):
            if retries >= retries_limit:
                # Max retries exceeded
                return
            else:
                try:
                    socket.connect(self._socket_address())
                except Exception as e:
                    time.sleep(1)
                    connect_retrying(socket, retries+1)

        connect_retrying(self._socket)

        self._poller = zmq.Poller()
        self._poller.register(self._socket, zmq.POLLIN)

    def disconnect(self):
        """
        Stop the connection.

        :raises ZMQError: If the socket was not connected.
        """
        self._socket.close()

    def send(self, request):
        """
        Send a Request to the C++ plugin.

        :param Request request: An instance of a Request subclass.
        """
        self._socket.send(request.to_string())

    def read_message(self):
        """
        Read a message from the socket. Blocks until it receives a response.

        :return: A message from the Alias plugin.
        :rtype: str
        """
        timeout = 1 * 1000 # 5 sec
        message = None

        sockets = dict(self._poller.poll(timeout))

        if sockets.get(self._socket) == zmq.POLLIN:
            message = self._socket.recv()

        return message
