from socket import *
import thread

def response(key):
    return "Server received: " + key

def hello_res(clientAddress, PORT):
    s = "HELO text\nIP:" + repr(clientAddress) + "\nPORT:" + str(PORT)
    return s

def handler(clientSocket, clientAddress, PORT):

    while True:
        data = clientSocket.recv(1024)
        if not data: break
        if "KILL_SERVICE" == data.rstrip():
            break
        if "HELO text" == data.rstrip():
            clientSocket.sendall(hello_res(clientAddress, PORT))
        else:
            print repr(clientAddress) + " Received: " + repr(data)
            clientSocket.sendall(response(data))
            print repr(clientAddress) + " Sent: " + repr(response(data))

    print "\nConnection ended: " + clientAddress
    clientSocket.close()



if __name__ == "__main__":

    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    HOST = ''
    PORT = 8002
    tcpSocket.bind((HOST, PORT))
    tcpSocket.listen(100)
    print "Waiting for connection..."
    
    while True:
        try:
            clientSocket, address = tcpSocket.accept()
            print "Connection from ", address
            thread.start_new_thread(handler, (clientSocket, address, PORT))
        except KeyboardInterrupt:
            print "KILLED."
            break
        except socket.error, msg:
            print "Socket error! %s" % msg
            break
    tcpSocket.close()
