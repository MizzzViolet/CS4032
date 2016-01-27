import socket, threading, os, sys, signal
from thread import *
from FileServer.Utils import FileServer


class FileServer():
    
    def __init__(self, name, port=8000, host="0.0.0.0", directoryServer=0, threads=3):
        self.port = port
        self.name = name
        self.host = host
        self.directoryServer = directoryServer
        self.fileLoc = "~/distributedFileServer/"
        self.semaphore = threading.BoundedSemaphore(value=threads)
        self.fileLoc = os.path.expanduser(self.fileLoc)
    
    
    def run(self):
        if not os.path.exists(self.fileLoc):
            os.makedirs(self.fileLoc)
    
        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        tcpSocket.bind((self.host, self.port))
        tcpSocket.listen(100)
        print "Listening"
        
        while True:
            try:
                connection, address = tcpSocket.accept()
                print "connectionection from ", address
                self.semaphore.acquire()
                start_new_thread(self.handler, (connection,))
            except KeyboardInterrupt:
                print "KILLED."
                break
            except socket.error, msg:
                print "Socket error! %s" % msg
                break

def handler(self, connection):
    try:
        dead = False
        response = ""
        handlerfiles = FileServer(self.fileLoc)
        while not dead:
            data = connection.recv(1024)
            command = data.split(" ", 1)[0]
            if (len(data.split(" ", 1)) > 1):
                param = data.split(" ", 1)[1]
            else:
                param =""
            if command == "NULL":
                response = "OK: NAME={} HOST={} PORT={}".format(self.name, self.host, self.port)
            elif command == "CREATE":
                response = handlerfiles.CREATE(param)
                tcpSocket=socket.socket(socket.AF_INIT, socket.SOCK_STREAM)
                tcpSocket.connect((self.host, self.directoryServer))
                tcpSocket.send("REGISTERFILE fileServer={}:{} file={}".format(self.host, self.port, param.split(" ")[0].split("=")[1]))
            elif command == "REMOVE":
                response = handlerfiles.REMOVE(param)
                tcpSocket=socket.socket(socket.AF_INIT, socket.SOCK_STREAM)
                tcpSocket.connect((self.host, self.directoryServer))
                tcpSocket.send("REMOVEFILE fileServer={}:{} file={}".format(self.host, self.port, param.split(" ")[0].split("=")[1]))
            elif command == "READ":
                response = handlerfiles.READ(param)
            elif command == "WRITE":
                response = handlerfiles.WRITE(param)
            elif command == "MKDIR":
                response = handlerfiles.MKDIR(param)
            elif command == "RMDIR":
                response = handlerfiles.RMDIR(param)
            elif command == "KILL_SERVICE":
                dead = True
                print "Connection ended."
                os.kill(os.getpid(), signal.SIGINT)
            else:
                response = "INVALID_COMMAND"
            connection.sendall(response)

        connection.close()
        print "Connection ended."
        self.semaphore.release()
    except Exception as e:
            print str(e)
            connection.send("ERROR")
            connection.close()


