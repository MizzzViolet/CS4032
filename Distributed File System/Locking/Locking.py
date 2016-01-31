import socket, os, threading
from thread import *

class LockingServer():

    def __init__(self, name, port=8000, host="0.0.0.0", threads=3):
        self.port = port
        self.name = name
        self.host = host
        self.semaphore = threading.BoundedSemaphore(value=threads)
        self.locked={}


    def run(self):
        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpSocket.bind((self.host, self.port))
        tcpSocket.listen(100)
        print "Locking Server: {}, {}:{}".format(self.name,self.host,self.port)

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
            param =""
            while not dead:
                data = connection.recv(1024)
                command = data.split(" ", 1)[0]
                if len(data.split(" ", 1)) > 1:
                    param = data.split(" ", 1)[1]                    
                if command == "PING":
                    response = "OK: NAME={} HOST={} PORT={} Locking Server".format(self.name, self.host, self.port)
                elif command == "CHECK":
                    filename = param.split(" ")[0].split("=")[1]
                    print "CHECKING {}".format(filename)
                    response = "OK: {} is not locked".format(filename)

                    if filename  in self.locked:
                        response = "OK: {} is locked".format(filename)
                elif command == "LOCK":
                    filename = param.split(" ")[0].split("=")[1]
                    secs = param.split(" ")[1].split("=")[1]

                    print "LOCKING {}".format(filename)
                    if filename in self.locked:
                        response = "ERROR: File already locked".format(self.files[filename])
                    else:
                        self.locked[filename] = secs
                        response = "OK: {} locked for {} sec".format(filename, secs)

                elif command == "UNLOCK":
                    filename = param.split(" ")[0].split("=")[1]

                    print "UNLOCKING {}".format(filename)
                    response = "OK: {} unlocked".format(filename)

                    if filename  not in self.locked:
                        response = "OK: {} already unlocked".format(filename)

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