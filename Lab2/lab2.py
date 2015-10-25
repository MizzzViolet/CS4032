from socket import *
from threading import Thread
from Queue import Queue
import sys, os, signal

def response(key):
    return "Server received: %s \n" % key

def kill():
    return "Connection ended. \n"

def hello_res(data, clientAddress, PORT):
    s = data + "\nIP: " + repr(clientAddress) + "\nPORT: " + str(PORT) + "StudentID: b56be41b6c15446d8ea27c05d121f0324c88a2beed698357e197527d43112b48 \n"
    return s

def client(worker):
    
    while True:
        
        clientSocket = worker.get()
        clientAddress = worker.get()
        dead = False

        while not dead:
            
            data = clientSocket.recv(1024)
            if not data: break
            if data == "KILL_SERVICE":
                clientSocket.sendall(kill())
                dead = True
            elif data[:4] == "HELO":
                print repr(clientAddress) + " Received: " + repr(data)
                clientSocket.sendall(hello_res(data,clientAddress, PORT))
                print repr(clientAddress) + " Sent: " + repr(hello_res(data,clientAddress, PORT))
            else:
                print repr(clientAddress) + " Received: " + repr(data)
                clientSocket.sendall(response(data))
                print repr(clientAddress) + " Sent: " + repr(response(data))
            
        if dead:
            print "\nConnection ended."
            os.kill(os.getpid(), signal.SIGINT)
                
    clientSocket.close()

def handler(HOST, PORT,workers):
    
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpSocket.bind((HOST, PORT))
    tcpSocket.listen(100)
    print "Waiting for connections..."
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
    if len(sys.argv) == 3:
        handler("0.0.0.0", int(sys.argv[1]), int(sys.argv[2]))
    else:   print "Format needed: python " + sys.argv[0] + " PORT THREADS"

