import socket

#HOST = '0.0.0.0'
#PORT = 8000

def connect(HOST, PORT, message):

	tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpSocket.connect((HOST, PORT))
	
	while True:
	    tcpSocket.send(message)
	    data = tcpSocket.recv(1024)
	    print data
	   
	tcpSocket.close()

# User has to input the host, port number, and message when running the program
if __name__ == "__main__":

    if len(sys.argv) == 4:
        print connect(sys.argv[1], int(sys.argv[2]), sys.argv[3]) + "\n"
    else:
        print "Invalid Input. Format needed: python " + sys.argv[0] + " HOST PORT Message\n"