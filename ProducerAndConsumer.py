import threading
import time
import random

BUFFER_SIZE = 5
buffer = []
mutex = threading.Semaphore(1)
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)

class Producer(threading.Thread):
    def run(self):
        global buffer
        for i in range(10):
            item = random.randint(1, 100)
            empty.acquire()
            mutex.acquire()
            buffer.append(item)
            print(f"Produced {item}. Buffer: {buffer}")
            mutex.release()
            full.release()
            time.sleep(random.random())

class Consumer(threading.Thread):
    def run(self):
        global buffer
        for i in range(10):
            full.acquire()
            mutex.acquire()
            item = buffer.pop(0)
            print(f"Consumed {item}. Buffer: {buffer}")
            mutex.release()
            empty.release()
            time.sleep(random.random())

if __name__ == "__main__":
    producer = Producer()
    consumer = Consumer()
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()
