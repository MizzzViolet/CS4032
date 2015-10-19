from socket import *
import thread
import sys
import time

#def handler(HOST, PORT, message):
def handler():
    HOST = ''
    PORT = 8002
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpSocket.connect((HOST, PORT))
    while True:
        message = raw_input("Message: ")
        tcpSocket.send(message)
        data = tcpSocket.recv(1024)
        print "Received: " + repr(data)
    tcpSocket.close()


if __name__ == '__main__':
    handler()
#    #input host, port number, message
#    for x in range(0,5):
#        t = thread.start_new(handler, (sys.argv[1], int(sys.argv[2]), sys.argv[3]))
#    time.sleep(10)
