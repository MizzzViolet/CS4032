import socket

def connect():
    
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = tcpSocket.connect(('0.0.0.0',8001))

    message = raw_input()
    tcpSocket.sendall("GET http://0.0.0.0/echo.php?message=%s HTTP/1.0\r\n\r\n" % message)

    data = tcpSocket.recv(1024)
    tcpSocket.close()
    return data

print connect()
