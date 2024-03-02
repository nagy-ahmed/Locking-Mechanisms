import threading
import time
import random

readers_count = 0
mutex = threading.Semaphore(1)
write_mutex = threading.Semaphore(1)

class Reader(threading.Thread):
    def run(self):
        global readers_count
        for i in range(10):
            mutex.acquire()
            readers_count += 1
            if readers_count == 1:
                write_mutex.acquire()
            mutex.release()
            # Reading operation
            print(f"Reading... Number of readers: {readers_count}")
            mutex.acquire()
            readers_count -= 1
            if readers_count == 0:
                write_mutex.release()
            mutex.release()
            time.sleep(random.random())

class Writer(threading.Thread):
    def run(self):
        for i in range(10):
            write_mutex.acquire()
            # Writing operation
            print("Writing...")
            write_mutex.release()
            time.sleep(random.random())

if __name__ == "__main__":
    for i in range(2):
        reader = Reader()
        reader.start()
    for i in range(1):
        writer = Writer()
        writer.start()
