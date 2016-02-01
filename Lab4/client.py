import logging, socket
from messages import JOIN_MESSAGE, LEAVE_MESSAGE, SEND_MESSAGE, DISCONNECT_MESSAGE

class Client:

  def __init__(self, port, handle):
    self.server_port = port
    self.handle = handle
    self.messages = []
    self.client_id = 0
    logging.info("Client attempts to connect to localhost:%d" % self.server_port)
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect(('localhost', self.server_port))

  def join_chatroom(self, chatroom):
    message = JOIN_MESSAGE.format(
      chatroom = chatroom,
      handle = self.handle
    )
    response = self._response(message)

  def send_message(self, room_ref, message):
    message = SEND_MESSAGE.format(
      room_ref = room_ref,
      client_id = self.client_id,
      handle = self.handle,
      message = self.message
    )
    response = self._response(message)

  def leave_chatroom(self, room_ref):
    message = LEAVE_MESSAGE.format(
      room_ref = room_ref, 
      client_id = self.client_id, 
      handle = self.handle
    )
    response = self._response(message)

  def disconnect(self, handle):
    message = DISCONNECT_MESSAGE.format(
      handle = self.handle
    )
    response = self._response(message)

  def _response(self, message):
    self.s.sendall(message)
    logging.info("Sending: " + message)
    response = self.s.recv(1024)
    logging.info("Received response: " + response)
    return response