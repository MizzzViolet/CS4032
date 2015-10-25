import socket
import sys

def connect(HOST, PORT, msg):

    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.connect((HOST, PORT))
    tcpSocket.sendall("GET /echo.php?message=%s HTTP/1.0\r\n\r\n" % msg)
    data = tcpSocket.recv(1024)
    tcpSocket.close()
    return data

# User has to input the host, port number, and message when running the program
if __name__ == "__main__":

    if len(sys.argv) == 4:
        print connect(sys.argv[1], int(sys.argv[2]), sys.argv[3]) + "\n"
    else:
        print "Invalid Input. Format needed: python " + sys.argv[0] + " HOST PORT Message\n"

