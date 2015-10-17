import socket
import thread
import sys
import time
def handler(host, port, message):

    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpSocket.connect((host, port))
    tcpSocket.sendall(msg + "\n")
    data = tcpSocket.recv(1024)
    tcpSocket.close()
    return data

print handler
if __name__ == '__main__':
    # for x in range(0,5):
        t = thread.start_new(handler, (sys.argv[1], int(sys.argv[2]), sys.argv[3]))
# time.sleep(10)
