import random
import threading
import time

class WaitSignalLock:
    def __init__(self):
        #Condition objects allow multiple threads to synchronize based on the state of an associated lock
        self.condition = threading.Condition()
        self.is_locked = False

    def wait(self):
        with self.condition:
            while self.is_locked:
                self.condition.wait()
            self.is_locked = True

    def signal(self):
        with self.condition:
            self.is_locked = False
            self.condition.notify_all()

class Process(threading.Thread):
    def __init__(self, process_id, lock):
        super(Process, self).__init__()
        self.process_id = process_id
        self.lock = lock

    def run(self):
        self.lock.wait()
        print(f"Process {self.process_id} trying to enter the critical section")
        print(f"Process {self.process_id} entered the critical section")
        print(f"Process {self.process_id} is performing operation on shared resource...")
        print(f"Process {self.process_id} exited the critical section.")
        time.sleep(random.uniform(2, 3))  #some work
        self.lock.signal()


def main():
    lock = WaitSignalLock()
    processes = [Process(i, lock) for i in range(5)]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    main()