# MT programming
# Issues of concurrency
# Testing MT programs

# barber shop --> X number of barbers

# each barber has a chair
# Waiting room with N chairs


# barber cuts customers hair and customer leaves (executes job)

# barber then checks waiting room
# if there is a customer:
#      next customer comes to chair
#      gets hair cut
# else (no customers waiting):
#      barber returns to chair
#      sleeps in chair


# customers come into shop randomly
# haircuts can take a random amount of time to complete

# all barbers busy --> customer waits in room
# if one or more barbers are sleeping --> customer wakes barber and sits in their chair

# event based :> customer enters shop / finished having hair cut

import threading
import time
import random
import multiprocessing

# For 40% of the marks, you should consider the case of one barber, and a waiting room with an infinite number of chairs. This means you do not have to cater for the fact that the waiting room might at any time become full.

def testCustomer(self):
    self.name = "Tod"

waiting_room = multiprocessing.Queue()

waiting_room.put(testCustomer)
waiting_room.put(testCustomer)
waiting_room.put(testCustomer)
waiting_room.put(testCustomer)
waiting_room.put(testCustomer)


#
#
#
#
# counting semaphore for the number of customers
semaphore_customerNum = 0

# this is for the single barber case (binary semaphore)
# either he is working, or he isn't working
# it begins that he is NOT working
semaphore_barber_working = 0

# mutex
# this mutex allows us to control who has access to the shared resource.
# either a customer can be written to it, or barber accesses it to take customer 
# when it's equal to 1, it can be messed with
mutex_accessWaitingRoomSeats = 1

infinite_waiting_room = 

def Barber():

def Customer():

if waiting_room == empty:
    semaphore_barber_working = 0


# --> Waiting room --> Queue() [FIFO served basis]
# --> Number of chairs (waiting rooms) == Length of Queue

# For 60% of the marks, you should consider the case of 1 barber, and a waiting room with 10 chairs.
waiting_room_10 = multiprocessing.Queue(10)

print(waiting_room.get())
print(waiting_room.get())
print(waiting_room.get())
print(waiting_room.get())
print(waiting_room.get())


# For 100% of the marks, you should consider the case of 3 barbers (minimum) and a waiting room with 15 chairs.



# Each barber operate on it's own thread? Accessing a shared queue?

# main program must start a thread of customers visiting the shop.



"""Example of how to wait for enqueued tasks to be completed:

def worker(): <-- this could be our barber??
    while True:
        item = q.get()
        if item is None:
            break
        do_work(item)
        q.task_done()

q = queue.Queue() --> could set a maxsize on this
threads = []
for i in range(num_worker_threads): <--- so we could set this to 3 i.e the number of barbers we want working?
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in source():
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()
"""