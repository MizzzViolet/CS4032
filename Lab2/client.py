from socket import *
import thread
import sys
import time

def handler(HOST, PORT, message):
    
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpSocket.connect((HOST, PORT))
    
    while True:
        tcpSocket.send(message)
        data = tcpSocket.recv(1024)
        print "Received: " + repr(data)
   
    tcpSocket.close()

for x in range(5):
    t = thread.start_new(handler, (sys.argv[1], int(sys.argv[2]), sys.argv[3]))
 
time.sleep(10)
