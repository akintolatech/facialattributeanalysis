import threading
import time


# Function that will be executed by each thread
def thread_function(name, delay):
    print(f"Thread {name} starting...")
    time.sleep(delay)  # Simulate some work or delay
    print(f"Thread {name} finishing...")


# Creating two threads
thread1 = threading.Thread(target=thread_function, args=("Thread 1", 2))
thread2 = threading.Thread(target=thread_function, args=("Thread 2", 1))

# Starting the threads
thread1.start()
thread2.start()

# Waiting for threads to complete (join)
thread1.join()
thread2.join()

print("All threads finished.")
