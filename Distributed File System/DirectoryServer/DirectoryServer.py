import socket, threading, os, hashlib, sys, signal
from thread import *

class DirectoryServer():

    def __init__(self, name, port=8001, host="0.0.0.0", directoryServer=0, threads=3):
        self.port = port
        self.name = name
        self.host = host
        self.semaphore = threading.BoundedSemaphore(value=threads)
        self.files={}
        self.FileServers={}

    def run(self):
        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpSocket.bind((self.host, self.port))
        tcpSocket.listen(100)
        print "Directory Server: {}, {}:{}".format(self.name,self.host,self.port)

        while True:
            try:
                connection, address = tcpSocket.accept()
                print "Connection from ", address
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
            while not dead:
                data = connection.recv(1024)
                command = data.split(" ", 1)[0]
                if (len(data.split(" ", 1)) > 1):
                    param = data.split(" ", 1)[1]
                else :
                    param = ""
                if command == "NULL":
                    response = "OK: NAME={} HOST={} PORT={}".format(self.name, self.host, self.port)
                elif command == "SEARCH":
                    filename = hashlib.md5(param.split(" ")[0].split("=")[1])
                    if filename in self.files:
                        response = "OK: Found file on {}".format(self.files[filename])
                    else:
                        response = "ERROR: File not found"
                elif command == "ADD":
                    servername = param.split(" ")[0].split("=")[1]
                    filename = param.split(" ")[1].split("=")[1] 
                    self.files[filename] = servername
                elif command == "REMOVE":
                    filename = param.split(" ")[0].split("=")[1] 
                    del(self.files[filename])
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



        