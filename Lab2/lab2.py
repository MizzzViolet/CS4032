from socket import *
from threading import Thread
from Queue import Queue

PORT = 8002

def response(key):
    return "Server received: " + key

def hello_res(clientAddress, PORT):
    s = "HELO text\nIP:" + repr(clientAddress) + "\nPORT:" + str(PORT)
    return s

def client(worker):
    
    while True:
        
        clientSocket = worker.get()
        clientAddress = worker.get()
        
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

def handler(HOST, workers):
    
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpSocket.bind((HOST, PORT))
    tcpSocket.listen(100)

    q = Queue(workers)
    
    for x in range(workers):
        t = Thread(target = client, args=(q,))
        t.daemon = True
        t.start()

    while True:
        try:
            clientSocket, address = tcpSocket.accept()
            print "Connection from ", address
            q.put(clientSocket)
            q.put(address)
        except KeyboardInterrupt:
            print "KILLED."
            break
        except socket.error, msg:
            print "Socket error! %s" % msg
            break


if __name__ == "__main__":

     handler("",10)

