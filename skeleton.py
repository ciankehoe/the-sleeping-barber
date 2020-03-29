import threading
import time
import random

CUSTOMERS = #set number of customers here. You may need to modify this to use a queue.
BARBERS = #of barbers depending on which version you choose.

ARRIVAL_WAIT = 0.01

def wait():
	time.sleep(ARRIVAL_WAIT * random.random())

class Barber(threading.Thread):
	condition = threading.Condition()
	customers = []
	should_stop = threading.Event()

	def run(self):
		while True:
			with self.condition:
				if not self.customers:
					# No customers, snore...
                    # we have to check the queue
				# Get the next customer (from the queue)
			# Actually service the next customer --> run said program

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