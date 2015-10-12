#Student no: 12307269
#python 2 !!!

import socket

def connect():
    
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #N.B. Please ping seanlth.duckdns.org if this ip address stops working. Then just change the address to the new one.
    result = tcpSocket.connect(('0.0.0.0',8000))

    message = raw_input()
    tcpSocket.sendall("GET http://0.0.0.0/echo.php?message=%s HTTP/1.0\r\n\r\n" % message)

    data = tcpSocket.recv(1024)
    tcpSocket.close()
    return data

print connect()
