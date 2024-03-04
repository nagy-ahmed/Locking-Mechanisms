import threading
import time
import random

class TestAndSetLock:
    def __init__(self):
        # self.lock: This attribute is initialized as a threading lock (threading.Lock()). 
        #It is used to synchronize access to shared resources among multiple threads.
        self.lock = threading.Lock()
        self.flag = False

    def test_and_set(self):
        with self.lock:
            old_flag = self.flag
            self.flag = True
            return old_flag

class Process(threading.Thread):
    #inheriting from threading.Thread means that instances of the Process class will behave as threads.
    # This inheritance allows you to create threads easily by instantiating objects of the Process class 
    #and starting them using the start() method provided by the Thread class.
    def __init__(self, process_id, lock):
        super(Process, self).__init__()
        self.process_id = process_id
        self.lock = lock

    #By subclassing threading.Thread, you can define the behavior of the thread by overriding the run() method.
    def run(self):
        print(f"Process {self.process_id} trying to enter the critical section")
        while self.lock.test_and_set():
            pass
        print(f"Process {self.process_id} entered the critical section")
        print(f"Process {self.process_id} is performing operation on shared resource...")
        time.sleep(random.uniform(2, 3))  #some work
        print(f"Process {self.process_id} exited the critical section.")
        self.lock.flag=False

def main():
    lock = TestAndSetLock()
    processes = [Process(i, lock) for i in range(5)]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    main()
