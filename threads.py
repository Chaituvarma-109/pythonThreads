import concurrent.futures 
import logging
import threading
import time


class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def locked_update(self, name):
        logging.info("Thread %s: starting update", name)
        logging.debug("Thread %s about to lock", name)
        with self._lock:
            logging.debug("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("Thread %s about to release lock", name)
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)
    
    # --------------------------------------- Single Thread ----------------------------------------

    # logging.info("Main    : before creating thread")
    # x = threading.Thread(target=thread_function, args=(1,), daemon=True)
    # logging.info("Main    : before running thread")
    # x.start()
    # logging.info("Main    : wait for the thread to finish")
    # x.join()
    # logging.info("Main    : all done")
    
    # --------------------------------------- Multiple Threads ----------------------------------------
    
    # threads = []
    # for index in range(3):
    #     logging.info("Main    : create and start thread %d.", index)
    #     x = threading.Thread(target=thread_function, args=(index,))
    #     threads.append(x)
    #     x.start()
    
    # for index, thread in enumerate(threads):
    #     logging.info("Main    : before joining thread %d.", index)
    #     thread.join()
    #     logging.info("Main    : thread %d done.", index)
        
    # --------------------------------------- ThreadPoolExecutor ----------------------------------------
    
    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     executor.map(thread_function, range(3))
    
    # --------------------------------------- Race Conditions -------------------------------------------
    
    database = FakeDatabase()
    logging.info("Testing update. Starting value is %d.", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            # executor.submit(database.update, index)
            executor.submit(database.locked_update, index)
    logging.info("Testing update. Ending value is %d.", database.value)
