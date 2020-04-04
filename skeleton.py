import threading
import time
import random

# need to throw in try and accepts here
print("Enter the number of seats available: ")
CUSTOMERS = int(input())#set number of customers here. You may need to modify this to use a queue.
print("Enter the number of barbers working: ")
BARBERS = int(input())#of barbers depending on which version you choose.

global opening_hours = input()
ARRIVAL_WAIT = 0.01

def wait():
	time.sleep(ARRIVAL_WAIT * random.random())

class Customer(threading.Thread):
	WAIT = 0.05
	def wait(self):
		time.sleep(self.WAIT * random.random())

	def trim(self):  # Called from Barber thread
		# Get a haircut

	def run(self):
		self.serviced = threading.Event()
		# Grab the barbers' attention, add ourselves to the customers,
		# and wait to be serviced

class Barber(threading.Thread):
	condition = threading.Condition()
	customers = []
	should_stop = threading.Event()

	def __init__(self, q):

	def check_waiting_room(self, q):


	def run(self):
		while True:
			with self.condition:
				if not self.customers:
					# No customers, snore...
                    # we have to check the queue
				# Get the next customer (from the queue)
			# Actually service the next customer --> run said program

if __name__ == '__main__':
	barbers = []
	for b in range(BARBERS):
		Barber().start()
	all_customers = []
	for c in range(CUSTOMERS):
		wait()
		c = Customer()
		all_customers.append(c)
		c.start()
	for c in all_customers:
		c.join()  # Wait for all customers to leave
	# Grab the barbers' attention and tell them all that it's time to leave

    ###################
	def opening_hours():
    print("OH LOOK AT ME PLEASE")
	    timer = threading.Timer(5.0, gfg)
    timer.start()
    print("yoyo")
	###################


	"""Example of how to wait for enqueued tasks to be completed:

def worker(): <-- this could be our barber??
    while True:
        item = q.get()
        if item is None:
            break
        trim(Customer)
        q.task_done()

q = queue.Queue(CUSTOMERS) --> could set a maxsize on this
threads = []
for i in range(num_worker_threads // BARBERS): <--- so we could set this to 3 i.e the number of barbers we want working?
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

print(threading.activeCount())

x.join() --> don't move past this line of code until thread x is finished running