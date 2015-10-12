#python 2 !!!

from socket import *
import thread

def connect(clientSocket, clientAddress):

    print "Connection from ", clientAddress
    while 1:
        data = tcpSocket.recv(1024)

    print "\nData :" + data
    if not data:
        break
    else:
        message = "\nMessage sent: %s" % data
        clientsocket.send(message)
    print "\nConnection ended.\n"
    clientSocket.close()


if __name__ == "__main__":

    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    host = "0.0.0.0"
    port = 8000
    tcpSocket.bind((host, port))
    tcpSocket.listen(5)

    while 1:

        print "Waiting for connections\n"
        clientSocket, address = tcpSocket.accept()
        thread.start_new_thread(connect, (clientSocket, address))

    tcpSocket.close()
