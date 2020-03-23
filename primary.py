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

def Customer(self):
    self.name = "Tod"

waiting_room = multiprocessing.Queue()

"""def Barber():
    while True:
        waiting_room.get()

def Customer():"""
waiting_room.put(Customer)
waiting_room.put(Customer)
waiting_room.put(Customer)
waiting_room.put(Customer)
waiting_room.put(Customer)


if waiting_room == empty


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