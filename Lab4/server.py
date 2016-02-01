from socket import *
from threading import Thread
from Queue import Queue
import sys, os, signal, logging
from time import sleep
from multiprocessing import Value
from messages import JOINED_CHATROOM_MESSAGE,ERROR_MESSAGE, LEFT_CHATROOM_MESSAGE, MESSAGE_RESPONSE, BAD_MESSAGE,SERVER

def route_message(connection, data):
  #use logging to track events 
  logging.info("Routing message: " + repr(data))

  try:
    if data[:13] == "JOIN_CHATROOM":
    	logging.info("Client joined chatroom")
		message = JOINED_CHATROOM_MESSAGE.format(
		    chatroom=None,
		    server_ip=None,
		    server_port=None,
		    room_ref=None,
		    client_id=None
		)
	    connection.sendall(message)

    elif data[:14] == "LEAVE_CHATROOM":
	    logging.info("Client leaves chatroom")
		message = LEAVE_CHATROOM_MESSAGE.format(
	    	room_ref=None,
	    	client_id=None
	    )
	  	connection.sendall(message)

    elif data[:4] == "CHAT":
    	logging.info("Client sent message")

    elif data[:] == "DISCONNECT":
      	logging.info("Client disconnectionected")
 		connection.close()

    else:
      client_error(connection, error_codes.BAD_MESSAGE, "Couldn't parse message")

  except Exception as e:
    client_error(connection, error_codes.SERVER, e.message)  
  
def client_error(connection, code, reason):
  logging.info("Client error %d: %s" % (code, reason))

  message = ERROR_MESSAGE.format(
    code=code,
    reason=reason
  )
  connection.sendall(message)

def run_server(port, max_worker_threads=10, max_queue_size=100):
  host = 'localhost'
  tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  q = Queue.Queue(maxsize=max_queue_size)
  threads = []

	def handler(queue):
	    BUFFER_SIZE = 8000

	    while True:
	      connection, address = queue.get()
	      logging.info("Thread recieved connectionection from queue from addressess %s:%d" % (address[0], address[1]))
	      data = connection.recv(BUFFER_SIZE) 
	      route_message(connection, data)

	try:
	    for i in xrange(max_worker_threads):
	      thread = Thread(target=handler, args=(q,))
	      thread.daemon = True 
	      thread.start()
	      threads.append(thread)

	    tcpSocket.bind((host, port))
	    tcpSocket.listen(10)
	    logging.info("Server has bound to socket on host '%s' and port '%d'" % (host, port))
	    while True:
	      connection, address = tcpSocket.accept()
	      logging.info("Connection from addressess '%s'" % address[0])
	      try:
	        q.put((connection, address), False) 
	      except Queue.Full:
	        logging.info("Server overload. Cannot accept anymore connections")

	    tcpSocket.close()

	  except (KeyboardInterrupt, SystemExit):
	    logging.info("Shutting down...")
	    tcpSocket.close()
	    sys.exit(0)

if __name__ == "__main__":
	if len(sys.argv) is not 3:
    	print "Format needed: python " + sys.argv[0] + " [PORT] [MAX_THREADS]"
  	else:
		run_server(int(sys.argv[1]), int(sys.argv[2]))

