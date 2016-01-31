from Locking import LockingServer

if __name__ == "__main__":
    lock = LockingServer("Locking Server")
    lock.run()